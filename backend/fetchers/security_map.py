"""
Downloads the Dhan API Scrip Master and maps it to our local database.
This is necessary to get the `security_id` needed for Dhan API calls.
"""
import io
import logging
import zipfile
import requests
import pandas as pd

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import DHAN_SCRIP_MASTER_CSV
from db.database import get_session
from db.models import Company

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('security_map')


def sync_dhan_security_ids():
    """
    Downloads Dhan's master CSV and updates companies in the DB with their dhan_security_id.
    Matches primarily using ISIN, or Symbol fallback.
    """
    logger.info(f"Downloading Dhan Scrip Master from {DHAN_SCRIP_MASTER_CSV}...")
    
    try:
        response = requests.get(DHAN_SCRIP_MASTER_CSV, timeout=60)
        response.raise_for_status()
        
        # It's a CSV file
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content))
        
        logger.info(f"Downloaded {len(df)} records from Dhan.")
        
        # We only care about Equities (EQ) on NSE and BSE
        df_eq = df[df['SEM_SEGMENT'] == 'E'].copy()
        logger.info(f"Filtered to {len(df_eq)} Equity records.")
        
        mapped_nse = 0
        mapped_bse = 0
        
        with get_session() as session:
            # Create a lookup for faster matching
            # SEM_EXM_EXCH_ID: 'NSE' or 'BSE'
            # SEM_SMST_SECURITY_ID: The ID we need
            # SEM_TRADING_SYMBOL: The symbol
            # SEM_CUSTOM_SYMBOL: ISIN (usually) or a custom format
            
            for _, row in df_eq.iterrows():
                exchange = str(row.get('SEM_EXM_EXCH_ID', '')).strip()
                security_id = str(row.get('SEM_SMST_SECURITY_ID', '')).strip()
                symbol = str(row.get('SEM_TRADING_SYMBOL', '')).strip()
                custom_symbol = str(row.get('SEM_CUSTOM_SYMBOL', '')).strip()
                
                # In Dhan's master, SEM_CUSTOM_SYMBOL often looks like 'RELIANCE-EQ' or holds ISIN.
                # Since we want to map reliably, we'll try ISIN first (if available in a known column), 
                # otherwise we use the symbol. Note: Dhan CSV structure sometimes changes.
                
                # Try matching by symbol and exchange
                if exchange == 'NSE':
                    company = session.query(Company).filter_by(symbol=symbol, exchange='NSE').first()
                    if company:
                        company.dhan_nse_security_id = security_id
                        mapped_nse += 1
                elif exchange == 'BSE':
                    # BSE symbols might have group suffixes, etc. We try direct match.
                    company = session.query(Company).filter_by(symbol=symbol).first()
                    if company:
                        company.dhan_bse_security_id = security_id
                        mapped_bse += 1
                        
        logger.info(f"Dhan ID Mapping complete! Mapped NSE: {mapped_nse}, BSE: {mapped_bse}")
        
    except Exception as e:
        logger.error(f"Failed to process Dhan scrip master: {e}")


if __name__ == "__main__":
    sync_dhan_security_ids()
