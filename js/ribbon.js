/**
 * MDB ARTHASPHERE — Unlisted Stock Ticker Ribbon
 * Reads directly from window.SHARES_DATA (unlisted stocks only).
 * Speed is calculated dynamically based on actual track width — always ~60px/sec.
 */
document.addEventListener('DOMContentLoaded', () => {
  const ribbon = document.getElementById('stock-ticker-ribbon');
  if (!ribbon) return;

  // Target scroll speed in px/sec — comfortable reading pace
  const PX_PER_SEC = 60;
  // Show only a manageable subset so the track isn't absurdly long
  const MAX_ITEMS = 80;

  function buildTicker(stocks) {
    if (!stocks || stocks.length === 0) {
      ribbon.style.display = 'none';
      return;
    }

    // Limit to MAX_ITEMS for a reasonable track length
    const subset = stocks.slice(0, MAX_ITEMS);

    // Duplicate 2x for seamless infinite loop (not 3x — track is already long enough)
    const looped = [...subset, ...subset];

    ribbon.innerHTML = '<div class="ticker-track" id="ticker-track">' +
      looped.map(s => {
        const isUp = (s.change || 0) >= 0;
        const chgPct = s.changePct != null
          ? Math.abs(s.changePct).toFixed(2)
          : s.prevPrice && s.prevPrice !== s.price
            ? Math.abs(((s.price - s.prevPrice) / s.prevPrice) * 100).toFixed(2)
            : '0.00';
        const arrow = isUp ? '▲' : '▼';
        const cls   = isUp ? 'up' : 'down';
        const priceStr = '₹' + (s.price >= 1000
          ? s.price.toLocaleString('en-IN')
          : s.price);

        // Truncate name to keep items compact
        const name = (s.shortName || s.name || '').substring(0, 20);

        return '<div class="ticker-item">' +
          '<span class="ticker-name">' + name + '</span>' +
          '<span class="ticker-price">' + priceStr + '</span>' +
          '<span class="ticker-chg ' + cls + '">' + arrow + ' ' + chgPct + '%</span>' +
        '</div>';
      }).join('') +
    '</div>';

    ribbon.style.display = 'flex';

    // Calculate dynamic duration based on actual rendered track width
    requestAnimationFrame(() => {
      const track = document.getElementById('ticker-track');
      if (!track) return;

      // Half the track width (since we translateX(-50%) to loop seamlessly)
      const halfWidth = track.scrollWidth / 2;
      const durationSec = halfWidth / PX_PER_SEC;

      track.style.animationDuration = durationSec.toFixed(1) + 's';
    });
  }

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
