"""
Exports data from SQLite database to static JSON files.
This enables the frontend to run purely statically without a live backend server.
"""
import json
import logging
from datetime import datetime
from typing import List, Dict, Any

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import DATA_DIR
from db.database import get_session
from db.models import Company, StockPrice

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('export_json')

def get_base_stock_dict(company: Company, sp: StockPrice) -> Dict[str, Any]:
    """Format a company and stock price into a frontend-friendly dict."""
    return {
        "id": company.id,
        "symbol": company.symbol,
        "name": company.company_name,
        "exchange": company.exchange,
        "sector": company.sector,
        "price": round(sp.price, 2) if sp and sp.price else 0,
        "change": round(sp.change, 2) if sp and sp.change else 0,
        "change_percent": round(sp.change_percent, 2) if sp and sp.change_percent else 0,
        "prev_close": round(sp.prev_close, 2) if sp and sp.prev_close else 0,
        "updated_at": sp.updated_at.isoformat() if sp and sp.updated_at else datetime.utcnow().isoformat()
    }

def export_ribbon_data():
    """Export top movers (gainers and losers) for the scrolling ticker ribbon."""
    logger.info("Exporting ribbon data...")
    with get_session() as session:
        # Get top 25 gainers
        gainers = session.query(Company, StockPrice).\
            join(StockPrice).\
            filter(StockPrice.price > 10).\
            order_by(StockPrice.change_percent.desc()).\
            limit(25).all()
            
        # Get top 25 losers
        losers = session.query(Company, StockPrice).\
            join(StockPrice).\
            filter(StockPrice.price > 10).\
            order_by(StockPrice.change_percent.asc()).\
            limit(25).all()
            
        ribbon_items = []
        for c, sp in gainers:
            ribbon_items.append(get_base_stock_dict(c, sp))
            
        for c, sp in losers:
            ribbon_items.append(get_base_stock_dict(c, sp))
            
        # Shuffle or interleave them if desired, for now just combine
        
        output_file = DATA_DIR / 'ribbon.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                "last_updated": datetime.utcnow().isoformat(),
                "items": ribbon_items
            }, f, indent=2)
            
    logger.info(f"Exported {len(ribbon_items)} items to ribbon.json")

def export_companies():
    """Export all companies for search indexing."""
    logger.info("Exporting all companies...")
    with get_session() as session:
        companies = session.query(Company).all()
        
        results = []
        for c in companies:
            results.append({
                "id": c.id,
                "symbol": c.symbol,
                "name": c.company_name,
                "exchange": c.exchange
            })
            
        output_file = DATA_DIR / 'companies.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
            
    logger.info(f"Exported {len(results)} companies to companies.json")

def export_all():
    """Run all JSON exports."""
    DATA_DIR.mkdir(exist_ok=True)
    export_ribbon_data()
    export_companies()
    
    # Write global last_updated
    with open(DATA_DIR / 'meta.json', 'w', encoding='utf-8') as f:
        json.dump({"last_updated": datetime.utcnow().isoformat()}, f)

if __name__ == "__main__":
    export_all()
