/**
 * MDB ARTHASPHERE — Stock Ticker Ribbon
 * Uses live SHARES_DATA from shares-data.js as the primary source.
 * Falls back gracefully if backend API is unavailable.
 */
document.addEventListener('DOMContentLoaded', () => {
  const ribbonContainer = document.getElementById('stock-ticker-ribbon');
  if (!ribbonContainer) return;

  function buildTicker(items) {
    if (!items || items.length === 0) {
      ribbonContainer.style.display = 'none';
      return;
    }

    // Duplicate items 3x for seamless infinite scroll
    const looped = [...items, ...items, ...items];

    const html = `<div class="ticker-track">
      ${looped.map(s => {
        const isUp = s.price >= (s.prevPrice || s.price);
        const chgPct = s.prevPrice
          ? (((s.price - s.prevPrice) / s.prevPrice) * 100).toFixed(2)
          : '0.00';
        const arrow = isUp ? '▲' : '▼';
        const cls   = isUp ? 'up' : 'down';
        const priceStr = s.price >= 1000
          ? '₹' + s.price.toLocaleString('en-IN')
          : '₹' + s.price;

        return `<div class="ticker-item">
          <span class="ticker-name">${s.shortName || s.name}</span>
          <span class="ticker-price">${priceStr}</span>
          <span class="ticker-chg ${cls}">${arrow} ${Math.abs(chgPct)}%</span>
        </div>`;
      }).join('')}
    </div>`;

    ribbonContainer.innerHTML = html;
    ribbonContainer.style.display = 'flex';
  }

  // ── Try SHARES_DATA first (always available, no API needed) ──
  function tryLoad() {
    const raw = window.SHARES_DATA || [];
    const stocks = raw.filter(s => s && s.price != null);

    if (stocks.length > 0) {
      buildTicker(stocks);
      return;
    }

    // Data not ready yet — try backend API
    const API_BASE = (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1')
      ? 'http://localhost:8000/api'
      : '/api';

    fetch(`${API_BASE}/stocks/ribbon`)
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if (data && data.items && data.items.length > 0) {
          buildTicker(data.items.map(i => ({
            shortName: i.symbol,
            price: i.price,
            prevPrice: i.price - (i.change || 0)
          })));
        } else {
          ribbonContainer.style.display = 'none';
        }
      })
      .catch(() => {
        ribbonContainer.style.display = 'none';
      });
  }

  // Small delay to ensure shares-data.js has been evaluated
  setTimeout(tryLoad, 100);
});
