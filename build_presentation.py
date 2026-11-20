import os
import sys

# Define 20 Slides for CampusCrew Master Proposal
slides_data = [
    {
        "slide_num": 1,
        "category": "PROJECT LAUNCH & MASTER ARCHITECTURE",
        "title": "CampusCrew - Platform Master Specification",
        "subtitle": "Where Local Businesses Meet Creators, and Talent Turns Into Opportunity",
        "type": "title",
        "cards": [
            {
                "title": "Platform Core Mission",
                "items": [
                    "Bridge local businesses & brands with hyperlocal micro-influencers.",
                    "Provide verified conversion tracking (QR & Coupon redemptions).",
                    "Protect creators with transparent agreements, milestones & payouts.",
                    "Engineered as a high-performance, real-world full-stack web application."
                ],
                "badge": "Core Identity"
            },
            {
                "title": "Dual Phasing Strategy",
                "items": [
                    "Phase 1: Dual Creator & Business Marketplace (20 Modules).",
                    "Phase 2: Modular Student Talent Hub & Certificate Engine (6 Modules).",
                    "Admin Governance & Audit Center for platform-wide dispute handling.",
                    "Production-ready data integrity with zero fake analytics or fake escrow."
                ],
                "badge": "Phased Delivery"
            }
        ]
    },
    {
        "slide_num": 2,
        "category": "SYSTEM ARCHITECTURE & TECH STACK",
        "title": "Modern Full-Stack Technical Stack",
        "subtitle": "Modular, Scalable, Secure & Reactive Architecture",
        "type": "grid",
        "cards": [
            {
                "title": "Frontend & UI Layer",
                "items": [
                    "Next.js 14 / React 18 with TypeScript for type-safe components.",
                    "Tailwind CSS with custom design tokens (Clean startup aesthetic).",
                    "Lucide React Icons + Framer Motion for subtle, purposeful micro-animations.",
                    "Fully responsive viewport system: Desktop, Laptop, Tablet & Mobile."
                ],
                "badge": "Frontend"
            },
            {
                "title": "Backend, DB & Real-Time",
                "items": [
                    "Node.js API Routes / Express REST endpoints with server-side validation.",
                    "PostgreSQL / SQLite with Prisma ORM (18 relational models).",
                    "WebSockets / Polling fallback for real-time messaging & alerts.",
                    "Zod schema validation on every single API route and mutation."
                ],
                "badge": "Backend & DB"
            },
            {
                "title": "Auth, Security & Storage",
                "items": [
                    "Bcrypt password hashing & JWT / HTTP-only secure session cookies.",
                    "Strict Role-Based Access Control (RBAC) guards on all protected routes.",
                    "Safe media/portfolio upload validation with strict MIME & size limits.",
                    "No API keys, credentials, or private addresses exposed to frontend."
                ],
                "badge": "Security"
            }
        ]
    },
    {
        "slide_num": 3,
        "category": "AUTHENTICATION & ROLES",
        "title": "User Roles & Access Control Matrix",
        "subtitle": "Role-Based Permissions & Strict Multi-Tenant Data Isolation",
        "type": "grid",
        "cards": [
            {
                "title": "Role A: Business / Brand",
                "items": [
                    "Create business entity, location, category & budget profile.",
                    "Post campaigns, browse/shortlist creators, review inbound bids.",
                    "Generate unique tracking QR/Coupons & view verifiable ROI dashboards.",
                    "Sign collaboration contracts & submit post-completion ratings."
                ],
                "badge": "Business"
            },
            {
                "title": "Role B: Content Creator",
                "items": [
                    "Build verified media kit: niche, location, verified handles & portfolio.",
                    "Browse campaigns, submit tailored proposals with deliverables & fees.",
                    "Access Collaboration Hub to submit drafts, log revisions & track pay.",
                    "Build transparent reputation score based on reliable deliveries."
                ],
                "badge": "Creator"
            },
            {
                "title": "Role C: Super Administrator",
                "items": [
                    "Full system oversight: dispute mediation & verification reviews.",
                    "Audit log of all sensitive admin mutations & fraud flags.",
                    "Content moderation (reports, reviews, campaigns, portfolios).",
                    "Feature-flag toggle for Student Talent Hub modular activation."
                ],
                "badge": "Super Admin"
            }
        ]
    },
    {
        "slide_num": 4,
        "category": "PHASE 1 - MODULES 1 & 2",
        "title": "Profiles & Smart Creator Discovery",
        "subtitle": "Rich Digital Media Kits & Granular Marketplace Filtering",
        "type": "grid",
        "cards": [
            {
                "title": "Module 1: User Profile Ecosystem",
                "items": [
                    "Business Profile: Category, bio, logo, past campaigns, reviews received.",
                    "Creator Media Kit: Niche, primary platforms, audience demographic tags.",
                    "Portfolio showcase: Verified video/reel embeds, previous campaign stats.",
                    "Privacy Guarantee: Residential addresses never exposed publicly."
                ],
                "badge": "Module 1"
            },
            {
                "title": "Module 2: Smart Discovery Engine",
                "items": [
                    "Granular Multi-Filter: Location, category, budget bracket, platform.",
                    "Engagement rate & audience relevance weighting.",
                    "Side-by-side Creator Comparison tray (rates, deliverables, past ratings).",
                    "One-click 'Send Direct Collaboration' or 'Add to Saved Shortlist'."
                ],
                "badge": "Module 2"
            }
        ]
    },
    {
        "slide_num": 5,
        "category": "PHASE 1 - MODULES 3 & 4",
        "title": "Hyperlocal Matching & Budget Intelligence",
        "subtitle": "Geographic Proximity Engine & Algorithmic Campaign Planning",
        "type": "grid",
        "cards": [
            {
                "title": "Module 3: Hyperlocal Matching Engine",
                "items": [
                    "Proximity calculation between business location & creator radius.",
                    "Audience verification transparency: Self-reported vs Verified flags.",
                    "Cross-matching of campaign target neighborhood with creator reach.",
                    "High relevance weighting for local community impact."
                ],
                "badge": "Module 3"
            },
            {
                "title": "Module 4: Budget-to-Campaign Intelligence",
                "items": [
                    "Input budget, objective (Footfall, Brand Awareness, Sales), and niche.",
                    "Dynamic creator bundle recommendations fitting the exact budget.",
                    "Clear disclaimer: Outcome estimates are models, never guarantees.",
                    "Pre-configured deliverable packages (e.g., 2 Reels + 3 Stories + 1 Event Visit)."
                ],
                "badge": "Module 4"
            }
        ]
    },
    {
        "slide_num": 6,
        "category": "PHASE 1 - MODULES 5 & 6",
        "title": "Campaign Marketplace & Opportunity Score",
        "subtitle": "End-to-End Campaign Lifecycle & Multi-Factor Compatibility Scoring",
        "type": "grid",
        "cards": [
            {
                "title": "Module 5: Campaign Marketplace",
                "items": [
                    "Campaign creation: Title, objective, budget, niche, deliverables, deadline.",
                    "Supports both Paid & Barter collaboration models.",
                    "Strict 9-State Lifecycle: Draft -> Published -> Applications Open -> Under Review -> Accepted -> In Progress -> Submitted -> Completed -> Cancelled.",
                    "Creators apply with proposed deliverables, timeline & pricing."
                ],
                "badge": "Module 5"
            },
            {
                "title": "Module 6: Creator Opportunity Score",
                "items": [
                    "Transparent 0-100 score shown to businesses on every applicant.",
                    "Scoring Factors: Location match (25%), Niche (25%), Budget (20%), Reliability & On-Time delivery (20%), Engagement Quality (10%).",
                    "Zero follower-bias: Micro-creators with high engagement rank top.",
                    "Clear 'Why this Creator Matches' bulleted justification breakdown."
                ],
                "badge": "Module 6"
            }
        ]
    },
    {
        "slide_num": 7,
        "category": "PHASE 1 - MODULES 7 & 8",
        "title": "Collaboration Hub & Secure Messaging",
        "subtitle": "Central Workspace for Execution, Deliverable Approval & Communication",
        "type": "grid",
        "cards": [
            {
                "title": "Module 7: Collaboration Management Hub",
                "items": [
                    "Dedicated shared workspace for every accepted campaign contract.",
                    "Scope agreement: Deliverable checklist, deadline countdown, revision tracker.",
                    "Content Submission Portal: Creator uploads draft reel/post links.",
                    "Two-stage Approval Flow: Business approves or requests revision with notes."
                ],
                "badge": "Module 7"
            },
            {
                "title": "Module 8: Messaging & Notification Center",
                "items": [
                    "Contextual Direct Messaging attached to specific collaborations.",
                    "Read receipts, message timestamps & file attachment support.",
                    "Automated alerts: Proposal received, draft submitted, revision requested.",
                    "Deadline countdown warnings (48h, 24h before submission cutoff)."
                ],
                "badge": "Module 8"
            }
        ]
    },
    {
        "slide_num": 8,
        "category": "PHASE 1 - MODULES 9 & 10",
        "title": "Conversion Tracking & ROI Dashboard",
        "subtitle": "Real-World Attribution: QR Codes, Creator Coupons & Clear Analytics",
        "type": "grid",
        "cards": [
            {
                "title": "Module 9: Campaign Conversion Tracking",
                "items": [
                    "Unique SVG/PNG QR Code generator for in-store footfall tracking.",
                    "Creator-specific promo codes (e.g., CREW-SARAH-15) for checkout attribution.",
                    "Strict funnel distinction: Scan != Lead != Redeemed Sale.",
                    "Prevents false attribution: Scans logged separately from transactions."
                ],
                "badge": "Module 9"
            },
            {
                "title": "Module 10: Campaign ROI Dashboard",
                "items": [
                    "Visual charts: Spend vs Verified Conversions over campaign lifetime.",
                    "Cost Per Acquisition (CPA) & Cost Per Verified Lead calculations.",
                    "Creator performance breakdown: Compare which creator drove top results.",
                    "Exportable PDF/CSV summary reports for business accounting."
                ],
                "badge": "Module 10"
            }
        ]
    },
    {
        "slide_num": 9,
        "category": "PHASE 1 - MODULES 11 & 12",
        "title": "Trust System & Mutual Reviews",
        "subtitle": "Two-Way Accountability, Verified Badges & Anti-Abuse Safeguards",
        "type": "grid",
        "cards": [
            {
                "title": "Module 11: Verification & Trust System",
                "items": [
                    "Social profile verification with connected profile URL checks.",
                    "Visual badge distinctions: 'Verified Business' & 'Verified Creator'.",
                    "Portfolio proof check: Admin-approved past collaboration links.",
                    "Flagging mechanism for suspect engagement or fake follower spikes."
                ],
                "badge": "Module 11"
            },
            {
                "title": "Module 12: Mutual Ratings & Reviews",
                "items": [
                    "Two-way reviews: Business rates creator, creator rates business.",
                    "Gated to Completed Collaborations only: Zero fake reviews possible.",
                    "One review per collaboration to prevent rating manipulation.",
                    "Rating metrics: Communication, Timeliness, Content Quality, Payment."
                ],
                "badge": "Module 12"
            }
        ]
    },
    {
        "slide_num": 10,
        "category": "PHASE 1 - MODULES 13 & 14",
        "title": "Creator Protection & Deal Management",
        "subtitle": "Transparent Collaboration Agreements & Transparent Payment Records",
        "type": "grid",
        "cards": [
            {
                "title": "Module 13: Creator Protection System",
                "items": [
                    "Standardized Collaboration Agreement generated on contract acceptance.",
                    "Enforced revision cap (Default: 2 revisions) preventing scope creep.",
                    "Clear cancellation policy: Partial compensation for work already drafted.",
                    "Built-in Dispute Escalation button submitting ticket to Super Admin."
                ],
                "badge": "Module 13"
            },
            {
                "title": "Module 14: Payment & Deal Management",
                "items": [
                    "Deal ledger: Tracks Pending, In-Progress, Released, and Paid fees.",
                    "Transaction reference number & invoice/receipt generation.",
                    "Zero fake escrow: Clearly labels milestone release states.",
                    "Card data compliance: PCI-compliant gateway integration hooks."
                ],
                "badge": "Module 14"
            }
        ]
    },
    {
        "slide_num": 11,
        "category": "PHASE 1 - MODULES 15 & 16",
        "title": "Multi-Creator Bundles & Open Bids",
        "subtitle": "Multi-Talent Campaign Management & Open Reverse-Auction Bidding",
        "type": "grid",
        "cards": [
            {
                "title": "Module 15: Multi-Creator Campaign Bundles",
                "items": [
                    "Aggregate 2-10 creators under a single umbrella brand campaign.",
                    "Unified campaign budget breakdown with individual creator allocations.",
                    "Consolidated timeline & deliverable master-schedule for brand managers.",
                    "Aggregated campaign analytics dashboard combining all creator reach."
                ],
                "badge": "Module 15"
            },
            {
                "title": "Module 16: Open Collaboration Bids",
                "items": [
                    "Reverse RFP: Business publishes target problem and budget ceiling.",
                    "Creators pitch unique creative angles, content hooks & custom prices.",
                    "Business compares incoming pitches side-by-side in bid review tray.",
                    "Direct 1-click contract acceptance and conversion to active project."
                ],
                "badge": "Module 16"
            }
        ]
    },
    {
        "slide_num": 12,
        "category": "PHASE 1 - MODULES 17 & 18",
        "title": "AI Content Brief Generator & Dashboards",
        "subtitle": "Smart Creative Ideation & Role-Tailored Command Centers",
        "type": "grid",
        "cards": [
            {
                "title": "Module 17: Content Brief Generator",
                "items": [
                    "Input category, target audience, and campaign objective.",
                    "Generates 3 Reel hooks, storyboards, caption concepts & CTA suggestions.",
                    "Reliable fallback engine: 50+ curated high-converting local templates.",
                    "AI Integration hook ready (Gemini API) with zero-failure offline mode."
                ],
                "badge": "Module 17"
            },
            {
                "title": "Module 18: Dual Role-Specific Dashboards",
                "items": [
                    "Business Dashboard: Spend tracker, active collabs, conversion stats, quick-hire.",
                    "Creator Dashboard: Incoming campaign invites, active deadlines, pending payouts.",
                    "Real-time summary widgets: Unread messages, tasks requiring review.",
                    "Fast action buttons: 'Post New Campaign' / 'Browse Matching Gigs'."
                ],
                "badge": "Module 18"
            }
        ]
    },
    {
        "slide_num": 13,
        "category": "PHASE 1 - MODULES 19 & 20",
        "title": "Discovery Map & Favourites / Repeat Gigs",
        "subtitle": "Interactive Geographic Search & Fast-Track Re-Hiring Workflows",
        "type": "grid",
        "cards": [
            {
                "title": "Module 19: Local Creator Discovery Map",
                "items": [
                    "Interactive Leaflet/Map view pinning creators by neighborhood / campus.",
                    "Privacy First: Pins reflect city/locality center, never exact residences.",
                    "Hover cards display creator niche, engagement score & starting rates.",
                    "Radius slider (1km, 5km, 15km, 30km) centered on business storefront."
                ],
                "badge": "Module 19"
            },
            {
                "title": "Module 20: Favourites & Repeat Deals",
                "items": [
                    "Create customized creator shortlists (e.g. 'Weekend Cafe Promos').",
                    "Past Collaboration History: One-click 'Re-Hire for New Campaign'.",
                    "Pre-filled deliverables based on successful previous collaborations.",
                    "Special repeat-client rate negotiation options."
                ],
                "badge": "Module 20"
            }
        ]
    },
    {
        "slide_num": 14,
        "category": "FUTURE EXPANSION - MODULES 21 TO 26",
        "title": "Modular Student Talent Hub",
        "subtitle": "Independent Subsystem: Freelance Gigs, Micro-Services & Verified Certificates",
        "type": "grid",
        "cards": [
            {
                "title": "Modules 21 & 22: Gigs & Skill Match",
                "items": [
                    "Freelance catalog: Video Editing, Reels, Graphic Design, Captions, Socials.",
                    "Businesses & Creators can hire student talent for post-production.",
                    "Skill-based matching engine filtering by software, tools & availability.",
                    "Student portfolio cards featuring verified Figma/Canva/Drive links."
                ],
                "badge": "Modular"
            },
            {
                "title": "Modules 23 & 24: Certificate Engine",
                "items": [
                    "Verified Experience Certificates issued upon successful project approval.",
                    "Unique Certificate ID + tamper-proof verification page with QR code.",
                    "Student profile showcases certified work hours & skill ratings.",
                    "Zero fake certificates: Locked until client submits final sign-off."
                ],
                "badge": "Certificates"
            },
            {
                "title": "Modules 25 & 26: Retainers & Growth",
                "items": [
                    "Monthly social media packages: Hire student teams on monthly retainers.",
                    "Shared content calendar with scheduled deliverable milestones.",
                    "Student Opportunity Hub: Free webinars, project bounties, career guides.",
                    "Feature-flagged: Can be turned on/off without affecting Core Phase 1."
                ],
                "badge": "Growth Hub"
            }
        ]
    },
    {
        "slide_num": 15,
        "category": "GOVERNANCE & PLATFORM OPERATIONS",
        "title": "Super Admin Panel & Dispute Center",
        "subtitle": "Comprehensive Administrative Control, Content Moderation & Auditing",
        "type": "grid",
        "cards": [
            {
                "title": "User & Campaign Governance",
                "items": [
                    "Manage all Business, Creator, and Student accounts with ban/flag tools.",
                    "Campaign moderation queue: Review flagged or suspicious listings.",
                    "Review moderation queue: Prevent slander or retaliatory fake reviews.",
                    "Creator badge verification approvals (checking connected socials)."
                ],
                "badge": "Moderation"
            },
            {
                "title": "Dispute Resolution & Audit Logs",
                "items": [
                    "Dispute Center: Examine chat history, uploaded drafts & contract terms.",
                    "Admin resolution actions: Rule in favor of creator or refund business.",
                    "Complete Audit Log: Records every administrative intervention with timestamp.",
                    "Feature Flag Management: Toggle Student Talent Hub visibility."
                ],
                "badge": "Disputes & Logs"
            }
        ]
    },
    {
        "slide_num": 16,
        "category": "DATA ARCHITECTURE",
        "title": "Relational Database Schema & Entities",
        "subtitle": "18 Structured Models Ensuring Complete Data Integrity & Relational Soundness",
        "type": "grid",
        "cards": [
            {
                "title": "Core Platform Entities (1-6)",
                "items": [
                    "User (id, email, password_hash, role, status, created_at)",
                    "BusinessProfile (user_id, name, category, location, bio, logo)",
                    "CreatorProfile (user_id, niche, location, bio, platforms, rates)",
                    "Campaign (id, business_id, title, budget, objective, status)",
                    "CampaignApplication (id, campaign_id, creator_id, bid_price, status)",
                    "Collaboration (id, campaign_id, business_id, creator_id, terms, status)"
                ],
                "badge": "Core Entities"
            },
            {
                "title": "Workflow & Tracking Entities (7-12)",
                "items": [
                    "DeliverableItem (collab_id, title, type, status, draft_url)",
                    "ChatMessage (collab_id, sender_id, receiver_id, message, read)",
                    "Notification (user_id, title, message, link, read, created_at)",
                    "TrackingCode (campaign_id, creator_id, qr_code, coupon_code)",
                    "TrackingEvent (code_id, event_type [SCAN/COUPON/LEAD], timestamp)",
                    "DealPayment (collab_id, amount, status, tx_ref, paid_at)"
                ],
                "badge": "Attribution & Ops"
            },
            {
                "title": "Trust, Student & Audit Entities (13-18)",
                "items": [
                    "Review (collab_id, author_id, target_id, rating, comment)",
                    "VerificationRequest (user_id, document_url, status, reviewed_by)",
                    "StudentProfile (user_id, university, skills, portfolio_links)",
                    "StudentCertificate (student_id, project_title, client_id, cert_id)",
                    "DisputeTicket (collab_id, raised_by, reason, status, resolution)",
                    "AuditLog (admin_id, action, target_entity, details, created_at)"
                ],
                "badge": "Trust & Expansion"
            }
        ]
    },
    {
        "slide_num": 17,
        "category": "NON-FUNCTIONAL SPECIFICATIONS",
        "title": "Security, Performance & Reliability",
        "subtitle": "Enterprise Standards Baked into Platform Foundations",
        "type": "grid",
        "cards": [
            {
                "title": "Rigorous Security Standards",
                "items": [
                    "Bcrypt password hashing (salt rounds 10+) & CSRF protection.",
                    "Input sanitization preventing SQL injection & XSS scripting.",
                    "Rate limiting on auth & sensitive API routes (10 req/min for auth).",
                    "Protected file upload pipelines with mime-type checking."
                ],
                "badge": "Security"
            },
            {
                "title": "High Performance Benchmarks",
                "items": [
                    "Lighthouse performance target > 90 across mobile & desktop.",
                    "Pagination on all marketplace grids & database queries.",
                    "Debounced search inputs & cached public creator directories.",
                    "Lazy loading images, modular code-splitting & optimistic UI updates."
                ],
                "badge": "Performance"
            },
            {
                "title": "Reliability & Resilience",
                "items": [
                    "Comprehensive Error Boundaries preventing cascade page crashes.",
                    "Structured empty states, loading skeletons & informative tooltips.",
                    "Fallback template algorithms for AI brief generator if offline.",
                    "Zero broken buttons or placeholder non-functional links."
                ],
                "badge": "Reliability"
            }
        ]
    },
    {
        "slide_num": 18,
        "category": "USER JOURNEYS",
        "title": "End-to-End User Experience Flows",
        "subtitle": "Step-by-Step Experience Mapping for Both Core Personas",
        "type": "grid",
        "cards": [
            {
                "title": "Business Persona Journey",
                "items": [
                    "1. Onboarding: Register business, define location & marketing goals.",
                    "2. Discovery: Search creators by locality & compare opportunity scores.",
                    "3. Campaign Launch: Post campaign budget & deliverables in marketplace.",
                    "4. Collaboration: Accept bids, approve draft content & monitor deadlines.",
                    "5. Attribution: Track in-store QR scans & coupon redemptions in real time.",
                    "6. Closeout: Release payment, generate invoice & write mutual review."
                ],
                "badge": "Business Journey"
            },
            {
                "title": "Creator Persona Journey",
                "items": [
                    "1. Onboarding: Build profile, link social handles & showcase top reels.",
                    "2. Exploration: Filter campaigns matching niche & hyperlocal radius.",
                    "3. Bidding: Apply with custom creative proposal & deliverable fees.",
                    "4. Production: Receive agreement, create drafts & upload to Collab Hub.",
                    "5. Revision: Address brand feedback within agreed 2-revision limit.",
                    "6. Payout: Final content approved, track deal payout & receive 5-star review."
                ],
                "badge": "Creator Journey"
            }
        ]
    },
    {
        "slide_num": 19,
        "category": "DELIVERY ROADMAP",
        "title": "Iterative Development & Build Roadmap",
        "subtitle": "Systematic Implementation Steps Towards Complete Working Product",
        "type": "grid",
        "cards": [
            {
                "title": "Milestone 1: Foundations & Auth",
                "items": [
                    "Next.js + Tailwind project setup, design system & typography.",
                    "Database schema setup with Prisma ORM & migrations.",
                    "Secure dual-role authentication & session state management."
                ],
                "badge": "Sprint 1"
            },
            {
                "title": "Milestone 2: Marketplace & Match",
                "items": [
                    "Business & Creator profile pages with rich media kit display.",
                    "Smart Creator Discovery marketplace with filters & compare tray.",
                    "Hyperlocal matching algorithm & budget-to-campaign planner."
                ],
                "badge": "Sprint 2"
            },
            {
                "title": "Milestone 3: Campaigns & Collab",
                "items": [
                    "Campaign creation, application & reverse bidding workflows.",
                    "Collaboration Hub with deliverable checklists & draft submissions.",
                    "Messaging system, notifications & automated deadline alerts."
                ],
                "badge": "Sprint 3"
            },
            {
                "title": "Milestone 4: Tracking & Final Polish",
                "items": [
                    "QR & coupon conversion engine + real-time ROI analytics dashboard.",
                    "Mutual review system, payment ledger & Super Admin panel.",
                    "Student Talent Hub modular shell & complete end-to-end verification."
                ],
                "badge": "Sprint 4"
            }
        ]
    },
    {
        "slide_num": 20,
        "category": "FINAL VERIFICATION & SIGN-OFF",
        "title": "Cross-Check Sign-Off & Green Light",
        "subtitle": "Review Confirmation Before Proceeding to Complete Website Code Construction",
        "type": "title",
        "cards": [
            {
                "title": "Module Verification Checklist",
                "items": [
                    "Are all 20 Phase-1 core marketplace modules aligned with your vision?",
                    "Is the dual-role authentication & access control matrix approved?",
                    "Are the QR & coupon conversion tracking requirements complete?",
                    "Is the modular Student Talent Hub architecture accepted for future expansion?"
                ],
                "badge": "Review Points"
            },
            {
                "title": "Next Step: Build Execution",
                "items": [
                    "Upon your confirmation, the entire working application will be created.",
                    "Every component will be fully functional with real persisted data.",
                    "A responsive, live local dev server will be started for interactive testing.",
                    "No mockup buttons, no fake analytics, and zero placeholder stubs."
                ],
                "badge": "Action Plan"
            }
        ]
    }
]

print(f"Loaded {len(slides_data)} slides successfully.")
