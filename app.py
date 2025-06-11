import streamlit as st
import ccxt
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Optional auto-refresh every 30 sec
st_autorefresh(interval=30 * 1000, key="data_refresh")

st.set_page_config(page_title="ArbSurfer", layout="wide")
st.title("🌊 ArbSurfer — Crypto Arbitrage Scanner")

kraken = ccxt.kraken()
kucoin = ccxt.kucoin()

kraken.load_markets()
kucoin.load_markets()

symbol_map = {
    "BTC": {"Kraken": "BTC/USD", "KuCoin": "BTC/USDT"},
    "ETH": {"Kraken": "ETH/USDT", "KuCoin": "ETH/USDT"},
    "SOL": {"Kraken": "SOL/USDT", "KuCoin": "SOL/USDT"},
    "XRP": {"Kraken": "XRP/USD", "KuCoin": "XRP/USDT"}
}

def fetch_price(exchange_obj, symbol):
    try:
        ticker = exchange_obj.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        st.error(f"{exchange_obj.id} error for {symbol}: {e}")
        return None

for asset, exchange_symbols in symbol_map.items():
    st.subheader(f"📈 {asset} Arbitrage")
    prices = {}
    for name, obj in {"Kraken": kraken, "KuCoin": kucoin}.items():
        symbol = exchange_symbols.get(name)
        price = fetch_price(obj, symbol)
        if price:
            prices[name] = price
    if len(prices) >= 2:
        df = pd.DataFrame(prices.items(), columns=["Exchange", "Price"]).sort_values("Price")
        st.dataframe(df)
        low = df.iloc[0]
        high = df.iloc[-1]
        spread = high["Price"] - low["Price"]
        profit_pct = (spread / low["Price"]) * 100
        st.success(f"Buy on {low['Exchange']} → Sell on {high['Exchange']} | 💰 Profit: {profit_pct:.2f}%")
    else:
        st.warning(f"Not enough data for {asset}")
