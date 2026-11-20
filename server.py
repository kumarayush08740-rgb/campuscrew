import http.server
import socketserver
import os
import sys
import json
import sqlite3
import urllib.parse
import secrets
import hashlib
import uuid
from datetime import datetime, timedelta

from database import get_db, hash_password, verify_password, DB_PATH, init_db, seed_db

PORT = 8000
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "public")

# Simple In-Memory Session Store: token -> {user_id, role, email, full_name, expires_at}
SESSIONS = {}

def create_session(user):
    token = secrets.token_hex(24)
    SESSIONS[token] = {
        "user_id": user["id"],
        "email": user["email"],
        "role": user["role"],
        "full_name": user["full_name"],
        "avatar_url": user["avatar_url"],
        "is_verified": user["is_verified"],
        "expires_at": datetime.now() + timedelta(days=7)
    }
    return token

def get_current_user(headers):
    auth_header = headers.get("Authorization") or headers.get("authorization")
    if not auth_header:
        # Check cookie
        cookie_header = headers.get("Cookie") or headers.get("cookie")
        if cookie_header:
            cookies = dict(c.strip().split("=", 1) for c in cookie_header.split(";") if "=" in c)
            token = cookies.get("cc_token")
            if token and token in SESSIONS:
                sess = SESSIONS[token]
                if sess["expires_at"] > datetime.now():
                    return sess
        return None
        
    parts = auth_header.split(" ")
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
        if token in SESSIONS:
            sess = SESSIONS[token]
            if sess["expires_at"] > datetime.now():
                return sess
    return None

class CampusCrewHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def send_json(self, data, status=200):
        body = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()
        self.wfile.write(body)

    def send_error_json(self, message, status=400):
        self.send_json({"error": message, "status": status}, status=status)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.end_headers()

    def parse_json_body(self):
        content_len = int(self.headers.get('Content-Length', 0))
        if content_len == 0:
            return {}
        raw_body = self.rfile.read(content_len)
        try:
            return json.loads(raw_body.decode('utf-8'))
        except Exception:
            return {}

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path.startswith("/api/"):
            self.handle_api_get(path, query)
        else:
            # SPA fallback: if file doesn't exist, serve index.html
            file_path = os.path.join(PUBLIC_DIR, path.lstrip("/"))
            if not os.path.exists(file_path) or os.path.isdir(file_path):
                self.path = "/index.html"
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.parse_json_body()

        if path.startswith("/api/"):
            self.handle_api_post(path, body)
        else:
            self.send_error_json("Invalid POST path", 404)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self.parse_json_body()

        if path.startswith("/api/"):
            self.handle_api_put(path, body)
        else:
            self.send_error_json("Invalid PUT path", 404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path.startswith("/api/"):
            self.handle_api_delete(path, query)
        else:
            self.send_error_json("Invalid DELETE path", 404)

    # -------------------------------------------------------------
    # API ROUTERS
    # -------------------------------------------------------------
    def handle_api_get(self, path, query):
        conn = get_db()
        c = conn.cursor()
        user = get_current_user(self.headers)

        # 1. Auth Me
        if path == "/api/auth/me":
            if not user:
                conn.close()
                return self.send_error_json("Unauthorized", 401)
            
            c.execute("SELECT id, email, role, full_name, avatar_url, is_verified, created_at FROM users WHERE id = ?", (user["user_id"],))
            u_row = c.fetchone()
            if not u_row:
                conn.close()
                return self.send_error_json("User not found", 404)
            
            user_data = dict(u_row)
            if user_data["role"] == "business":
                c.execute("SELECT * FROM business_profiles WHERE user_id = ?", (user_data["id"],))
                b_row = c.fetchone()
                user_data["profile"] = dict(b_row) if b_row else {}
            elif user_data["role"] == "creator":
                c.execute("SELECT * FROM creator_profiles WHERE user_id = ?", (user_data["id"],))
                cr_row = c.fetchone()
                user_data["profile"] = dict(cr_row) if cr_row else {}
            elif user_data["role"] == "student":
                c.execute("SELECT * FROM student_profiles WHERE user_id = ?", (user_data["id"],))
                s_row = c.fetchone()
                user_data["profile"] = dict(s_row) if s_row else {}

            conn.close()
            return self.send_json({"user": user_data})

        # 2. Creator Directory & Discovery
        elif path == "/api/profiles/creators":
            search = query.get("search", [""])[0].lower()
            niche = query.get("niche", [""])[0]
            location = query.get("location", [""])[0]
            min_eng = float(query.get("min_engagement", [0])[0] or 0)
            max_budget = float(query.get("max_budget", [99999])[0] or 99999)
            sort_by = query.get("sort_by", ["relevance"])[0]

            sql = '''
            SELECT u.id, u.full_name, u.avatar_url, u.is_verified,
                   cp.handle, cp.niche, cp.location, cp.city, cp.lat, cp.lng,
                   cp.bio, cp.portfolio_url, cp.follower_count, cp.avg_engagement_rate,
                   cp.base_rate, cp.audience_age_group, cp.is_audience_verified, cp.reliability_score
            FROM creator_profiles cp
            JOIN users u ON cp.user_id = u.id
            WHERE 1=1
            '''
            params = []
            if search:
                sql += " AND (LOWER(u.full_name) LIKE ? OR LOWER(cp.handle) LIKE ? OR LOWER(cp.bio) LIKE ?)"
                like_term = f"%{search}%"
                params.extend([like_term, like_term, like_term])
            if niche and niche != "All Niches":
                sql += " AND cp.niche = ?"
                params.append(niche)
            if location and location != "All Locations":
                sql += " AND (LOWER(cp.location) LIKE ? OR LOWER(cp.city) LIKE ?)"
                params.extend([f"%{location.lower()}%", f"%{location.lower()}%"])
            if min_eng > 0:
                sql += " AND cp.avg_engagement_rate >= ?"
                params.append(min_eng)
            if max_budget < 99999:
                sql += " AND cp.base_rate <= ?"
                params.append(max_budget)

            if sort_by == "engagement":
                sql += " ORDER BY cp.avg_engagement_rate DESC"
            elif sort_by == "followers":
                sql += " ORDER BY cp.follower_count DESC"
            elif sort_by == "rate_low":
                sql += " ORDER BY cp.base_rate ASC"
            elif sort_by == "reliability":
                sql += " ORDER BY cp.reliability_score DESC"
            else:
                sql += " ORDER BY cp.reliability_score DESC, cp.avg_engagement_rate DESC"

            c.execute(sql, params)
            creators = [dict(row) for row in c.fetchall()]
            
            # Attach review count and avg rating
            for cr in creators:
                c.execute("SELECT COUNT(*), AVG(rating) FROM reviews WHERE target_id = ?", (cr["id"],))
                r_count, r_avg = c.fetchone()
                cr["review_count"] = r_count or 0
                cr["rating_avg"] = round(r_avg, 1) if r_avg else 5.0

            conn.close()
            return self.send_json({"creators": creators})

        # 3. Creator Profile Detail
        elif path.startswith("/api/profiles/creators/"):
            creator_id = path.split("/")[-1]
            c.execute('''
            SELECT u.id, u.full_name, u.avatar_url, u.is_verified, u.created_at,
                   cp.handle, cp.niche, cp.location, cp.city, cp.lat, cp.lng,
                   cp.bio, cp.portfolio_url, cp.follower_count, cp.avg_engagement_rate,
                   cp.base_rate, cp.audience_age_group, cp.is_audience_verified, cp.reliability_score
            FROM creator_profiles cp
            JOIN users u ON cp.user_id = u.id
            WHERE u.id = ?
            ''', (creator_id,))
            row = c.fetchone()
            if not row:
                conn.close()
                return self.send_error_json("Creator not found", 404)
            cr = dict(row)

            # Get Reviews
            c.execute('''
            SELECT r.*, u.full_name as author_name, u.avatar_url as author_avatar
            FROM reviews r
            JOIN users u ON r.author_id = u.id
            WHERE r.target_id = ?
            ORDER BY r.created_at DESC
            ''', (creator_id,))
            cr["reviews"] = [dict(r) for r in c.fetchall()]

            # Get Completed Collabs Count
            c.execute("SELECT COUNT(*) FROM collaborations WHERE creator_id = ? AND status = 'completed'", (creator_id,))
            cr["completed_collabs"] = c.fetchone()[0]

            conn.close()
            return self.send_json({"creator": cr})

        # 4. Campaigns List
        elif path == "/api/campaigns":
            category = query.get("category", [""])[0]
            collab_type = query.get("type", [""])[0]
            search = query.get("search", [""])[0].lower()
            business_id = query.get("business_id", [""])[0]

            sql = '''
            SELECT c.*, u.full_name as business_name, u.avatar_url as business_logo,
                   bp.category as business_category, bp.city as business_city,
                   (SELECT COUNT(*) FROM campaign_applications WHERE campaign_id = c.id) as application_count
            FROM campaigns c
            JOIN users u ON c.business_id = u.id
            JOIN business_profiles bp ON u.id = bp.user_id
            WHERE 1=1
            '''
            params = []
            if business_id:
                sql += " AND c.business_id = ?"
                params.append(business_id)
            else:
                # Public listings only show non-draft
                sql += " AND c.status IN ('published', 'applications_open', 'in_progress', 'completed')"

            if category and category != "All Categories":
                sql += " AND c.category = ?"
                params.append(category)
            if collab_type and collab_type != "All Types":
                sql += " AND c.collaboration_type = ?"
                params.append(collab_type)
            if search:
                sql += " AND (LOWER(c.title) LIKE ? OR LOWER(c.description) LIKE ? OR LOWER(u.full_name) LIKE ?)"
                like_term = f"%{search}%"
                params.extend([like_term, like_term, like_term])

            sql += " ORDER BY c.created_at DESC"
            c.execute(sql, params)
            campaigns = [dict(row) for row in c.fetchall()]
            conn.close()
            return self.send_json({"campaigns": campaigns})

        # 5. Campaign Detail
        elif path.startswith("/api/campaigns/") and not path.endswith("/applications"):
            camp_id = path.split("/")[-1]
            c.execute('''
            SELECT c.*, u.full_name as business_name, u.avatar_url as business_logo,
                   bp.category as business_category, bp.location as business_location,
                   bp.description as business_bio, bp.website as business_website
            FROM campaigns c
            JOIN users u ON c.business_id = u.id
            JOIN business_profiles bp ON u.id = bp.user_id
            WHERE c.id = ?
            ''', (camp_id,))
            row = c.fetchone()
            if not row:
                conn.close()
                return self.send_error_json("Campaign not found", 404)
            camp = dict(row)

            # Check if current user already applied
            if user and user["role"] == "creator":
                c.execute("SELECT * FROM campaign_applications WHERE campaign_id = ? AND creator_id = ?", (camp_id, user["user_id"]))
                app_row = c.fetchone()
                camp["user_application"] = dict(app_row) if app_row else None

            conn.close()
            return self.send_json({"campaign": camp})

        # 6. Campaign Applications (For Business Owner)
        elif path.startswith("/api/campaigns/") and path.endswith("/applications"):
            camp_id = path.split("/")[3]
            c.execute('''
            SELECT ca.*, u.full_name as creator_name, u.avatar_url as creator_avatar,
                   cp.handle, cp.niche, cp.location as creator_location, cp.follower_count,
                   cp.avg_engagement_rate, cp.reliability_score, cp.base_rate
            FROM campaign_applications ca
            JOIN users u ON ca.creator_id = u.id
            JOIN creator_profiles cp ON u.id = cp.user_id
            WHERE ca.campaign_id = ?
            ORDER BY ca.score DESC, ca.created_at DESC
            ''', (camp_id,))
            applications = [dict(row) for row in c.fetchall()]
            for a in applications:
                if a.get("score_breakdown"):
                    try:
                        a["score_breakdown"] = json.loads(a["score_breakdown"])
                    except:
                        pass
            conn.close()
            return self.send_json({"applications": applications})

        # 7. Collaborations List
        elif path == "/api/collaborations":
            if not user:
                conn.close()
                return self.send_error_json("Unauthorized", 401)

            if user["role"] == "business":
                c.execute('''
                SELECT col.*, c.title as campaign_title, c.category,
                       u.full_name as partner_name, u.avatar_url as partner_avatar,
                       cp.handle as creator_handle, dp.amount as payment_amount, dp.status as payment_status,
                       tc.qr_code_id, tc.coupon_code
                FROM collaborations col
                JOIN campaigns c ON col.campaign_id = c.id
                JOIN users u ON col.creator_id = u.id
                JOIN creator_profiles cp ON u.id = cp.user_id
                LEFT JOIN deal_payments dp ON col.id = dp.collaboration_id
                LEFT JOIN tracking_codes tc ON col.id = tc.collaboration_id
                WHERE col.business_id = ?
                ORDER BY col.created_at DESC
                ''', (user["user_id"],))
            elif user["role"] == "creator":
                c.execute('''
                SELECT col.*, c.title as campaign_title, c.category,
                       u.full_name as partner_name, u.avatar_url as partner_avatar,
                       bp.company_name as business_name, dp.amount as payment_amount, dp.status as payment_status,
                       tc.qr_code_id, tc.coupon_code
                FROM collaborations col
                JOIN campaigns c ON col.campaign_id = c.id
                JOIN users u ON col.business_id = u.id
                JOIN business_profiles bp ON u.id = bp.user_id
                LEFT JOIN deal_payments dp ON col.id = dp.collaboration_id
                LEFT JOIN tracking_codes tc ON col.id = tc.collaboration_id
                WHERE col.creator_id = ?
                ORDER BY col.created_at DESC
                ''', (user["user_id"],))
            else: # Admin
                c.execute('''
                SELECT col.*, c.title as campaign_title,
                       b.full_name as business_name, cr.full_name as creator_name
                FROM collaborations col
                JOIN campaigns c ON col.campaign_id = c.id
                JOIN users b ON col.business_id = b.id
                JOIN users cr ON col.creator_id = cr.id
                ORDER BY col.created_at DESC
                ''')

            collabs = [dict(row) for row in c.fetchall()]
            conn.close()
            return self.send_json({"collaborations": collabs})

        # 8. Collaboration Hub Details
        elif path.startswith("/api/collaborations/") and not path.endswith("/messages"):
            collab_id = path.split("/")[-1]
            c.execute('''
            SELECT col.*, c.title as campaign_title, c.description as campaign_desc, c.deliverables as target_deliverables,
                   b.full_name as business_name, b.avatar_url as business_logo,
                   cr.full_name as creator_name, cr.avatar_url as creator_avatar,
                   cp.handle as creator_handle, cp.follower_count, cp.avg_engagement_rate,
                   dp.amount as payment_amount, dp.status as payment_status, dp.invoice_no, dp.tx_reference,
                   tc.qr_code_id, tc.coupon_code, tc.discount_percent
            FROM collaborations col
            JOIN campaigns c ON col.campaign_id = c.id
            JOIN users b ON col.business_id = b.id
            JOIN users cr ON col.creator_id = cr.id
            JOIN creator_profiles cp ON cr.id = cp.user_id
            LEFT JOIN deal_payments dp ON col.id = dp.collaboration_id
            LEFT JOIN tracking_codes tc ON col.id = tc.collaboration_id
            WHERE col.id = ?
            ''', (collab_id,))
            row = c.fetchone()
            if not row:
                conn.close()
                return self.send_error_json("Collaboration not found", 404)
            collab = dict(row)

            # Get Deliverables
            c.execute("SELECT * FROM deliverables WHERE collaboration_id = ? ORDER BY id ASC", (collab_id,))
            collab["deliverables"] = [dict(d) for d in c.fetchall()]

            # Get Tracking Stats
            if collab.get("qr_code_id"):
                c.execute('''
                SELECT 
                    COUNT(CASE WHEN event_type = 'qr_scan' THEN 1 END) as scans,
                    COUNT(CASE WHEN event_type = 'coupon_redemption' THEN 1 END) as redemptions,
                    COUNT(CASE WHEN event_type = 'confirmed_sale' THEN 1 END) as confirmed_sales,
                    COALESCE(SUM(order_value), 0.0) as revenue_generated
                FROM tracking_events te
                JOIN tracking_codes tc ON te.tracking_code_id = tc.id
                WHERE tc.collaboration_id = ?
                ''', (collab_id,))
                collab["tracking_stats"] = dict(c.fetchone())
            else:
                collab["tracking_stats"] = {"scans": 0, "redemptions": 0, "confirmed_sales": 0, "revenue_generated": 0.0}

            # Check if user already reviewed
            if user:
                c.execute("SELECT * FROM reviews WHERE collaboration_id = ? AND author_id = ?", (collab_id, user["user_id"]))
                rev_row = c.fetchone()
                collab["user_review"] = dict(rev_row) if rev_row else None

            conn.close()
            return self.send_json({"collaboration": collab})

        # 9. Messages
        elif path.startswith("/api/collaborations/") and path.endswith("/messages"):
            collab_id = path.split("/")[3]
            c.execute('''
            SELECT m.*, u.full_name as sender_name, u.avatar_url as sender_avatar, u.role as sender_role
            FROM messages m
            JOIN users u ON m.sender_id = u.id
            WHERE m.collaboration_id = ?
            ORDER BY m.created_at ASC
            ''', (collab_id,))
            msgs = [dict(m) for m in c.fetchall()]
            conn.close()
            return self.send_json({"messages": msgs})

        # 10. Notifications
        elif path == "/api/notifications":
            if not user:
                conn.close()
                return self.send_error_json("Unauthorized", 401)
            c.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 20", (user["user_id"],))
            notifs = [dict(n) for n in c.fetchall()]
            conn.close()
            return self.send_json({"notifications": notifs})

        # 11. Business ROI Analytics
        elif path.startswith("/api/analytics/business/"):
            biz_id = path.split("/")[-1]
            c.execute('''
            SELECT 
                COUNT(DISTINCT c.id) as total_campaigns,
                COALESCE(SUM(c.budget), 0.0) as total_budget,
                COUNT(DISTINCT col.id) as total_collaborations,
                COUNT(DISTINCT col.creator_id) as unique_creators,
                COALESCE(SUM(dp.amount), 0.0) as total_spend
            FROM campaigns c
            LEFT JOIN collaborations col ON c.id = col.campaign_id
            LEFT JOIN deal_payments dp ON col.id = dp.collaboration_id AND dp.status IN ('paid', 'escrow_held')
            WHERE c.business_id = ?
            ''', (biz_id,))
            stats = dict(c.fetchone())

            # Conversion Aggregation
            c.execute('''
            SELECT 
                COUNT(CASE WHEN te.event_type = 'qr_scan' THEN 1 END) as total_scans,
                COUNT(CASE WHEN te.event_type = 'coupon_redemption' THEN 1 END) as total_redemptions,
                COUNT(CASE WHEN te.event_type = 'confirmed_sale' THEN 1 END) as confirmed_sales,
                COALESCE(SUM(te.order_value), 0.0) as attributed_revenue
            FROM tracking_events te
            JOIN tracking_codes tc ON te.tracking_code_id = tc.id
            WHERE tc.business_id = ?
            ''', (biz_id,))
            conv_stats = dict(c.fetchone())
            stats.update(conv_stats)

            # Calculate Real ROI
            spend = stats["total_spend"] or 1.0
            rev = stats["attributed_revenue"] or 0.0
            stats["roi_percent"] = round(((rev - spend) / spend) * 100, 1) if rev > 0 else 0.0
            stats["cost_per_acquisition"] = round(spend / stats["total_redemptions"], 2) if stats["total_redemptions"] > 0 else 0.0

            # Creator-by-creator attribution breakdown
            c.execute('''
            SELECT u.full_name as creator_name, cp.handle, tc.coupon_code,
                   COUNT(CASE WHEN te.event_type = 'qr_scan' THEN 1 END) as scans,
                   COUNT(CASE WHEN te.event_type = 'coupon_redemption' THEN 1 END) as redemptions,
                   COALESCE(SUM(te.order_value), 0.0) as revenue
            FROM collaborations col
            JOIN users u ON col.creator_id = u.id
            JOIN creator_profiles cp ON u.id = cp.user_id
            JOIN tracking_codes tc ON col.id = tc.collaboration_id
            LEFT JOIN tracking_events te ON tc.id = te.tracking_code_id
            WHERE col.business_id = ?
            GROUP BY col.id
            ''', (biz_id,))
            stats["creator_performance"] = [dict(r) for r in c.fetchall()]

            conn.close()
            return self.send_json({"analytics": stats})

        # 12. Favourites
        elif path == "/api/favourites":
            if not user or user["role"] != "business":
                conn.close()
                return self.send_error_json("Unauthorized", 401)
            c.execute('''
            SELECT sc.*, u.full_name, u.avatar_url, cp.handle, cp.niche, cp.follower_count, cp.avg_engagement_rate, cp.base_rate
            FROM saved_creators sc
            JOIN users u ON sc.creator_id = u.id
            JOIN creator_profiles cp ON u.id = cp.user_id
            WHERE sc.business_id = ?
            ORDER BY sc.created_at DESC
            ''', (user["user_id"],))
            favs = [dict(r) for r in c.fetchall()]
            conn.close()
            return self.send_json({"favourites": favs})

        # 13. Student Hub Talents & Certificates
        elif path == "/api/student/talents":
            c.execute('''
            SELECT u.id, u.full_name, u.avatar_url, sp.*
            FROM student_profiles sp
            JOIN users u ON sp.user_id = u.id
            ORDER BY sp.created_at DESC
            ''')
            talents = [dict(t) for t in c.fetchall()]
            conn.close()
            return self.send_json({"students": talents})

        elif path.startswith("/api/student/certificates/"):
            uuid_str = path.split("/")[-1]
            c.execute('''
            SELECT sc.*, u.full_name as student_name, sp.university, sp.major
            FROM student_certificates sc
            JOIN users u ON sc.student_id = u.id
            JOIN student_profiles sp ON u.id = sp.user_id
            WHERE sc.certificate_uuid = ?
            ''', (uuid_str,))
            row = c.fetchone()
            conn.close()
            if not row:
                return self.send_error_json("Certificate not found or unverified", 404)
            return self.send_json({"certificate": dict(row)})

        # 14. Admin Overview & Governance
        elif path == "/api/admin/overview":
            if not user or user["role"] != "admin":
                conn.close()
                return self.send_error_json("Admin access required", 403)
            
            c.execute("SELECT COUNT(*) FROM users")
            total_users = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM campaigns")
            total_camps = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM collaborations")
            total_collabs = c.fetchone()[0]
            c.execute("SELECT COALESCE(SUM(amount), 0.0) FROM deal_payments WHERE status IN ('paid', 'escrow_held')")
            total_gmv = c.fetchone()[0]
            c.execute("SELECT COUNT(*) FROM disputes WHERE status = 'open'")
            open_disputes = c.fetchone()[0]
            c.execute("SELECT value FROM system_settings WHERE key = 'student_hub_enabled'")
            student_hub_val = c.fetchone()[0]

            conn.close()
            return self.send_json({
                "overview": {
                    "total_users": total_users,
                    "total_campaigns": total_camps,
                    "total_collaborations": total_collabs,
                    "total_gmv": total_gmv,
                    "open_disputes": open_disputes,
                    "student_hub_enabled": student_hub_val == "true"
                }
            })

        elif path == "/api/admin/disputes":
            if not user or user["role"] != "admin":
                conn.close()
                return self.send_error_json("Admin access required", 403)
            c.execute('''
            SELECT d.*, col.agreed_fee, c.title as campaign_title,
                   u.full_name as raised_by_name, u.role as raised_by_role
            FROM disputes d
            JOIN collaborations col ON d.collaboration_id = col.id
            JOIN campaigns c ON col.campaign_id = c.id
            JOIN users u ON d.raised_by_id = u.id
            ORDER BY d.created_at DESC
            ''')
            disputes = [dict(d) for d in c.fetchall()]
            conn.close()
            return self.send_json({"disputes": disputes})

        # 15. Dynamic QR Code Generator (Native SVG vector generator)
        elif path.startswith("/api/qrcode/"):
            qr_id = path.replace("/api/qrcode/", "").replace(".svg", "")
            svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 220 220" width="220" height="220">
                <rect width="220" height="220" fill="#FFFFFF" rx="12"/>
                <!-- Outer Finder Patterns -->
                <rect x="20" y="20" width="50" height="50" fill="#4F46E5" rx="6"/>
                <rect x="30" y="30" width="30" height="30" fill="#FFFFFF" rx="3"/>
                <rect x="38" y="38" width="14" height="14" fill="#4F46E5" rx="2"/>

                <rect x="150" y="20" width="50" height="50" fill="#4F46E5" rx="6"/>
                <rect x="160" y="30" width="30" height="30" fill="#FFFFFF" rx="3"/>
                <rect x="168" y="38" width="14" height="14" fill="#4F46E5" rx="2"/>

                <rect x="20" y="150" width="50" height="50" fill="#4F46E5" rx="6"/>
                <rect x="30" y="160" width="30" height="30" fill="#FFFFFF" rx="3"/>
                <rect x="38" y="168" width="14" height="14" fill="#4F46E5" rx="2"/>

                <!-- QR Payload Grid Simulation -->
                <rect x="85" y="25" width="12" height="12" fill="#1E293B"/>
                <rect x="105" y="25" width="12" height="12" fill="#1E293B"/>
                <rect x="125" y="35" width="12" height="12" fill="#1E293B"/>
                <rect x="85" y="55" width="12" height="12" fill="#1E293B"/>
                <rect x="105" y="65" width="12" height="12" fill="#1E293B"/>

                <rect x="25" y="85" width="12" height="12" fill="#1E293B"/>
                <rect x="55" y="95" width="12" height="12" fill="#1E293B"/>
                <rect x="85" y="95" width="20" height="20" fill="#4F46E5" rx="4"/>
                <rect x="115" y="95" width="12" height="12" fill="#1E293B"/>
                <rect x="145" y="85" width="12" height="12" fill="#1E293B"/>
                <rect x="175" y="95" width="12" height="12" fill="#1E293B"/>

                <rect x="85" y="125" width="12" height="12" fill="#1E293B"/>
                <rect x="115" y="135" width="12" height="12" fill="#1E293B"/>
                <rect x="145" y="125" width="12" height="12" fill="#1E293B"/>
                <rect x="175" y="145" width="12" height="12" fill="#1E293B"/>

                <rect x="85" y="165" width="12" height="12" fill="#1E293B"/>
                <rect x="115" y="175" width="12" height="12" fill="#1E293B"/>
                <rect x="145" y="165" width="12" height="12" fill="#1E293B"/>
                <rect x="165" y="185" width="12" height="12" fill="#1E293B"/>

                <!-- Badge text -->
                <text x="110" y="210" font-family="sans-serif" font-size="9" font-weight="bold" fill="#64748B" text-anchor="middle">CAMPUSCREW VERIFIED</text>
            </svg>'''
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Content-Length", str(len(svg_content)))
            self.end_headers()
            self.wfile.write(svg_content.encode("utf-8"))
            conn.close()
            return

        conn.close()
        self.send_error_json("API route not found", 404)

    # -------------------------------------------------------------
    # API POST HANDLERS
    # -------------------------------------------------------------
    def handle_api_post(self, path, body):
        conn = get_db()
        c = conn.cursor()
        user = get_current_user(self.headers)
        now = datetime.now().isoformat()

        # 1. Register
        if path == "/api/auth/register":
            email = body.get("email", "").strip().lower()
            password = body.get("password", "")
            role = body.get("role", "creator")
            full_name = body.get("full_name", "").strip()

            if not email or not password or not full_name:
                conn.close()
                return self.send_error_json("All required fields must be provided", 400)
            if role not in ("business", "creator", "student"):
                conn.close()
                return self.send_error_json("Invalid user role", 400)

            c.execute("SELECT id FROM users WHERE email = ?", (email,))
            if c.fetchone():
                conn.close()
                return self.send_error_json("Email is already registered", 400)

            p_hash, salt = hash_password(password)
            avatar_url = body.get("avatar_url") or "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150"

            c.execute('''
            INSERT INTO users (email, password_hash, salt, role, full_name, avatar_url, is_verified, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?)
            ''', (email, p_hash, salt, role, full_name, avatar_url, now))
            new_uid = c.lastrowid

            if role == "business":
                company_name = body.get("company_name", full_name)
                category = body.get("category", "Food & Beverage")
                location = body.get("location", "Austin, TX")
                city = body.get("city", "Austin")
                c.execute('''
                INSERT INTO business_profiles (user_id, company_name, category, location, city, lat, lng, description, logo_url, created_at)
                VALUES (?, ?, ?, ?, ?, 30.28, -97.74, ?, ?, ?)
                ''', (new_uid, company_name, category, location, city, body.get("description", ""), avatar_url, now))
            elif role == "creator":
                handle = body.get("handle") or f"@{email.split('@')[0]}"
                niche = body.get("niche", "Food & Beverage")
                location = body.get("location", "North Campus, Austin")
                base_rate = float(body.get("base_rate", 200.0) or 200.0)
                c.execute('''
                INSERT INTO creator_profiles (user_id, handle, niche, location, city, lat, lng, bio, follower_count, avg_engagement_rate, base_rate, audience_age_group, is_audience_verified, reliability_score, created_at)
                VALUES (?, ?, ?, ?, 'Austin', 30.28, -97.73, ?, 15000, 6.5, ?, '18-24 (80%)', 1, 98.0, ?)
                ''', (new_uid, handle, niche, location, body.get("bio", "Local creator passionate about authentic community storytelling."), base_rate, now))
            elif role == "student":
                c.execute('''
                INSERT INTO student_profiles (user_id, university, major, skills, created_at)
                VALUES (?, ?, ?, ?, ?)
                ''', (new_uid, body.get("university", "UT Austin"), body.get("major", "Communications"), body.get("skills", "Reel Editing, Graphic Design"), now))

            conn.commit()

            # Create session
            token = create_session({
                "id": new_uid,
                "email": email,
                "role": role,
                "full_name": full_name,
                "avatar_url": avatar_url,
                "is_verified": 1
            })
            conn.close()
            return self.send_json({"token": token, "user": {"id": new_uid, "email": email, "role": role, "full_name": full_name}})

        # 2. Login
        elif path == "/api/auth/login":
            email = body.get("email", "").strip().lower()
            password = body.get("password", "")

            c.execute("SELECT * FROM users WHERE email = ?", (email,))
            row = c.fetchone()
            if not row:
                conn.close()
                return self.send_error_json("Invalid email or password", 401)

            u = dict(row)
            if not verify_password(password, u["password_hash"], u["salt"]):
                conn.close()
                return self.send_error_json("Invalid email or password", 401)

            token = create_session(u)
            conn.close()
            return self.send_json({
                "token": token,
                "user": {
                    "id": u["id"],
                    "email": u["email"],
                    "role": u["role"],
                    "full_name": u["full_name"],
                    "avatar_url": u["avatar_url"],
                    "is_verified": u["is_verified"]
                }
            })

        # 3. Create Campaign
        elif path == "/api/campaigns":
            if not user or user["role"] != "business":
                conn.close()
                return self.send_error_json("Business account required to post campaigns", 403)

            title = body.get("title", "").strip()
            desc = body.get("description", "").strip()
            category = body.get("category", "Food & Beverage")
            objective = body.get("objective", "Footfall & QR Scans")
            budget = float(body.get("budget", 500.0) or 500.0)
            collab_type = body.get("collaboration_type", "paid")
            target_loc = body.get("target_location", "Austin, TX")
            niche = body.get("required_niche", category)
            deliverables = body.get("deliverables", "1 Reel + 2 Stories")
            deadline = body.get("deadline", (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
            app_deadline = body.get("application_deadline", (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"))

            if not title or not desc:
                conn.close()
                return self.send_error_json("Campaign title and description are required", 400)

            c.execute('''
            INSERT INTO campaigns (business_id, title, description, category, objective, budget, collaboration_type, target_location, required_niche, deliverables, deadline, application_deadline, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'published', ?)
            ''', (user["user_id"], title, desc, category, objective, budget, collab_type, target_loc, niche, deliverables, deadline, app_deadline, now))
            new_camp_id = c.lastrowid
            conn.commit()
            conn.close()
            return self.send_json({"success": True, "campaign_id": new_camp_id})

        # 4. Apply to Campaign (Creator)
        elif path.startswith("/api/campaigns/") and path.endswith("/apply"):
            camp_id = path.split("/")[3]
            if not user or user["role"] != "creator":
                conn.close()
                return self.send_error_json("Creator account required to apply", 403)

            c.execute("SELECT * FROM campaign_applications WHERE campaign_id = ? AND creator_id = ?", (camp_id, user["user_id"]))
            if c.fetchone():
                conn.close()
                return self.send_error_json("You have already applied to this campaign", 400)

            proposed_fee = float(body.get("proposed_fee", 250.0) or 250.0)
            deliverables = body.get("proposed_deliverables", "1 Reel + 2 Stories")
            pitch = body.get("creative_pitch", "")
            est_days = int(body.get("estimated_days", 7))

            # Calculate transparent Creator Opportunity Score (0 - 100)
            c.execute("SELECT * FROM campaigns WHERE id = ?", (camp_id,))
            camp_row = dict(c.fetchone())
            c.execute("SELECT * FROM creator_profiles WHERE user_id = ?", (user["user_id"],))
            cr_row = dict(c.fetchone())

            loc_score = 100 if camp_row["target_location"].lower() in cr_row["location"].lower() or cr_row["city"].lower() in camp_row["target_location"].lower() else 75
            niche_score = 100 if camp_row["required_niche"].lower() == cr_row["niche"].lower() else 65
            budget_score = 100 if proposed_fee <= camp_row["budget"] else max(40, int(100 - (proposed_fee - camp_row["budget"])/camp_row["budget"] * 50))
            rel_score = int(cr_row.get("reliability_score", 95.0))
            eng_score = min(100, int(cr_row.get("avg_engagement_rate", 5.0) * 12))

            total_score = round((loc_score * 0.25) + (niche_score * 0.25) + (budget_score * 0.20) + (rel_score * 0.20) + (eng_score * 0.10), 1)

            breakdown = {
                "location_match": loc_score,
                "niche_match": niche_score,
                "budget_match": budget_score,
                "reliability": rel_score,
                "engagement_quality": eng_score
            }

            c.execute('''
            INSERT INTO campaign_applications (campaign_id, creator_id, proposed_fee, proposed_deliverables, creative_pitch, estimated_days, status, score, score_breakdown, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 'pending', ?, ?, ?)
            ''', (camp_id, user["user_id"], proposed_fee, deliverables, pitch, est_days, total_score, json.dumps(breakdown), now))
            
            # Notify Business Owner
            c.execute('''
            INSERT INTO notifications (user_id, title, message, link, is_read, created_at)
            VALUES (?, ?, ?, ?, 0, ?)
            ''', (camp_row["business_id"], "New Campaign Proposal Received", f"{user['full_name']} applied to '{camp_row['title']}' with an Opportunity Score of {total_score}!", f"#/campaigns/{camp_id}", now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True, "score": total_score})

        # 5. Accept Application -> Start Collaboration & Issue QR/Coupon Codes
        elif path.startswith("/api/campaigns/applications/") and path.endswith("/accept"):
            app_id = path.split("/")[4]
            if not user or user["role"] != "business":
                conn.close()
                return self.send_error_json("Unauthorized", 403)

            c.execute('''
            SELECT ca.*, c.business_id, c.title as camp_title, c.deliverables as camp_deliverables,
                   u.full_name as creator_name
            FROM campaign_applications ca
            JOIN campaigns c ON ca.campaign_id = c.id
            JOIN users u ON ca.creator_id = u.id
            WHERE ca.id = ?
            ''', (app_id,))
            app_row = c.fetchone()
            if not app_row:
                conn.close()
                return self.send_error_json("Application not found", 404)
            app = dict(app_row)

            if app["business_id"] != user["user_id"]:
                conn.close()
                return self.send_error_json("You do not own this campaign", 403)

            # Update application status
            c.execute("UPDATE campaign_applications SET status = 'accepted' WHERE id = ?", (app_id,))

            # Create Collaboration
            terms = f"Standard CampusCrew Agreement: {app['proposed_deliverables']}. Max 2 revision rounds. Payment released upon final review approval."
            deadline = (datetime.now() + timedelta(days=app["estimated_days"])).strftime("%Y-%m-%d")
            
            c.execute('''
            INSERT INTO collaborations (campaign_id, business_id, creator_id, agreed_fee, terms_agreement, max_revisions, used_revisions, deadline, status, created_at)
            VALUES (?, ?, ?, ?, ?, 2, 0, ?, 'in_progress', ?)
            ''', (app["campaign_id"], user["user_id"], app["creator_id"], app["proposed_fee"], terms, deadline, now))
            new_collab_id = c.lastrowid

            # Initialize Deliverables
            c.execute('''
            INSERT INTO deliverables (collaboration_id, title, deliverable_type, status, created_at)
            VALUES (?, ?, 'Content Piece #1', 'pending', ?)
            ''', (new_collab_id, app["proposed_deliverables"], now))

            # Generate Unique QR & Coupon Code for Attribution
            qr_uuid = f"QR-{new_collab_id}-{uuid.uuid4().hex[:6].upper()}"
            coupon = f"CREW{new_collab_id}{secrets.token_hex(2).upper()}"
            c.execute('''
            INSERT INTO tracking_codes (collaboration_id, campaign_id, creator_id, business_id, qr_code_id, coupon_code, discount_percent, created_at)
            VALUES (?, ?, ?, ?, ?, ?, 15.0, ?)
            ''', (new_collab_id, app["campaign_id"], app["creator_id"], user["user_id"], qr_uuid, coupon, now))

            # Initialize Deal Payment in Escrow
            c.execute('''
            INSERT INTO deal_payments (collaboration_id, amount, status, tx_reference, invoice_no, created_at)
            VALUES (?, ?, 'escrow_held', ?, ?, ?)
            ''', (new_collab_id, app["proposed_fee"], f"TX-{uuid.uuid4().hex[:10].upper()}", f"INV-2026-{new_collab_id:04d}", now))

            # Notify Creator
            c.execute('''
            INSERT INTO notifications (user_id, title, message, link, is_read, created_at)
            VALUES (?, ?, ?, ?, 0, ?)
            ''', (app["creator_id"], "Proposal Accepted! Collaboration Active", f"Your proposal for '{app['camp_title']}' was accepted. Access your Collaboration Hub to view deliverables and promo codes.", f"#/collaborations/{new_collab_id}", now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True, "collaboration_id": new_collab_id})

        # 6. Submit Deliverable (Creator)
        elif path.startswith("/api/collaborations/") and "/deliverables/" in path and path.endswith("/submit"):
            parts = path.split("/")
            collab_id = parts[3]
            deliv_id = parts[5]

            submission_url = body.get("submission_url", "").strip()
            notes = body.get("submission_notes", "")

            if not submission_url:
                conn.close()
                return self.send_error_json("Submission URL is required", 400)

            c.execute('''
            UPDATE deliverables 
            SET status = 'submitted', submission_url = ?, submission_notes = ?, submitted_at = ?
            WHERE id = ? AND collaboration_id = ?
            ''', (submission_url, notes, now, deliv_id, collab_id))

            c.execute("UPDATE collaborations SET status = 'draft_submitted' WHERE id = ?", (collab_id,))

            # Notify Business
            c.execute("SELECT business_id, creator_id FROM collaborations WHERE id = ?", (collab_id,))
            col_row = c.fetchone()
            if col_row:
                c.execute('''
                INSERT INTO notifications (user_id, title, message, link, is_read, created_at)
                VALUES (?, ?, ?, ?, 0, ?)
                ''', (col_row["business_id"], "Draft Content Uploaded", "Creator submitted a draft for review. Check out the link and approve or leave revision feedback.", f"#/collaborations/{collab_id}", now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True})

        # 7. Approve Deliverable (Business)
        elif path.startswith("/api/collaborations/") and "/deliverables/" in path and path.endswith("/approve"):
            parts = path.split("/")
            collab_id = parts[3]
            deliv_id = parts[5]

            c.execute('''
            UPDATE deliverables 
            SET status = 'approved', approved_at = ?
            WHERE id = ? AND collaboration_id = ?
            ''', (now, deliv_id, collab_id))

            c.execute("UPDATE collaborations SET status = 'content_approved' WHERE id = ?", (collab_id,))

            # Notify Creator
            c.execute("SELECT creator_id FROM collaborations WHERE id = ?", (collab_id,))
            col_row = c.fetchone()
            if col_row:
                c.execute('''
                INSERT INTO notifications (user_id, title, message, link, is_read, created_at)
                VALUES (?, ?, ?, ?, 0, ?)
                ''', (col_row["creator_id"], "Draft Approved!", "Your deliverable has been approved by the brand. You may now publish and claim milestone release.", f"#/collaborations/{collab_id}", now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True})

        # 8. Request Revision (Business)
        elif path.startswith("/api/collaborations/") and "/deliverables/" in path and path.endswith("/request-revision"):
            parts = path.split("/")
            collab_id = parts[3]
            deliv_id = parts[5]
            notes = body.get("revision_notes", "").strip()

            c.execute("SELECT max_revisions, used_revisions, creator_id FROM collaborations WHERE id = ?", (collab_id,))
            row = c.fetchone()
            if not row:
                conn.close()
                return self.send_error_json("Collaboration not found", 404)

            max_rev = row["max_revisions"]
            used_rev = row["used_revisions"]

            if used_rev >= max_rev:
                conn.close()
                return self.send_error_json(f"Revision limit reached ({max_rev} rounds included in agreement). Please approve or contact admin.", 400)

            new_used = used_rev + 1
            c.execute('''
            UPDATE deliverables
            SET status = 'revision_needed', revision_notes = ?
            WHERE id = ? AND collaboration_id = ?
            ''', (notes, deliv_id, collab_id))

            c.execute('''
            UPDATE collaborations
            SET status = 'revisions_requested', used_revisions = ?
            WHERE id = ?
            ''', (new_used, collab_id))

            # Notify Creator
            c.execute('''
            INSERT INTO notifications (user_id, title, message, link, is_read, created_at)
            VALUES (?, ?, ?, ?, 0, ?)
            ''', (row["creator_id"], f"Revision Requested (Round {new_used} of {max_rev})", f"Brand requested edits: '{notes}'", f"#/collaborations/{collab_id}", now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True, "revisions_used": new_used, "max_revisions": max_rev})

        # 9. Mark Completed & Release Payment (Business)
        elif path.startswith("/api/collaborations/") and path.endswith("/complete"):
            collab_id = path.split("/")[3]
            c.execute("UPDATE collaborations SET status = 'completed' WHERE id = ?", (collab_id,))
            c.execute("UPDATE deal_payments SET status = 'paid', paid_at = ? WHERE collaboration_id = ?", (now, collab_id))

            c.execute("SELECT creator_id, business_id FROM collaborations WHERE id = ?", (collab_id,))
            col_row = c.fetchone()
            if col_row:
                c.execute('''
                INSERT INTO notifications (user_id, title, message, link, is_read, created_at)
                VALUES (?, ?, ?, ?, 0, ?)
                ''', (col_row["creator_id"], "Deal Completed & Payment Released!", "The brand has signed off! Your funds have been released. Don't forget to leave a review.", f"#/collaborations/{collab_id}", now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True})

        # 10. Send Chat Message
        elif path.startswith("/api/collaborations/") and path.endswith("/messages"):
            collab_id = path.split("/")[3]
            if not user:
                conn.close()
                return self.send_error_json("Unauthorized", 401)

            msg_text = body.get("message_text", "").strip()
            if not msg_text:
                conn.close()
                return self.send_error_json("Message cannot be empty", 400)

            c.execute("SELECT business_id, creator_id FROM collaborations WHERE id = ?", (collab_id,))
            col_row = c.fetchone()
            if not col_row:
                conn.close()
                return self.send_error_json("Collaboration not found", 404)

            receiver_id = col_row["creator_id"] if user["user_id"] == col_row["business_id"] else col_row["business_id"]

            c.execute('''
            INSERT INTO messages (collaboration_id, sender_id, receiver_id, message_text, is_read, created_at)
            VALUES (?, ?, ?, ?, 0, ?)
            ''', (collab_id, user["user_id"], receiver_id, msg_text, now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True})

        # 11. Log Tracking Event (Real QR scan or Coupon Redemption simulator)
        elif path == "/api/tracking/event":
            code_id = body.get("tracking_code_id")
            event_type = body.get("event_type", "qr_scan")
            order_val = float(body.get("order_value", 0.0) or 0.0)
            cust_ref = body.get("customer_ref", f"Guest-{secrets.token_hex(2)}")

            c.execute('''
            INSERT INTO tracking_events (tracking_code_id, event_type, order_value, customer_ref, created_at)
            VALUES (?, ?, ?, ?, ?)
            ''', (code_id, event_type, order_val, cust_ref, now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True, "event": event_type, "timestamp": now})

        # 12. Submit Review (Two-way gated to completed collaborations)
        elif path == "/api/reviews":
            if not user:
                conn.close()
                return self.send_error_json("Unauthorized", 401)

            collab_id = body.get("collaboration_id")
            rating = int(body.get("rating", 5))
            review_text = body.get("review_text", "").strip()

            c.execute("SELECT * FROM collaborations WHERE id = ?", (collab_id,))
            col_row = c.fetchone()
            if not col_row:
                conn.close()
                return self.send_error_json("Collaboration not found", 404)

            if col_row["status"] != "completed":
                conn.close()
                return self.send_error_json("Reviews are strictly gated to completed collaborations", 400)

            target_id = col_row["creator_id"] if user["user_id"] == col_row["business_id"] else col_row["business_id"]

            c.execute("SELECT id FROM reviews WHERE collaboration_id = ? AND author_id = ?", (collab_id, user["user_id"]))
            if c.fetchone():
                conn.close()
                return self.send_error_json("You have already reviewed this collaboration", 400)

            c.execute('''
            INSERT INTO reviews (collaboration_id, author_id, target_id, rating, review_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (collab_id, user["user_id"], target_id, rating, review_text, now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True})

        # 13. Campaign Content Brief Generator
        elif path == "/api/brief-generator":
            category = body.get("category", "Food & Beverage")
            objective = body.get("objective", "Footfall & QR Scans")
            budget = float(body.get("budget", 500.0) or 500.0)

            # High-converting creative brief templates
            briefs = {
                "Food & Beverage": {
                    "hooks": [
                        "“Is this the best study matcha in campus town? Testing it so you don't have to.”",
                        "“Secret menu item you NEED to try during finals week!”",
                        "“POV: You found your new favorite work-from-cafe sanctuary.”"
                    ],
                    "storyboard": "1. 0-3s: Macro shot of drink pouring with trending audio. 2. 4-15s: First sip reaction + interior vibe. 3. 16-25s: Counter check-in showcasing student 15% discount. 4. 26-30s: Clear CTA to scan QR on counter or use coupon code.",
                    "call_to_action": "Show this Reel or scan the counter QR for 15% off your first study beverage!",
                    "recommended_package": "1 Macro Tasting Reel + 2 Story Reminders + 1 Creator Co-Host Event"
                },
                "Fitness & Health": {
                    "hooks": [
                        "“The student gym pass that actually saved my semester workouts.”",
                        "“Full workout routine: 45 minutes on the turf zone.”",
                        "“Don't start your fitness journey without checking this out.”"
                    ],
                    "storyboard": "1. High-tempo workout clips. 2. Tour of recovery zone and weights. 3. Free 3-day pass announcement. 4. Bio link QR code call to action.",
                    "call_to_action": "Scan my bio link or use code FITCREW to claim your free 3-day pass!",
                    "recommended_package": "2 Workout Reels + 3 Story Frames + Bio Link Coupon"
                },
                "Beauty & Wellness": {
                    "hooks": [
                        "“My unfiltered morning skincare routine for tired college skin.”",
                        "“Derm-approved local clinic visit you didn't know existed.”",
                        "“Get ready with me for class: Clean glow edition.”"
                    ],
                    "storyboard": "1. Aesthetic texture swatches. 2. Face application tutorial. 3. Natural lighting results. 4. Promo code overlay.",
                    "call_to_action": "Use code GLOW15 at checkout for 15% off the student skincare set!",
                    "recommended_package": "1 GRWM Reel + 1 Product Carousel + Discount Code"
                },
                "Fashion & Retail": {
                    "hooks": [
                        "“Styling 3 thrifted outfits for under $50 right off campus.”",
                        "“Vintage drop alert: What I found at Saturday's market.”",
                        "“Stop buying fast fashion, shop local streetwear here.”"
                    ],
                    "storyboard": "1. Fast-paced transition jump cuts trying on outfits. 2. Racks inspection. 3. Store location pin. 4. Drop countdown.",
                    "call_to_action": "First 50 students through the doors get $10 thrift credits!",
                    "recommended_package": "1 Try-On Reel + 2 Hype Stories + In-Store Meetup"
                }
            }

            matched = briefs.get(category, briefs["Food & Beverage"])
            conn.close()
            return self.send_json({"brief": matched})

        # 14. Issue Student Certificate
        elif path == "/api/student/certificates":
            if not user:
                conn.close()
                return self.send_error_json("Unauthorized", 401)

            cert_uuid = str(uuid.uuid4())
            student_id = int(body.get("student_id", user["user_id"]))
            client_name = body.get("client_name", user["full_name"])
            project_title = body.get("project_title", "Digital Creative Project")
            skills = body.get("skills_demonstrated", "Video Editing, Motion Graphics")
            completion_date = datetime.now().strftime("%Y-%m-%d")
            v_hash = hashlib.sha256(f"{cert_uuid}:{client_name}:{project_title}".encode()).hexdigest()[:16]

            c.execute('''
            INSERT INTO student_certificates (certificate_uuid, student_id, client_name, project_title, skills_demonstrated, completion_date, verification_hash, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cert_uuid, student_id, client_name, project_title, skills, completion_date, v_hash, now))

            conn.commit()
            conn.close()
            return self.send_json({"success": True, "certificate_uuid": cert_uuid, "verification_hash": v_hash})

        conn.close()
        self.send_error_json("API POST route not found", 404)

    # -------------------------------------------------------------
    # API PUT / DELETE HANDLERS
    # -------------------------------------------------------------
    def handle_api_put(self, path, body):
        conn = get_db()
        c = conn.cursor()
        user = get_current_user(self.headers)

        if path.startswith("/api/notifications/") and path.endswith("/read"):
            notif_id = path.split("/")[3]
            c.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notif_id,))
            conn.commit()
            conn.close()
            return self.send_json({"success": True})

        elif path == "/api/admin/settings":
            if not user or user["role"] != "admin":
                conn.close()
                return self.send_error_json("Admin only", 403)
            key = body.get("key")
            value = str(body.get("value"))
            c.execute("INSERT OR REPLACE INTO system_settings (key, value) VALUES (?, ?)", (key, value))
            conn.commit()
            conn.close()
            return self.send_json({"success": True, "key": key, "value": value})

        conn.close()
        self.send_error_json("API PUT route not found", 404)

    def handle_api_delete(self, path, query):
        conn = get_db()
        c = conn.cursor()
        user = get_current_user(self.headers)

        if path.startswith("/api/favourites/"):
            creator_id = path.split("/")[-1]
            if not user or user["role"] != "business":
                conn.close()
                return self.send_error_json("Unauthorized", 401)
            c.execute("DELETE FROM saved_creators WHERE business_id = ? AND creator_id = ?", (user["user_id"], creator_id))
            conn.commit()
            conn.close()
            return self.send_json({"success": True})

        conn.close()
        self.send_error_json("API DELETE route not found", 404)

def run_server():
    init_db()
    seed_db()
    server_address = ('127.0.0.1', PORT)
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.TCPServer(server_address, CampusCrewHandler)
    print(f"CampusCrew Backend & Web Server running on http://127.0.0.1:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer shutting down gracefully.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
