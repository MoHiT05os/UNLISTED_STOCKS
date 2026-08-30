import os

with open('about.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the main section
new_main = """
  <main>
    <section class="section" style="padding-top: 80px; padding-bottom: 60px;">
      <div class="wrap text-center">
        <!-- Big Logo in center top -->
        <img src="images/logo.png" alt="MDB Arthasphere Logo" style="height: 120px; width: auto; object-fit: contain; margin-bottom: 24px;">
        
        <h1 class="text-gradient" style="margin-bottom: 24px; font-size: 36px;">About MDB ARTHASPHERE</h1>
        
        <p style="color: var(--text-muted); font-size: 18px; max-width: 800px; margin: 0 auto; line-height: 1.6;">
          MDB Arthasphere is a growing financial markets platform focused on connecting investors with opportunities across unlisted shares, IPOs, equities, bonds, money markets, and beyond. Through transparency, market intelligence, and a client-first approach, we aim to make investing opportunities more accessible and easier to understand.
        </p>
      </div>
    </section>

    <!-- DRHP / IPO Lifecycle Timeline -->
    <section class="section" style="padding-bottom: 80px; background: rgba(255,255,255,0.02);">
      <div class="wrap">
        <h2 class="text-center" style="margin-bottom: 40px; font-size: 28px;">Our IPO & DRHP Tracking System</h2>
        
        <div style="max-width: 800px; margin: 0 auto;">
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
            
            <!-- Box 1 -->
            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; position: relative;">
              <div style="position: absolute; top: -12px; left: 20px; background: var(--primary); color: #000; font-weight: bold; font-size: 12px; padding: 4px 10px; border-radius: 20px;">Stage 1</div>
              <h3 style="margin-top: 10px; margin-bottom: 8px; font-size: 18px;">DRHP Filed</h3>
              <p style="font-size: 14px; color: var(--text-muted);">Company files the Draft Red Herring Prospectus with SEBI.</p>
            </div>
            
            <!-- Box 2 -->
            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; position: relative;">
              <div style="position: absolute; top: -12px; left: 20px; background: var(--primary); color: #000; font-weight: bold; font-size: 12px; padding: 4px 10px; border-radius: 20px;">Stage 2</div>
              <h3 style="margin-top: 10px; margin-bottom: 8px; font-size: 18px;">SEBI Observations</h3>
              <p style="font-size: 14px; color: var(--text-muted);">SEBI reviews and provides approval/observations.</p>
            </div>
            
            <!-- Box 3 -->
            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; position: relative;">
              <div style="position: absolute; top: -12px; left: 20px; background: var(--primary); color: #000; font-weight: bold; font-size: 12px; padding: 4px 10px; border-radius: 20px;">Stage 3</div>
              <h3 style="margin-top: 10px; margin-bottom: 8px; font-size: 18px;">Updated DRHP</h3>
              <p style="font-size: 14px; color: var(--text-muted);">Company incorporates SEBI feedback and files addendum.</p>
            </div>
            
            <!-- Box 4 -->
            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; position: relative;">
              <div style="position: absolute; top: -12px; left: 20px; background: var(--primary); color: #000; font-weight: bold; font-size: 12px; padding: 4px 10px; border-radius: 20px;">Stage 4</div>
              <h3 style="margin-top: 10px; margin-bottom: 8px; font-size: 18px;">RHP Filed</h3>
              <p style="font-size: 14px; color: var(--text-muted);">Red Herring Prospectus filed with final dates & price band.</p>
            </div>
            
            <!-- Box 5 -->
            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; position: relative;">
              <div style="position: absolute; top: -12px; left: 20px; background: var(--primary); color: #000; font-weight: bold; font-size: 12px; padding: 4px 10px; border-radius: 20px;">Stage 5</div>
              <h3 style="margin-top: 10px; margin-bottom: 8px; font-size: 18px;">IPO Opens</h3>
              <p style="font-size: 14px; color: var(--text-muted);">Public subscription window officially opens.</p>
            </div>
            
            <!-- Box 6 -->
            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; position: relative;">
              <div style="position: absolute; top: -12px; left: 20px; background: var(--primary); color: #000; font-weight: bold; font-size: 12px; padding: 4px 10px; border-radius: 20px;">Stage 6</div>
              <h3 style="margin-top: 10px; margin-bottom: 8px; font-size: 18px;">IPO Closes</h3>
              <p style="font-size: 14px; color: var(--text-muted);">Bidding ends and subscription data is finalized.</p>
            </div>
            
            <!-- Box 7 -->
            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; position: relative;">
              <div style="position: absolute; top: -12px; left: 20px; background: var(--primary); color: #000; font-weight: bold; font-size: 12px; padding: 4px 10px; border-radius: 20px;">Stage 7</div>
              <h3 style="margin-top: 10px; margin-bottom: 8px; font-size: 18px;">Allotment</h3>
              <p style="font-size: 14px; color: var(--text-muted);">Shares are allotted to successful bidders.</p>
            </div>
            
            <!-- Box 8 -->
            <div style="background: var(--bg-surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; position: relative;">
              <div style="position: absolute; top: -12px; left: 20px; background: var(--primary); color: #000; font-weight: bold; font-size: 12px; padding: 4px 10px; border-radius: 20px;">Stage 8</div>
              <h3 style="margin-top: 10px; margin-bottom: 8px; font-size: 18px;">Listing</h3>
              <p style="font-size: 14px; color: var(--text-muted);">Shares debut on the NSE/BSE for public trading.</p>
            </div>

          </div>
        </div>
      </div>
    </section>
  </main>
"""

import re
content = re.sub(r'<main>.*?</main>', new_main, content, flags=re.DOTALL)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("about.html updated.")
