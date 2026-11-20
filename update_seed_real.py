import sqlite3
import hashlib
import secrets
import json
import uuid
from datetime import datetime, timedelta

from database import get_db, hash_password, DB_PATH

def update_real_assets():
    conn = get_db()
    c = conn.cursor()
    now = datetime.now().isoformat()
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    last_week = (datetime.now() - timedelta(days=7)).isoformat()
    
    default_pw = "campus123"

    # Check if Nati Ruchi already exists
    c.execute("SELECT id FROM users WHERE email = 'natiruchi@local.com'")
    existing = c.fetchone()
    
    if not existing:
        ph, s = hash_password(default_pw)
        # 1. Insert Nati Ruchi User
        c.execute('''
        INSERT INTO users (email, password_hash, salt, role, full_name, avatar_url, is_verified, created_at)
        VALUES (?, ?, ?, 'business', 'SNR Nati Ruchi Family Restaurant', '/images/real/nati_ruchi_storefront.jpg', 1, ?)
        ''', ('natiruchi@local.com', ph, s, last_week))
        nati_uid = c.lastrowid

        # 2. Insert Business Profile
        c.execute('''
        INSERT INTO business_profiles (user_id, company_name, category, location, city, lat, lng, description, logo_url, website, phone, budget_range, created_at)
        VALUES (?, 'SNR Nati Ruchi Family Restaurant', 'Food & Beverage', 'Opposite Campus Hub, College Main Rd', 'Bangalore', 12.9716, 77.5946, 
        'Authentic Nati-style dining and biryani house popular among college students, hostellers and campus visitors. Partnered with CampusCrew creators for in-store counter QR discount campaigns.', 
        '/images/real/nati_ruchi_storefront.jpg', 'https://natiruchi.campuscrew.me', '+91-98450-12890', '$400 - $1,500', ?)
        ''', (nati_uid, last_week))

        # 3. Insert Real Creator (Aditya - Campus Ambassador at the counter)
        c.execute("SELECT id FROM users WHERE email = 'aditya@creator.com'")
        existing_aditya = c.fetchone()
        if not existing_aditya:
            ph_cr, s_cr = hash_password(default_pw)
            c.execute('''
            INSERT INTO users (email, password_hash, salt, role, full_name, avatar_url, is_verified, created_at)
            VALUES (?, ?, ?, 'creator', 'Aditya Kumar', '/images/real/counter_qr_campaign_review.jpg', 1, ?)
            ''', ('aditya@creator.com', ph_cr, s_cr, last_week))
            aditya_uid = c.lastrowid

            c.execute('''
            INSERT INTO creator_profiles (user_id, handle, niche, location, city, lat, lng, bio, portfolio_url, instagram_handle, youtube_handle, follower_count, avg_engagement_rate, base_rate, audience_age_group, is_audience_verified, reliability_score, created_at)
            VALUES (?, '@aditya_campus_bites', 'Food & Beverage', 'College Campus Road', 'Bangalore', 12.9720, 77.5950,
            'Campus Ambassador & Food Creator connecting students with genuine local dining spots. Proven track record with in-store counter QR promotions.',
            'https://portfolio.campuscrew.me/aditya', '@aditya_campus_bites', 'aditya_campus_yt', 28500, 7.8, 280.0, '18-24 (84%)', 1, 99.0, ?)
            ''', (aditya_uid, last_week))
        else:
            aditya_uid = existing_aditya[0]

        # 4. Insert Campaign for Nati Ruchi
        c.execute('''
        INSERT INTO campaigns (business_id, title, description, category, objective, budget, collaboration_type, target_location, required_niche, deliverables, deadline, application_deadline, status, created_at)
        VALUES (?, 'SNR Nati Ruchi - Weekend Biryani & Student Thali Promotion',
        'Looking for local campus food creators to visit in-person, film an authentic tasting reel of our signature Nati chicken biryani and mutton thali, and set up our dedicated student 15% discount counter QR standee at the reception.',
        'Food & Beverage', 'Footfall & QR Redemptions', 500.0, 'paid', 'Campus Hub, Bangalore', 'Food & Beverage',
        '1 In-Store Tasting Reel (30-45s) + 2 Stories with Counter QR Standee Shoutout + Counter Placement',
        '2026-12-05', '2026-11-28', 'in_progress', ?)
        ''', (nati_uid, last_week))
        camp_id = c.lastrowid

        # 5. Insert Collaboration Contract
        c.execute('''
        INSERT INTO collaborations (campaign_id, business_id, creator_id, agreed_fee, terms_agreement, max_revisions, used_revisions, deadline, status, created_at)
        VALUES (?, ?, ?, 350.0,
        'CampusCrew Verified Agreement: 1 30-45s In-Store Reel + 2 Stories + Counter QR standee review. Max 2 revisions. In-store counter verification agreed.',
        2, 0, '2026-11-26', 'in_progress', ?)
        ''', (camp_id, nati_uid, aditya_uid, yesterday))
        collab_id = c.lastrowid

        # 6. Deliverables with real photos
        c.execute('''
        INSERT INTO deliverables (collaboration_id, title, deliverable_type, status, submission_url, submission_notes, revision_notes, submitted_at, approved_at)
        VALUES (?, 'In-Store Counter Review & QR Standee Setup', 'Instagram Reel & QR Placement', 'submitted',
        '/images/real/counter_qr_campaign_review.jpg',
        'Visited SNR Nati Ruchi, met the owner at the billing counter, set up the orange QR standee, and recorded reel with customer reactions.', NULL, ?, NULL)
        ''', (collab_id, yesterday))

        c.execute('''
        INSERT INTO deliverables (collaboration_id, title, deliverable_type, status, submission_url, submission_notes, revision_notes, submitted_at, approved_at)
        VALUES (?, 'Storefront Handshake & Announcement Stories', 'Instagram Stories', 'approved',
        '/images/real/business_creator_handshake.jpg',
        'Official campaign announcement story under the illuminated Nati Ruchi sign with the proprietor.', NULL, ?, ?)
        ''', (collab_id, yesterday, now))

        # 7. Tracking Code with QR & Coupon
        c.execute('''
        INSERT INTO tracking_codes (collaboration_id, campaign_id, creator_id, business_id, qr_code_id, coupon_code, discount_percent, created_at)
        VALUES (?, ?, ?, ?, 'QR-NATI-RUCHI-01', 'NATIRUCHI15', 15.0, ?)
        ''', (collab_id, camp_id, aditya_uid, nati_uid, yesterday))
        tcode_id = c.lastrowid

        # 8. Tracking Events
        events = [
            ('qr_scan', 0.0, 'Campus Visitor #12'),
            ('qr_scan', 0.0, 'Hostel Student #45'),
            ('coupon_redemption', 320.0, 'Table #4 - Biryani Combo'),
            ('coupon_redemption', 450.0, 'Table #7 - Special Thali Feast'),
            ('qr_scan', 0.0, 'Campus Visitor #19'),
            ('confirmed_sale', 650.0, 'Takeaway - Biryani Box (Order #902)')
        ]
        for ev, val, cust in events:
            c.execute('''
            INSERT INTO tracking_events (tracking_code_id, event_type, order_value, customer_ref, created_at)
            VALUES (?, ?, ?, ?, ?)
            ''', (tcode_id, ev, val, cust, yesterday))

        # 9. Review from Nati Ruchi Owner
        c.execute('''
        INSERT INTO reviews (collaboration_id, author_id, target_id, rating, review_text, communication_rating, timeliness_rating, quality_rating, created_at)
        VALUES (?, ?, ?, 5,
        'CampusCrew and Aditya brought real students right to our dining tables. The orange counter QR standee at our reception counter made it effortless to verify student orders and track the exact footfall. Highly recommended for local restaurants!',
        5, 5, 5, ?)
        ''', (collab_id, nati_uid, aditya_uid, yesterday))

        # 10. Messages
        c.execute('''
        INSERT INTO messages (collaboration_id, sender_id, receiver_id, message_text, is_read, created_at)
        VALUES (?, ?, ?, 'Namaste Aditya! We are delighted to partner with CampusCrew. The student response to the weekend biryani campaign has been wonderful!', 1, ?)
        ''', (collab_id, nati_uid, aditya_uid, yesterday))

        c.execute('''
        INSERT INTO messages (collaboration_id, sender_id, receiver_id, message_text, is_read, created_at)
        VALUES (?, ?, ?, 'Thank you sir! The in-store reel has already crossed 8,000 local student views, and the counter QR code is getting steady scans daily.', 1, ?)
        ''', (collab_id, aditya_uid, nati_uid, now))

        conn.commit()
        print("Real business SNR Nati Ruchi and Creator Aditya seeded successfully into SQLite!")

    conn.close()

update_real_assets()
