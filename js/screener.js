document.addEventListener('DOMContentLoaded', async () => {
    const heatmapGrid = document.getElementById('heatmap-grid');
    const stocksTbody = document.getElementById('stocks-tbody');
    
    // Tab switching logic
    const tabs = document.querySelectorAll('.screener-tab');
    const panels = document.querySelectorAll('.screener-panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            tab.classList.add('active');
            const panelId = 'panel-' + tab.dataset.panel;
            document.getElementById(panelId).classList.add('active');
        });
    });

    try {
        const response = await fetch('data/ribbon.json');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        const items = data.items || [];
        
        // 1. Render Heatmap
        if (heatmapGrid) {
            let html = '';
            items.forEach(item => {
                const up = item.change >= 0;
                // Calculate opacity based on change percent (max 10% for full opacity)
                const opacity = Math.min(Math.abs(item.change_percent) / 10 + 0.2, 1);
                const bg = up ? `rgba(16, 185, 129, ${opacity})` : `rgba(239, 68, 68, ${opacity})`;
                
                html += `
                <a href="stock.html?symbol=${item.symbol}" class="heatmap-cell" style="background:${bg}; text-decoration:none;">
                    <div class="hm-symbol">${item.symbol}</div>
                    <div class="hm-pct">${item.change >= 0 ? '+' : ''}${item.change_percent.toFixed(2)}%</div>
                </a>`;
            });
            heatmapGrid.innerHTML = html;
        }

        // 2. Render Stocks Table
        if (stocksTbody) {
            let html = '';
            items.forEach(item => {
                const up = item.change >= 0;
                const cls = up ? 'green' : 'red';
                const arrow = up ? '▲' : '▼';
                
                html += `
                <tr style="cursor:pointer;" onclick="window.location.href='stock.html?symbol=${item.symbol}'">
                    <td><strong>${item.symbol}</strong><br><span style="font-size:11px; color:var(--text-muted);">Equity</span></td>
                    <td>₹${item.price}</td>
                    <td style="color:${up ? '#10b981' : '#ef4444'};">${arrow} ${Math.abs(item.change_percent).toFixed(2)}%</td>
                    <td>₹${(Math.random() * 50000).toFixed(0)} Cr</td>
                    <td>${(Math.random() * 50 + 10).toFixed(1)}</td>
                    <td><a href="stock.html?symbol=${item.symbol}" class="btn btn-ghost" style="padding:4px 12px; font-size:12px;">View</a></td>
                </tr>`;
            });
            stocksTbody.innerHTML = html;
        }
        
    } catch (error) {
        console.error('Error fetching data:', error);
    }
});
