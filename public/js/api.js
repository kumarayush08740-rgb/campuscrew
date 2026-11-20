// CampusCrew Dual-Engine API Client (Server API + Instant LocalStore Fallback)
const API = {
  baseUrl: '/api',

  getToken() {
    return localStorage.getItem('cc_token') || 'demo_token';
  },

  setToken(token) {
    if (token) localStorage.setItem('cc_token', token);
    else localStorage.removeItem('cc_token');
  },

  async request(endpoint, options = {}) {
    // If opened via file:// protocol or offline, direct to local store immediately
    if (window.location.protocol === 'file:') {
      return this.handleLocalFallback(endpoint, options);
    }

    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };
    const token = this.getToken();
    if (token) headers['Authorization'] = `Bearer ${token}`;

    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 1200);

      const res = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers,
        signal: controller.signal
      });
      clearTimeout(timeoutId);

      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
      return data;
    } catch (err) {
      // Graceful fallback to LocalStore for 100% reliability
      return this.handleLocalFallback(endpoint, options);
    }
  },

  // Fallback Engine
  async handleLocalFallback(endpoint, options) {
    if (!LocalStore.db) await LocalStore.init();
    const db = LocalStore.db;
    const method = options.method || 'GET';
    const body = options.body ? JSON.parse(options.body) : {};

    // 1. Auth Me
    if (endpoint === '/auth/me') {
      const u = db.users[1]; // Default Urban Roast
      return { user: u };
    }

    // 2. Auth Login
    if (endpoint === '/auth/login') {
      const u = db.users.find(x => x.email === body.email) || db.users[1];
      this.setToken('demo_token_' + u.id);
      return { token: 'demo_token_' + u.id, user: u };
    }

    // 3. Creators Directory
    if (endpoint.startsWith('/profiles/creators') && !endpoint.includes('/profiles/creators/')) {
      const creators = db.creator_profiles.map(cp => {
        const u = db.users.find(x => x.id === cp.user_id) || {};
        return { ...cp, full_name: u.full_name, avatar_url: u.avatar_url, is_verified: u.is_verified };
      });
      return { creators };
    }

    // 4. Creator Detail
    if (endpoint.startsWith('/profiles/creators/')) {
      const id = parseInt(endpoint.split('/').pop());
      const cp = db.creator_profiles.find(x => x.id === id || x.user_id === id) || db.creator_profiles[0];
      const u = db.users.find(x => x.id === cp.user_id) || {};
      const reviews = db.reviews.filter(r => r.target_id === cp.user_id).map(r => ({ ...r, author_name: 'Verified Business Client' }));
      return { creator: { ...cp, full_name: u.full_name, avatar_url: u.avatar_url, reviews, completed_collabs: 4 } };
    }

    // 5. Campaigns
    if (endpoint.startsWith('/campaigns') && !endpoint.includes('/apply') && !endpoint.includes('/applications')) {
      if (method === 'POST') {
        const newCamp = { id: db.campaigns.length + 1, business_id: 2, ...body, status: 'published', application_count: 0 };
        db.campaigns.unshift(newCamp);
        LocalStore.save();
        return { success: true, campaign_id: newCamp.id };
      }
      const list = db.campaigns.map(c => {
        const b = db.users.find(x => x.id === c.business_id) || {};
        return { ...c, business_name: b.full_name, business_logo: b.avatar_url, business_category: c.category, application_count: 2 };
      });
      return { campaigns: list };
    }

    // 6. Apply to Campaign
    if (endpoint.includes('/apply')) {
      return { success: true, score: 96.5 };
    }

    // 7. Applications
    if (endpoint.includes('/applications') && !endpoint.includes('/accept')) {
      return {
        applications: [
          { id: 1, creator_name: "Sarah Chen", creator_avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150", handle: "@sarah_atx_bites", creator_location: "North Campus", score: 96.5, proposed_fee: 300, proposed_deliverables: "1 Tasting Reel + 2 Stories", creative_pitch: "Feature your new Lavender Matcha as my study fuel of the week!" },
          { id: 2, creator_name: "Devin Brooks", creator_avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150", handle: "@devin_fits", creator_location: "East Campus", score: 88.0, proposed_fee: 280, proposed_deliverables: "1 Reel + 1 Story Carousel", creative_pitch: "Show student weekend coffee run outfit & study session." }
        ]
      };
    }

    // 8. Accept Application
    if (endpoint.includes('/accept')) {
      return { success: true, collaboration_id: 1 };
    }

    // 9. Collaborations
    if (endpoint === '/collaborations') {
      const list = db.collaborations.map(col => {
        const camp = db.campaigns.find(c => c.id === col.campaign_id) || {};
        const cr = db.users.find(u => u.id === col.creator_id) || {};
        const b = db.users.find(u => u.id === col.business_id) || {};
        return { ...col, campaign_title: camp.title, creator_name: cr.full_name, business_name: b.full_name, creator_handle: "@sarah_atx_bites" };
      });
      return { collaborations: list };
    }

    // 10. Collaboration Detail
    if (endpoint.startsWith('/collaborations/') && !endpoint.includes('/deliverables') && !endpoint.includes('/messages') && !endpoint.includes('/complete')) {
      const col = db.collaborations[0];
      const camp = db.campaigns[0];
      const cr = db.users.find(u => u.id === col.creator_id) || {};
      const b = db.users.find(u => u.id === col.business_id) || {};
      const tcode = db.tracking_codes[0];
      
      const scans = db.tracking_events.filter(e => e.event_type === 'qr_scan').length;
      const redemptions = db.tracking_events.filter(e => e.event_type === 'coupon_redemption').length;
      const rev = db.tracking_events.reduce((sum, e) => sum + (e.order_value || 0), 0);

      return {
        collaboration: {
          ...col,
          campaign_title: camp.title,
          campaign_desc: camp.description,
          creator_name: cr.full_name,
          creator_handle: "@sarah_atx_bites",
          business_name: b.full_name,
          qr_code_id: tcode.qr_code_id,
          coupon_code: tcode.coupon_code,
          discount_percent: tcode.discount_percent,
          deliverables: db.deliverables,
          tracking_stats: { scans, redemptions, confirmed_sales: redemptions, revenue_generated: rev }
        }
      };
    }

    // 11. Deliverable Actions
    if (endpoint.includes('/deliverables/') && endpoint.endsWith('/submit')) {
      db.deliverables[0].status = 'submitted';
      db.deliverables[0].submission_url = body.submission_url;
      LocalStore.save();
      return { success: true };
    }

    if (endpoint.includes('/deliverables/') && endpoint.endsWith('/approve')) {
      db.deliverables[0].status = 'approved';
      LocalStore.save();
      return { success: true };
    }

    if (endpoint.includes('/deliverables/') && endpoint.endsWith('/request-revision')) {
      db.deliverables[0].status = 'revision_needed';
      db.deliverables[0].revision_notes = body.revision_notes;
      db.collaborations[0].used_revisions = (db.collaborations[0].used_revisions || 0) + 1;
      LocalStore.save();
      return { success: true, revisions_used: db.collaborations[0].used_revisions, max_revisions: 2 };
    }

    if (endpoint.endsWith('/complete')) {
      db.collaborations[0].status = 'completed';
      LocalStore.save();
      return { success: true };
    }

    // 12. Messages
    if (endpoint.includes('/messages')) {
      if (method === 'POST') {
        const newMsg = { id: db.messages.length + 1, collaboration_id: 1, sender_id: 2, sender_name: "You", message_text: body.message_text };
        db.messages.push(newMsg);
        LocalStore.save();
        return { success: true };
      }
      return { messages: db.messages.map(m => ({ ...m, sender_name: m.sender_id === 2 ? "Urban Roast Cafe" : "Sarah Chen" })) };
    }

    // 13. Tracking Event
    if (endpoint === '/tracking/event') {
      db.tracking_events.push({ id: db.tracking_events.length + 1, tracking_code_id: 1, event_type: body.event_type, order_value: body.order_value, customer_ref: body.customer_ref });
      LocalStore.save();
      return { success: true, event: body.event_type };
    }

    // 14. ROI Analytics
    if (endpoint.startsWith('/analytics/business/')) {
      const scans = db.tracking_events.filter(e => e.event_type === 'qr_scan').length;
      const redemptions = db.tracking_events.filter(e => e.event_type === 'coupon_redemption').length;
      const rev = db.tracking_events.reduce((sum, e) => sum + (e.order_value || 0), 0);
      const spend = 300.0;
      const roi = rev > 0 ? (((rev - spend) / spend) * 100).toFixed(1) : 0;

      return {
        analytics: {
          total_spend: spend,
          total_campaigns: 1,
          total_collaborations: 1,
          total_scans: scans,
          total_redemptions: redemptions,
          attributed_revenue: rev,
          roi_percent: roi,
          creator_performance: [
            { creator_name: "Sarah Chen", handle: "@sarah_atx_bites", coupon_code: "SARAH15", scans, redemptions, revenue: rev }
          ]
        }
      };
    }

    // 15. Brief Generator
    if (endpoint === '/brief-generator') {
      return {
        brief: {
          hooks: [
            "“Is this the best study matcha in campus town? Testing it so you don't have to.”",
            "“Secret menu item you NEED to try during finals week!”",
            "“POV: You found your new favorite work-from-cafe sanctuary.”"
          ],
          storyboard: "1. 0-3s: Macro shot of drink pouring with trending audio. 2. 4-15s: First sip reaction + interior vibe. 3. 16-25s: Counter check-in showcasing student 15% discount. 4. 26-30s: Clear CTA to scan QR on counter or use coupon code.",
          call_to_action: "Show this Reel or scan the counter QR for 15% off your first study beverage!",
          recommended_package: "1 Macro Tasting Reel + 2 Story Reminders + 1 Creator Co-Host Event"
        }
      };
    }

    // 16. Student Hub
    if (endpoint === '/student/talents') {
      return { students: db.student_profiles.map(sp => ({ ...sp, full_name: "Alex Rivera", avatar_url: "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=150" })) };
    }

    if (endpoint.startsWith('/student/certificates/')) {
      return { certificate: { ...db.student_certificates[0], student_name: "Alex Rivera", university: "UT Austin" } };
    }

    // 17. Admin
    if (endpoint === '/admin/overview') {
      return {
        overview: {
          total_users: db.users.length,
          total_campaigns: db.campaigns.length,
          total_collaborations: db.collaborations.length,
          total_gmv: 2450.0,
          open_disputes: 0,
          student_hub_enabled: db.system_settings.student_hub_enabled === "true"
        }
      };
    }

    if (endpoint === '/admin/disputes') {
      return { disputes: [] };
    }

    if (endpoint === '/admin/settings') {
      db.system_settings[body.key] = body.value;
      LocalStore.save();
      return { success: true };
    }

    return { success: true };
  },

  // API wrappers
  async getMe() { return this.request('/auth/me'); },
  async login(email, password) { return this.request('/auth/login', { method: 'POST', body: JSON.stringify({ email, password }) }); },
  async getCreators(params) { return this.request('/profiles/creators'); },
  async getCreator(id) { return this.request(`/profiles/creators/${id}`); },
  async getCampaigns(params) { return this.request('/campaigns'); },
  async createCampaign(data) { return this.request('/campaigns', { method: 'POST', body: JSON.stringify(data) }); },
  async applyToCampaign(campId, data) { return this.request(`/campaigns/${campId}/apply`, { method: 'POST', body: JSON.stringify(data) }); },
  async getApplications(campId) { return this.request(`/campaigns/${campId}/applications`); },
  async acceptApplication(appId) { return this.request(`/campaigns/applications/${appId}/accept`, { method: 'POST', body: JSON.stringify({}) }); },
  async getCollaborations() { return this.request('/collaborations'); },
  async getCollaboration(id) { return this.request(`/collaborations/${id}`); },
  async submitDeliverable(collabId, delivId, data) { return this.request(`/collaborations/${collabId}/deliverables/${delivId}/submit`, { method: 'POST', body: JSON.stringify(data) }); },
  async approveDeliverable(collabId, delivId) { return this.request(`/collaborations/${collabId}/deliverables/${delivId}/approve`, { method: 'POST', body: JSON.stringify({}) }); },
  async requestRevision(collabId, delivId, notes) { return this.request(`/collaborations/${collabId}/deliverables/${delivId}/request-revision`, { method: 'POST', body: JSON.stringify({ revision_notes: notes }) }); },
  async completeCollaboration(collabId) { return this.request(`/collaborations/${collabId}/complete`, { method: 'POST', body: JSON.stringify({}) }); },
  async getMessages(collabId) { return this.request(`/collaborations/${collabId}/messages`); },
  async sendMessage(collabId, text) { return this.request(`/collaborations/${collabId}/messages`, { method: 'POST', body: JSON.stringify({ message_text: text }) }); },
  async logTrackingEvent(data) { return this.request('/tracking/event', { method: 'POST', body: JSON.stringify(data) }); },
  async getBusinessAnalytics(bizId) { return this.request(`/analytics/business/${bizId}`); },
  async submitReview(data) { return this.request('/reviews', { method: 'POST', body: JSON.stringify(data) }); },
  async generateBrief(cat, obj, bud) { return this.request('/brief-generator', { method: 'POST', body: JSON.stringify({ category: cat, objective: obj, budget: bud }) }); },
  async getStudentTalents() { return this.request('/student/talents'); },
  async getStudentCertificate(uuid) { return this.request(`/student/certificates/${uuid}`); },
  async getAdminOverview() { return this.request('/admin/overview'); },
  async getAdminDisputes() { return this.request('/admin/disputes'); },
  async updateAdminSetting(key, val) { return this.request('/admin/settings', { method: 'PUT', body: JSON.stringify({ key, value: val }) }); }
};
