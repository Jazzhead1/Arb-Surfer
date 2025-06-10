import streamlit as st
import ccxt
import pandas as pd
import time

# --- Styled Title ---
st.markdown(
    "<h1 style='text-align: center; color: #00BFFF;'>🌊 ArbSurfer: Ride the Crypto Waves</h1>",
    unsafe_allow_html=True
)

# --- Sleek UI CSS Styling ---
st.markdown(
    """
    <style>
        .stDataFrame {
            border: 1px solid #00BFFF;
            border-radius: 10px;
            overflow: hidden;
        }
        .stButton>button {
            background-color: #00BFFF;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            padding: 8px 16px;
        }
        .block-container {
            padding-top: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Initialize Exchanges ---
kraken = ccxt.kraken()
kucoin = ccxt.kucoin()

kraken.load_markets()
kucoin.load_markets()

symbol_map = {
    "BTC": {"Kraken": "XBT/USD", "KuCoin": "BTC/USDT"},
    "ETH": {"Kraken": "ETH/USDT", "KuCoin": "ETH/USDT"},
    "SOL": {"Kraken": "SOL/USDT", "KuCoin": "SOL/USDT"},
    "XRP": {"Kraken": "XRP/USD", "KuCoin": "XRP/USDT"}
}

def fetch_price(exchange_obj, symbol):
    if symbol == "XBT/USDT":
        st.warning(f"Skipping unsupported pair: {symbol}")
        return None
    try:
        ticker = exchange_obj.fetch_ticker(symbol)
        st.write(f"✅ Fetched {symbol} from {exchange_obj.id}: {ticker['last']}")
        return ticker['last']
    except Exception as e:
        st.error(f"❌ Error fetching {symbol} from {exchange_obj.id}: {e}")
        return None

while True:
    for asset, exchange_symbols in symbol_map.items():
        st.subheader(f"📊 Prices for {asset}")
        prices = {}
        for exchange_name, exchange_obj in {"Kraken": kraken, "KuCoin": kucoin}.items():
            symbol = exchange_symbols.get(exchange_name)
            if symbol:
                price = fetch_price(exchange_obj, symbol)
                if price:
                    prices[exchange_name] = price
        if len(prices) >= 2:
            df = pd.DataFrame(prices.items(), columns=["Exchange", "Price"]).sort_values(by="Price")
            st.dataframe(df)
            low = df.iloc[0]
            high = df.iloc[-1]
            spread = high["Price"] - low["Price"]
            profit_percent = (spread / low["Price"]) * 100
            st.success(f"💸 Buy on {low['Exchange']} at {low['Price']:.4f}, Sell on {high['Exchange']} at {high['Price']:.4f} → Profit: {profit_percent:.2f}%")
        else:
            st.warning(f"⚠️ Not enough data for {asset}")
    st.info("🔄 Refreshing in 30 seconds...")
    time.sleep(30)
    st.experimental_rerun()
