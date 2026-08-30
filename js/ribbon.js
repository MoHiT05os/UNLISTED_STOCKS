/**
 * MDB ARTHASPHERE — Unlisted Stock Ticker Ribbon
 * Reads directly from window.SHARES_DATA (unlisted stocks only).
 * No backend API call needed.
 */
document.addEventListener('DOMContentLoaded', () => {
  const ribbon = document.getElementById('stock-ticker-ribbon');
  if (!ribbon) return;

  function buildTicker(stocks) {
    if (!stocks || stocks.length === 0) {
      ribbon.style.display = 'none';
      return;
    }

    // Duplicate 3x for seamless infinite loop
    const looped = [...stocks, ...stocks, ...stocks];

    ribbon.innerHTML = '<div class="ticker-track">' +
      looped.map(s => {
        const isUp = s.price >= (s.prevPrice || s.price);
        const chgPct = s.prevPrice && s.prevPrice !== s.price
          ? Math.abs(((s.price - s.prevPrice) / s.prevPrice) * 100).toFixed(2)
          : '0.00';
        const arrow = isUp ? '▲' : '▼';
        const cls   = isUp ? 'up' : 'down';
        const priceStr = '₹' + (s.price >= 1000
          ? s.price.toLocaleString('en-IN')
          : s.price);

        return '<div class="ticker-item">' +
          '<span class="ticker-name">' + (s.shortName || s.name) + '</span>' +
          '<span class="ticker-price">' + priceStr + '</span>' +
          '<span class="ticker-chg ' + cls + '">' + arrow + ' ' + chgPct + '%</span>' +
        '</div>';
      }).join('') +
    '</div>';

    ribbon.style.display = 'flex';
  }

  // Wait for SHARES_DATA then render (no backend API)
  function tryLoad() {
    const raw = window.SHARES_DATA || [];
    const stocks = raw.filter(s => s && s.price != null && !isNaN(s.price));
    if (stocks.length > 0) {
      buildTicker(stocks);
    } else {
      ribbon.style.display = 'none';
    }
  }

  setTimeout(tryLoad, 150);
});
