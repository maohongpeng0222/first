#  streamlit run test.py

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class StockRequest(BaseModel):
    symbol: str

@app.post("/get_stock")
async def get_stock(data: StockRequest):
    # Here you might fetch real stock data, for simplicity returning a static response
    return {"symbol": data.symbol, "price": 100.0}



import streamlit as st
import requests

st.title('Stock Price App')

symbol = st.text_input("Enter Stock Symbol:", value="AAPL")

if st.button('Get Price'):
    response = requests.post("http://localhost:8502", json={"symbol": symbol})
    if response.status_code == 200:
        stock_data = response.json()
        st.write(f"The price of {stock_data['symbol']} is ${stock_data['price']}")
    else:
        st.write("Error fetching the stock price")
