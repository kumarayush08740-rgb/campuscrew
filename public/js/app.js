// CampusCrew Application Controller & Router
const App = {
  currentUser: null,
  currentView: 'landing',
  creators: [],
  campaigns: [],
  compareList: [],
  activeFilters: {},
  debounceTimer: null,
  mapInstance: null,

  async init() {
    this.setupNavigation();
    
    // Auto-login or verify current session
    try {
      const res = await API.getMe();
      if (res.user) {
        this.currentUser = res.user;
      }
    } catch (e) {
      // Default to Business Demo for immediate smooth experience
      await this.showRoleDemo('business', false);
    }

    this.renderHeaderUser();
    this.handleRoute();
    window.addEventListener('hashchange', () => this.handleRoute());
  },

  setupNavigation() {
    // Top nav link active styling
    const updateActiveNav = (hash) => {
      document.querySelectorAll('.nav-link').forEach(link => {
        const href = link.getAttribute('href');
        if (href === hash || (hash === '' && href === '#')) {
          link.classList.add('text-white', 'bg-slate-800');
          link.classList.remove('text-slate-400');
        } else {
          link.classList.remove('text-white', 'bg-slate-800');
          link.classList.add('text-slate-400');
        }
      });
    };
    window.addEventListener('hashchange', () => updateActiveNav(window.location.hash));
  },

  renderHeaderUser() {
    const el = document.getElementById('user-header-profile');
    if (!el) return;

    if (this.currentUser) {
      el.innerHTML = `
        <div class="flex items-center gap-2.5 bg-slate-900 border border-slate-700/80 rounded-full pl-2 pr-3 py-1 shadow-sm">
          <img src="${this.currentUser.avatar_url || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'}" 
               class="w-6 h-6 rounded-full object-cover border border-indigo-400" />
          <div class="flex flex-col text-left">
            <span class="text-xs font-bold text-white leading-tight">${this.currentUser.full_name}</span>
            <span class="text-[10px] text-indigo-400 font-semibold uppercase">${this.currentUser.role}</span>
          </div>
        </div>
      `;
    } else {
      el.innerHTML = `
        <button onclick="App.showLoginModal()" class="px-4 py-1.5 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold">
          Log In
        </button>
      `;
    }
  },

  async handleRoute() {
    const hash = window.location.hash || '#';
    const main = document.getElementById('main-content');
    if (!main) return;

    if (hash === '#' || hash === '') {
      this.currentView = 'landing';
      main.innerHTML = Views.renderLanding(this.currentUser);
    } 
    else if (hash === '#explore') {
      this.currentView = 'explore';
      main.innerHTML = `<div class="text-center py-20 text-slate-400 text-sm">Loading verified local creators...</div>`;
      try {
        const data = await API.getCreators(this.activeFilters);
        this.creators = data.creators || [];
        main.innerHTML = Views.renderDiscovery(this.creators, this.activeFilters);
      } catch (err) {
        main.innerHTML = `<div class="p-8 text-center text-red-400 text-sm">Failed to load creators: ${err.message}</div>`;
      }
    } 
    else if (hash === '#campaigns') {
      this.currentView = 'campaigns';
      main.innerHTML = `<div class="text-center py-20 text-slate-400 text-sm">Loading active campaigns...</div>`;
      try {
        const data = await API.getCampaigns();
        this.campaigns = data.campaigns || [];
        main.innerHTML = Views.renderCampaigns(this.campaigns, this.currentUser);
      } catch (err) {
        main.innerHTML = `<div class="p-8 text-center text-red-400 text-sm">Failed to load campaigns: ${err.message}</div>`;
      }
    } 
    else if (hash === '#collaborations') {
      this.currentView = 'collaborations';
      main.innerHTML = `<div class="text-center py-20 text-slate-400 text-sm">Loading collaborations...</div>`;
      try {
        const data = await API.getCollaborations();
        const collabs = data.collaborations || [];
        if (collabs.length > 0) {
          // Open the first active collaboration
          window.location.hash = `#collaborations/${collabs[0].id}`;
        } else {
          main.innerHTML = `
            <div class="max-w-4xl mx-auto px-4 py-20 text-center">
              <div class="glass-card rounded-2xl p-12 border border-slate-800">
                <span class="text-4xl block mb-3">🤝</span>
                <h2 class="text-xl font-bold text-white mb-2">No Active Collaborations Yet</h2>
                <p class="text-xs text-slate-400 mb-6">Explore the marketplace or launch a campaign to start collaborating.</p>
                <a href="#campaigns" class="px-5 py-2.5 rounded-xl bg-indigo-600 text-white text-xs font-semibold">Explore Campaigns</a>
              </div>
            </div>
          `;
        }
      } catch (err) {
        main.innerHTML = `<div class="p-8 text-center text-red-400 text-sm">Error: ${err.message}</div>`;
      }
    } 
    else if (hash.startsWith('#collaborations/')) {
      const collabId = hash.split('/')[1];
      this.currentView = 'collab-detail';
      main.innerHTML = `<div class="text-center py-20 text-slate-400 text-sm">Opening collaboration workspace...</div>`;
      try {
        const data = await API.getCollaboration(collabId);
        main.innerHTML = Views.renderCollaborationHub(data.collaboration, this.currentUser);
        this.loadChatMessages(collabId);
      } catch (err) {
        main.innerHTML = `<div class="p-8 text-center text-red-400 text-sm">Error loading workspace: ${err.message}</div>`;
      }
    } 
    else if (hash === '#analytics') {
      this.currentView = 'analytics';
      main.innerHTML = `<div class="text-center py-20 text-slate-400 text-sm">Calculating verified ROI metrics...</div>`;
      try {
        const bizId = (this.currentUser && this.currentUser.role === 'business') ? this.currentUser.id : 2; // Default to Urban Roast
        const data = await API.getBusinessAnalytics(bizId);
        main.innerHTML = Views.renderROI(data.analytics, this.currentUser);
      } catch (err) {
        main.innerHTML = `<div class="p-8 text-center text-red-400 text-sm">Error: ${err.message}</div>`;
      }
    } 
    else if (hash === '#map') {
      this.currentView = 'map';
      const data = await API.getCreators();
      this.creators = data.creators || [];
      main.innerHTML = Views.renderMap(this.creators);
      setTimeout(() => this.initMap(this.creators), 100);
    } 
    else if (hash === '#briefs') {
      this.currentView = 'briefs';
      main.innerHTML = Views.renderBriefGenerator();
    } 
    else if (hash === '#student-hub') {
      this.currentView = 'student-hub';
      const [talentData, adminData] = await Promise.all([
        API.getStudentTalents(),
        API.getAdminOverview().catch(() => ({ overview: { student_hub_enabled: true } }))
      ]);
      const isEnabled = adminData.overview ? adminData.overview.student_hub_enabled : true;
      main.innerHTML = Views.renderStudentHub(talentData.students || [], isEnabled);
    } 
    else if (hash === '#admin') {
      this.currentView = 'admin';
      try {
        const [overviewData, disputeData] = await Promise.all([
          API.getAdminOverview(),
          API.getAdminDisputes()
        ]);
        main.innerHTML = Views.renderAdmin(overviewData.overview || {}, disputeData.disputes || []);
      } catch (err) {
        // If not admin, switch to admin demo
        await this.showRoleDemo('admin');
      }
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  },

  // Role Switcher / Demo Handlers
  async showRoleDemo(role, navigate = true) {
    const creds = {
      business: { email: 'natiruchi@local.com', pw: 'campus123' },
      creator: { email: 'aditya@creator.com', pw: 'campus123' },
      student: { email: 'alex@student.com', pw: 'campus123' },
      admin: { email: 'admin@campuscrew.com', pw: 'campus123' }
    };
    const c = creds[role] || creds.business;
    try {
      const res = await API.login(c.email, c.pw);
      this.currentUser = res.user;
      this.renderHeaderUser();
      this.showToast(`Switched to ${role.toUpperCase()} View (${res.user.full_name})`, 'success');
      
      if (navigate) {
        if (role === 'business') window.location.hash = '#analytics';
        else if (role === 'creator') window.location.hash = '#collaborations';
        else if (role === 'student') window.location.hash = '#student-hub';
        else if (role === 'admin') window.location.hash = '#admin';
        else this.handleRoute();
      }
    } catch (err) {
      this.showToast(`Failed to switch demo user: ${err.message}`, 'error');
    }
  },

  // Map Initialization
  initMap(creators) {
    const mapEl = document.getElementById('creator-map');
    if (!mapEl || typeof L === 'undefined') return;

    if (this.mapInstance) {
      this.mapInstance.remove();
    }

    // Centered on UT Austin Campus area (30.2849, -97.7341)
    const map = L.map('creator-map').setView([30.2849, -97.7341], 14);
    this.mapInstance = map;

    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; OpenStreetMap &copy; CARTO',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);

    creators.forEach(cr => {
      const lat = cr.lat || (30.28 + (Math.random() - 0.5) * 0.02);
      const lng = cr.lng || (-97.73 + (Math.random() - 0.5) * 0.02);

      const customIcon = L.divIcon({
        className: 'custom-map-marker',
        html: `<div style="background-color: #6366f1; width: 34px; height: 34px; border-radius: 50%; border: 3px solid white; box-shadow: 0 4px 12px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: bold; color: white;">
                 📸
               </div>`,
        iconSize: [34, 34],
        iconAnchor: [17, 17]
      });

      const popupHtml = `
        <div style="font-family: sans-serif; min-width: 180px; color: #111;">
          <h4 style="margin: 0; font-size: 14px; font-weight: bold;">${cr.full_name}</h4>
          <span style="font-size: 11px; color: #6366f1; font-weight: 600;">${cr.niche}</span>
          <div style="margin: 6px 0; font-size: 12px;">📍 ${cr.location}</div>
          <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 8px;">
            <span>Rate: <strong>$${cr.base_rate}</strong></span>
            <span>Eng: <strong>${cr.avg_engagement_rate}%</strong></span>
          </div>
          <button onclick="App.viewCreatorProfile(${cr.id})" style="background: #6366f1; color: white; border: none; width: 100%; padding: 6px; border-radius: 6px; font-size: 11px; font-weight: bold; cursor: pointer;">
            View Media Kit
          </button>
        </div>
      `;

      L.marker([lat, lng], { icon: customIcon }).addTo(map).bindPopup(popupHtml);
    });
  },

  // Messaging & Chat
  async loadChatMessages(collabId) {
    const container = document.getElementById('chat-messages-container');
    if (!container) return;

    try {
      const data = await API.getMessages(collabId);
      const msgs = data.messages || [];

      if (msgs.length === 0) {
        container.innerHTML = `<div class="text-center py-8 text-xs text-slate-500">No messages yet. Send a greeting to kick off!</div>`;
        return;
      }

      container.innerHTML = msgs.map(m => {
        const isMe = this.currentUser && m.sender_id === this.currentUser.id;
        return `
          <div class="flex items-start gap-2.5 ${isMe ? 'flex-row-reverse' : ''}">
            <img src="${m.sender_avatar || 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150'}" 
                 class="w-7 h-7 rounded-full object-cover border border-slate-700" />
            <div class="max-w-[75%]">
              <div class="text-[10px] text-slate-500 mb-0.5 ${isMe ? 'text-right' : ''}">${m.sender_name}</div>
              <div class="rounded-2xl px-3.5 py-2 text-xs leading-relaxed ${
                isMe ? 'bg-indigo-600 text-white rounded-tr-none' : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-tl-none'
              }">
                ${m.message_text}
              </div>
            </div>
          </div>
        `;
      }).join('');

      container.scrollTop = container.scrollHeight;
    } catch (e) {
      console.error("Error loading chat:", e);
    }
  },

  async handleSendMessage(e, collabId) {
    e.preventDefault();
    const input = document.getElementById('chat-input');
    const text = input ? input.value.trim() : '';
    if (!text) return;

    try {
      await API.sendMessage(collabId, text);
      input.value = '';
      this.loadChatMessages(collabId);
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  // Conversion Simulators (QR Scans & Coupons)
  async simulateScan(collabId) {
    try {
      await API.logTrackingEvent({
        tracking_code_id: 1,
        event_type: 'qr_scan',
        order_value: 0.0,
        customer_ref: `Student-Scan-${Math.floor(Math.random() * 900 + 100)}`
      });

      const el = document.getElementById('stat-scans');
      if (el) {
        el.innerText = parseInt(el.innerText || '0') + 1;
        el.classList.add('text-indigo-300', 'scale-110');
        setTimeout(() => el.classList.remove('scale-110'), 200);
      }
      this.showToast('⚡ In-Store Counter QR Code Scanned!', 'info');
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  async simulateRedemption(collabId) {
    try {
      const orderVal = (Math.random() * 20 + 15).toFixed(2);
      await API.logTrackingEvent({
        tracking_code_id: 1,
        event_type: 'coupon_redemption',
        order_value: parseFloat(orderVal),
        customer_ref: `POS-Order-#${Math.floor(Math.random() * 9000 + 1000)}`
      });

      const el = document.getElementById('stat-redemptions');
      if (el) {
        el.innerText = parseInt(el.innerText || '0') + 1;
        el.classList.add('text-emerald-300', 'scale-110');
        setTimeout(() => el.classList.remove('scale-110'), 200);
      }
      this.showToast(`🎉 Coupon Redeemed! Attributed $${orderVal} checkout sale!`, 'success');
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  // AI Content Brief Generator Action
  async generateCreativeBrief() {
    const cat = document.getElementById('brief-category').value;
    const obj = document.getElementById('brief-objective').value;
    const bud = document.getElementById('brief-budget').value;

    const out = document.getElementById('brief-output');
    out.classList.remove('hidden');
    out.innerHTML = `<div class="text-center py-8 text-indigo-400 text-sm">Generating optimized local content brief...</div>`;

    try {
      const res = await API.generateBrief(cat, obj, bud);
      const b = res.brief;
      out.innerHTML = `
        <div class="space-y-6 animate-fade-in">
          <div>
            <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider block mb-1">Generated Reel Hooks</span>
            <ul class="space-y-2 mt-2">
              ${b.hooks.map(h => `<li class="p-3 bg-slate-900 rounded-xl border border-slate-800 text-sm text-slate-200 font-medium">${h}</li>`).join('')}
            </ul>
          </div>

          <div>
            <span class="text-xs font-bold text-slate-400 uppercase tracking-wider block mb-1">Suggested 30-Second Storyboard</span>
            <p class="text-xs text-slate-300 bg-slate-900/90 p-4 rounded-xl border border-slate-800 leading-relaxed">${b.storyboard}</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <span class="text-xs text-slate-400 font-medium block mb-1">Call to Action (CTA)</span>
              <strong class="text-emerald-400 text-sm">${b.call_to_action}</strong>
            </div>
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <span class="text-xs text-slate-400 font-medium block mb-1">Recommended Deliverables</span>
              <strong class="text-indigo-300 text-sm">${b.recommended_package}</strong>
            </div>
          </div>
        </div>
      `;
    } catch (err) {
      out.innerHTML = `<div class="text-red-400 text-sm">Failed to generate brief: ${err.message}</div>`;
    }
  },

  // Filters & Search
  debounceFilter() {
    clearTimeout(this.debounceTimer);
    this.debounceTimer = setTimeout(() => this.applyFilters(), 250);
  },

  applyFilters() {
    this.activeFilters = {
      search: document.getElementById('filter-search')?.value || '',
      niche: document.getElementById('filter-niche')?.value || '',
      max_budget: document.getElementById('filter-rate')?.value || '99999',
      sort_by: document.getElementById('filter-sort')?.value || 'relevance'
    };
    this.handleRoute();
  },

  resetFilters() {
    this.activeFilters = {};
    this.handleRoute();
  },

  // Modals & Action Handlers
  showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  },

  showModal(contentHtml) {
    let modalRoot = document.getElementById('modal-root');
    if (!modalRoot) {
      modalRoot = document.createElement('div');
      modalRoot.id = 'modal-root';
      document.body.appendChild(modalRoot);
    }
    modalRoot.innerHTML = `
      <div class="fixed inset-0 z-50 flex items-center justify-center p-4 modal-backdrop" onclick="App.closeModal(event)">
        <div class="bg-slate-950 border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl relative animate-fade-in" onclick="event.stopPropagation()">
          <button onclick="App.closeModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white text-lg font-bold">✕</button>
          ${contentHtml}
        </div>
      </div>
    `;
  },

  closeModal() {
    const modalRoot = document.getElementById('modal-root');
    if (modalRoot) modalRoot.innerHTML = '';
  },

  // Creator Media Kit Profile Modal
  async viewCreatorProfile(creatorId) {
    try {
      const data = await API.getCreator(creatorId);
      const c = data.creator;
      const reviews = c.reviews || [];

      this.showModal(`
        <div>
          <div class="flex items-center gap-4 mb-4">
            <img src="${c.avatar_url}" class="w-16 h-16 rounded-full object-cover border-2 border-indigo-500" />
            <div>
              <h3 class="text-xl font-bold text-white">${c.full_name}</h3>
              <div class="text-xs text-indigo-400 font-mono">${c.handle}</div>
              <div class="text-xs text-slate-400 mt-1">📍 ${c.location} • Niche: ${c.niche}</div>
            </div>
          </div>

          <p class="text-xs text-slate-300 leading-relaxed mb-4">${c.bio}</p>

          <div class="grid grid-cols-3 gap-2 p-3 bg-slate-900 rounded-xl text-center mb-4">
            <div>
              <div class="text-[11px] text-slate-400">Followers</div>
              <strong class="text-sm text-white">${(c.follower_count || 0).toLocaleString()}</strong>
            </div>
            <div>
              <div class="text-[11px] text-slate-400">Engagement</div>
              <strong class="text-sm text-indigo-400">${c.avg_engagement_rate}%</strong>
            </div>
            <div>
              <div class="text-[11px] text-slate-400">Base Deliverable</div>
              <strong class="text-sm text-emerald-400">$${c.base_rate}</strong>
            </div>
          </div>

          <div class="mb-4">
            <span class="text-xs font-bold text-slate-300 block mb-2">Verified Client Reviews (${reviews.length})</span>
            <div class="max-h-36 overflow-y-auto space-y-2">
              ${reviews.length === 0 ? '<div class="text-xs text-slate-500">No reviews yet.</div>' : reviews.map(r => `
                <div class="p-2.5 bg-slate-900 rounded-lg text-xs">
                  <div class="flex items-center justify-between text-amber-400 font-bold mb-1">
                    <span>${'★'.repeat(r.rating)}</span>
                    <span class="text-slate-400 font-normal">${r.author_name}</span>
                  </div>
                  <div class="text-slate-300">"${r.review_text}"</div>
                </div>
              `).join('')}
            </div>
          </div>

          <div class="flex gap-2">
            <button onclick="App.quickInvite(${c.id})" class="flex-1 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold">
              Invite to Campaign
            </button>
          </div>
        </div>
      `);
    } catch (e) {
      this.showToast(e.message, 'error');
    }
  },

  // Apply to Campaign Modal
  showApplyModal(campId) {
    this.showModal(`
      <div>
        <h3 class="text-lg font-bold text-white mb-2">Apply & Pitch Campaign</h3>
        <p class="text-xs text-slate-400 mb-4">Submit your proposed deliverable, fee, and unique creative hook.</p>

        <form onsubmit="App.handleApplySubmit(event, ${campId})" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Proposed Fee ($)</label>
            <input type="number" id="apply-fee" value="300" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white" />
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Proposed Deliverables</label>
            <input type="text" id="apply-deliverables" value="1 Tasting Reel (30s) + 2 Stories with QR" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white" />
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Creative Angle / Pitch</label>
            <textarea id="apply-pitch" rows="3" placeholder="How will you feature this business to your audience?" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white"></textarea>
          </div>

          <button type="submit" class="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition">
            Submit Proposal & Compute Opportunity Score
          </button>
        </form>
      </div>
    `);
  },

  async handleApplySubmit(e, campId) {
    e.preventDefault();
    const fee = document.getElementById('apply-fee').value;
    const deliverables = document.getElementById('apply-deliverables').value;
    const pitch = document.getElementById('apply-pitch').value;

    try {
      const res = await API.applyToCampaign(campId, {
        proposed_fee: fee,
        proposed_deliverables: deliverables,
        creative_pitch: pitch
      });
      this.closeModal();
      this.showToast(`Proposal Submitted! Your Creator Opportunity Score: ${res.score}/100`, 'success');
      this.handleRoute();
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  // Review Inbound Applications Modal (Business Owner)
  async viewApplications(campId) {
    try {
      const res = await API.getApplications(campId);
      const apps = res.applications || [];

      this.showModal(`
        <div class="max-w-xl">
          <h3 class="text-lg font-bold text-white mb-2">Campaign Proposals Received (${apps.length})</h3>
          <p class="text-xs text-slate-400 mb-4">Ranked by Transparent Creator Opportunity Score (no follower bias).</p>

          <div class="max-h-96 overflow-y-auto space-y-4">
            ${apps.length === 0 ? '<div class="text-xs text-slate-500 py-6 text-center">No proposals received yet.</div>' : apps.map(a => `
              <div class="p-4 rounded-xl bg-slate-900 border border-slate-800">
                <div class="flex items-start justify-between gap-3 mb-2">
                  <div class="flex items-center gap-2.5">
                    <img src="${a.creator_avatar}" class="w-10 h-10 rounded-full object-cover" />
                    <div>
                      <div class="font-bold text-white text-sm">${a.creator_name}</div>
                      <div class="text-[11px] text-indigo-400 font-mono">${a.handle} • ${a.creator_location}</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <span class="px-2 py-0.5 rounded text-xs font-black bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                      Score: ${a.score}
                    </span>
                    <div class="text-emerald-400 font-bold text-xs mt-1">$${a.proposed_fee}</div>
                  </div>
                </div>

                <div class="text-xs text-slate-300 bg-slate-950 p-2.5 rounded-lg border border-slate-800/80 mb-3">
                  <strong>Pitch:</strong> "${a.creative_pitch || 'Ready to deliver high-quality authentic content.'}"
                </div>

                <div class="flex items-center justify-between pt-2 border-t border-slate-800">
                  <span class="text-[11px] text-slate-400">${a.proposed_deliverables}</span>
                  ${a.status === 'accepted' ? `
                    <span class="text-emerald-400 text-xs font-bold">✓ Accepted</span>
                  ` : `
                    <button onclick="App.acceptApplication(${a.id})" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition">
                      Accept & Issue Contract
                    </button>
                  `}
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `);
    } catch (e) {
      this.showToast(e.message, 'error');
    }
  },

  async acceptApplication(appId) {
    try {
      const res = await API.acceptApplication(appId);
      this.closeModal();
      this.showToast('Contract Accepted! Collaboration Workspace & QR Code Generated!', 'success');
      window.location.hash = `#collaborations/${res.collaboration_id}`;
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  // Submit Draft Deliverable Modal
  showSubmitDraftModal(collabId, delivId) {
    this.showModal(`
      <div>
        <h3 class="text-lg font-bold text-white mb-2">Upload Draft Content URL</h3>
        <p class="text-xs text-slate-400 mb-4">Paste your unlisted Instagram, Google Drive, or TikTok draft link for brand review.</p>

        <form onsubmit="App.handleSubmitDraft(event, ${collabId}, ${delivId})" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Draft Video / Asset URL</label>
            <input type="url" id="draft-url" placeholder="https://instagram.com/reel/... or drive link" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white" />
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Notes for Brand</label>
            <textarea id="draft-notes" rows="2" placeholder="e.g. Added audio track, featured the counter QR at 0:18" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white"></textarea>
          </div>

          <button type="submit" class="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold">
            Submit for Review
          </button>
        </form>
      </div>
    `);
  },

  async handleSubmitDraft(e, collabId, delivId) {
    e.preventDefault();
    const url = document.getElementById('draft-url').value;
    const notes = document.getElementById('draft-notes').value;

    try {
      await API.submitDeliverable(collabId, delivId, { submission_url: url, submission_notes: notes });
      this.closeModal();
      this.showToast('Draft Submitted for Brand Review!', 'success');
      this.handleRoute();
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  // Request Revision Modal
  showRequestRevisionModal(collabId, delivId) {
    this.showModal(`
      <div>
        <h3 class="text-lg font-bold text-white mb-2">Request Edits & Revisions</h3>
        <p class="text-xs text-slate-400 mb-4">Provide clear, actionable feedback within the contract's revision limit.</p>

        <form onsubmit="App.handleRequestRevision(event, ${collabId}, ${delivId})" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Actionable Edit Instructions</label>
            <textarea id="revision-notes" rows="3" placeholder="e.g. Please show the drink texture closer to the camera and mention our 15% student coupon code." required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white"></textarea>
          </div>

          <button type="submit" class="w-full py-2.5 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-xs font-semibold">
            Send Revision Request
          </button>
        </form>
      </div>
    `);
  },

  async handleRequestRevision(e, collabId, delivId) {
    e.preventDefault();
    const notes = document.getElementById('revision-notes').value;

    try {
      const res = await API.requestRevision(collabId, delivId, notes);
      this.closeModal();
      this.showToast(`Revision Request Sent (${res.revisions_used}/${res.max_revisions} used)`, 'info');
      this.handleRoute();
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  async approveDeliverable(collabId, delivId) {
    try {
      await API.approveDeliverable(collabId, delivId);
      this.showToast('Deliverable Approved!', 'success');
      this.handleRoute();
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  async markCollabCompleted(collabId) {
    if (!confirm("Confirm completion? This will sign off all deliverables and release payout to the creator.")) return;
    try {
      await API.completeCollaboration(collabId);
      this.showToast('Collaboration Completed & Funds Released!', 'success');
      this.handleRoute();
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  // Review Modal
  showReviewModal(collabId) {
    this.showModal(`
      <div>
        <h3 class="text-lg font-bold text-white mb-2">Submit Verified Review</h3>
        <p class="text-xs text-slate-400 mb-4">Leave feedback for your completed collaboration.</p>

        <form onsubmit="App.handleReviewSubmit(event, ${collabId})" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Rating</label>
            <select id="review-rating" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-white">
              <option value="5">★★★★★ (5 Stars - Outstanding)</option>
              <option value="4">★★★★☆ (4 Stars - Very Good)</option>
              <option value="3">★★★☆☆ (3 Stars - Average)</option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Review Feedback</label>
            <textarea id="review-text" rows="3" placeholder="Share your experience working together..." required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white"></textarea>
          </div>

          <button type="submit" class="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold">
            Post Verified Review
          </button>
        </form>
      </div>
    `);
  },

  async handleReviewSubmit(e, collabId) {
    e.preventDefault();
    const rating = document.getElementById('review-rating').value;
    const text = document.getElementById('review-text').value;

    try {
      await API.submitReview({ collaboration_id: collabId, rating, review_text: text });
      this.closeModal();
      this.showToast('Verified Review Posted Successfully!', 'success');
      this.handleRoute();
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  // Dispute Modal
  showDisputeModal(collabId) {
    this.showModal(`
      <div>
        <h3 class="text-lg font-bold text-red-400 mb-2">Escalate to Admin Mediation</h3>
        <p class="text-xs text-slate-400 mb-4">Submit a ticket to Super Admin if there is an unresolved breach of contract.</p>

        <textarea id="dispute-reason" rows="3" placeholder="Describe the issue in detail..." class="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white mb-4"></textarea>

        <button onclick="App.showToast('Dispute ticket submitted to Admin Governance team.', 'info'); App.closeModal();" class="w-full py-2.5 rounded-xl bg-red-600 hover:bg-red-500 text-white text-xs font-semibold">
          Submit Dispute Ticket
        </button>
      </div>
    `);
  },

  // Toggle Feature Flag (Admin)
  async toggleStudentHubSetting(newVal) {
    try {
      await API.updateAdminSetting('student_hub_enabled', newVal ? 'true' : 'false');
      this.showToast(`Student Talent Hub ${newVal ? 'ENABLED' : 'DISABLED'}`, 'info');
      this.handleRoute();
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  // Creator Comparison
  toggleCompare(creatorId) {
    const idx = this.compareList.findIndex(c => c.id === creatorId);
    if (idx >= 0) {
      this.compareList.splice(idx, 1);
    } else {
      if (this.compareList.length >= 3) {
        this.showToast('You can compare up to 3 creators at once.', 'info');
        return;
      }
      const cr = this.creators.find(c => c.id === creatorId);
      if (cr) this.compareList.push(cr);
    }
    this.renderCompareTray();
    this.handleRoute();
  },

  renderCompareTray() {
    let tray = document.getElementById('compare-tray');
    if (!tray) {
      tray = document.createElement('div');
      tray.id = 'compare-tray';
      document.body.appendChild(tray);
    }

    if (this.compareList.length === 0) {
      tray.classList.remove('open');
      return;
    }

    tray.classList.add('open');
    tray.innerHTML = `
      <div class="max-w-6xl mx-auto flex items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <span class="text-xs font-bold text-indigo-400 uppercase tracking-wider">Comparing (${this.compareList.length}/3):</span>
          <div class="flex items-center gap-2">
            ${this.compareList.map(c => `
              <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs text-white">
                <span>${c.full_name}</span>
                <button onclick="App.toggleCompare(${c.id})" class="text-slate-400 hover:text-white">✕</button>
              </span>
            `).join('')}
          </div>
        </div>

        <div class="flex items-center gap-2">
          <button onclick="App.showCompareModal()" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold">
            View Comparison
          </button>
          <button onclick="App.compareList = []; App.renderCompareTray(); App.handleRoute();" class="text-xs text-slate-400 hover:text-white px-2">
            Clear
          </button>
        </div>
      </div>
    `;
  },

  showCompareModal() {
    this.showModal(`
      <div class="max-w-3xl">
        <h3 class="text-lg font-bold text-white mb-4">Side-by-Side Creator Comparison</h3>
        <div class="grid grid-cols-${this.compareList.length} gap-4">
          ${this.compareList.map(c => `
            <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 text-center">
              <img src="${c.avatar_url}" class="w-14 h-14 rounded-full mx-auto mb-2 object-cover border border-indigo-400" />
              <h4 class="font-bold text-white text-sm">${c.full_name}</h4>
              <div class="text-[11px] text-indigo-400 font-mono mb-3">${c.handle}</div>
              
              <div class="space-y-2 text-xs text-left pt-3 border-t border-slate-800">
                <div class="flex justify-between"><span class="text-slate-400">Niche:</span><strong class="text-white">${c.niche}</strong></div>
                <div class="flex justify-between"><span class="text-slate-400">Followers:</span><strong class="text-white">${c.follower_count.toLocaleString()}</strong></div>
                <div class="flex justify-between"><span class="text-slate-400">Engagement:</span><strong class="text-indigo-400">${c.avg_engagement_rate}%</strong></div>
                <div class="flex justify-between"><span class="text-slate-400">Reliability:</span><strong class="text-emerald-400">${c.reliability_score}%</strong></div>
                <div class="flex justify-between"><span class="text-slate-400">Base Rate:</span><strong class="text-emerald-400">$${c.base_rate}</strong></div>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `);
  },

  // Post Campaign Modal
  showCreateCampaignModal() {
    this.showModal(`
      <div>
        <h3 class="text-lg font-bold text-white mb-2">Create New Campaign</h3>
        <p class="text-xs text-slate-400 mb-4">Set clear deliverables, budget pool, and verification requirements.</p>

        <form onsubmit="App.handleCreateCampaignSubmit(event)" class="space-y-3.5">
          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Campaign Title</label>
            <input type="text" id="new-camp-title" placeholder="e.g. Spring Study Drinks Launch" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-medium text-slate-300 mb-1">Category</label>
              <select id="new-camp-category" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-2.5 py-2 text-xs text-white">
                <option value="Food & Beverage">Food & Beverage</option>
                <option value="Fitness & Health">Fitness & Health</option>
                <option value="Beauty & Wellness">Beauty & Wellness</option>
                <option value="Fashion & Retail">Fashion & Retail</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-300 mb-1">Budget ($)</label>
              <input type="number" id="new-camp-budget" value="600" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white" />
            </div>
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Target Deliverables</label>
            <input type="text" id="new-camp-deliverables" value="1 Reel + 2 Stories with QR Check-In" required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white" />
          </div>

          <div>
            <label class="block text-xs font-medium text-slate-300 mb-1">Description & Creative Goal</label>
            <textarea id="new-camp-desc" rows="3" placeholder="Explain what creators need to feature..." required class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white"></textarea>
          </div>

          <button type="submit" class="w-full py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold">
            Publish Campaign to Marketplace
          </button>
        </form>
      </div>
    `);
  },

  async handleCreateCampaignSubmit(e) {
    e.preventDefault();
    const title = document.getElementById('new-camp-title').value;
    const category = document.getElementById('new-camp-category').value;
    const budget = document.getElementById('new-camp-budget').value;
    const deliverables = document.getElementById('new-camp-deliverables').value;
    const desc = document.getElementById('new-camp-desc').value;

    try {
      await API.createCampaign({
        title,
        category,
        budget,
        deliverables,
        description: desc,
        objective: 'Footfall & QR Scans',
        collaboration_type: 'paid',
        target_location: 'Austin, TX'
      });
      this.closeModal();
      this.showToast('Campaign Published Successfully!', 'success');
      this.handleRoute();
    } catch (err) {
      this.showToast(err.message, 'error');
    }
  },

  // Student Certificate Modal
  async showVerifyCertificateModal() {
    this.showModal(`
      <div>
        <h3 class="text-lg font-bold text-white mb-2">Verify Student Experience Certificate</h3>
        <p class="text-xs text-slate-400 mb-4">Enter certificate UUID or scan QR to check tamper-proof registry.</p>

        <div class="flex gap-2 mb-4">
          <input type="text" id="cert-uuid-input" placeholder="e.g. UUID..." class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white" />
          <button onclick="App.verifyCert()" class="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold">
            Verify
          </button>
        </div>
        <div id="cert-result"></div>
      </div>
    `);
  },

  async verifyCert() {
    const input = document.getElementById('cert-uuid-input').value.trim();
    const resEl = document.getElementById('cert-result');
    if (!input) return;

    try {
      const data = await API.getStudentCertificate(input);
      const c = data.certificate;
      resEl.innerHTML = `
        <div class="p-4 rounded-xl bg-emerald-950/40 border border-emerald-600/50 text-xs text-emerald-200">
          <div class="font-bold text-sm text-emerald-300 mb-1">✓ VERIFIED AUTHENTIC CERTIFICATE</div>
          <div>Recipient: <strong>${c.student_name}</strong> (${c.university})</div>
          <div>Issued by: <strong>${c.client_name}</strong></div>
          <div>Project: <strong>${c.project_title}</strong></div>
          <div>Skills: ${c.skills_demonstrated}</div>
          <div class="mt-2 text-[10px] text-emerald-400/80 font-mono">Hash: ${c.verification_hash}</div>
        </div>
      `;
    } catch (e) {
      resEl.innerHTML = `<div class="p-3 bg-red-950/40 border border-red-800 text-xs text-red-300">Invalid or unverified certificate ID.</div>`;
    }
  }
};

window.App = App;
document.addEventListener('DOMContentLoaded', () => App.init());

// =========================================================
// Real Photo Carousel & Testimonial Engine
// =========================================================

App.carouselInterval = null;
App.carouselCurrentIndex = 0;
App.carouselTotalSlides = 4;
App.touchStartX = 0;
App.touchEndX = 0;

App.initHeroCarousel = function() {
  const container = document.getElementById('hero-carousel-container');
  if (!container) return;

  // Clear existing interval
  if (App.carouselInterval) {
    clearInterval(App.carouselInterval);
  }

  App.carouselCurrentIndex = 0;

  // Auto transition every 4.5 seconds
  App.carouselInterval = setInterval(() => {
    App.carouselNext();
  }, 4500);

  // Pause on hover
  container.addEventListener('mouseenter', () => {
    clearInterval(App.carouselInterval);
    App.carouselInterval = null;
  });

  container.addEventListener('mouseleave', () => {
    if (!App.carouselInterval) {
      App.carouselInterval = setInterval(() => {
        App.carouselNext();
      }, 4500);
    }
  });

  // Mobile Touch Swipe Handlers
  container.addEventListener('touchstart', (e) => {
    App.touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  container.addEventListener('touchend', (e) => {
    App.touchEndX = e.changedTouches[0].screenX;
    App.handleCarouselSwipe();
  }, { passive: true });
};

App.handleCarouselSwipe = function() {
  const threshold = 40;
  if (App.touchEndX < App.touchStartX - threshold) {
    App.carouselNext();
  } else if (App.touchEndX > App.touchStartX + threshold) {
    App.carouselPrev();
  }
};

App.carouselGoTo = function(index) {
  const slides = document.querySelectorAll('.carousel-slide');
  const dots = document.querySelectorAll('.carousel-dot');
  if (!slides.length) return;

  App.carouselCurrentIndex = (index + slides.length) % slides.length;

  slides.forEach((s, idx) => {
    if (idx === App.carouselCurrentIndex) {
      s.classList.add('active');
    } else {
      s.classList.remove('active');
    }
  });

  dots.forEach((d, idx) => {
    if (idx === App.carouselCurrentIndex) {
      d.classList.add('active');
    } else {
      d.classList.remove('active');
    }
  });
};

App.carouselNext = function() {
  App.carouselGoTo(App.carouselCurrentIndex + 1);
};

App.carouselPrev = function() {
  App.carouselGoTo(App.carouselCurrentIndex - 1);
};

// Testimonial Rotator
App.testimonialIndex = 0;
App.testimonialInterval = null;

App.initTestimonials = function() {
  if (App.testimonialInterval) clearInterval(App.testimonialInterval);
  App.testimonialInterval = setInterval(() => {
    App.testimonialIndex = (App.testimonialIndex + 1) % 3;
    App.setTestimonial(App.testimonialIndex);
  }, 6000);
};

App.setTestimonial = function(idx) {
  App.testimonialIndex = idx;
  for (let i = 0; i < 3; i++) {
    const el = document.getElementById(`testimonial-${i}`);
    if (el) {
      if (i === idx) el.classList.add('active');
      else el.classList.remove('active');
    }
  }
};

// Hook into handleRoute to initialize carousel on landing
const originalHandleRoute = App.handleRoute;
App.handleRoute = async function() {
  await originalHandleRoute.apply(this, arguments);
  if (this.currentView === 'landing') {
    setTimeout(() => {
      this.initHeroCarousel();
      this.initTestimonials();
    }, 50);
  } else {
    if (this.carouselInterval) {
      clearInterval(this.carouselInterval);
      this.carouselInterval = null;
    }
    if (this.testimonialInterval) {
      clearInterval(this.testimonialInterval);
      this.testimonialInterval = null;
    }
  }
};
