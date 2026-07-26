"""
FastAPI Server Entry Point.
Provides REST endpoints for frontend to fetch stock data (if not using static JSON).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.routes import stocks, assets

app = FastAPI(title="ASSET BOX - Stock API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stocks.router, prefix="/api/stocks", tags=["stocks"])
app.include_router(assets.router, prefix="/api/assets", tags=["assets"])

@app.get("/api/health", tags=["health"])
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
