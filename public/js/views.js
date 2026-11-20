// CampusCrew Views & UI Components (Upgraded with Real Photographic Assets)
const Views = {
  // 1. Landing View with Real Photo Carousel, Business Trust Spotlight, & Photographic Workflow
  renderLanding(user) {
    return `
      <div class="relative overflow-hidden pt-6 pb-20">
        <!-- Background Gradient Glows -->
        <div class="absolute -top-24 left-1/2 -translate-x-1/2 w-[700px] h-[350px] bg-indigo-600/15 blur-[120px] rounded-full pointer-events-none"></div>
        <div class="absolute top-1/2 -left-20 w-[400px] h-[400px] bg-purple-600/10 blur-[100px] rounded-full pointer-events-none"></div>

        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10 mb-10">
          <!-- Tagline Pill -->
          <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs sm:text-sm font-semibold mb-6 animate-fade-in">
            <span class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
            Where Local Businesses Meet Creators, and Talent Turns Into Opportunity
          </div>

          <h1 class="text-3xl sm:text-5xl lg:text-6xl font-extrabold text-white tracking-tight leading-tight sm:leading-none max-w-4xl mx-auto mb-6">
            Real Local Creators. <br class="hidden sm:inline" />
            <span class="bg-gradient-to-r from-indigo-400 via-purple-300 to-pink-400 bg-clip-text text-transparent">
              Measurable In-Store Dining & Retail Sales
            </span>
          </h1>

          <p class="text-slate-400 text-sm sm:text-lg max-w-2xl mx-auto mb-8 leading-relaxed">
            CampusCrew connects authentic neighborhood businesses with vetted campus micro-influencers. Track direct footfall through in-store counter QR code standees and exclusive creator student discounts.
          </p>

          <div class="flex flex-wrap items-center justify-center gap-3.5 mb-10">
            <a href="#explore" class="px-6 py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm shadow-lg shadow-indigo-600/30 transition transform hover:-translate-y-0.5 flex items-center gap-2">
              <span>Explore Verified Creators</span>
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/></svg>
            </a>
            <a href="#campaigns" class="px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-sm border border-slate-700 transition flex items-center gap-2">
              <span>View Active Campaigns</span>
            </a>
            <a href="#briefs" class="px-5 py-3 rounded-xl bg-slate-900/80 hover:bg-slate-800 text-indigo-300 font-medium text-sm border border-indigo-900/60 transition flex items-center gap-2">
              <svg class="w-4 h-4 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
              <span>AI Reel Briefs</span>
            </a>
          </div>
        </div>

        <!-- =========================================================
             SECTION 1: AUTOMATIC 3D HERO IMAGE CAROUSEL
             ========================================================= -->
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 mb-20">
          <div class="carousel-viewport" id="hero-carousel-container">
            <span class="carousel-paused-badge">⏸ Paused on hover</span>

            <!-- Slide 1: In-Store Counter QR Code Review (Photo 7) -->
            <div class="carousel-slide active" data-index="0">
              <img src="images/real/counter_qr_campaign_review.jpg" alt="Creator reviewing counter QR standee with business owner" class="carousel-img" loading="eager" />
              <div class="carousel-overlay">
                <div class="max-w-2xl text-left">
                  <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 mb-2 inline-block">
                    ✓ Real Campaign Execution
                  </span>
                  <h3 class="text-xl sm:text-2xl font-extrabold text-white mb-1">Direct In-Store Footfall & Counter QR Attribution</h3>
                  <p class="text-xs sm:text-sm text-slate-200 line-clamp-2">
                    Campus ambassador reviewing campaign progress with the proprietor of SNR Nati Ruchi Family Restaurant, featuring the live student discount counter QR standee.
                  </p>
                </div>
              </div>
            </div>

            <!-- Slide 2: Real Business Partnership Handshake (Photo 6) -->
            <div class="carousel-slide" data-index="1">
              <img src="images/real/business_creator_handshake.jpg" alt="Business owner and creator shaking hands" class="carousel-img" loading="lazy" />
              <div class="carousel-overlay">
                <div class="max-w-2xl text-left">
                  <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 mb-2 inline-block">
                    🤝 Verified Partnership Handshake
                  </span>
                  <h3 class="text-xl sm:text-2xl font-extrabold text-white mb-1">Local Business Meets Verified Campus Creator</h3>
                  <p class="text-xs sm:text-sm text-slate-200 line-clamp-2">
                    Official partnership agreement sealed outside SNR Nati Ruchi under the restaurant sign. Milestone terms, delivery dates, and payouts fully protected.
                  </p>
                </div>
              </div>
            </div>

            <!-- Slide 3: Hyperlocal Campus Engagement (Photo 3) -->
            <div class="carousel-slide" data-index="2">
              <img src="images/real/campus_creator_interview.jpg" alt="Campus creator interviewing student on scooter" class="carousel-img" loading="lazy" />
              <div class="carousel-overlay">
                <div class="max-w-2xl text-left">
                  <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-purple-500/20 text-purple-300 border border-purple-500/30 mb-2 inline-block">
                    📍 Hyperlocal Campus Reach
                  </span>
                  <h3 class="text-xl sm:text-2xl font-extrabold text-white mb-1">Connecting Student Communities Directly with Local Spots</h3>
                  <p class="text-xs sm:text-sm text-slate-200 line-clamp-2">
                    Creators conducting real interviews and capturing campus dining recommendations right outside college lecture halls and hostels.
                  </p>
                </div>
              </div>
            </div>

            <!-- Slide 4: Campus Lecture Hall Strategy Pitch (Photo 1) -->
            <div class="carousel-slide" data-index="3">
              <img src="images/real/campus_pitch_session.jpg" alt="Student creator presenting campaign strategy in lecture hall" class="carousel-img" loading="lazy" />
              <div class="carousel-overlay">
                <div class="max-w-2xl text-left">
                  <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-pink-500/20 text-pink-300 border border-pink-500/30 mb-2 inline-block">
                    🎓 Student Talent Hub
                  </span>
                  <h3 class="text-xl sm:text-2xl font-extrabold text-white mb-1">Data-Driven Campaign Planning by Campus Creators</h3>
                  <p class="text-xs sm:text-sm text-slate-200 line-clamp-2">
                    Student creator team pitching reel concepts, timing schedules, and deliverable targets in a campus auditorium before brand launch.
                  </p>
                </div>
              </div>
            </div>

            <!-- Manual Controls: Left / Right Arrows -->
            <button onclick="App.carouselPrev()" class="absolute left-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-slate-950/70 hover:bg-slate-900 text-white flex items-center justify-center border border-white/20 transition backdrop-blur z-20" aria-label="Previous Slide">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
            </button>
            <button onclick="App.carouselNext()" class="absolute right-3 top-1/2 -translate-y-1/2 w-10 h-10 rounded-full bg-slate-950/70 hover:bg-slate-900 text-white flex items-center justify-center border border-white/20 transition backdrop-blur z-20" aria-label="Next Slide">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
            </button>

            <!-- Slide Indicator Dots -->
            <div class="absolute bottom-4 left-1/2 -translate-x-1/2 flex items-center gap-2 z-20" id="carousel-dots-container">
              <span class="carousel-dot active" onclick="App.carouselGoTo(0)"></span>
              <span class="carousel-dot" onclick="App.carouselGoTo(1)"></span>
              <span class="carousel-dot" onclick="App.carouselGoTo(2)"></span>
              <span class="carousel-dot" onclick="App.carouselGoTo(3)"></span>
            </div>
          </div>
        </div>

        <!-- =========================================================
             SECTION 2: REAL BUSINESS TRUST & CASE STUDY SPOTLIGHT
             ========================================================= -->
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 mb-24">
          <div class="text-center max-w-3xl mx-auto mb-12">
            <span class="px-3.5 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 mb-3 inline-block">
              Real Partner Trust & Customer Story
            </span>
            <h2 class="text-2xl sm:text-4xl font-extrabold text-white">Genuine Local Business In Action</h2>
            <p class="text-slate-400 text-sm mt-2">
              See how authentic local businesses collaborate with CampusCrew creators to drive measurable dining footfall through counter QR code tracking.
            </p>
          </div>

          <!-- Featured Partner Card: SNR Nati Ruchi Family Restaurant -->
          <div class="trust-spotlight-card rounded-2xl p-6 sm:p-8 relative overflow-hidden">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
              
              <!-- Left: Storefront & Handshake Image Grid (5 Cols) -->
              <div class="lg:col-span-5 space-y-4">
                <!-- Storefront Banner (Photo 5) -->
                <div class="rounded-xl overflow-hidden border border-slate-700/80 shadow-lg relative group">
                  <img src="images/real/nati_ruchi_storefront.jpg" alt="SNR Nati Ruchi Family Restaurant Storefront" class="w-full h-44 object-cover group-hover:scale-105 transition duration-500" />
                  <div class="absolute inset-0 bg-gradient-to-t from-slate-950/80 via-transparent to-transparent flex items-end p-3">
                    <span class="text-xs font-bold text-white flex items-center gap-1.5">
                      <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                      Verified Dining Partner Storefront
                    </span>
                  </div>
                </div>

                <!-- Deal Handshake Photo (Photo 6) -->
                <div class="grid grid-cols-2 gap-3">
                  <div class="rounded-xl overflow-hidden border border-slate-700/80 h-36 relative">
                    <img src="images/real/business_creator_handshake.jpg" alt="Partnership Handshake" class="w-full h-full object-cover" />
                    <span class="absolute bottom-1.5 left-2 text-[10px] bg-slate-950/80 px-2 py-0.5 rounded text-slate-200">
                      Deal Handshake
                    </span>
                  </div>
                  <div class="rounded-xl overflow-hidden border border-slate-700/80 h-36 relative">
                    <img src="images/real/counter_qr_campaign_review.jpg" alt="Billing Counter QR Standee" class="w-full h-full object-cover" />
                    <span class="absolute bottom-1.5 left-2 text-[10px] bg-slate-950/80 px-2 py-0.5 rounded text-emerald-300 font-semibold">
                      Counter QR Standee
                    </span>
                  </div>
                </div>
              </div>

              <!-- Right: Business Details & Measurable Attribution (7 Cols) -->
              <div class="lg:col-span-7 space-y-5 text-left">
                <div class="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-slate-800">
                  <div>
                    <div class="flex items-center gap-2">
                      <h3 class="text-xl sm:text-2xl font-bold text-white">SNR Nati Ruchi Family Restaurant</h3>
                      <span class="text-emerald-400 text-sm" title="Verified Business">✓</span>
                    </div>
                    <span class="text-xs text-indigo-400 font-medium">Authentic Nati Cuisine & Biryani Hub • Bangalore Campus District</span>
                  </div>
                  <span class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    Live Partner Case
                  </span>
                </div>

                <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
                  "CampusCrew and Aditya brought real students right to our dining tables. The orange counter QR standee placed at our reception desk made it effortless to verify student orders and track the exact footfall. Highly recommended for local dining establishments!"
                </p>

                <!-- 3 Proven Result Metrics -->
                <div class="grid grid-cols-3 gap-3 py-3 px-4 bg-slate-900/90 rounded-xl border border-slate-800">
                  <div>
                    <span class="text-[11px] text-slate-400 block">Counter Scans</span>
                    <strong class="text-lg font-black text-indigo-400">142+ Scans</strong>
                  </div>
                  <div>
                    <span class="text-[11px] text-slate-400 block">Orders Verified</span>
                    <strong class="text-lg font-black text-emerald-400">38 Redemptions</strong>
                  </div>
                  <div>
                    <span class="text-[11px] text-slate-400 block">Attributed Sales</span>
                    <strong class="text-lg font-black text-white">₹14,250+</strong>
                  </div>
                </div>

                <div class="pt-2 flex flex-wrap items-center gap-3">
                  <a href="#campaigns" class="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs transition">
                    View Nati Ruchi Campaign
                  </a>
                  <button onclick="App.showRoleDemo('business')" class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold text-xs border border-slate-700 transition">
                    Try Business Dashboard
                  </button>
                </div>
              </div>

            </div>
          </div>
        </div>

        <!-- =========================================================
             SECTION 3: HOW CAMPUSCREW WORKS (REAL PHOTO WORKFLOW)
             ========================================================= -->
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 mb-24">
          <div class="text-center max-w-2xl mx-auto mb-12">
            <span class="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-2 inline-block">
              4-Step Real Collaboration Journey
            </span>
            <h2 class="text-2xl sm:text-3xl font-extrabold text-white">How CampusCrew Works In Reality</h2>
            <p class="text-slate-400 text-sm mt-1">From on-campus strategy pitches to physical in-store counter QR attribution.</p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 text-left">
            
            <!-- Step 1 (Photo 1) -->
            <div class="glass-card rounded-2xl overflow-hidden border border-slate-800 flex flex-col justify-between group hover:border-indigo-500/50 transition">
              <div>
                <div class="h-44 overflow-hidden relative">
                  <img src="images/real/campus_pitch_session.jpg" alt="Step 1: On-Campus Pitch" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
                  <span class="absolute top-2.5 left-2.5 w-7 h-7 rounded-lg bg-indigo-600 text-white font-bold text-xs flex items-center justify-center shadow">1</span>
                </div>
                <div class="p-5">
                  <h4 class="font-bold text-white text-base mb-1.5">Campus Creator Pitch</h4>
                  <p class="text-xs text-slate-400 leading-relaxed">
                    Student creators pitch campaign angles and review business requirements directly on campus grounds.
                  </p>
                </div>
              </div>
            </div>

            <!-- Step 2 (Photo 2) -->
            <div class="glass-card rounded-2xl overflow-hidden border border-slate-800 flex flex-col justify-between group hover:border-indigo-500/50 transition">
              <div>
                <div class="h-44 overflow-hidden relative">
                  <img src="images/real/creator_duo_discussion.jpg" alt="Step 2: Content Angle Planning" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
                  <span class="absolute top-2.5 left-2.5 w-7 h-7 rounded-lg bg-purple-600 text-white font-bold text-xs flex items-center justify-center shadow">2</span>
                </div>
                <div class="p-5">
                  <h4 class="font-bold text-white text-base mb-1.5">Content Angle Planning</h4>
                  <p class="text-xs text-slate-400 leading-relaxed">
                    Creators brainstorm authentic hooks and plan short-form video reels that resonate with local students.
                  </p>
                </div>
              </div>
            </div>

            <!-- Step 3 (Photo 6) -->
            <div class="glass-card rounded-2xl overflow-hidden border border-slate-800 flex flex-col justify-between group hover:border-indigo-500/50 transition">
              <div>
                <div class="h-44 overflow-hidden relative">
                  <img src="images/real/business_creator_handshake.jpg" alt="Step 3: Agreement Handshake" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
                  <span class="absolute top-2.5 left-2.5 w-7 h-7 rounded-lg bg-emerald-600 text-white font-bold text-xs flex items-center justify-center shadow">3</span>
                </div>
                <div class="p-5">
                  <h4 class="font-bold text-white text-base mb-1.5">Agreement & Handshake</h4>
                  <p class="text-xs text-slate-400 leading-relaxed">
                    Business owner and creator meet at the storefront, agreeing on deliverable dates and fair milestone compensation.
                  </p>
                </div>
              </div>
            </div>

            <!-- Step 4 (Photo 7) -->
            <div class="glass-card rounded-2xl overflow-hidden border border-slate-800 flex flex-col justify-between group hover:border-indigo-500/50 transition">
              <div>
                <div class="h-44 overflow-hidden relative">
                  <img src="images/real/counter_qr_campaign_review.jpg" alt="Step 4: Counter QR Attribution" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
                  <span class="absolute top-2.5 left-2.5 w-7 h-7 rounded-lg bg-pink-600 text-white font-bold text-xs flex items-center justify-center shadow">4</span>
                </div>
                <div class="p-5">
                  <h4 class="font-bold text-white text-base mb-1.5">Counter QR Attribution</h4>
                  <p class="text-xs text-slate-400 leading-relaxed">
                    Placing the dedicated counter QR standee at the billing desk to track confirmed in-store student visits and sales.
                  </p>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- =========================================================
             SECTION 4: REAL TESTIMONIAL CAROUSEL
             ========================================================= -->
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mb-24 text-center">
          <div class="glass-card rounded-2xl p-8 border border-slate-800 relative">
            <span class="text-3xl block mb-3">💬</span>
            <div class="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-2">Verified Collaboration Reviews</div>

            <!-- Testimonial 1 -->
            <div class="testimonial-card active" id="testimonial-0">
              <p class="text-base sm:text-lg text-slate-200 font-medium italic mb-6 leading-relaxed">
                "The orange counter QR standee at our reception counter made it effortless to verify student orders and track the exact footfall. Highly recommended for local dining establishments!"
              </p>
              <div class="flex items-center justify-center gap-3">
                <img src="images/real/nati_ruchi_storefront.jpg" alt="Nati Ruchi" class="w-11 h-11 rounded-full object-cover border-2 border-emerald-500/50" />
                <div class="text-left">
                  <div class="font-bold text-white text-sm">Proprietor & Management</div>
                  <div class="text-xs text-slate-400">SNR Nati Ruchi Family Restaurant</div>
                </div>
              </div>
            </div>

            <!-- Testimonial 2 -->
            <div class="testimonial-card" id="testimonial-1">
              <p class="text-base sm:text-lg text-slate-200 font-medium italic mb-6 leading-relaxed">
                "Instead of vanity follower counts, CampusCrew lets me show local business owners the exact sales and scans generated through our in-store reviews. The contract protection is top notch."
              </p>
              <div class="flex items-center justify-center gap-3">
                <img src="images/real/counter_qr_campaign_review.jpg" alt="Aditya" class="w-11 h-11 rounded-full object-cover border-2 border-indigo-500/50" />
                <div class="text-left">
                  <div class="font-bold text-white text-sm">Aditya Kumar</div>
                  <div class="text-xs text-slate-400">Campus Ambassador & Food Creator (@aditya_campus_bites)</div>
                </div>
              </div>
            </div>

            <!-- Testimonial 3 -->
            <div class="testimonial-card" id="testimonial-2">
              <p class="text-base sm:text-lg text-slate-200 font-medium italic mb-6 leading-relaxed">
                "Pitching campaign concepts directly on campus and turning them into working client projects gave our student creative team genuine commercial experience and verified certificates."
              </p>
              <div class="flex items-center justify-center gap-3">
                <img src="images/real/campus_pitch_session.jpg" alt="Strategy Team" class="w-11 h-11 rounded-full object-cover border-2 border-purple-500/50" />
                <div class="text-left">
                  <div class="font-bold text-white text-sm">Campus Creative Team</div>
                  <div class="text-xs text-slate-400">Student Talent Hub Lead</div>
                </div>
              </div>
            </div>

            <!-- Testimonial Dots Navigation -->
            <div class="flex items-center justify-center gap-2 mt-6">
              <button onclick="App.setTestimonial(0)" class="w-2.5 h-2.5 rounded-full bg-indigo-500"></button>
              <button onclick="App.setTestimonial(1)" class="w-2.5 h-2.5 rounded-full bg-slate-700"></button>
              <button onclick="App.setTestimonial(2)" class="w-2.5 h-2.5 rounded-full bg-slate-700"></button>
            </div>
          </div>
        </div>

        <!-- =========================================================
             SECTION 5: ROLE PATHS SELECTION
             ========================================================= -->
        <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          <div class="grid md:grid-cols-2 gap-8 text-left">
            <!-- Business Card -->
            <div class="glass-card rounded-2xl p-8 border border-slate-800 relative overflow-hidden group hover:border-indigo-500/40 transition">
              <div class="w-12 h-12 rounded-xl bg-indigo-500/10 text-indigo-400 flex items-center justify-center font-bold text-xl mb-5">
                🏢
              </div>
              <h3 class="text-xl font-bold text-white mb-2">For Local Businesses & Restaurants</h3>
              <p class="text-slate-400 text-sm mb-6 leading-relaxed">
                Connect directly with genuine campus creators. Receive verifiable footfall through counter QR stands and creator coupon codes.
              </p>
              <ul class="space-y-3 mb-8 text-sm text-slate-300">
                <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Post custom campaigns with target deliverables</li>
                <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Enforced 2-revision limit & fair milestone releases</li>
                <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Real-time ROI analytics with Cost Per Acquisition (CPA)</li>
              </ul>
              <button onclick="App.showRoleDemo('business')" class="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition">
                Explore as Business (Nati Ruchi Demo)
              </button>
            </div>

            <!-- Creator Card -->
            <div class="glass-card rounded-2xl p-8 border border-slate-800 relative overflow-hidden group hover:border-purple-500/40 transition">
              <div class="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center font-bold text-xl mb-5">
                📸
              </div>
              <h3 class="text-xl font-bold text-white mb-2">For Campus Creators & Ambassadors</h3>
              <p class="text-slate-400 text-sm mb-6 leading-relaxed">
                Monetize your voice with genuine local restaurant and retail deals. Protected contracts, agreed deliverables, and on-time payouts.
              </p>
              <ul class="space-y-3 mb-8 text-sm text-slate-300">
                <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Transparent Creator Opportunity Score (no follower bias)</li>
                <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Unified Collaboration Hub to submit drafts and receive feedback</li>
                <li class="flex items-center gap-2"><span class="text-emerald-400">✓</span> Verified client reviews and milestone deal ledger</li>
              </ul>
              <button onclick="App.showRoleDemo('creator')" class="w-full py-3 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-sm transition">
                Explore as Creator (Aditya Demo)
              </button>
            </div>
          </div>
        </div>

      </div>
    `;
  },

  // 2. Creator Discovery View
  renderDiscovery(creators, activeFilters = {}) {
    return `
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in text-left">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8">
          <div>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Smart Creator Discovery</h1>
            <p class="text-slate-400 text-sm mt-1">Discover verified local campus and neighborhood creators. Filter by engagement, location, and rates.</p>
          </div>
          <div class="flex items-center gap-3">
            <a href="#map" class="px-4 py-2 rounded-xl bg-slate-900 border border-slate-700 hover:border-indigo-500 text-slate-200 text-xs font-semibold flex items-center gap-2 transition">
              <span>🗺️ Discovery Map</span>
            </a>
            <a href="#briefs" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-2 transition">
              <span>✨ AI Brief Planner</span>
            </a>
          </div>
        </div>

        <!-- Filter Controls Bar -->
        <div class="glass-card rounded-2xl p-5 mb-8 border border-slate-800">
          <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3.5">
            <div class="md:col-span-2 relative">
              <input type="text" id="filter-search" value="${activeFilters.search || ''}" placeholder="Search name, handle, or bio..." 
                     oninput="App.debounceFilter()" 
                     class="w-full bg-slate-900 border border-slate-700 rounded-xl pl-4 pr-4 py-2 text-sm text-white focus:outline-none focus:border-indigo-500" />
            </div>

            <div>
              <select id="filter-niche" onchange="App.applyFilters()" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500">
                <option value="">All Categories</option>
                <option value="Food & Beverage" ${activeFilters.niche === 'Food & Beverage' ? 'selected' : ''}>Food & Beverage</option>
                <option value="Fitness & Health" ${activeFilters.niche === 'Fitness & Health' ? 'selected' : ''}>Fitness & Health</option>
                <option value="Beauty & Wellness" ${activeFilters.niche === 'Beauty & Wellness' ? 'selected' : ''}>Beauty & Wellness</option>
                <option value="Fashion & Retail" ${activeFilters.niche === 'Fashion & Retail' ? 'selected' : ''}>Fashion & Retail</option>
              </select>
            </div>

            <div>
              <select id="filter-rate" onchange="App.applyFilters()" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500">
                <option value="99999">Any Budget</option>
                <option value="200" ${activeFilters.max_budget === '200' ? 'selected' : ''}>Under $200</option>
                <option value="300" ${activeFilters.max_budget === '300' ? 'selected' : ''}>Under $300</option>
                <option value="500" ${activeFilters.max_budget === '500' ? 'selected' : ''}>Under $500</option>
              </select>
            </div>

            <div>
              <select id="filter-sort" onchange="App.applyFilters()" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500">
                <option value="relevance">Top Match & Reliability</option>
                <option value="engagement" ${activeFilters.sort_by === 'engagement' ? 'selected' : ''}>Highest Engagement %</option>
                <option value="followers" ${activeFilters.sort_by === 'followers' ? 'selected' : ''}>Most Followers</option>
                <option value="rate_low" ${activeFilters.sort_by === 'rate_low' ? 'selected' : ''}>Budget (Lowest First)</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Creator Cards Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          ${creators.map(c => Views.renderCreatorCard(c)).join('')}
        </div>
      </div>
    `;
  },

  renderCreatorCard(c) {
    const isCompared = App.compareList.some(item => item.id === c.id);
    return `
      <div class="glass-card rounded-2xl p-6 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between group relative text-left">
        <div>
          <div class="flex items-start justify-between gap-3 mb-4">
            <div class="flex items-center gap-3">
              <img src="${c.avatar_url || 'images/real/counter_qr_campaign_review.jpg'}" 
                   alt="${c.full_name}" 
                   class="w-14 h-14 rounded-full object-cover border-2 border-indigo-500/40" />
              <div>
                <div class="flex items-center gap-1.5">
                  <h3 class="font-bold text-white text-base">${c.full_name}</h3>
                  <span class="text-indigo-400 text-xs font-bold" title="Verified Creator">★</span>
                </div>
                <div class="text-xs text-indigo-400 font-mono">${c.handle}</div>
                <div class="text-xs text-slate-400 mt-0.5">📍 ${c.location}</div>
              </div>
            </div>

            <span class="px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              ${c.reliability_score || 98}% Rel.
            </span>
          </div>

          <div class="flex flex-wrap items-center gap-1.5 mb-3">
            <span class="px-2.5 py-0.5 rounded-md text-[11px] font-medium bg-slate-800 text-slate-300 border border-slate-700">
              ${c.niche}
            </span>
            <span class="px-2.5 py-0.5 rounded-md text-[11px] font-medium bg-indigo-950 text-indigo-300 border border-indigo-800">
              ✓ Verified Audience: ${c.audience_age_group || '18-24 (80%)'}
            </span>
          </div>

          <p class="text-slate-300 text-xs line-clamp-2 mb-4 leading-relaxed">${c.bio || 'Local campus creator.'}</p>

          <div class="grid grid-cols-3 gap-2 py-3 px-3.5 bg-slate-900/90 rounded-xl border border-slate-800 mb-4 text-center">
            <div>
              <div class="text-xs text-slate-400">Followers</div>
              <div class="text-sm font-bold text-white">${(c.follower_count || 0).toLocaleString()}</div>
            </div>
            <div>
              <div class="text-xs text-slate-400">Engagement</div>
              <div class="text-sm font-bold text-indigo-400">${c.avg_engagement_rate}%</div>
            </div>
            <div>
              <div class="text-xs text-slate-400">Base Rate</div>
              <div class="text-sm font-bold text-emerald-400">$${c.base_rate}</div>
            </div>
          </div>
        </div>

        <div class="pt-3 border-t border-slate-800/80 flex items-center gap-2">
          <button onclick="App.viewCreatorProfile(${c.id})" class="flex-1 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition">
            View Media Kit
          </button>
          <button onclick="App.toggleCompare(${c.id})" class="px-3 py-2 rounded-xl border ${isCompared ? 'bg-indigo-600 border-indigo-500 text-white' : 'border-slate-700 bg-slate-900 text-slate-300 hover:text-white'} text-xs font-semibold transition">
            ${isCompared ? 'Added' : 'Compare'}
          </button>
          <button onclick="App.quickInvite(${c.id})" class="px-3 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition">
            Invite
          </button>
        </div>
      </div>
    `;
  },

  // 3. Campaign Marketplace View
  renderCampaigns(campaigns, user) {
    const isBusiness = user && user.role === 'business';
    return `
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in text-left">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Campaign Marketplace</h1>
            <p class="text-slate-400 text-sm mt-1">Browse active campaigns from local businesses featuring counter QR codes and milestone deliverables.</p>
          </div>
          <div>
            ${isBusiness ? `
              <button onclick="App.showCreateCampaignModal()" class="px-5 py-2.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold shadow-lg transition">
                + Post New Campaign
              </button>
            ` : `
              <button onclick="App.showRoleDemo('business')" class="px-4 py-2 rounded-xl bg-slate-800 border border-slate-700 text-slate-300 text-xs font-semibold">
                Switch to Business to Post
              </button>
            `}
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          ${campaigns.map(camp => Views.renderCampaignCard(camp, user)).join('')}
        </div>
      </div>
    `;
  },

  renderCampaignCard(camp, user) {
    const isOwner = user && user.id === camp.business_id;
    return `
      <div class="glass-card rounded-2xl p-6 border border-slate-800 hover:border-slate-700 transition flex flex-col justify-between text-left">
        <div>
          <div class="flex items-start justify-between gap-3 mb-3">
            <div class="flex items-center gap-3">
              <img src="${camp.business_logo || 'images/real/nati_ruchi_storefront.jpg'}" 
                   alt="${camp.business_name}" 
                   class="w-12 h-12 rounded-xl object-cover border border-slate-700" />
              <div>
                <h3 class="font-bold text-white text-base">${camp.title}</h3>
                <div class="text-xs text-indigo-400 font-medium">${camp.business_name} • ${camp.business_category}</div>
              </div>
            </div>
            <span class="px-3 py-1 rounded-full text-xs font-bold uppercase ${
              camp.collaboration_type === 'paid' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
            }">
              ${camp.collaboration_type}
            </span>
          </div>

          <p class="text-slate-300 text-sm mb-4 leading-relaxed">${camp.description}</p>

          <div class="bg-slate-900/90 rounded-xl p-3 border border-slate-800 mb-4">
            <div class="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1">Target Deliverables</div>
            <div class="text-xs font-medium text-slate-200">${camp.deliverables}</div>
          </div>

          <div class="flex flex-wrap items-center gap-2 mb-4 text-xs text-slate-400">
            <span class="bg-slate-800 px-2.5 py-1 rounded-md border border-slate-700">📍 ${camp.target_location}</span>
            <span class="bg-slate-800 px-2.5 py-1 rounded-md border border-slate-700">🎯 ${camp.objective}</span>
          </div>
        </div>

        <div class="pt-4 border-t border-slate-800 flex items-center justify-between">
          <div>
            <div class="text-[11px] text-slate-400">Budget Pool</div>
            <div class="text-lg font-extrabold text-emerald-400">$${camp.budget}</div>
          </div>

          <div class="flex items-center gap-2">
            ${isOwner ? `
              <button onclick="App.viewApplications(${camp.id})" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition">
                Review Bids (${camp.application_count || 0})
              </button>
            ` : `
              <button onclick="App.showApplyModal(${camp.id})" class="px-5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition">
                Apply & Pitch
              </button>
            `}
          </div>
        </div>
      </div>
    `;
  },

  // 4. Collaboration Workspace Hub View
  renderCollaborationHub(collab, user) {
    const isBusiness = user && user.id === collab.business_id;
    const deliverables = collab.deliverables || [];
    const stats = collab.tracking_stats || { scans: 0, redemptions: 0, confirmed_sales: 0, revenue_generated: 0 };

    return `
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in text-left">
        <!-- Back Navigation & Title -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div class="flex items-center gap-3">
            <a href="#collaborations" class="p-2 rounded-xl bg-slate-900 border border-slate-700 text-slate-300 hover:text-white transition">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
            </a>
            <div>
              <div class="flex items-center gap-2">
                <h1 class="text-2xl font-extrabold text-white">${collab.campaign_title}</h1>
                <span class="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase ${
                  collab.status === 'completed' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30'
                }">
                  ${collab.status.replace('_', ' ')}
                </span>
              </div>
              <p class="text-xs text-slate-400 mt-0.5">Agreement between <strong>${collab.business_name}</strong> and <strong>${collab.creator_name}</strong></p>
            </div>
          </div>

          <div class="flex items-center gap-2">
            ${isBusiness && collab.status !== 'completed' ? `
              <button onclick="App.markCollabCompleted(${collab.id})" class="px-4 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow transition">
                ✓ Sign-off & Release Payment ($${collab.agreed_fee})
              </button>
            ` : ''}
            <button onclick="App.showDisputeModal(${collab.id})" class="px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 hover:border-red-500/50 text-slate-400 hover:text-red-400 text-xs font-medium transition">
              Dispute
            </button>
          </div>
        </div>

        <!-- 3-Column Workspace Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div class="lg:col-span-2 space-y-6">
            
            <!-- Standard Agreement Terms Card -->
            <div class="glass-card rounded-2xl p-5 border border-slate-800">
              <div class="flex items-center justify-between mb-3">
                <h3 class="font-bold text-white text-sm flex items-center gap-2">
                  <span>📜 Milestone Contract & Creator Protection</span>
                </h3>
                <span class="text-xs font-semibold text-slate-400">
                  Revisions: <strong class="text-indigo-400">${collab.used_revisions}</strong> of ${collab.max_revisions} Used
                </span>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed bg-slate-900/70 p-3 rounded-xl border border-slate-800">${collab.terms_agreement}</p>
              
              <div class="grid grid-cols-3 gap-3 mt-4 text-center text-xs">
                <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                  <span class="text-slate-400 block">Agreed Fee</span>
                  <strong class="text-emerald-400 text-sm">$${collab.agreed_fee}</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                  <span class="text-slate-400 block">Payment State</span>
                  <strong class="text-indigo-400 text-sm capitalize">${collab.payment_status || 'In Escrow'}</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                  <span class="text-slate-400 block">Deadline</span>
                  <strong class="text-slate-200 text-sm">${collab.deadline}</strong>
                </div>
              </div>
            </div>

            <!-- Deliverables Execution Checklist -->
            <div class="glass-card rounded-2xl p-5 border border-slate-800">
              <div class="flex items-center justify-between mb-4">
                <h3 class="font-bold text-white text-base">Content Deliverables</h3>
                <span class="text-xs text-slate-400">Verified milestone flow</span>
              </div>

              <div class="space-y-4">
                ${deliverables.map(deliv => `
                  <div class="bg-slate-900/90 rounded-xl p-4 border border-slate-800">
                    <div class="flex items-start justify-between gap-3 mb-2">
                      <div>
                        <h4 class="font-semibold text-white text-sm">${deliv.title}</h4>
                        <span class="text-xs text-slate-400">${deliv.deliverable_type}</span>
                      </div>
                      <span class="px-2.5 py-0.5 rounded-full text-[11px] font-bold uppercase ${
                        deliv.status === 'approved' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
                        deliv.status === 'submitted' ? 'bg-indigo-500/20 text-indigo-400 border border-indigo-500/30' :
                        deliv.status === 'revision_needed' ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' :
                        'bg-slate-800 text-slate-400'
                      }">
                        ${deliv.status.replace('_', ' ')}
                      </span>
                    </div>

                    ${deliv.submission_url ? `
                      <div class="mt-3 p-2.5 bg-slate-950 rounded-lg border border-slate-800 text-xs">
                        <div class="text-slate-400 mb-1">Attached Verification / Draft Asset:</div>
                        ${deliv.submission_url.startsWith('/images/real') ? `
                          <div class="flex items-center gap-3">
                            <img src="${deliv.submission_url}" class="w-16 h-16 rounded-lg object-cover border border-slate-700" />
                            <div>
                              <span class="font-semibold text-slate-200 block">In-Store Photographic Proof</span>
                              <span class="text-[11px] text-slate-400">${deliv.submission_notes || 'Verified on location with business partner.'}</span>
                            </div>
                          </div>
                        ` : `
                          <a href="${deliv.submission_url}" target="_blank" class="text-indigo-400 hover:underline break-all font-mono">
                            ${deliv.submission_url}
                          </a>
                        `}
                      </div>
                    ` : ''}

                    <!-- Actions Bar for this Deliverable -->
                    <div class="mt-3 pt-3 border-t border-slate-800 flex items-center justify-end gap-2">
                      ${!isBusiness && deliv.status !== 'approved' ? `
                        <button onclick="App.showSubmitDraftModal(${collab.id}, ${deliv.id})" class="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition">
                          ${deliv.status === 'revision_needed' ? 'Submit Revised Draft' : 'Upload Draft URL'}
                        </button>
                      ` : ''}

                      ${isBusiness && deliv.status === 'submitted' ? `
                        <button onclick="App.showRequestRevisionModal(${collab.id}, ${deliv.id})" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-300 text-xs font-semibold border border-amber-900/40 transition">
                          Request Edits
                        </button>
                        <button onclick="App.approveDeliverable(${collab.id}, ${deliv.id})" class="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold transition">
                          Approve Content
                        </button>
                      ` : ''}
                    </div>
                  </div>
                `).join('')}
              </div>
            </div>

            <!-- In-Store Counter QR Code Attribution Card -->
            <div class="glass-card rounded-2xl p-5 border border-slate-800">
              <div class="flex items-center justify-between mb-4">
                <div>
                  <h3 class="font-bold text-white text-base">In-Store Counter QR Attribution</h3>
                  <p class="text-xs text-slate-400">Separates physical counter scans from confirmed checkout sales.</p>
                </div>
                <span class="px-2.5 py-1 rounded-md text-xs font-mono font-bold bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">
                  Promo: ${collab.coupon_code || 'NATIRUCHI15'}
                </span>
              </div>

              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 flex flex-col items-center text-center">
                  <div class="w-36 h-36 bg-white p-2 rounded-xl mb-3 shadow-md flex items-center justify-center">
                    <img src="/api/qrcode/${collab.qr_code_id || 'sample'}.svg" alt="Campaign QR Code" class="w-full h-full" />
                  </div>
                  <div class="text-xs font-mono text-slate-400 mb-2">QR Standee ID: ${collab.qr_code_id}</div>
                  <button onclick="App.simulateScan(${collab.id})" class="w-full py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 text-xs font-semibold border border-indigo-500/30 transition">
                    ⚡ Simulate Customer QR Scan
                  </button>
                </div>

                <div class="p-4 rounded-xl bg-slate-900 border border-slate-800 flex flex-col justify-between">
                  <div>
                    <div class="text-xs text-slate-400 font-medium mb-1">In-Store Counter Discount Code:</div>
                    <div class="text-2xl font-black text-indigo-400 font-mono tracking-wider mb-2">${collab.coupon_code || 'NATIRUCHI15'}</div>
                    <p class="text-xs text-slate-400 mb-4">Students receive 15% discount at checkout upon scan verification.</p>

                    <div class="grid grid-cols-2 gap-2 text-center">
                      <div class="p-2 bg-slate-950 rounded-lg">
                        <span class="text-[10px] text-slate-500 block">QR Scans</span>
                        <strong class="text-lg text-white" id="stat-scans">${stats.scans}</strong>
                      </div>
                      <div class="p-2 bg-slate-950 rounded-lg">
                        <span class="text-[10px] text-slate-500 block">Redemptions</span>
                        <strong class="text-lg text-emerald-400" id="stat-redemptions">${stats.redemptions}</strong>
                      </div>
                    </div>
                  </div>

                  <button onclick="App.simulateRedemption(${collab.id})" class="mt-4 w-full py-1.5 rounded-lg bg-emerald-600/20 hover:bg-emerald-600/40 text-emerald-300 text-xs font-semibold border border-emerald-500/30 transition">
                    ⚡ Simulate Coupon Checkout ($25 order)
                  </button>
                </div>
              </div>
            </div>

          </div>

          <!-- Direct Messaging Thread -->
          <div class="glass-card rounded-2xl p-5 border border-slate-800 flex flex-col h-[650px]">
            <div class="pb-3 border-b border-slate-800 flex items-center justify-between">
              <div>
                <h3 class="font-bold text-white text-sm">Direct Collaboration Chat</h3>
                <span class="text-[11px] text-slate-400">Contextual & secure communication</span>
              </div>
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
            </div>

            <div id="chat-messages-container" class="flex-1 overflow-y-auto py-4 space-y-3">
              <div class="text-center text-xs text-slate-500">Loading conversation...</div>
            </div>

            <form onsubmit="App.handleSendMessage(event, ${collab.id})" class="pt-3 border-t border-slate-800 flex items-center gap-2">
              <input type="text" id="chat-input" placeholder="Type a message or paste a link..." 
                     class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2 text-xs text-white focus:outline-none focus:border-indigo-500" />
              <button type="submit" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold transition">
                Send
              </button>
            </form>
          </div>

        </div>
      </div>
    `;
  },

  // 5. Campaign ROI Dashboard View
  renderROI(analytics, user) {
    return `
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in text-left">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Campaign ROI & Attribution</h1>
            <p class="text-slate-400 text-sm mt-1">Measurable return on investment based on real in-store scans & coupon redemptions.</p>
          </div>
          <button onclick="window.print()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 flex items-center gap-2">
            <span>Export Report (PDF)</span>
          </button>
        </div>

        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          <div class="glass-card rounded-2xl p-5 border border-slate-800">
            <span class="text-xs text-slate-400 font-medium">Total Campaign Spend</span>
            <div class="text-2xl sm:text-3xl font-black text-white mt-1">$${(analytics.total_spend || 0).toLocaleString()}</div>
            <span class="text-[11px] text-slate-500 mt-1 block">${analytics.total_collaborations || 0} collaborations</span>
          </div>

          <div class="glass-card rounded-2xl p-5 border border-slate-800">
            <span class="text-xs text-slate-400 font-medium">Verified Footfall Scans</span>
            <div class="text-2xl sm:text-3xl font-black text-indigo-400 mt-1">${(analytics.total_scans || 0).toLocaleString()}</div>
            <span class="text-[11px] text-indigo-400/80 mt-1 block">In-store QR interactions</span>
          </div>

          <div class="glass-card rounded-2xl p-5 border border-slate-800">
            <span class="text-xs text-slate-400 font-medium">Coupon Redemptions</span>
            <div class="text-2xl sm:text-3xl font-black text-emerald-400 mt-1">${(analytics.total_redemptions || 0).toLocaleString()}</div>
            <span class="text-[11px] text-emerald-400/80 mt-1 block">Attributed checkout sales</span>
          </div>

          <div class="glass-card rounded-2xl p-5 border border-slate-800">
            <span class="text-xs text-slate-400 font-medium">Attributed Sales Revenue</span>
            <div class="text-2xl sm:text-3xl font-black text-purple-400 mt-1">$${(analytics.attributed_revenue || 0).toLocaleString()}</div>
            <span class="text-[11px] text-purple-400/80 mt-1 block">ROI: ${(analytics.roi_percent || 0)}%</span>
          </div>
        </div>

        <div class="glass-card rounded-2xl p-6 border border-slate-800 mb-8">
          <h3 class="text-lg font-bold text-white mb-4">Creator Attribution Breakdown</h3>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs">
              <thead class="text-slate-400 uppercase tracking-wider border-b border-slate-800 bg-slate-900/50">
                <tr>
                  <th class="py-3 px-4">Creator</th>
                  <th class="py-3 px-4">Promo Code</th>
                  <th class="py-3 px-4">QR Scans</th>
                  <th class="py-3 px-4">Redemptions</th>
                  <th class="py-3 px-4">Attributed Revenue</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-800">
                ${(analytics.creator_performance || []).map(cp => `
                  <tr class="hover:bg-slate-900/40">
                    <td class="py-3.5 px-4 font-semibold text-white">${cp.creator_name} <span class="text-slate-500 font-mono text-[11px]">${cp.handle}</span></td>
                    <td class="py-3.5 px-4 font-mono font-bold text-indigo-400">${cp.coupon_code}</td>
                    <td class="py-3.5 px-4">${cp.scans}</td>
                    <td class="py-3.5 px-4 text-emerald-400 font-bold">${cp.redemptions}</td>
                    <td class="py-3.5 px-4 font-bold text-white">$${cp.revenue.toFixed(2)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;
  },

  // 6. Interactive Local Creator Discovery Map View
  renderMap(creators) {
    return `
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in text-left">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Local Creator Discovery Map</h1>
            <p class="text-slate-400 text-sm mt-1">Explore creators stationed in your neighborhood or campus district. Privacy-first location consent.</p>
          </div>
        </div>

        <div class="glass-card rounded-2xl p-4 border border-slate-800 mb-6 relative">
          <div id="creator-map"></div>
        </div>

        <div class="text-xs text-slate-500 flex items-center justify-between">
          <span>* Privacy Notice: Creator location pins represent neighborhood centroids, never personal residential addresses.</span>
          <span>Click any marker to view media kit & starting rates.</span>
        </div>
      </div>
    `;
  },

  // 7. AI Campaign Brief Generator View
  renderBriefGenerator() {
    return `
      <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in text-left">
        <div class="text-center max-w-2xl mx-auto mb-10">
          <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-semibold mb-3">
            <span>✨ Creative Planning Assistant</span>
          </div>
          <h1 class="text-3xl font-extrabold text-white">Campaign Idea & Content Brief Generator</h1>
          <p class="text-slate-400 text-sm mt-2">Generate high-converting Reel hooks, storyboards, and call-to-actions tailored to your local business category.</p>
        </div>

        <div class="glass-card rounded-2xl p-6 sm:p-8 border border-slate-800 mb-8">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div>
              <label class="block text-xs font-medium text-slate-300 mb-1.5">Business Category</label>
              <select id="brief-category" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500">
                <option value="Food & Beverage">Food & Beverage (Cafes, Restaurants)</option>
                <option value="Fitness & Health">Fitness & Health (Gyms, Studios)</option>
                <option value="Beauty & Wellness">Beauty & Wellness (Skincare, Salons)</option>
                <option value="Fashion & Retail">Fashion & Retail (Boutiques, Vintage)</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-medium text-slate-300 mb-1.5">Primary Objective</label>
              <select id="brief-objective" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500">
                <option value="Footfall & QR Scans">In-Store Footfall & QR Scans</option>
                <option value="Coupon Redemptions">Coupon Sales & Checkout Redemptions</option>
                <option value="Event Attendance">Local Event / Drop Attendance</option>
              </select>
            </div>

            <div>
              <label class="block text-xs font-medium text-slate-300 mb-1.5">Campaign Budget ($)</label>
              <input type="number" id="brief-budget" value="500" class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-indigo-500" />
            </div>
          </div>

          <button onclick="App.generateCreativeBrief()" class="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-sm transition shadow-lg flex items-center justify-center gap-2">
            <span>✨ Generate Creative Concepts</span>
          </button>
        </div>

        <div id="brief-output" class="hidden glass-card rounded-2xl p-6 sm:p-8 border border-indigo-500/30 animate-fade-in"></div>
      </div>
    `;
  },

  // 8. Modular Student Talent Hub View
  renderStudentHub(students, isEnabled) {
    if (!isEnabled) {
      return `
        <div class="max-w-4xl mx-auto px-4 py-16 text-center animate-fade-in">
          <div class="glass-card rounded-2xl p-12 border border-slate-800">
            <span class="text-4xl block mb-4">🎓</span>
            <h2 class="text-2xl font-bold text-white mb-2">Student Talent Hub (Modular Expansion)</h2>
            <p class="text-slate-400 text-sm max-w-md mx-auto mb-6">
              This module is currently toggled OFF via the Admin Feature Flags to keep Phase 1 lean and clean.
            </p>
            <button onclick="App.switchView('admin')" class="px-5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700">
              Open Admin Settings to Toggle On
            </button>
          </div>
        </div>
      `;
    }

    return `
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in text-left">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-400 text-xs font-semibold mb-2">
              <span>Phase 2 Modular Expansion</span>
            </div>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Student Talent Hub & Experience Certificates</h1>
            <p class="text-slate-400 text-sm mt-1">Hire student talent for video editing, thumbnail design & reels. Issue verified digital experience certificates.</p>
          </div>
          <div>
            <button onclick="App.showVerifyCertificateModal()" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 flex items-center gap-2">
              <span>Verify a Student Certificate</span>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          ${students.map(s => `
            <div class="glass-card rounded-2xl p-6 border border-slate-800 flex flex-col justify-between">
              <div>
                <div class="flex items-center gap-3 mb-4">
                  <img src="${s.avatar_url || 'images/real/campus_pitch_session.jpg'}" class="w-14 h-14 rounded-full object-cover border border-purple-500/40" />
                  <div>
                    <h3 class="font-bold text-white text-base">${s.full_name}</h3>
                    <div class="text-xs text-purple-400 font-medium">${s.university}</div>
                    <div class="text-[11px] text-slate-400">${s.major} (Class of ${s.graduation_year || 2026})</div>
                  </div>
                </div>

                <div class="flex flex-wrap gap-1.5 mb-4">
                  ${(s.skills || '').split(',').map(skill => `
                    <span class="px-2 py-0.5 rounded text-[11px] bg-slate-900 border border-slate-800 text-slate-300">${skill.trim()}</span>
                  `).join('')}
                </div>

                <p class="text-xs text-slate-300 leading-relaxed mb-4">${s.bio}</p>
              </div>

              <div class="pt-4 border-t border-slate-800 flex items-center justify-between">
                <span class="text-emerald-400 font-bold text-sm">$${s.hourly_rate || 25}/hr</span>
                <button onclick="App.showToast('Student talent contacted for gig assignment.', 'success')" class="px-4 py-1.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-semibold transition">
                  Hire for Gigs
                </button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  },

  // 9. Super Admin Governance View
  renderAdmin(overview, disputes) {
    return `
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in text-left">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
          <div>
            <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Super Admin Governance & Audit</h1>
            <p class="text-slate-400 text-sm mt-1">Platform-wide health, dispute mediation, feature flags & data integrity audit.</p>
          </div>
          <span class="px-3 py-1 rounded-full text-xs font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
            System Status: Healthy
          </span>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div class="glass-card rounded-2xl p-5 border border-slate-800">
            <span class="text-xs text-slate-400">Total Users Registered</span>
            <div class="text-2xl font-black text-white mt-1">${overview.total_users || 0}</div>
          </div>
          <div class="glass-card rounded-2xl p-5 border border-slate-800">
            <span class="text-xs text-slate-400">Active Campaigns</span>
            <div class="text-2xl font-black text-indigo-400 mt-1">${overview.total_campaigns || 0}</div>
          </div>
          <div class="glass-card rounded-2xl p-5 border border-slate-800">
            <span class="text-xs text-slate-400">Executed Collaborations</span>
            <div class="text-2xl font-black text-emerald-400 mt-1">${overview.total_collaborations || 0}</div>
          </div>
          <div class="glass-card rounded-2xl p-5 border border-slate-800">
            <span class="text-xs text-slate-400">Total Deal Flow (GMV)</span>
            <div class="text-2xl font-black text-purple-400 mt-1">$${(overview.total_gmv || 0).toLocaleString()}</div>
          </div>
        </div>

        <div class="glass-card rounded-2xl p-6 border border-slate-800 mb-8">
          <h3 class="text-base font-bold text-white mb-2">Modular Feature Flags</h3>
          <p class="text-xs text-slate-400 mb-4">Toggle platform expansions without altering core Phase 1 codebase.</p>
          
          <div class="flex items-center justify-between p-4 bg-slate-900 rounded-xl border border-slate-800">
            <div>
              <div class="font-semibold text-white text-sm">Student Talent Hub (Modules 21 - 26)</div>
              <div class="text-xs text-slate-400">Enables student freelance gig marketplace & certificate generator.</div>
            </div>
            <button onclick="App.toggleStudentHubSetting(${!overview.student_hub_enabled})" 
                    class="px-4 py-2 rounded-xl text-xs font-semibold transition ${
                      overview.student_hub_enabled ? 'bg-emerald-600 text-white' : 'bg-slate-800 text-slate-400'
                    }">
              ${overview.student_hub_enabled ? 'Enabled' : 'Disabled'}
            </button>
          </div>
        </div>
      </div>
    `;
  }
};
