"""
Fetches and parses the official NSE master CSV files to populate the database.
"""
import io
import logging
import requests
import pandas as pd
from datetime import datetime

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import NSE_EQUITY_CSV, NSE_SME_CSV, NSE_HEADERS
from db.database import get_session
from db.models import Company

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('nse_master')


def download_csv(url: str) -> pd.DataFrame:
    """Download a CSV from NSE and return it as a pandas DataFrame."""
    logger.info(f"Downloading from {url}...")
    try:
        response = requests.get(url, headers=NSE_HEADERS, timeout=30)
        response.raise_for_status()
        
        # Parse CSV content
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content))
        
        # Clean column names (strip whitespace)
        df.columns = df.columns.str.strip()
        
        logger.info(f"Downloaded {len(df)} records.")
        return df
    except Exception as e:
        logger.error(f"Failed to download {url}: {e}")
        return pd.DataFrame()


def sync_nse_companies():
    """Download mainboard and SME files and upsert into the companies table."""
    logger.info("Starting NSE company sync...")
    
    df_main = download_csv(NSE_EQUITY_CSV)
    df_sme = download_csv(NSE_SME_CSV)
    
    if df_main.empty and df_sme.empty:
        logger.error("No data downloaded. Aborting sync.")
        return

    # Combine dataframes
    frames = []
    if not df_main.empty:
        df_main['IS_SME'] = False
        frames.append(df_main)
    if not df_sme.empty:
        df_sme['IS_SME'] = True
        frames.append(df_sme)
        
    df_all = pd.concat(frames, ignore_index=True)
    
    # Expected columns: SYMBOL, NAME OF COMPANY, SERIES, DATE OF LISTING, PAID UP VALUE, MARKET LOT, ISIN NUMBER, FACE VALUE
    
    added = 0
    updated = 0
    
    with get_session() as session:
        for _, row in df_all.iterrows():
            symbol = str(row.get('SYMBOL', '')).strip()
            if not symbol:
                continue
                
            isin = str(row.get('ISIN NUMBER', '')).strip()
            name = str(row.get('NAME OF COMPANY', '')).strip()
            series = str(row.get('SERIES', '')).strip()
            
            # Parse listing date if available
            listing_date = None
            date_str = str(row.get('DATE OF LISTING', ''))
            if date_str and date_str.lower() != 'nan':
                try:
                    # Usually DD-MMM-YYYY format
                    listing_date = datetime.strptime(date_str, '%d-%b-%Y').date()
                except ValueError:
                    pass

            # Check if company already exists by ISIN or Symbol
            company = None
            if isin:
                company = session.query(Company).filter_by(isin=isin).first()
            if not company:
                company = session.query(Company).filter_by(symbol=symbol, exchange='NSE').first()
                
            if company:
                # Update existing
                company.company_name = name
                company.symbol = symbol # Update symbol in case it changed but ISIN remained
                company.series = series
                if listing_date:
                    company.listing_date = listing_date
                updated += 1
            else:
                # Create new
                company = Company(
                    symbol=symbol,
                    company_name=name,
                    isin=isin if isin else None,
                    exchange='NSE',
                    series=series,
                    listing_date=listing_date,
                    face_value=float(row.get('FACE VALUE', 0)) if pd.notna(row.get('FACE VALUE')) else None,
                    paid_up_value=float(row.get('PAID UP VALUE', 0)) if pd.notna(row.get('PAID UP VALUE')) else None
                )
                session.add(company)
                added += 1
                
    logger.info(f"NSE Sync complete! Added: {added}, Updated: {updated}")


if __name__ == "__main__":
    sync_nse_companies()
