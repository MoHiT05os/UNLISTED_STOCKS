"""
Fetches hourly price updates from Yahoo Finance and stores them in the database.
Also triggers JSON export for the static frontend.
"""
import logging
import time
from datetime import datetime
import argparse
import yfinance as yf

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db.database import get_session
from db.models import Company, StockPrice

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('hourly_prices')

# Popular NSE symbols for the ticker ribbon
POPULAR_SYMBOLS = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "BHARTIARTL", 
    "SBIN", "INFY", "LICI", "ITC", "HINDUNILVR", 
    "LT", "BAJFINANCE", "HCLTECH", "MARUTI", "SUNPHARMA",
    "ADANIENT", "KOTAKBANK", "TITAN", "ONGC", "TATAMOTORS",
    "NTPC", "AXISBANK", "DMART", "POWERGRID", "ULTRACEMCO",
    "ASIANPAINT", "COALINDIA", "BAJAJFINSV", "BAJAJ-AUTO", "M&M",
    "HAL", "DLF", "ADANIPORTS", "WIPRO", "NESTLEIND",
    "IOC", "TATASTEEL", "ZOMATO", "GRASIM", "TECHM",
    "SBILIFE", "HINDALCO", "INDUSINDBK", "GODREJCP", "HDFCLIFE",
    "DRREDDY", "BRITANNIA", "CIPLA", "APOLLOHOSP", "EICHERMOT"
]

def run_price_update():
    """Fetch prices for popular companies and update database."""
    logger.info("Starting hourly price update using yfinance...")
    
    with get_session() as session:
        # Get company records for popular symbols
        companies = session.query(Company).filter(
            Company.symbol.in_(POPULAR_SYMBOLS),
            Company.exchange == 'NSE'
        ).all()
        
        if not companies:
            logger.warning("No companies found matching popular symbols. Ensure init_db was run.")
            return
            
        logger.info(f"Found {len(companies)} matching companies in DB.")
        
        company_map = {c.symbol: c for c in companies}
        yf_symbols = [f"{sym}.NS" for sym in POPULAR_SYMBOLS]
        
        logger.info("Downloading data from Yahoo Finance...")
        # Download 2 days of data to get today's and yesterday's close (for prev close)
        data = yf.download(yf_symbols, period="2d", group_by="ticker", threads=True, progress=False)
        
        updated_count = 0
        added_count = 0
        
        for symbol in POPULAR_SYMBOLS:
            yf_sym = f"{symbol}.NS"
            if yf_sym not in data or data[yf_sym].empty:
                continue
                
            df = data[yf_sym]
            if len(df) == 0:
                continue
                
            # Latest day
            latest = df.iloc[-1]
            price = float(latest['Close'].iloc[0] if isinstance(latest['Close'], pd.Series) else latest['Close'])
            
            # Previous close (if we have 2 days)
            prev_close = price
            if len(df) > 1:
                prev = df.iloc[-2]
                prev_close = float(prev['Close'].iloc[0] if isinstance(prev['Close'], pd.Series) else prev['Close'])
                
            open_price = float(latest['Open'].iloc[0] if isinstance(latest['Open'], pd.Series) else latest['Open'])
            high = float(latest['High'].iloc[0] if isinstance(latest['High'], pd.Series) else latest['High'])
            low = float(latest['Low'].iloc[0] if isinstance(latest['Low'], pd.Series) else latest['Low'])
            
            change = price - prev_close
            change_percent = (change / prev_close * 100) if prev_close else 0
            
            company = company_map.get(symbol)
            if not company:
                continue
                
            # Upsert StockPrice
            stock_price = session.query(StockPrice).filter_by(company_id=company.id).first()
            if stock_price:
                stock_price.price = price
                stock_price.open = open_price
                stock_price.high = high
                stock_price.low = low
                stock_price.prev_close = prev_close
                stock_price.change = change
                stock_price.change_percent = change_percent
                updated_count += 1
            else:
                stock_price = StockPrice(
                    company_id=company.id,
                    price=price,
                    open=open_price,
                    high=high,
                    low=low,
                    prev_close=prev_close,
                    change=change,
                    change_percent=change_percent
                )
                session.add(stock_price)
                added_count += 1
                
        logger.info(f"Price update complete! Added: {added_count}, Updated: {updated_count}")
        
    # Trigger JSON export after update
    try:
        from scripts.export_json import export_all
        logger.info("Exporting updated JSON files for frontend...")
        export_all()
    except Exception as e:
        logger.error(f"Failed to export JSON: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update stock prices from yfinance')
    parser.add_argument('--test', action='store_true', help='Ignored for yfinance')
    parser.add_argument('--limit', type=int, default=None, help='Ignored for yfinance')
    args = parser.parse_args()
    
    # Needs pandas for type checking
    import pandas as pd
    
    run_price_update()
