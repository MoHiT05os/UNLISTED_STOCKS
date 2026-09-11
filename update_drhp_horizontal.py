import re

html_file = 'drhp.html'
with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

new_layout = """<!-- ── Horizontal Scrollytelling Section ── -->
    <div class="horizontal-scroll-section" style="height: 400vh; position: relative;">
        <div class="sticky-wrapper" style="position: sticky; top: 0; height: 100vh; display: flex; align-items: center; overflow: hidden; padding-top: 60px;">
            
            <div class="ipo-tree-left" style="width: 380px; flex-shrink: 0; padding: 0 40px; z-index: 10;">
                <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1.5px;color:var(--primary);margin-bottom:8px;">IPO Journey</div>
                <h2 style="font-size:clamp(32px,4vw,48px); font-weight:900; line-height:1.1; margin-bottom:20px; color:#0f172a; letter-spacing:-1px;">
                  Track Every Step.<br>
                  <span style="color:#64748b; font-weight:700;">From Private to Public.</span>
                </h2>
                <div style="font-size:16px;color:var(--text-muted);line-height:1.7;">Scroll down to journey through the stages side-by-side.</div>
            </div>

            <div class="ipo-tree-right" style="flex: 1; overflow: hidden; padding: 40px 0;">
                <div class="cards-track" style="display: flex; gap: 40px; padding-right: 40vw; will-change: transform; transition: transform 0.1s ease-out;">
                    
                    <!-- Stage 1 -->
                    <div class="stage-card" style="background: #eef2ff; color: #312e81;">
                        <div class="card-top">
                            <span class="card-pill" style="background: #c7d2fe; color: #4338ca;">Stage 1</span>
                            <span class="card-icon">📄</span>
                        </div>
                        <h3 class="card-title">DRHP Filed</h3>
                        <p class="card-desc">The company hires investment bankers (lead managers) and files a Draft Red Herring Prospectus (DRHP) with SEBI. This document contains everything about the company — financials, risk factors, promoter background, use of IPO proceeds, and more. It is made public on the SEBI website for investor feedback.</p>
                        <div class="card-timeline" style="background: rgba(255,255,255,0.6); color: #3730a3;">⏱ Timeline: Anytime — no fixed window</div>
                    </div>

                    <!-- Stage 2 -->
                    <div class="stage-card" style="background: #fffbeb; color: #78350f;">
                        <div class="card-top">
                            <span class="card-pill" style="background: #fde68a; color: #b45309;">Stage 2</span>
                            <span class="card-icon">🔍</span>
                        </div>
                        <h3 class="card-title">SEBI Observations</h3>
                        <p class="card-desc">SEBI reviews the DRHP within 30 days. It may raise objections on disclosures, related-party transactions, promoter credentials, or financial statements. SEBI issues an "Observations Letter" which is NOT an approval — it just means disclosures are adequate. Companies must incorporate feedback before proceeding.</p>
                        <div class="card-timeline" style="background: rgba(255,255,255,0.6); color: #92400e;">⏱ Timeline: 30–75 days after DRHP filing</div>
                    </div>

                    <!-- Stage 3 -->
                    <div class="stage-card" style="background: #fff7ed; color: #7c2d12;">
                        <div class="card-top">
                            <span class="card-pill" style="background: #fed7aa; color: #c2410c;">Stage 3</span>
                            <span class="card-icon">✏️</span>
                        </div>
                        <h3 class="card-title">Updated DRHP</h3>
                        <p class="card-desc">Company files a revised or updated DRHP incorporating SEBI's observations. Additional disclosures, restated financials, or addendums may be filed. This is also when the company roadshows with institutional investors (QIBs) to gauge demand.</p>
                        <div class="card-timeline" style="background: rgba(255,255,255,0.6); color: #9a3412;">⏱ Timeline: 15–60 days after observations</div>
                    </div>

                    <!-- Stage 4 -->
                    <div class="stage-card" style="background: #eff6ff; color: #1e3a8a;">
                        <div class="card-top">
                            <span class="card-pill" style="background: #bfdbfe; color: #1d4ed8;">Stage 4</span>
                            <span class="card-icon">📋</span>
                        </div>
                        <h3 class="card-title">RHP Filed</h3>
                        <p class="card-desc">The Red Herring Prospectus (final) is filed with the Registrar of Companies (ROC) and stock exchanges (NSE/BSE). This contains the price band (e.g. ₹371–₹390), lot size, IPO dates, and final allocation ratios for QIB/HNI/Retail. This is the document investors use to make their bidding decision.</p>
                        <div class="card-timeline" style="background: rgba(255,255,255,0.6); color: #1e40af;">⏱ Timeline: 3–7 days before IPO opens</div>
                    </div>

                    <!-- Stage 5 -->
                    <div class="stage-card" style="background: #ecfdf5; color: #064e3b;">
                        <div class="card-top">
                            <span class="card-pill" style="background: #a7f3d0; color: #047857;">Stage 5</span>
                            <span class="card-icon">🟢</span>
                        </div>
                        <h3 class="card-title">IPO Opens</h3>
                        <p class="card-desc">The subscription window opens on NSE and BSE platforms. Investors can bid at any price within the price band using ASBA (Application Supported by Blocked Amount). The IPO stays open for 3 working days. QIBs, High Net Worth Individuals (HNI/NII), and Retail investors bid in separate categories.</p>
                        <div class="card-timeline" style="background: rgba(255,255,255,0.6); color: #065f46;">⏱ Timeline: 3 working days (mandatory)</div>
                    </div>

                    <!-- Stage 6 -->
                    <div class="stage-card" style="background: #fef2f2; color: #7f1d1d;">
                        <div class="card-top">
                            <span class="card-pill" style="background: #fecaca; color: #b91c1c;">Stage 6</span>
                            <span class="card-icon">🔴</span>
                        </div>
                        <h3 class="card-title">IPO Closed</h3>
                        <p class="card-desc">Bidding ends at 5 PM on Day 3. Final subscription numbers are released by BSE/NSE. If oversubscribed, retail allotment is done via computerised lottery. HNI/NII allotment is pro-rata. QIB allotment is discretionary. The basis of allotment document is published post-closure.</p>
                        <div class="card-timeline" style="background: rgba(255,255,255,0.6); color: #991b1b;">⏱ Timeline: Same day as IPO close date</div>
                    </div>

                    <!-- Stage 7 -->
                    <div class="stage-card" style="background: #f0fdf4; color: #14532d;">
                        <div class="card-top">
                            <span class="card-pill" style="background: #bbf7d0; color: #15803d;">Stage 7</span>
                            <span class="card-icon">💳</span>
                        </div>
                        <h3 class="card-title">Allotment</h3>
                        <p class="card-desc">Shares are credited to successful bidders' demat accounts. Blocked funds of unsuccessful bidders are released (ASBA unblocking). The registrar (e.g. KFintech, Link Intime) manages this process. You can check allotment status on the registrar's website using PAN or application number.</p>
                        <div class="card-timeline" style="background: rgba(255,255,255,0.6); color: #166534;">⏱ Timeline: T+6 days after IPO close</div>
                    </div>

                    <!-- Stage 8 -->
                    <div class="stage-card" style="background: #fefce8; color: #713f12;">
                        <div class="card-top">
                            <span class="card-pill" style="background: #fef08a; color: #a16207;">Stage 8</span>
                            <span class="card-icon">🏆</span>
                        </div>
                        <h3 class="card-title">Listed!</h3>
                        <p class="card-desc">The company's shares begin trading on NSE and BSE on the listing date. The opening price (listing price) is determined by pre-market discovery between 9–10 AM. From this point the company is a publicly listed entity — investors can buy and sell freely. The unlisted/GMP market price no longer applies.</p>
                        <div class="card-timeline" style="background: rgba(255,255,255,0.6); color: #854d0e;">⏱ Timeline: T+7 days after IPO close</div>
                    </div>

                </div>
            </div>
        </div>
    </div>

    <script>
        document.addEventListener('scroll', () => {
            if (window.innerWidth < 900) return; // Ignore on mobile
            
            const section = document.querySelector('.horizontal-scroll-section');
            const track = document.querySelector('.cards-track');
            if (!section || !track) return;
            
            const rect = section.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            
            // Calculate scroll progress within this 400vh section
            const scrollableDistance = rect.height - windowHeight;
            let scrolled = -rect.top;
            
            let progress = scrolled / scrollableDistance;
            progress = Math.max(0, Math.min(1, progress));
            
            // Translate the track horizontally based on vertical scroll progress
            const maxTranslate = track.scrollWidth - track.parentElement.offsetWidth + 80;
            if (maxTranslate > 0) {
                track.style.transform = `translateX(-${progress * maxTranslate}px)`;
            }
        });
    </script>

    <style>
        .stage-card {
            width: 420px;
            min-height: 480px;
            flex-shrink: 0;
            border-radius: 28px;
            padding: 40px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.03);
            transition: transform 0.3s ease;
        }
        
        .stage-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        }

        .card-top { display: flex; justify-content: space-between; align-items: center; }
        .card-pill { padding: 8px 16px; border-radius: 99px; font-size: 14px; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; }
        .card-icon { font-size: 48px; line-height: 1; }
        .card-title { font-size: clamp(28px, 4vw, 36px); font-weight: 900; margin: 0; letter-spacing: -1px; }
        .card-desc { font-size: 17px; line-height: 1.6; margin: 0; opacity: 0.9; }
        .card-timeline { margin-top: auto; padding: 14px 20px; border-radius: 12px; font-size: 15px; font-weight: 700; display: inline-table; width: fit-content; }
        
        @media (max-width: 899px) {
            .horizontal-scroll-section { height: auto !important; }
            .sticky-wrapper { position: static !important; height: auto !important; flex-direction: column; align-items: stretch !important; padding: 40px 20px 20px 20px; }
            .ipo-tree-left { width: 100% !important; padding: 0 !important; margin-bottom: 30px; }
            .ipo-tree-right { overflow-x: auto !important; -webkit-overflow-scrolling: touch; padding: 20px 0 !important; margin: 0 -20px; scroll-snap-type: x mandatory; scroll-padding-left: 20px; }
            .cards-track { transform: none !important; padding: 0 20px !important; gap: 20px !important; }
            .stage-card { width: 320px !important; min-height: 400px !important; padding: 28px; scroll-snap-align: start; }
        }
    </style>"""

pattern = re.compile(r'<div class="ipo-tree-wrap".*?</style>', re.DOTALL)
new_content = pattern.sub(new_layout, content)

with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_content)
