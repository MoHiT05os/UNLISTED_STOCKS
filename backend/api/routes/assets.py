from fastapi import APIRouter
import random

router = APIRouter()

def generate_mock_data(prefix: str, count: int = 15, is_yield: bool = False):
    items = []
    for i in range(1, count + 1):
        if is_yield:
            # Yields don't have large price changes, they have small bps changes
            price = round(5.0 + random.random() * 4.0, 2) # Yield %
            change = (random.random() - 0.5) * 0.1
            change_percent = (change / price) * 100
            items.append({
                "symbol": f"{prefix}{i}",
                "name": f"{prefix} Bond {i}Y",
                "price": price,
                "change": round(change, 4),
                "change_percent": round(change_percent, 2),
                "volume": int(random.random() * 10000)
            })
        else:
            price = round(100 + random.random() * 500, 2)
            change = (random.random() - 0.5) * 10
            change_percent = (change / price) * 100
            items.append({
                "symbol": f"{prefix}{i}",
                "name": f"{prefix} Asset {i}",
                "price": price,
                "change": round(change, 2),
                "change_percent": round(change_percent, 2),
                "volume": int(random.random() * 500000)
            })
    return {"items": items}

@router.get("/futures")
def get_futures():
    return generate_mock_data("NIFTY_FUT_")

@router.get("/govt_bonds")
def get_govt_bonds():
    return generate_mock_data("GSEC_", is_yield=True)

@router.get("/corp_bonds")
def get_corp_bonds():
    return generate_mock_data("CORP_", is_yield=True)

@router.get("/etfs")
def get_etfs():
    return generate_mock_data("ETF_")
