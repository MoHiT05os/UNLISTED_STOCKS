/**
 * ASSET BOX — Live Market Data Engine
 * Powers the ticker ribbon + the Market Movers green/red grid.
 * Fetches data/ribbon.json and splits items into gainers (green) & losers (red).
 */
document.addEventListener('DOMContentLoaded', () => {
    const ribbonContainer  = document.getElementById('stock-ticker-ribbon');
    const moversSection    = document.getElementById('market-movers');
    const moversGrid       = document.getElementById('movers-grid');

    let allItems = [];

    const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 'http://localhost:8000/api' : '/api';

    // ─── Data Fetch ────────────────────────────────────────────
    async function fetchRibbonData() {
        try {
            const response = await fetch(`${API_BASE}/stocks/ribbon`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            allItems = data.items || [];
            renderRibbon(allItems);
            renderMovers('gainers');
            setupTabs();
        } catch (error) {
            console.error('Error fetching ribbon data:', error);
            if (ribbonContainer) ribbonContainer.style.display = 'none';
        }
    }

    // ─── 1. Scrolling Ticker Ribbon ────────────────────────────
    function renderRibbon(items) {
        if (!ribbonContainer || !items || items.length === 0) return;

        let html = '<div class="ticker-content">';
        // Duplicate 4× for seamless marquee loop
        const display = [...items, ...items, ...items, ...items];

        display.forEach(item => {
            const up   = item.change >= 0;
            const cls  = up ? 'green' : 'red';
            const arrow = up ? '▲' : '▼';

            html += `
                <div class="modern-pill">
                    <div class="pill-dot ${cls}"></div>
                    <span class="pill-symbol">${item.symbol}</span>
                    <span class="pill-price">₹${item.price}</span>
                    <span class="pill-change text-${cls}">${arrow} ${Math.abs(item.change_percent).toFixed(2)}%</span>
                </div>`;
        });

        html += '</div>';
        ribbonContainer.innerHTML = html;
        ribbonContainer.style.display = 'flex';
    }

    // ─── 2. Market Movers Grid (green/red cards) ───────────────
    function renderMovers(filter) {
        if (!moversGrid || allItems.length === 0) return;

        const sorted = [...allItems].sort((a, b) => {
            return filter === 'gainers'
                ? b.change_percent - a.change_percent
                : a.change_percent - b.change_percent;
        });

        const filtered = filter === 'gainers'
            ? sorted.filter(i => i.change >= 0).slice(0, 12)
            : sorted.filter(i => i.change < 0).slice(0, 12);

        if (filtered.length === 0) {
            moversGrid.innerHTML = '<p style="color:var(--text-muted); text-align:center; grid-column:1/-1;">No data available.</p>';
            if (moversSection) moversSection.style.display = 'block';
            return;
        }

        const type = filter === 'gainers' ? 'gainer' : 'loser';

        moversGrid.innerHTML = filtered.map(item => {
            const arrow = item.change >= 0 ? '▲' : '▼';
            const barWidth = Math.min(Math.abs(item.change_percent) * 10, 100);
            return `
            <a href="stock.html?symbol=${item.symbol}" class="mover-card ${type}" style="text-decoration:none; display:block;">
                <div class="mover-card-top">
                    <span class="mover-card-symbol">${item.symbol}</span>
                    <span class="mover-card-badge">${arrow} ${Math.abs(item.change_percent).toFixed(2)}%</span>
                </div>
                <div class="mover-card-price">₹${item.price}</div>
                <div class="mover-card-change">${arrow} ₹${Math.abs(item.change).toFixed(2)}</div>
                <div class="mover-card-bar" style="width:${barWidth}%"></div>
            </a>`;
        }).join('');

        if (moversSection) moversSection.style.display = 'block';
    }

    // ─── 3. Tab Switching ──────────────────────────────────────
    function setupTabs() {
        const tabs = document.querySelectorAll('.mover-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', () => {
                tabs.forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
                const filter = tab.dataset.filter;
                renderMovers(filter);
            });
        });
    }

    // ─── Init ──────────────────────────────────────────────────
    fetchRibbonData();
    setInterval(fetchRibbonData, 300000); // refresh every 5 min
});
