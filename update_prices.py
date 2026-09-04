"""
╔══════════════════════════════════════════════════════════════════╗
║   MDB ARTHASPHERE — Daily Auto Price Updater                    ║
║   Fetches prices via API and updates Supabase automatically.     ║
║   Run via GitHub Actions or locally: python update_prices.py     ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import requests
from datetime import datetime

# ── Dependency check ───────────────────────────────────────────────
try:
    import psycopg2
except ImportError:
    print("[!] Missing psycopg2. Run: pip install psycopg2-binary")
    sys.exit(1)

# ── Config ─────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL', 
    "postgresql://postgres.zgctcrizcunvnioxjkyb:ELkb2B4-FGpS6Z3"
    "@aws-0-ap-southeast-2.pooler.supabase.com:5432/postgres")

ALPHA_VANTAGE_KEY = os.environ.get('ALPHA_VANTAGE_KEY', '2WLZ4OZBRRY3QT4U')

# Define which stocks we want to auto-update via Alpha Vantage
# Note: Alpha Vantage mainly tracks listed stocks (NSE/BSE/US). 
# For unlisted stocks, you typically use manual Excel uploads.
# This script demonstrates how to fetch APIs for any symbols you want to track.
SYMBOLS_TO_TRACK = ['RELIANCE.BSE', 'TCS.BSE', 'HDFCBANK.BSE'] 

def fetch_alpha_vantage_price(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_KEY}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        quote = data.get('Global Quote', {})
        if quote:
            return {
                'price': float(quote.get('05. price', 0)),
                'prev_close': float(quote.get('08. previous close', 0)),
                'change': float(quote.get('09. change', 0)),
                'change_percent': float(quote.get('10. change percent', '0%').replace('%','')),
                'volume': int(quote.get('06. volume', 0))
            }
    except Exception as e:
        print(f"Error fetching {symbol}: {e}")
    return None

def update_db(symbol, data):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # 1. Ensure company exists
        clean_sym = symbol.replace('.BSE', '').replace('.NSE', '')
        cur.execute("SELECT id FROM companies WHERE symbol = %s", (clean_sym,))
        row = cur.fetchone()
        
        if not row:
            cur.execute("""
                INSERT INTO companies (symbol, company_name, exchange) 
                VALUES (%s, %s, 'API') RETURNING id
            """, (clean_sym, clean_sym))
            c_id = cur.fetchone()[0]
        else:
            c_id = row[0]
            
        # 2. Update price
        cur.execute("""
            INSERT INTO stock_prices (company_id, price, prev_close, change, change_percent, volume, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id) DO UPDATE SET
                price = EXCLUDED.price,
                prev_close = EXCLUDED.prev_close,
                change = EXCLUDED.change,
                change_percent = EXCLUDED.change_percent,
                updated_at = EXCLUDED.updated_at
        """, (c_id, data['price'], data['prev_close'], data['change'], data['change_percent'], data['volume'], datetime.utcnow()))
        
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"DB Error for {symbol}: {e}")
        return False

def main():
    print(f"--- Starting Daily Auto-Update ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    success_count = 0
    
    for sym in SYMBOLS_TO_TRACK:
        print(f"Fetching {sym}...")
        data = fetch_alpha_vantage_price(sym)
        if data:
            print(f"  -> Price: ₹{data['price']}, Change: {data['change_percent']}%")
            if update_db(sym, data):
                success_count += 1
                print("  -> Saved to Supabase")
        else:
            print("  -> Failed to fetch.")
            
    print(f"--- Completed: {success_count}/{len(SYMBOLS_TO_TRACK)} updated ---")

if __name__ == '__main__':
    main()
