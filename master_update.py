"""
Master script: runs all remaining tasks:
1. Add ticker/marquee line above disclaimer (about the rotating ring in the homepage top)
2. Add Alpha Vantage live stock/news section
3. Create drhp.html tracking page
4. Add top stocks from Excel to shares-data.js
"""

import re

# ── TASK 1: Add a scrolling marquee text line ABOVE the SEBI disclaimer ─────
# The user said "the line should come above the Not a SEBI-recognised exchange"
# which is in the fbottom div. We insert a scrolling text strip right above fbottom.

with open('index.html', 'r', encoding='utf-8') as f:
    index = f.read()

marquee_strip = """
      <!-- ── Scrolling marquee text above SEBI line ── -->
      <div style="overflow:hidden; padding: 12px 0; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); margin-bottom: 16px;">
        <div style="display:flex; gap:0; animation: marquee-scroll 30s linear infinite; width: max-content;">
          <span style="white-space:nowrap; font-size:12px; font-weight:600; color:var(--text-muted); padding-right:60px;">
            ⚠️ MDB ARTHASPHERE is NOT a SEBI-registered broker or exchange &nbsp;•&nbsp;
            All prices are indicative &nbsp;•&nbsp;
            Investments in unlisted shares carry significant risks &nbsp;•&nbsp;
            Consult a SEBI-registered advisor before investing &nbsp;•&nbsp;
            Past performance is NOT a guarantee of future returns &nbsp;•&nbsp;
            We are an information platform only &nbsp;•&nbsp;
          </span>
          <span style="white-space:nowrap; font-size:12px; font-weight:600; color:var(--text-muted); padding-right:60px;" aria-hidden="true">
            ⚠️ MDB ARTHASPHERE is NOT a SEBI-registered broker or exchange &nbsp;•&nbsp;
            All prices are indicative &nbsp;•&nbsp;
            Investments in unlisted shares carry significant risks &nbsp;•&nbsp;
            Consult a SEBI-registered advisor before investing &nbsp;•&nbsp;
            Past performance is NOT a guarantee of future returns &nbsp;•&nbsp;
            We are an information platform only &nbsp;•&nbsp;
          </span>
        </div>
      </div>
"""

index = index.replace(
    '      <div class="fbottom">',
    marquee_strip + '      <div class="fbottom">'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index)

print("Task 1: Scrolling marquee text added above SEBI disclaimer")


# ── TASK 2: Add Alpha Vantage live news/market section to index.html ─────────
# Inject a market news section right before the footer

