from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from db.database import get_db
from db.models import Company, StockPrice

router = APIRouter()

def get_base_stock_dict(company: Company, sp: StockPrice) -> Dict[str, Any]:
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
    }

@router.get("/ribbon")
def get_ribbon_data():
    """Returns mock top gainers and losers for the scrolling ticker ribbon."""
    import json
    import os
    
    # Try to read from frontend data if available
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "..", "data", "ribbon.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            return json.load(f)
            
    return {
        "items": [
            {"symbol": "RELIANCE", "name": "Reliance Industries", "price": 2450.50, "change": 45.20, "change_percent": 1.88},
            {"symbol": "TCS", "name": "Tata Consultancy", "price": 3400.10, "change": -20.50, "change_percent": -0.60},
            {"symbol": "INFY", "name": "Infosys Ltd", "price": 1420.00, "change": 15.00, "change_percent": 1.07},
            {"symbol": "HDFCBANK", "name": "HDFC Bank", "price": 1650.75, "change": -10.25, "change_percent": -0.62},
            {"symbol": "ICICIBANK", "name": "ICICI Bank", "price": 950.25, "change": 25.50, "change_percent": 2.76},
            {"symbol": "SBI", "name": "State Bank of India", "price": 580.40, "change": 12.10, "change_percent": 2.13},
            {"symbol": "HUL", "name": "Hindustan Unilever", "price": 2540.00, "change": -5.50, "change_percent": -0.22},
            {"symbol": "ITC", "name": "ITC Ltd", "price": 450.80, "change": 8.40, "change_percent": 1.90},
            {"symbol": "L&T", "name": "Larsen & Toubro", "price": 2890.30, "change": 40.10, "change_percent": 1.41},
            {"symbol": "BAJFINANCE", "name": "Bajaj Finance", "price": 7200.50, "change": -150.00, "change_percent": -2.04}
        ]
    }

# from api.dhan_client import get_realtime_quote

@router.get("/quote/{symbol}")
def get_quote(symbol: str):
    import random
    
    # Simple mock data based on symbol
    price = 100 + random.random() * 2000
    change = (random.random() - 0.5) * 50
    change_pct = (change / price) * 100
    
    return {
        "symbol": symbol,
        "name": symbol + " Ltd",
        "price": price,
        "change": change,
        "change_percent": change_pct,
        "high_52w": price * 1.2,
        "low_52w": price * 0.8,
        "mcap": str(int(price * 15.3)) + " Cr",
        "pe": round(random.random() * 30 + 10, 2)
    }
