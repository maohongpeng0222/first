from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


class StockRequest(BaseModel):
    symbol: str

@app.post("/get_stock")
async def get_stock(data: StockRequest):
    # Here you might fetch real stock data, for simplicity returning a static response
    return {"symbol": data.symbol, "price": 100.0}