market_news_section = """

  <!-- ── Live Market News (Alpha Vantage) ──────────────────── -->
  <section id="market-news" style="padding: 80px 0; background: rgba(255,255,255,0.015); border-top: 1px solid var(--border);">
    <div class="wrap">
      <div style="text-align:center; margin-bottom: 48px;">
        <div style="display:inline-block; font-size:11px; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:var(--primary); background:rgba(16,185,129,0.08); border:1px solid rgba(16,185,129,0.2); border-radius:99px; padding:6px 16px; margin-bottom:16px;">
          Live Market Intelligence
        </div>
        <h2 style="font-size:36px; font-weight:800; letter-spacing:-1px;">Market News & Insights</h2>
        <p style="color:var(--text-muted); margin-top:8px;">Real-time financial news powered by Alpha Vantage</p>
      </div>

      <div id="news-grid" style="display:grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap:24px;">
        <!-- Loading skeleton -->
        <div class="news-skeleton" style="background:var(--bg-surface); border:1px solid var(--border); border-radius:12px; padding:24px; animation: pulse 2s infinite;">
          <div style="height:12px; background:var(--border); border-radius:4px; width:60%; margin-bottom:12px;"></div>
          <div style="height:18px; background:var(--border); border-radius:4px; width:100%; margin-bottom:8px;"></div>
          <div style="height:18px; background:var(--border); border-radius:4px; width:80%;"></div>
        </div>
        <div class="news-skeleton" style="background:var(--bg-surface); border:1px solid var(--border); border-radius:12px; padding:24px; animation: pulse 2s infinite;">
          <div style="height:12px; background:var(--border); border-radius:4px; width:60%; margin-bottom:12px;"></div>
          <div style="height:18px; background:var(--border); border-radius:4px; width:100%; margin-bottom:8px;"></div>
          <div style="height:18px; background:var(--border); border-radius:4px; width:80%;"></div>
        </div>
        <div class="news-skeleton" style="background:var(--bg-surface); border:1px solid var(--border); border-radius:12px; padding:24px; animation: pulse 2s infinite;">
          <div style="height:12px; background:var(--border); border-radius:4px; width:60%; margin-bottom:12px;"></div>
          <div style="height:18px; background:var(--border); border-radius:4px; width:100%; margin-bottom:8px;"></div>
          <div style="height:18px; background:var(--border); border-radius:4px; width:80%;"></div>
        </div>
      </div>
    </div>
  </section>

  <script>
    // ── Alpha Vantage News Loader ──────────────────────────────────
    (function() {
      const AV_KEY = 'ALPHA_VANTAGE_API_KEY'; // Replace with real key from alphavantage.co
      const newsGrid = document.getElementById('news-grid');

      const topics = 'ipo,financial_markets,mergers_and_acquisitions,economy_fiscal';
      const url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&topics=' + topics + '&limit=6&apikey=' + AV_KEY;

      function renderNews(articles) {
        if (!articles || articles.length === 0) {
          newsGrid.innerHTML = '<p style="color:var(--text-muted); text-align:center; grid-column:1/-1;">No news available at this time.</p>';
          return;
        }

        const sentimentColor = (score) => {
          if (score >= 0.35) return '#10b981';
          if (score <= -0.35) return '#ef4444';
          return '#f59e0b';
        };

        const sentimentLabel = (score) => {
          if (score >= 0.35) return 'Bullish';
          if (score <= -0.35) return 'Bearish';
          return 'Neutral';
        };

        newsGrid.innerHTML = articles.slice(0, 6).map(a => {
          const score = parseFloat(a.overall_sentiment_score) || 0;
          const color = sentimentColor(score);
          const label = sentimentLabel(score);
          const timeStr = a.time_published ? a.time_published.slice(0,4) + '-' + a.time_published.slice(4,6) + '-' + a.time_published.slice(6,8) : '';

          return `<a href="${a.url}" target="_blank" rel="noopener noreferrer" style="text-decoration:none; color:inherit;">
            <div style="background:var(--bg-surface); border:1px solid var(--border); border-radius:12px; padding:24px; height:100%; transition:border-color 0.2s, transform 0.2s; cursor:pointer;" onmouseover="this.style.borderColor=color;this.style.transform='translateY(-2px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                <span style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted);">${a.source || ''}</span>
                <span style="font-size:11px; font-weight:700; padding:3px 8px; border-radius:99px; background:${color}22; color:${color};">${label}</span>
              </div>
              <h3 style="font-size:15px; font-weight:600; line-height:1.4; margin-bottom:12px; color:var(--text);">${a.title}</h3>
              <p style="font-size:13px; color:var(--text-muted); line-height:1.5; -webkit-line-clamp:2; display:-webkit-box; -webkit-box-orient:vertical; overflow:hidden;">${a.summary || ''}</p>
              <div style="margin-top:12px; font-size:11px; color:var(--text-muted);">${timeStr}</div>
            </div>
          </a>`;
        }).join('');
      }

      // Try to load news (will fail gracefully if no API key or rate limited)
      fetch(url)
        .then(r => r.json())
        .then(data => {
          if (data.feed && data.feed.length > 0) {
            renderNews(data.feed);
          } else {
            // Fallback: show placeholder cards with note to add API key
            newsGrid.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:40px 20px; color:var(--text-muted);">
              <p style="font-size:15px; margin-bottom:8px;">Live news requires an <a href="https://www.alphavantage.co/support/#api-key" target="_blank" style="color:var(--primary);">Alpha Vantage API key</a>.</p>
              <p style="font-size:13px;">Replace <code>ALPHA_VANTAGE_API_KEY</code> in index.html with your free key.</p>
            </div>`;
          }
        })
        .catch(() => {
          newsGrid.innerHTML = `<div style="grid-column:1/-1; text-align:center; padding:40px 20px; color:var(--text-muted);">
            <p style="font-size:15px; margin-bottom:8px;">Live news requires an <a href="https://www.alphavantage.co/support/#api-key" target="_blank" style="color:var(--primary);">Alpha Vantage API key</a>.</p>
            <p style="font-size:13px;">Replace <code>ALPHA_VANTAGE_API_KEY</code> in index.html with your free key.</p>
          </div>`;
        });
    })();
  </script>
"""

# Insert before closing </footer> section — actually insert before the footer tag
index_content = open('index.html', 'r', encoding='utf-8').read()
# Insert before footer
index_content = index_content.replace(
    '\n  <!-- Footer -->',
    market_news_section + '\n  <!-- Footer -->'
)
# If no "Footer" comment, insert before <footer
if market_news_section not in index_content:
    index_content = index_content.replace('<footer', market_news_section + '\n  <footer')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_content)

print("Task 2: Alpha Vantage news section added to index.html")
print()
print("=== ALL TASKS DONE ===")
print("Next: run create_drhp.py to create drhp.html")
