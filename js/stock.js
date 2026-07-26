document.addEventListener('DOMContentLoaded', async () => {
    // 1. Get symbol from URL
    const urlParams = new URLSearchParams(window.location.search);
    const symbol = urlParams.get('symbol') || 'HDFCBANK';

    // Update UI placeholders
    document.getElementById('display-symbol').textContent = symbol;
    document.title = `${symbol} | ASSET BOX`;
    
    // Fetch data from backend
    try {
        const response = await fetch(`http://localhost:8000/api/stocks/quote/${symbol}`);
        if (!response.ok) throw new Error('Failed to fetch stock data');
        const data = await response.json();

        const isUp = data.change >= 0;
        const price = data.price.toFixed(2);
        const change = Math.abs(data.change).toFixed(2);
        const changePct = Math.abs(data.change_percent).toFixed(2);
        
        document.getElementById('display-name').textContent = data.name || symbol + ' Limited';
        document.getElementById('display-price').textContent = `₹${price}`;
        
        const changeEl = document.getElementById('display-change');
        changeEl.classList.add(isUp ? 'positive' : 'negative');
        changeEl.textContent = `${isUp ? '▲' : '▼'} ₹${change} (${changePct}%)`;
        
        document.getElementById('about-name').textContent = data.name || symbol;
        
        // Fill stats
        document.getElementById('stat-mcap').textContent = data.mcap || '₹' + (Math.random() * 500000).toFixed(0) + ' Cr';
        document.getElementById('stat-high').textContent = data.high_52w ? '₹' + data.high_52w : '₹' + (parseFloat(price) * 1.2).toFixed(2);
        document.getElementById('stat-low').textContent = data.low_52w ? '₹' + data.low_52w : '₹' + (parseFloat(price) * 0.8).toFixed(2);
        document.getElementById('stat-pe').textContent = data.pe || (Math.random() * 50 + 10).toFixed(2);
        
        window.stockCurrentPrice = parseFloat(price); // store for chart
    } catch (e) {
        console.error(e);
        // Fallback for UI visualization
        const isUp = Math.random() > 0.5;
        const price = (Math.random() * 2000 + 100).toFixed(2);
        window.stockCurrentPrice = parseFloat(price);
        document.getElementById('display-price').textContent = `₹${price}`;
    }

    // 2. Initialize TradingView Chart
    const chartProperties = {
        layout: {
            background: { type: 'solid', color: 'transparent' },
            textColor: '#94a3b8',
        },
        grid: {
            vertLines: { color: 'rgba(255,255,255,0.05)' },
            horzLines: { color: 'rgba(255,255,255,0.05)' },
        },
        crosshair: {
            mode: LightweightCharts.CrosshairMode.Normal,
        },
        rightPriceScale: {
            borderColor: 'rgba(255,255,255,0.1)',
        },
        timeScale: {
            borderColor: 'rgba(255,255,255,0.1)',
        }
    };

    const container = document.getElementById('tv-chart');
    const chart = LightweightCharts.createChart(container, chartProperties);
    
    // Make chart responsive
    new ResizeObserver(entries => {
        if (entries.length === 0 || entries[0].target !== container) return;
        const newRect = entries[0].contentRect;
        chart.applyOptions({ height: newRect.height, width: newRect.width });
    }).observe(container);

    const candleSeries = chart.addCandlestickSeries({
        upColor: '#10b981',
        downColor: '#ef4444',
        borderDownColor: '#ef4444',
        borderUpColor: '#10b981',
        wickDownColor: '#ef4444',
        wickUpColor: '#10b981',
    });

    // Generate mock historical data
    const generateData = () => {
        let res = [];
        let time = new Date('2023-01-01').getTime();
        let lastClose = parseFloat(price) * 0.8;
        
        for (let i = 0; i < 200; i++) {
            let open = lastClose + (Math.random() - 0.5) * 10;
            let close = open + (Math.random() - 0.5) * 20;
            let high = Math.max(open, close) + Math.random() * 10;
            let low = Math.min(open, close) - Math.random() * 10;
            
            res.push({
                time: time / 1000,
                open: open,
                high: high,
                low: low,
                close: close
            });
            
            time += 24 * 60 * 60 * 1000;
            lastClose = close;
        }
        return res;
    };

    candleSeries.setData(generateData());
    chart.timeScale().fitContent();
});
