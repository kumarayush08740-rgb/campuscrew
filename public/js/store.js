// CampusCrew Local Data Engine (Enables 100% offline & file:// protocol operation)
const LocalStore = {
  db: null,

  async init() {
    const saved = localStorage.getItem('cc_local_db_v2');
    if (saved) {
      try {
        this.db = JSON.parse(saved);
        return;
      } catch (e) {
        console.warn("Resetting corrupted local store");
      }
    }
    
    // Fetch initial seed data
    try {
      const res = await fetch('/js/seed_data.json');
      if (res.ok) {
        this.db = await res.json();
        this.save();
        return;
      }
    } catch (e) {}

    // Fallback embedded minimal seed if fetch blocked
    this.db = {
      users: [
        { id: 1, email: "admin@campuscrew.com", role: "admin", full_name: "CampusCrew Governance", avatar_url: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150", is_verified: 1 },
        { id: 2, email: "natiruchi@local.com", role: "business", full_name: "SNR Nati Ruchi Family Restaurant", avatar_url: "images/real/nati_ruchi_storefront.jpg", is_verified: 1 },
        { id: 3, email: "aditya@creator.com", role: "creator", full_name: "Aditya Kumar", avatar_url: "images/real/counter_qr_campaign_review.jpg", is_verified: 1 },
        { id: 4, email: "alex@student.com", role: "student", full_name: "Alex Rivera", avatar_url: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150", is_verified: 1 }
      ],
      creator_profiles: [
        { id: 1, user_id: 3, handle: "@aditya_campus_bites", niche: "Food & Beverage", location: "College Campus Road", city: "Bangalore", lat: 12.972, lng: 77.595, bio: "Campus Ambassador & Food Creator connecting students with genuine local dining spots. Proven track record with in-store counter QR promotions.", follower_count: 28500, avg_engagement_rate: 7.8, base_rate: 280.0, audience_age_group: "18-24 (84%)", is_audience_verified: 1, reliability_score: 99.0 }
      ],
      campaigns: [
        { id: 1, business_id: 2, title: "SNR Nati Ruchi - Weekend Biryani & Student Thali Promotion", description: "Looking for local campus food creators to visit in-person, film an authentic tasting reel of our signature Nati chicken biryani and mutton thali, and set up our dedicated student 15% discount counter QR standee at the reception.", category: "Food & Beverage", objective: "Footfall & QR Redemptions", budget: 500.0, collaboration_type: "paid", target_location: "Campus Hub, Bangalore", required_niche: "Food & Beverage", deliverables: "1 In-Store Tasting Reel (30-45s) + 2 Stories with Counter QR Standee Shoutout", deadline: "2026-12-05", application_deadline: "2026-11-28", status: "in_progress" },
        { id: 2, business_id: 3, title: "Semester Fitness Reboot – 3-Day Free Pass Challenge", description: "Boost student memberships by showcasing our state-of-the-art turf zone and group classes. Creators will receive a complimentary 6-month VIP membership and $450 payment per creator.", category: "Fitness & Health", objective: "New Gym Memberships & QR Scans", budget: 900.0, collaboration_type: "paid", target_location: "West Campus, Austin", required_niche: "Fitness & Health", deliverables: "1 High-Energy Workout Reel + 3 Story frames highlighting student discount", deadline: "2026-12-10", application_deadline: "2026-11-30", status: "published" },
        { id: 3, business_id: 4, title: "Clean Skin Campus Kit Unboxing & Routine", description: "Gifting our bestselling Acne Defense Duo. Create a real 'Get Ready With Me' (GRWM) morning routine showing application and texture.", category: "Beauty & Wellness", objective: "Online Orders & Brand Awareness", budget: 450.0, collaboration_type: "hybrid", target_location: "SoCo & University Campus", required_niche: "Beauty & Wellness", deliverables: "1 GRWM Reel + 1 Product Carousel + Discount code promotion", deadline: "2026-12-08", application_deadline: "2026-11-29", status: "applications_open" },
        { id: 4, business_id: 5, title: "Vintage Drop Saturday: First 50 Shoppers Event", description: "Promote our monthly vintage clothing thrift drop this Saturday morning. Need 2 creators to try on outfits and announce the in-store morning giveaway.", category: "Fashion & Retail", objective: "Event Attendance & Footfall", budget: 350.0, collaboration_type: "paid", target_location: "East Campus Arts Corner", required_niche: "Fashion & Retail", deliverables: "2 Try-On Haul Stories + 1 Event Teaser Reel", deadline: "2026-11-28", application_deadline: "2026-11-22", status: "published" }
      ],
      collaborations: [
        { id: 1, campaign_id: 1, business_id: 2, creator_id: 3, agreed_fee: 350.0, terms_agreement: "CampusCrew Verified Agreement: 1 30-45s In-Store Reel + 2 Stories + Counter QR standee review. Max 2 revisions. In-store counter verification agreed.", max_revisions: 2, used_revisions: 0, deadline: "2026-11-28", status: "in_progress" }
      ],
      deliverables: [
        { id: 1, collaboration_id: 1, title: "In-Store Counter Review & QR Standee Setup", deliverable_type: "Instagram Reel & Standee", status: "submitted", submission_url: "images/real/counter_qr_campaign_review.jpg", submission_notes: "Recorded tasting reel with owner at the billing counter with live QR code standee in place." },
        { id: 2, collaboration_id: 1, title: "Storefront Handshake & Announcement Stories", deliverable_type: "Instagram Stories", status: "approved", submission_url: "images/real/business_creator_handshake.jpg", submission_notes: "Campaign kickoff story under the illuminated Nati Ruchi sign." }
      ],
      tracking_codes: [
        { id: 1, collaboration_id: 1, campaign_id: 1, creator_id: 3, business_id: 2, qr_code_id: "QR-NATI-RUCHI-01", coupon_code: "NATIRUCHI15", discount_percent: 15.0 }
      ],
      tracking_events: [
        { id: 1, tracking_code_id: 1, event_type: "qr_scan", order_value: 0.0, customer_ref: "Visitor #12" },
        { id: 2, tracking_code_id: 1, event_type: "qr_scan", order_value: 0.0, customer_ref: "Visitor #45" },
        { id: 3, tracking_code_id: 1, event_type: "coupon_redemption", order_value: 320.0, customer_ref: "Table #4 - Biryani Combo" },
        { id: 4, tracking_code_id: 1, event_type: "coupon_redemption", order_value: 450.0, customer_ref: "Table #7 - Special Thali Feast" }
      ],
      messages: [
        { id: 1, collaboration_id: 1, sender_id: 2, receiver_id: 3, message_text: "Namaste Aditya! The weekend biryani campaign response has been wonderful!", is_read: 1 },
        { id: 2, collaboration_id: 1, sender_id: 3, receiver_id: 2, message_text: "Thank you sir! The in-store reel is performing great and the counter QR code is getting steady scans.", is_read: 1 }
      ],
      reviews: [
        { id: 1, collaboration_id: 1, author_id: 2, target_id: 3, rating: 5, review_text: "The orange counter QR standee at our reception counter made it effortless to verify student orders and track the exact footfall. Highly recommended for local dining establishments!" }
      ],
      student_profiles: [
        { id: 1, user_id: 11, university: "University of Texas at Austin", major: "Radio-Television-Film (RTF)", graduation_year: 2026, skills: "Reel Editing, CapCut, Premiere Pro, Color Grading, Thumbnail Design", hourly_rate: 25.0, bio: "Film student specializing in fast-paced vertical video editing and TikTok hooks for local businesses and creators." }
      ],
      student_certificates: [
        { id: 1, certificate_uuid: "45f8a847-9dc4-4d8b-bd1e-5390e1cb2f5b", student_id: 11, client_name: "Urban Roast Cafe", project_title: "Fall Campaign 10-Reel Batch Editing & Sound Design", skills_demonstrated: "Adobe Premiere Pro, Color Correction, Vertical Formats", verification_hash: "9f82d1c6843a0e1b" }
      ],
      system_settings: { student_hub_enabled: "true" }
    };
    this.save();
  },

  save() {
    try {
      localStorage.setItem('cc_local_db_v1', JSON.stringify(this.db));
    } catch (e) {}
  }
};
