import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove compliance bar
html = re.sub(r'<!-- 1\. Compliance Marquee -->.*?<!-- 2\. Header -->', '<!-- 2. Header -->', html, flags=re.DOTALL)

# 2. Update Header links
nav_old = '''<nav class="nav-links" id="nav-links">
        <a href="shares.html">All Shares</a>
        <a href="#drhp">DRHP Filed</a>
        <a href="#events">Events</a>
        <a href="#screener">Screener</a>
        <a href="about.html">About</a>
        <a href="contact.html">Contact Us</a>
      </nav>'''
nav_new = '''<nav class="nav-links" id="nav-links">
        <a href="index.html" style="color: var(--primary);">Home</a>
        <a href="shares.html">Marketplace</a>
        <a href="#drhp">DRHP Insights</a>
        <a href="#events">Events</a>
        <a href="#screener">Screener</a>
        <a href="#resources">Resources <svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M6 9l6 6 6-6"/></svg></a>
        <a href="about.html">About</a>
      </nav>'''
html = html.replace(nav_old, nav_new)

# 3. Replace Hero and USP Strip
hero_old_match = re.search(r'<!-- 3\. Hero Section -->.*?<!-- 5\. Popular Shares -->', html, flags=re.DOTALL)
if hero_old_match:
    hero_old = hero_old_match.group(0)

    hero_new = '''<!-- 3. Hero Section Split -->
    <section class="hero">
      <div class="wrap hero-split">
        
        <!-- Left Column -->
        <div class="hero-left reveal visible">
          <div class="hero-pill">
            <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
            India's Most Trusted Unlisted Shares Platform
          </div>
          
          <h1 class="hero-title">Invest in India's<br>Next Big <em>Stories</em></h1>
          
          <p class="text-muted" style="font-size: 18px; line-height: 1.6; margin-bottom: 40px; max-width: 500px;">
            Track prices, analyze insights, and invest in unlisted, pre-IPO, and ESOP shares — all in one seamless platform.
          </p>
          
          <div style="display:flex; gap:16px;">
            <a href="shares.html" class="btn btn-primary" style="padding: 16px 24px; font-size: 16px;">Explore Shares &rarr;</a>
            <a href="#how" class="btn btn-ghost" style="padding: 16px 24px; font-size: 16px;">
              <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M10 8l6 4-6 4V8z"/></svg>
              How It Works
            </a>
          </div>
          
          <div class="hero-tags">
            <div class="hero-tag">
              <div class="hero-tag-icon">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              </div>
              <div>
                <div class="hero-tag-text">Real-time Price Tracking</div>
                <div class="hero-tag-sub">Live & indicative prices</div>
              </div>
            </div>
            <div class="hero-tag">
              <div class="hero-tag-icon">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
              </div>
              <div>
                <div class="hero-tag-text">Research & Insights</div>
                <div class="hero-tag-sub">DRHPs, financials & more</div>
              </div>
            </div>
            <div class="hero-tag">
              <div class="hero-tag-icon">
                <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
              </div>
              <div>
                <div class="hero-tag-text">Secure & Transparent</div>
                <div class="hero-tag-sub">Trusted by 1L+ investors</div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Column: Dashboard Card -->
        <div class="hero-right reveal visible reveal-delay-1">
          <div class="dashboard-card">
            <div class="dash-header">
              <div style="font-weight: 700; font-size: 18px;">Market Overview <span style="font-size: 12px; color: var(--text-muted); font-weight: 400; margin-left: 8px;">All prices are indicative ⓘ</span></div>
            </div>
            
            <div class="dash-stats-grid">
              <div class="dash-stat">
                <div class="dash-stat-label">Total Shares</div>
                <div class="dash-stat-val">2,543+</div>
                <div class="dash-stat-chg">+12.5% today</div>
              </div>
              <div class="dash-stat">
                <div class="dash-stat-label">Investors</div>
                <div class="dash-stat-val">1,00,000+</div>
                <div class="dash-stat-chg">+8.2% this month</div>
              </div>
              <div class="dash-stat">
                <div class="dash-stat-label">Active Orders</div>
                <div class="dash-stat-val">1,245+</div>
                <div class="dash-stat-chg">+15.3% today</div>
              </div>
              <div class="dash-stat" style="background: rgba(0, 230, 118, 0.05); border-color: rgba(0, 230, 118, 0.2);">
                <div class="dash-stat-label">Market Movement</div>
                <div class="dash-stat-val" style="color: var(--primary);">Bullish <svg width="16" height="16" style="float:right" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg></div>
                <div class="dash-stat-chg">Market is up 1.2%</div>
              </div>
            </div>
            
            <div class="dash-tabs">
              <div class="dash-tab active">Trending</div>
              <div class="dash-tab">Top Gainers</div>
              <div class="dash-tab">Most Active</div>
              <div class="dash-tab">Newly Added</div>
            </div>
            
            <div class="dash-table-header">
              <div>Company</div>
              <div>Price Range</div>
              <div>Change</div>
              <div></div>
            </div>
            
            <!-- Rows -->
            <div class="dash-row">
              <div style="display:flex; gap:12px; align-items:center;">
                <div style="width:32px; height:32px; background:#8b5cf6; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:12px;">ZP</div>
                <div><div style="font-weight:600; font-size:14px;">Zepto</div><div style="font-size:11px; color:var(--text-muted);">Unlisted</div></div>
              </div>
              <div style="font-size:13px; font-weight:500;">₹1,280 - ₹1,350</div>
              <div style="font-size:13px; color:var(--primary); font-weight:500;">+12.45%</div>
              <div><svg width="60" height="20" fill="none" stroke="var(--primary)" stroke-width="1.5"><path d="M0,15 Q5,5 15,10 T30,12 T45,5 T60,8"/></svg></div>
            </div>
            
            <div class="dash-row">
              <div style="display:flex; gap:12px; align-items:center;">
                <div style="width:32px; height:32px; background:#00d09c; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:12px;">GR</div>
                <div><div style="font-weight:600; font-size:14px;">Groww</div><div style="font-size:11px; color:var(--text-muted);">Unlisted</div></div>
              </div>
              <div style="font-size:13px; font-weight:500;">₹1,150 - ₹1,210</div>
              <div style="font-size:13px; color:var(--primary); font-weight:500;">+8.32%</div>
              <div><svg width="60" height="20" fill="none" stroke="var(--primary)" stroke-width="1.5"><path d="M0,18 Q10,15 20,8 T40,10 T60,5"/></svg></div>
            </div>
            
            <div class="dash-row">
              <div style="display:flex; gap:12px; align-items:center;">
                <div style="width:32px; height:32px; background:#333; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:12px;">PW</div>
                <div><div style="font-weight:600; font-size:14px;">PhysicsWallah</div><div style="font-size:11px; color:var(--text-muted);">Pre-IPO</div></div>
              </div>
              <div style="font-size:13px; font-weight:500;">₹2,850 - ₹3,100</div>
              <div style="font-size:13px; color:var(--primary); font-weight:500;">+15.21%</div>
              <div><svg width="60" height="20" fill="none" stroke="var(--primary)" stroke-width="1.5"><path d="M0,12 Q15,18 25,10 T45,8 T60,2"/></svg></div>
            </div>
            
            <div class="dash-row">
              <div style="display:flex; gap:12px; align-items:center;">
                <div style="width:32px; height:32px; background:#e11d48; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:12px;">NU</div>
                <div><div style="font-weight:600; font-size:14px;">Nuvama</div><div style="font-size:11px; color:var(--text-muted);">Unlisted</div></div>
              </div>
              <div style="font-size:13px; font-weight:500;">₹4,100 - ₹4,450</div>
              <div style="font-size:13px; color:var(--primary); font-weight:500;">+6.18%</div>
              <div><svg width="60" height="20" fill="none" stroke="var(--primary)" stroke-width="1.5"><path d="M0,10 Q10,15 25,5 T45,12 T60,6"/></svg></div>
            </div>
            
            <div style="text-align:center; padding-top:16px; border-top:1px solid rgba(255,255,255,0.05); margin-top:12px;">
              <a href="shares.html" style="color:var(--text-muted); font-size:13px; text-decoration:none;">View All Trending Shares &rarr;</a>
            </div>
          </div>
          
          <!-- Mobile Mockup Overlapping -->
          <div class="mobile-mockup">
            <div style="font-size:11px; color:var(--text-muted); margin-bottom:4px;">Portfolio Value</div>
            <div style="font-size:24px; font-weight:700; margin-bottom:4px;">₹12,45,000 <span style="font-size:10px; background:rgba(0,230,118,0.2); color:var(--primary); padding:2px 6px; border-radius:10px; vertical-align:middle;">+14.6%</span></div>
            <div style="font-size:10px; color:var(--text-muted); margin-bottom:16px;">Overall Gain <span style="color:var(--primary);">+₹1,58,750 (14.6%)</span></div>
            
            <svg width="100%" height="60" fill="none" style="margin-bottom:16px;">
               <path d="M0,50 Q20,60 40,30 T80,40 T120,20 T160,25 T200,5 T230,10" stroke="var(--primary)" stroke-width="2"/>
               <path d="M0,50 Q20,60 40,30 T80,40 T120,20 T160,25 T200,5 T230,10 L230,60 L0,60 Z" fill="var(--primary)" opacity="0.1"/>
            </svg>
            
            <div style="display:flex; justify-content:space-between; font-size:10px; color:var(--text-muted); border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:8px; margin-bottom:12px;">
              <div style="color:var(--text); border-bottom:1px solid var(--primary); padding-bottom:7px; margin-bottom:-8px; font-weight:500;">Holdings</div>
              <div>Orders</div>
              <div>Watchlist</div>
            </div>
            
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
              <div style="display:flex; gap:8px;">
                 <div style="width:24px; height:24px; background:#8b5cf6; border-radius:50%; font-size:9px; display:flex; align-items:center; justify-content:center;">ZP</div>
                 <div><div style="font-size:11px; font-weight:600;">Zepto</div><div style="font-size:9px; color:var(--text-muted);">20 Shares &middot; Avg ₹1,225</div></div>
              </div>
              <div style="text-align:right;">
                 <div style="font-size:11px; font-weight:600;">₹2,45,000</div>
                 <div style="font-size:9px; color:var(--primary);">+18.5%</div>
              </div>
            </div>
            
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
              <div style="display:flex; gap:8px;">
                 <div style="width:24px; height:24px; background:#00d09c; border-radius:50%; font-size:9px; display:flex; align-items:center; justify-content:center;">GR</div>
                 <div><div style="font-size:11px; font-weight:600;">Groww</div><div style="font-size:9px; color:var(--text-muted);">15 Shares &middot; Avg ₹1,150</div></div>
              </div>
              <div style="text-align:right;">
                 <div style="font-size:11px; font-weight:600;">₹1,85,000</div>
                 <div style="font-size:9px; color:var(--primary);">+11.2%</div>
              </div>
            </div>
            
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
              <div style="display:flex; gap:8px;">
                 <div style="width:24px; height:24px; background:#333; border-radius:50%; font-size:9px; display:flex; align-items:center; justify-content:center;">PW</div>
                 <div><div style="font-size:11px; font-weight:600;">PhysicsWallah</div><div style="font-size:9px; color:var(--text-muted);">10 Shares &middot; Avg ₹3,000</div></div>
              </div>
              <div style="text-align:right;">
                 <div style="font-size:11px; font-weight:600;">₹3,75,000</div>
                 <div style="font-size:9px; color:var(--primary);">+15.3%</div>
              </div>
            </div>
            
            <div style="margin-top:auto; display:flex; justify-content:space-between; border-top:1px solid rgba(255,255,255,0.05); padding-top:12px; color:var(--text-muted);">
               <div style="text-align:center; color:var(--primary);"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg><div style="font-size:8px; margin-top:2px;">Home</div></div>
               <div style="text-align:center;"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg><div style="font-size:8px; margin-top:2px;">Explore</div></div>
               <div style="text-align:center;"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg><div style="font-size:8px; margin-top:2px;">Orders</div></div>
               <div style="text-align:center;"><svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg><div style="font-size:8px; margin-top:2px;">More</div></div>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Trusted By / Features Strip -->
    <div class="wrap">
      <div class="trusted-strip reveal visible">
        <div style="text-align:center; font-size:12px; font-weight:600; letter-spacing:1px; color:var(--text-muted); text-transform:uppercase; margin-bottom:32px;">Trusted by Smart Investors</div>
        <div class="trusted-grid">
           <div style="display:flex; align-items:center; gap:16px;">
              <div style="width:40px; height:40px; border-radius:8px; background:rgba(255,255,255,0.05); display:flex; align-items:center; justify-content:center;">
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
              </div>
              <div><div style="font-weight:700; font-size:18px;">1,00,000+</div><div style="font-size:12px; color:var(--text-muted);">Investors Served</div></div>
           </div>
           
           <div style="display:flex; align-items:center; gap:16px;">
              <div style="width:40px; height:40px; border-radius:8px; background:rgba(255,255,255,0.05); display:flex; align-items:center; justify-content:center;">
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
              </div>
              <div><div style="font-weight:700; font-size:18px;">255+</div><div style="font-size:12px; color:var(--text-muted);">Shares Tracked</div></div>
           </div>
           
           <div style="display:flex; align-items:center; gap:16px;">
              <div style="width:40px; height:40px; border-radius:8px; background:rgba(255,255,255,0.05); display:flex; align-items:center; justify-content:center;">
                <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              </div>
              <div><div style="font-weight:700; font-size:18px;">250+</div><div style="font-size:12px; color:var(--text-muted);">Active Brokers</div></div>
           </div>
           
           <div style="display:flex; align-items:center; gap:16px;">
              <div style="width:40px; height:40px; border-radius:8px; background:rgba(255,255,255,0.05); display:flex; align-items:center; justify-content:center;">
                <svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.31-8.86c-1.77-.45-2.34-.94-2.34-1.67 0-.84.79-1.43 2.1-1.43 1.38 0 1.9.66 1.94 1.64h1.71c-.05-1.97-1.3-3.15-3.17-3.41V4h-1v2.1c-1.58.22-3 1.25-3 2.92 0 1.88 1.48 2.65 3.55 3.12 1.94.46 2.45 1.15 2.45 1.95 0 .61-.43 1.51-2.22 1.51-1.71 0-2.43-.88-2.52-2.03H7.13c.12 2.01 1.48 3.19 3.37 3.52V20h1v-2.04c1.78-.22 3.16-1.22 3.16-3.04.01-1.89-1.31-2.61-3.35-3.12z"/></svg>
              </div>
              <div><div style="font-weight:700; font-size:18px;">₹500Cr+</div><div style="font-size:12px; color:var(--text-muted);">Volume Traded</div></div>
           </div>
           
           <div class="trusted-logos">
              <div style="font-size:20px; font-weight:800; font-family:serif;">Accel</div>
              <div style="font-size:20px; font-weight:400; font-family:sans-serif; letter-spacing:2px;">SEQUOIA</div>
              <div style="font-size:20px; font-weight:800; font-family:serif;">TIGER</div>
           </div>
        </div>
      </div>
      
      <div class="feature-strip reveal visible reveal-delay-1">
         <div class="feature-card-hz">
            <div class="icon"><svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/></svg></div>
            <div>
               <div style="font-weight:600; font-size:14px; margin-bottom:4px;">Wide Range of Opportunities</div>
               <div style="font-size:12px; color:var(--text-muted);">Unlisted, Pre-IPO & ESOPs</div>
            </div>
         </div>
         <div class="feature-card-hz">
            <div class="icon"><svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg></div>
            <div>
               <div style="font-weight:600; font-size:14px; margin-bottom:4px;">Deep Research & Insights</div>
               <div style="font-size:12px; color:var(--text-muted);">DRHPs, Financials, News & More</div>
            </div>
         </div>
         <div class="feature-card-hz">
            <div class="icon"><svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg></div>
            <div>
               <div style="font-weight:600; font-size:14px; margin-bottom:4px;">Easy & Secure Transactions</div>
               <div style="font-size:12px; color:var(--text-muted);">Seamless buying & selling</div>
            </div>
         </div>
         <div class="feature-card-hz">
            <div class="icon"><svg width="20" height="20" fill="currentColor" viewBox="0 0 24 24"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg></div>
            <div>
               <div style="font-weight:600; font-size:14px; margin-bottom:4px;">Dedicated Support</div>
               <div style="font-size:12px; color:var(--text-muted);">Expert help, whenever you need</div>
            </div>
         </div>
      </div>
    </div>
    <!-- 5. Popular Shares -->'''
    html = html.replace(hero_old, hero_new)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated index.html')
else:
    print('Error: Could not find old hero section')
