import sqlite3
import os
import hashlib
import secrets
import json
import uuid
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), "campuscrew.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def hash_password(password, salt=None):
    if not salt:
        salt = secrets.token_hex(16)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt.encode('utf-8'), 
        100000
    ).hex()
    return pw_hash, salt

def verify_password(password, stored_hash, salt):
    pw_hash, _ = hash_password(password, salt)
    return pw_hash == stored_hash

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # 1. Users Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('business', 'creator', 'admin', 'student')),
        full_name TEXT NOT NULL,
        avatar_url TEXT,
        is_verified INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    )''')
    
    # 2. Business Profiles
    c.execute('''
    CREATE TABLE IF NOT EXISTS business_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        company_name TEXT NOT NULL,
        category TEXT NOT NULL,
        location TEXT NOT NULL,
        city TEXT NOT NULL,
        lat REAL DEFAULT 0.0,
        lng REAL DEFAULT 0.0,
        description TEXT,
        logo_url TEXT,
        website TEXT,
        phone TEXT,
        budget_range TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    
    # 3. Creator Profiles
    c.execute('''
    CREATE TABLE IF NOT EXISTS creator_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        handle TEXT UNIQUE NOT NULL,
        niche TEXT NOT NULL,
        location TEXT NOT NULL,
        city TEXT NOT NULL,
        lat REAL DEFAULT 0.0,
        lng REAL DEFAULT 0.0,
        bio TEXT,
        portfolio_url TEXT,
        instagram_handle TEXT,
        youtube_handle TEXT,
        follower_count INTEGER DEFAULT 0,
        avg_engagement_rate REAL DEFAULT 0.0,
        base_rate REAL DEFAULT 0.0,
        audience_age_group TEXT,
        is_audience_verified INTEGER DEFAULT 0,
        reliability_score REAL DEFAULT 95.0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    
    # 4. Campaigns Table
    c.execute('''
    CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        category TEXT NOT NULL,
        objective TEXT NOT NULL,
        budget REAL NOT NULL,
        collaboration_type TEXT NOT NULL CHECK(collaboration_type IN ('paid', 'barter', 'hybrid')),
        target_location TEXT NOT NULL,
        required_niche TEXT NOT NULL,
        deliverables TEXT NOT NULL,
        deadline TEXT NOT NULL,
        application_deadline TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'published' 
            CHECK(status IN ('draft', 'published', 'applications_open', 'under_review', 'accepted', 'in_progress', 'submitted', 'completed', 'cancelled')),
        created_at TEXT NOT NULL,
        FOREIGN KEY (business_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    
    # 5. Campaign Applications
    c.execute('''
    CREATE TABLE IF NOT EXISTS campaign_applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        proposed_fee REAL NOT NULL,
        proposed_deliverables TEXT NOT NULL,
        creative_pitch TEXT,
        estimated_days INTEGER DEFAULT 7,
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'under_review', 'accepted', 'rejected', 'withdrawn')),
        score REAL DEFAULT 0.0,
        score_breakdown TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
        FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(campaign_id, creator_id)
    )''')
    
    # 6. Collaborations (Active Contracts)
    c.execute('''
    CREATE TABLE IF NOT EXISTS collaborations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        campaign_id INTEGER NOT NULL,
        business_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        agreed_fee REAL NOT NULL,
        terms_agreement TEXT NOT NULL,
        max_revisions INTEGER DEFAULT 2,
        used_revisions INTEGER DEFAULT 0,
        deadline TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'in_progress' 
            CHECK(status IN ('in_progress', 'draft_submitted', 'revisions_requested', 'content_approved', 'completed', 'disputed', 'cancelled')),
        created_at TEXT NOT NULL,
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
        FOREIGN KEY (business_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    
    # 7. Deliverables Items
    c.execute('''
    CREATE TABLE IF NOT EXISTS deliverables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collaboration_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        deliverable_type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'submitted', 'revision_needed', 'approved')),
        submission_url TEXT,
        submission_notes TEXT,
        revision_notes TEXT,
        submitted_at TEXT,
        approved_at TEXT,
        FOREIGN KEY (collaboration_id) REFERENCES collaborations(id) ON DELETE CASCADE
    )''')
    
    # 8. Messages
    c.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collaboration_id INTEGER NOT NULL,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        message_text TEXT NOT NULL,
        attachment_url TEXT,
        is_read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (collaboration_id) REFERENCES collaborations(id) ON DELETE CASCADE,
        FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    
    # 9. Notifications
    c.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        link TEXT,
        is_read INTEGER DEFAULT 0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    
    # 10. Tracking Codes (QR & Coupons)
    c.execute('''
    CREATE TABLE IF NOT EXISTS tracking_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collaboration_id INTEGER NOT NULL,
        campaign_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        business_id INTEGER NOT NULL,
        qr_code_id TEXT UNIQUE NOT NULL,
        coupon_code TEXT UNIQUE NOT NULL,
        discount_percent REAL DEFAULT 15.0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (collaboration_id) REFERENCES collaborations(id) ON DELETE CASCADE
    )''')
    
    # 11. Tracking Events
    c.execute('''
    CREATE TABLE IF NOT EXISTS tracking_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking_code_id INTEGER NOT NULL,
        event_type TEXT NOT NULL CHECK(event_type IN ('qr_scan', 'coupon_redemption', 'lead_form', 'confirmed_sale')),
        order_value REAL DEFAULT 0.0,
        customer_ref TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (tracking_code_id) REFERENCES tracking_codes(id) ON DELETE CASCADE
    )''')
    
    # 12. Deal Payments & Invoices
    c.execute('''
    CREATE TABLE IF NOT EXISTS deal_payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collaboration_id INTEGER UNIQUE NOT NULL,
        amount REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'escrow_held' CHECK(status IN ('pending', 'escrow_held', 'in_transit', 'paid', 'refunded')),
        tx_reference TEXT UNIQUE NOT NULL,
        invoice_no TEXT UNIQUE NOT NULL,
        paid_at TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (collaboration_id) REFERENCES collaborations(id) ON DELETE CASCADE
    )''')
    
    # 13. Reviews (Two-way gated to completed collaborations)
    c.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collaboration_id INTEGER NOT NULL,
        author_id INTEGER NOT NULL,
        target_id INTEGER NOT NULL,
        rating INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
        review_text TEXT NOT NULL,
        communication_rating INTEGER DEFAULT 5,
        timeliness_rating INTEGER DEFAULT 5,
        quality_rating INTEGER DEFAULT 5,
        created_at TEXT NOT NULL,
        FOREIGN KEY (collaboration_id) REFERENCES collaborations(id) ON DELETE CASCADE,
        FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (target_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(collaboration_id, author_id)
    )''')
    
    # 14. Saved Creators (Favourites)
    c.execute('''
    CREATE TABLE IF NOT EXISTS saved_creators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        business_id INTEGER NOT NULL,
        creator_id INTEGER NOT NULL,
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (business_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (creator_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(business_id, creator_id)
    )''')
    
    # 15. Disputes
    c.execute('''
    CREATE TABLE IF NOT EXISTS disputes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        collaboration_id INTEGER NOT NULL,
        raised_by_id INTEGER NOT NULL,
        reason TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'open' CHECK(status IN ('open', 'under_review', 'resolved', 'dismissed')),
        resolution_notes TEXT,
        resolved_by_id INTEGER,
        created_at TEXT NOT NULL,
        FOREIGN KEY (collaboration_id) REFERENCES collaborations(id) ON DELETE CASCADE,
        FOREIGN KEY (raised_by_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    
    # 16. Audit Logs
    c.execute('''
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT NOT NULL,
        target_type TEXT NOT NULL,
        target_id INTEGER,
        details TEXT,
        created_at TEXT NOT NULL
    )''')
    
    # 17. Student Profiles (Future Modular Expansion)
    c.execute('''
    CREATE TABLE IF NOT EXISTS student_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        university TEXT NOT NULL,
        major TEXT NOT NULL,
        graduation_year INTEGER,
        skills TEXT NOT NULL, -- comma separated
        portfolio_links TEXT,
        hourly_rate REAL DEFAULT 20.0,
        bio TEXT,
        availability TEXT DEFAULT 'Part-Time',
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    
    # 18. Student Certificates
    c.execute('''
    CREATE TABLE IF NOT EXISTS student_certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        certificate_uuid TEXT UNIQUE NOT NULL,
        student_id INTEGER NOT NULL,
        client_name TEXT NOT NULL,
        project_title TEXT NOT NULL,
        skills_demonstrated TEXT NOT NULL,
        completion_date TEXT NOT NULL,
        verification_hash TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
    )''')
    
    # 19. System Settings
    c.execute('''
    CREATE TABLE IF NOT EXISTS system_settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )''')
    
    # Default settings
    c.execute('''INSERT OR IGNORE INTO system_settings (key, value) VALUES ('student_hub_enabled', 'true')''')
    c.execute('''INSERT OR IGNORE INTO system_settings (key, value) VALUES ('platform_commission_percent', '10.0')''')
    
    conn.commit()
    conn.close()

