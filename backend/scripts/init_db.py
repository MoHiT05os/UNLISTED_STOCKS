"""
Initializes the database, creates tables, and runs the first-time master data sync.
Run this script once when setting up the project.
"""
import logging
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from db.database import init_db
from fetchers.nse_master import sync_nse_companies
from fetchers.security_map import sync_dhan_security_ids

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('init_db')

def main():
    logger.info("Step 1: Initializing Database...")
    init_db()
    
    logger.info("Step 2: Syncing NSE Master Data...")
    sync_nse_companies()
    
    logger.info("Step 3: Syncing Dhan Security IDs...")
    sync_dhan_security_ids()
    
    logger.info("Database initialization and master data sync complete!")
    logger.info("You can now run 'python scheduler/hourly_prices.py' to fetch initial prices.")

if __name__ == "__main__":
    main()
