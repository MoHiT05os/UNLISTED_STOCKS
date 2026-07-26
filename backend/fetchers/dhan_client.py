"""
Dhan API Client wrapper.
Uses the official dhanhq library to interact with the Trading API for market data.
"""
import time
import logging
from typing import List, Dict, Any, Tuple
from dhanhq import dhanhq

from dhanhq.dhan_context import DhanContext

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import DHAN_CLIENT_ID, DHAN_ACCESS_TOKEN, BATCH_SIZE, RATE_LIMIT_DELAY

# Setup logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger('dhan_client')

class DhanDataClient:
    def __init__(self):
        if not DHAN_CLIENT_ID or not DHAN_ACCESS_TOKEN:
            logger.warning("Dhan API credentials missing. API calls will fail.")
        
        context = DhanContext(
            client_id=DHAN_CLIENT_ID,
            access_token=DHAN_ACCESS_TOKEN
        )
        self.dhan = dhanhq(context)

    def test_connection(self) -> bool:
        """Test if the credentials are valid by fetching fund limits."""
        try:
            response = self.dhan.get_fund_limits()
            if isinstance(response, dict) and response.get('status') == 'success':
                logger.info("Dhan API connection successful!")
                return True
            else:
                logger.error(f"Dhan API test failed: {response}")
                return False
        except Exception as e:
            logger.error(f"Dhan API connection error: {e}")
            return False

    def _chunk_list(self, lst: List, n: int):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def get_ltp_bulk(self, instruments: List[Tuple[str, str]]) -> Dict[str, float]:
        """
        Fetch Last Traded Price (LTP) for a list of instruments.
        instruments: List of tuples (exchange_segment, security_id)
                     Example: [("NSE_EQ", "1333"), ("BSE_EQ", "532540")]
        Returns a dictionary mapping security_id -> LTP.
        """
        results = {}
        
        # Dhan API has limits on the number of instruments per request (often 100 or 500).
        # We batch them and add a small delay to avoid rate limits.
        for i, chunk in enumerate(self._chunk_list(instruments, BATCH_SIZE)):
            logger.info(f"Fetching LTP for batch {i+1} ({len(chunk)} instruments)...")
            try:
                # Dhan API expects a dictionary formatted appropriately, or the Python wrapper 
                # might expect a list of dictionaries. The exact format depends on the version.
                # Standard dhanhq format for get_ltp:
                
                # dict_keys(['status', 'remarks', 'data']) -> data is a dict with exchange: {sec_id: ltp}
                req_dict = {}
                for exch, sec_id in chunk:
                    if exch not in req_dict:
                        req_dict[exch] = []
                    req_dict[exch].append(sec_id)
                
                response = self.dhan.ticker_data(req_dict)
                
                if response.get('status') == 'success' and 'data' in response:
                    for exch, data_dict in response['data'].items():
                        for sec_id, ltp in data_dict.items():
                            results[sec_id] = float(ltp)
                else:
                    logger.warning(f"Batch {i+1} failed: {response.get('remarks')}")
                
            except Exception as e:
                logger.error(f"Error fetching batch {i+1}: {e}")
                
            # Rate limiting pause
            time.sleep(RATE_LIMIT_DELAY)
            
        return results

    def get_ohlc_bulk(self, instruments: List[Tuple[str, str]]) -> Dict[str, Dict[str, float]]:
        """
        Fetch OHLC (Open, High, Low, Close) for a list of instruments.
        Returns a dictionary mapping security_id -> {open, high, low, close}.
        """
        results = {}
        for i, chunk in enumerate(self._chunk_list(instruments, BATCH_SIZE)):
            logger.info(f"Fetching OHLC for batch {i+1} ({len(chunk)} instruments)...")
            try:
                req_dict = {}
                for exch, sec_id in chunk:
                    if exch not in req_dict:
                        req_dict[exch] = []
                    req_dict[exch].append(sec_id)
                
                response = self.dhan.ohlc_data(req_dict)
                
                if response.get('status') == 'success' and 'data' in response:
                    for exch, data_dict in response['data'].items():
                        for sec_id, ohlc_data in data_dict.items():
                            results[sec_id] = {
                                'open': float(ohlc_data.get('open', 0)),
                                'high': float(ohlc_data.get('high', 0)),
                                'low': float(ohlc_data.get('low', 0)),
                                'close': float(ohlc_data.get('close', 0)), # This acts as prev_close for the day
                                'price': float(ohlc_data.get('ltp', ohlc_data.get('close', 0))) # Often includes LTP
                            }
                else:
                    logger.warning(f"Batch {i+1} failed: {response.get('remarks')}")
                    
            except Exception as e:
                logger.error(f"Error fetching OHLC batch {i+1}: {e}")
                
            time.sleep(RATE_LIMIT_DELAY)
            
        return results

if __name__ == "__main__":
    # Simple test
    client = DhanDataClient()
    client.test_connection()