def seed_db():
    conn = get_db()
    c = conn.cursor()
    
    # Check if already seeded
    c.execute("SELECT COUNT(*) FROM users")
    if c.fetchone()[0] > 0:
        conn.close()
        return

    now = datetime.now().isoformat()
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    last_week = (datetime.now() - timedelta(days=7)).isoformat()
    
    default_pw = "campus123"
    
    # 1. Create Super Admin
    p_hash, salt = hash_password(default_pw)
    c.execute('''
    INSERT INTO users (email, password_hash, salt, role, full_name, avatar_url, is_verified, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('admin@campuscrew.com', p_hash, salt, 'admin', 'CampusCrew Governance', 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150', 1, last_week))
    admin_id = c.lastrowid

    # 2. Seed Businesses
    businesses = [
        {
            "name": "Urban Roast Cafe & Roastery",
            "email": "urbanroast@local.com",
            "category": "Food & Beverage",
            "location": "North Campus Main Street",
            "city": "Austin",
            "lat": 30.2849,
            "lng": -97.7341,
            "bio": "Artisanal coffee house, matcha bar and study sanctuary catering to university students and creative remote workers.",
            "logo": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=150",
            "budget": "$500 - $2,000"
        },
        {
            "name": "Apex Strength & Athletic Club",
            "email": "apex@fitness.com",
            "category": "Fitness & Health",
            "location": "West Campus Boulevard",
            "city": "Austin",
            "lat": 30.2889,
            "lng": -97.7420,
            "bio": "24/7 modern strength training facility, HIIT studios, and student fitness wellness challenges.",
            "logo": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=150",
            "budget": "$1,000 - $3,500"
        },
        {
            "name": "Luna Botanicals Skincare",
            "email": "hello@lunabotanicals.com",
            "category": "Beauty & Wellness",
            "location": "SoCo District Plaza",
            "city": "Austin",
            "lat": 30.2500,
            "lng": -97.7490,
            "bio": "Eco-friendly, cruelty-free organic skincare crafted for young professionals and Gen-Z skin wellness.",
            "logo": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=150",
            "budget": "$800 - $2,500"
        },
        {
            "name": "Neon Thread Vintage Boutique",
            "email": "threads@neonvintage.com",
            "category": "Fashion & Retail",
            "location": "East Campus Arts Corner",
            "city": "Austin",
            "lat": 30.2720,
            "lng": -97.7250,
            "bio": "Curated streetwear, 90s vintage finds, and sustainable upcycled college apparel.",
            "logo": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=150",
            "budget": "$300 - $1,200"
        }
    ]

    biz_user_ids = []
    for b in businesses:
        ph, s = hash_password(default_pw)
        c.execute('''
        INSERT INTO users (email, password_hash, salt, role, full_name, avatar_url, is_verified, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (b["email"], ph, s, 'business', b["name"], b["logo"], 1, last_week))
        uid = c.lastrowid
        biz_user_ids.append(uid)
        
        c.execute('''
        INSERT INTO business_profiles (user_id, company_name, category, location, city, lat, lng, description, logo_url, website, phone, budget_range, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (uid, b["name"], b["category"], b["location"], b["city"], b["lat"], b["lng"], b["bio"], b["logo"], f"https://{b['name'].lower().replace(' ', '')}.com", "+1-512-555-0199", b["budget"], last_week))

    # 3. Seed Creators
    creators = [
        {
            "name": "Sarah Chen",
            "handle": "@sarah_atx_bites",
            "email": "sarah@creator.com",
            "niche": "Food & Beverage",
            "location": "North Campus",
            "city": "Austin",
            "lat": 30.2860,
            "lng": -97.7330,
            "bio": "UT Senior & foodie creator highlighting hidden gem cafes, budget study snacks, and campus lunch spots.",
            "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
            "followers": 24500,
            "engagement": 6.8,
            "base_rate": 250.0,
            "age_group": "18-24 (78%)",
            "verified_audience": 1,
            "reliability": 98.5
        },
        {
            "name": "Marcus Vance",
            "handle": "@marcus_lifts",
            "email": "marcus@creator.com",
            "niche": "Fitness & Health",
            "location": "West Campus",
            "city": "Austin",
            "lat": 30.2895,
            "lng": -97.7410,
            "bio": "Collegiate track athlete sharing student workout routines, high-protein meal preps, and gym reviews.",
            "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150",
            "followers": 18200,
            "engagement": 7.4,
            "base_rate": 200.0,
            "age_group": "18-24 (82%)",
            "verified_audience": 1,
            "reliability": 96.0
        },
        {
            "name": "Elena Rodriguez",
            "handle": "@elena_glow",
            "email": "elena@creator.com",
            "niche": "Beauty & Wellness",
            "location": "Downtown / SoCo",
            "city": "Austin",
            "lat": 30.2600,
            "lng": -97.7450,
            "bio": "Dermatology student & clean skincare advocate reviewing local spa treatments and non-toxic routines.",
            "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=150",
            "followers": 31000,
            "engagement": 5.9,
            "base_rate": 320.0,
            "age_group": "18-30 (72%)",
            "verified_audience": 1,
            "reliability": 99.0
        },
        {
            "name": "Devin Brooks",
            "handle": "@devin_fits",
            "email": "devin@creator.com",
            "niche": "Fashion & Retail",
            "location": "East Campus",
            "city": "Austin",
            "lat": 30.2740,
            "lng": -97.7230,
            "bio": "Thrifter, streetwear styler and campus fashion week director. Helping local vintage shops sell out drops.",
            "avatar": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150",
            "followers": 14800,
            "engagement": 8.1,
            "base_rate": 180.0,
            "age_group": "18-24 (86%)",
            "verified_audience": 0,
            "reliability": 94.0
        },
        {
            "name": "Chloe Miller",
            "handle": "@chloe_campus_life",
            "email": "chloe@creator.com",
            "niche": "Lifestyle & Events",
            "location": "Campus Center",
            "city": "Austin",
            "lat": 30.2855,
            "lng": -97.7370,
            "bio": "Daily college vlogger, student council social chair, and campus guide. Event promos and hangout spots.",
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150",
            "followers": 42000,
            "engagement": 6.2,
            "base_rate": 400.0,
            "age_group": "18-25 (88%)",
            "verified_audience": 1,
            "reliability": 97.5
        }
    ]

    creator_user_ids = []
    for cr in creators:
        ph, s = hash_password(default_pw)
        c.execute('''
        INSERT INTO users (email, password_hash, salt, role, full_name, avatar_url, is_verified, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (cr["email"], ph, s, 'creator', cr["name"], cr["avatar"], 1, last_week))
        uid = c.lastrowid
        creator_user_ids.append(uid)
        
        c.execute('''
        INSERT INTO creator_profiles (user_id, handle, niche, location, city, lat, lng, bio, portfolio_url, instagram_handle, youtube_handle, follower_count, avg_engagement_rate, base_rate, audience_age_group, is_audience_verified, reliability_score, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (uid, cr["handle"], cr["niche"], cr["location"], cr["city"], cr["lat"], cr["lng"], cr["bio"], "https://portfolio.campuscrew.me/" + cr["handle"][1:], cr["handle"], cr["handle"][1:] + "_yt", cr["followers"], cr["engagement"], cr["base_rate"], cr["age_group"], cr["verified_audience"], cr["reliability"], last_week))

    # 4. Seed Campaigns
    campaigns = [
        {
            "biz_idx": 0, # Urban Roast
            "title": "Fall Nitro Matcha Launch & Study Night Promo",
            "desc": "We are introducing our seasonal Iced Lavender Oat Matcha and 24-hr study nights for finals week. Looking for 2 local food/campus creators to visit in-person, film an aesthetic reel tasting the drink, and share an exclusive 15% student coupon code with their followers.",
            "category": "Food & Beverage",
            "objective": "Footfall & Coupon Redemptions",
            "budget": 600.0,
            "type": "paid",
            "target_loc": "North Campus, Austin",
            "niche": "Food & Beverage",
            "deliverables": "1 Instagram Reel (30-45s) + 2 IG Stories with clickable QR link + In-store check-in",
            "deadline": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
            "app_deadline": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "status": "in_progress"
        },
        {
            "biz_idx": 1, # Apex Strength
            "title": "Semester Fitness Reboot – 3-Day Free Pass Challenge",
            "desc": "Boost student memberships by showcasing our state-of-the-art turf zone and group classes. Creators will receive a complimentary 6-month VIP membership and $450 payment per creator.",
            "category": "Fitness & Health",
            "objective": "New Gym Memberships & QR Scans",
            "budget": 900.0,
            "type": "paid",
            "target_loc": "West Campus, Austin",
            "niche": "Fitness & Health",
            "deliverables": "1 High-Energy Workout Reel + 3 Story frames highlighting student discount + Bio link QR code",
            "deadline": (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d"),
            "app_deadline": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
            "status": "published"
        },
        {
            "biz_idx": 2, # Luna Botanicals
            "title": "Clean Skin Campus Kit Unboxing & Routine",
            "desc": "Gifting our bestselling Acne Defense Duo. Create a real 'Get Ready With Me' (GRWM) morning routine showing application and texture. Looking for aesthetic skin creators.",
            "category": "Beauty & Wellness",
            "objective": "Online Orders & Brand Awareness",
            "budget": 450.0,
            "type": "hybrid",
            "target_loc": "SoCo & University Campus",
            "niche": "Beauty & Wellness",
            "deliverables": "1 GRWM Reel + 1 Product Carousel + Discount code promotion",
            "deadline": (datetime.now() + timedelta(days=18)).strftime("%Y-%m-%d"),
            "app_deadline": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
            "status": "applications_open"
        },
        {
            "biz_idx": 3, # Neon Thread
            "title": "Vintage Drop Saturday: First 50 Shoppers Event",
            "desc": "Promote our monthly vintage clothing thrift drop this Saturday morning. Need 2 creators to try on outfits and announce the in-store morning giveaway.",
            "category": "Fashion & Retail",
            "objective": "Event Attendance & Footfall",
            "budget": 350.0,
            "type": "paid",
            "target_loc": "East Campus Arts Corner",
            "niche": "Fashion & Retail",
            "deliverables": "2 Try-On Haul Stories + 1 Event Teaser Reel",
            "deadline": (datetime.now() + timedelta(days=8)).strftime("%Y-%m-%d"),
            "app_deadline": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "status": "published"
        }
    ]

    camp_ids = []
    for cmp in campaigns:
        b_uid = biz_user_ids[cmp["biz_idx"]]
        c.execute('''
        INSERT INTO campaigns (business_id, title, description, category, objective, budget, collaboration_type, target_location, required_niche, deliverables, deadline, application_deadline, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (b_uid, cmp["title"], cmp["desc"], cmp["category"], cmp["objective"], cmp["budget"], cmp["type"], cmp["target_loc"], cmp["niche"], cmp["deliverables"], cmp["deadline"], cmp["app_deadline"], cmp["status"], last_week))
        camp_ids.append(c.lastrowid)

    # 5. Create an Active Collaboration for Urban Roast & Sarah Chen
    # Campaign 1 + Creator 1 (Sarah)
    active_camp_id = camp_ids[0]
    active_biz_id = biz_user_ids[0]
    active_creator_id = creator_user_ids[0]

    # Application
    c.execute('''
    INSERT INTO campaign_applications (campaign_id, creator_id, proposed_fee, proposed_deliverables, creative_pitch, estimated_days, status, score, score_breakdown, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (active_camp_id, active_creator_id, 300.0, "1 Tasting Reel + 2 Stories + QR Table Card Shoutout", "I have a highly active student audience that studies in North Campus. I can feature your new Lavender Matcha as my 'study fuel of the week'!", 5, 'accepted', 96.5, json.dumps({
        "location_match": 100,
        "niche_match": 100,
        "budget_match": 95,
        "reliability": 98,
        "engagement_quality": 92
    }), last_week))

    # Collaboration Contract
    c.execute('''
    INSERT INTO collaborations (campaign_id, business_id, creator_id, agreed_fee, terms_agreement, max_revisions, used_revisions, deadline, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (active_camp_id, active_biz_id, active_creator_id, 300.0, "CampusCrew Standard Agreement: 1 30-45s Reel + 2 Stories. Up to 2 revisions included. Payment released within 48h of final approval. No unapproved music.", 2, 0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"), 'in_progress', yesterday))
    collab_id = c.lastrowid

    # Deliverables
    c.execute('''
    INSERT INTO deliverables (collaboration_id, title, deliverable_type, status, submission_url, submission_notes, revision_notes, submitted_at, approved_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (collab_id, "Draft Reel: Lavender Matcha Tasting & Study Vibe", "Instagram Reel", "submitted", "https://instagram.com/p/sample_reel_draft_preview", "Hey team! Here is the draft video cut with trending audio. Let me know if the color grading looks great!", None, yesterday, None))
    
    c.execute('''
    INSERT INTO deliverables (collaboration_id, title, deliverable_type, status, submission_url, submission_notes, revision_notes, submitted_at, approved_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (collab_id, "2 Instagram Story Slides with QR Link", "Instagram Stories", "pending", None, None, None, None, None))

    # Tracking Code for Sarah's campaign
    qr_uuid = "QR-URBAN-SARAH-01"
    coupon_code = "SARAH15"
    c.execute('''
    INSERT INTO tracking_codes (collaboration_id, campaign_id, creator_id, business_id, qr_code_id, coupon_code, discount_percent, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (collab_id, active_camp_id, active_creator_id, active_biz_id, qr_uuid, coupon_code, 15.0, yesterday))
    tcode_id = c.lastrowid

    # Seed Tracking Events (Simulating real footfall & redemptions)
    events_data = [
        ('qr_scan', 0.0, 'Visitor #101'),
        ('qr_scan', 0.0, 'Visitor #102'),
        ('qr_scan', 0.0, 'Visitor #103'),
        ('coupon_redemption', 18.50, 'Order #A412'),
        ('coupon_redemption', 24.00, 'Order #A419'),
        ('qr_scan', 0.0, 'Visitor #104'),
        ('coupon_redemption', 14.75, 'Order #A430'),
        ('confirmed_sale', 42.00, 'Order #A445'),
        ('qr_scan', 0.0, 'Visitor #105'),
        ('qr_scan', 0.0, 'Visitor #106'),
        ('coupon_redemption', 29.50, 'Order #A462'),
    ]
    for ev_type, val, cust in events_data:
        c.execute('''
        INSERT INTO tracking_events (tracking_code_id, event_type, order_value, customer_ref, created_at)
        VALUES (?, ?, ?, ?, ?)
        ''', (tcode_id, ev_type, val, cust, yesterday))

    # Payment Record in Escrow
    c.execute('''
    INSERT INTO deal_payments (collaboration_id, amount, status, tx_reference, invoice_no, paid_at, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (collab_id, 300.0, 'escrow_held', f'TX-{uuid.uuid4().hex[:10].upper()}', f'INV-2026-0081', None, yesterday))

    # Contextual Chat Messages
    c.execute('''
    INSERT INTO messages (collaboration_id, sender_id, receiver_id, message_text, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (collab_id, active_biz_id, active_creator_id, "Hi Sarah! Welcome to the campaign. We are so excited to work together on this launch. Let us know when you can drop by for the tasting!", 1, yesterday))

    c.execute('''
    INSERT INTO messages (collaboration_id, sender_id, receiver_id, message_text, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (collab_id, active_creator_id, active_biz_id, "Thank you! I stopped by yesterday afternoon and filmed 4 great angles. Just uploaded the first Reel draft to our Collaboration Hub for your review!", 1, now))

    # Seed Notifications
    c.execute('''
    INSERT INTO notifications (user_id, title, message, link, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (active_biz_id, "Draft Submitted for Review", "Sarah Chen uploaded a draft for 'Fall Nitro Matcha Launch'. Review and approve or request revision.", f"#/collaborations/{collab_id}", 0, now))

    c.execute('''
    INSERT INTO notifications (user_id, title, message, link, is_read, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (active_creator_id, "Campaign Agreement Active", "Your proposal for Urban Roast was accepted. Milestones are in progress.", f"#/collaborations/{collab_id}", 1, yesterday))

    # Seed Past Completed Collaboration with Reviews
    # Luna Botanicals + Elena Rodriguez
    c.execute('''
    INSERT INTO collaborations (campaign_id, business_id, creator_id, agreed_fee, terms_agreement, max_revisions, used_revisions, deadline, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (camp_ids[2], biz_user_ids[2], creator_user_ids[2], 320.0, "Standard Terms Completed", 2, 1, last_week, 'completed', last_week))
    past_collab_id = c.lastrowid

    # Reviews
    c.execute('''
    INSERT INTO reviews (collaboration_id, author_id, target_id, rating, review_text, communication_rating, timeliness_rating, quality_rating, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (past_collab_id, biz_user_ids[2], creator_user_ids[2], 5, "Elena produced phenomenal visual assets! Her GRWM video drove over 40 direct code redemptions in the first 48 hours. Absolute professional.", 5, 5, 5, last_week))

    c.execute('''
    INSERT INTO reviews (collaboration_id, author_id, target_id, rating, review_text, communication_rating, timeliness_rating, quality_rating, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (past_collab_id, creator_user_ids[2], biz_user_ids[2], 5, "Luna Botanicals is such a pleasure to work with! Clear creative guidelines, fast approvals, and payment released immediately upon posting.", 5, 5, 5, last_week))

    # Seed Saved Creators
    c.execute('''
    INSERT INTO saved_creators (business_id, creator_id, notes, created_at)
    VALUES (?, ?, ?, ?)
    ''', (biz_user_ids[0], creator_user_ids[0], "Top candidate for seasonal beverage launches", last_week))

    # Seed Student Profiles (For the Modular Student Talent Hub)
    student_pw_hash, s_salt = hash_password(default_pw)
    c.execute('''
    INSERT INTO users (email, password_hash, salt, role, full_name, avatar_url, is_verified, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ('alex@student.com', student_pw_hash, s_salt, 'student', 'Alex Rivera', 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150', 1, last_week))
    student_uid = c.lastrowid

    c.execute('''
    INSERT INTO student_profiles (user_id, university, major, graduation_year, skills, portfolio_links, hourly_rate, bio, availability, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (student_uid, "University of Texas at Austin", "Radio-Television-Film (RTF)", 2026, "Reel Editing, CapCut, Premiere Pro, Color Grading, Thumbnail Design", "https://behance.net/alex_creative", 25.0, "Film student specializing in fast-paced vertical video editing, sound design, and TikTok hooks for local businesses and creators.", "15-20 hrs/week", last_week))

    # Seed a Verified Experience Certificate
    cert_uuid = str(uuid.uuid4())
    c.execute('''
    INSERT INTO student_certificates (certificate_uuid, student_id, client_name, project_title, skills_demonstrated, completion_date, verification_hash, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (cert_uuid, student_uid, "Urban Roast Cafe", "Fall Campaign 10-Reel Batch Editing & Sound Design", "Adobe Premiere Pro, Color Correction, Vertical Formats, Audio Mixing", "2026-11-15", hashlib.sha256(f"{cert_uuid}:Urban Roast:Alex Rivera".encode()).hexdigest()[:16], last_week))

    conn.commit()
    conn.close()
    print("DATABASE INITIALIZED AND SEEDED WITH RICH PRODUCTION DATA SUCCESSFULLY!")

if __name__ == "__main__":
    init_db()
    seed_db()
