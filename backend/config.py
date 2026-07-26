"""
Configuration loader for the backend.
Reads .env file and provides settings to all modules.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend directory
ENV_PATH = Path(__file__).parent / '.env'
load_dotenv(ENV_PATH)

# ── Dhan API ──────────────────────────────────────────────
DHAN_CLIENT_ID = os.getenv('DHAN_CLIENT_ID', '')
DHAN_ACCESS_TOKEN = os.getenv('DHAN_ACCESS_TOKEN', '')

# ── Database ──────────────────────────────────────────────
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./stocks.db')

# ── Scheduler ─────────────────────────────────────────────
UPDATE_INTERVAL_MINUTES = int(os.getenv('UPDATE_INTERVAL_MINUTES', '60'))
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '100'))
RATE_LIMIT_DELAY = float(os.getenv('RATE_LIMIT_DELAY', '0.5'))

# ── Paths ─────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR.parent / 'data'
DB_PATH = BASE_DIR / 'stocks.db'

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# ── NSE/BSE Master CSV URLs ──────────────────────────────
NSE_EQUITY_CSV = 'https://nsearchives.nseindia.com/content/equities/EQUITY_L.csv'
NSE_SME_CSV = 'https://nsearchives.nseindia.com/content/equities/SME_EQUITY_L.csv'
DHAN_SCRIP_MASTER_CSV = 'https://images.dhan.co/api-data/api-scrip-master.csv'

# ── Request Headers (NSE blocks requests without User-Agent) ─
NSE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}
