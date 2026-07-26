from dhanhq import dhanhq
from config import DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN
import datetime

dhan = dhanhq({"client_id": DHAN_CLIENT_ID, "access_token": DHAN_ACCESS_TOKEN})

def get_realtime_quote(symbol: str, exchange: str = "NSE"):
    """
    Since we don't have security_id mapped yet in our DB, we'll return a mock response for now, 
    but in a real implementation we would fetch security_id from the scrip master.
    """
    # For now, we will mock the return to let the frontend work. 
    # Real implementation needs dhan.get_market_quote() which requires a list of dicts: {exchange, security_id}
    # Example: return dhan.get_market_quote({"exchange_segment": "NSE_EQ", "security_id": "1333"})
    return {
        "symbol": symbol,
        "price": 1500.25,
        "change": 12.50,
        "change_percent": 0.84,
        "exchange": exchange,
        "mcap": "₹1,25,000 Cr",
        "high_52w": 1600.00,
        "low_52w": 1300.00,
        "pe": 24.5
    }

def get_historical_data(symbol: str, exchange: str = "NSE"):
    # Mock data for charts
    return []
