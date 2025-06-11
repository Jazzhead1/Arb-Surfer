import streamlit as st
import ccxt
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# 🔧 Must be the very first Streamlit command!
st.set_page_config(page_title="ArbSurfer", layout="wide")

# 🔄 Auto-refresh every 30 seconds
st_autorefresh(interval=30_000, limit=None, key="arbsurferrefresh")

# 🎨 App Header
st.markdown("<h1 style='color:#00adb5;'>🌊 ArbSurfer — Real-Time Crypto Arbitrage Scanner</h1>", unsafe_allow_html=True)

# 🔌 Exchange setup
kraken = ccxt.kraken()
kucoin = ccxt.kucoin()

# 🔃 Load markets
try:
    kraken.load_markets()
except Exception as e:
    st.error(f"⚠️ Failed to load Kraken markets: {e}")

# 🧠 Handle Kraken BTC symbol differences
kraken_btc_pair = 'XBT/USDT' if 'XBT/USDT' in kraken.markets else None
if not kraken_btc_pair:
    st.warning("Kraken BTC pair (XBT/USDT) not available. Skipping BTC for Kraken.")

# 💱 Symbol map
symbol_map = {
    "BTC": {"Kraken": kraken_btc_pair, "KuCoin": "BTC/USDT"} if kraken_btc_pair else {"KuCoin": "BTC/USDT"},
    "ETH": {"Kraken": "ETH/USDT", "KuCoin": "ETH/USDT"},
    "SOL": {"Kraken": "SOL/USDT", "KuCoin": "SOL/USDT"},
    "XRP": {"Kraken": "XRP/USD", "KuCoin": "XRP/USDT"}
}

# 🏷️ Price fetcher
def fetch_price(exchange_obj, symbol):
    try:
        ticker = exchange_obj.fetch_ticker(symbol)
        return ticker['last']
    except Exception as e:
        st.error(f"❌ Error fetching {symbol} from {exchange_obj.id}: {e}")
        return None

# 🔍 Arbitrage logic and display
for asset, exchange_symbols in symbol_map.items():
    st.markdown(f"### 📈 {asset}")
    prices = {}
    for exchange_name, symbol in exchange_symbols.items():
        exchange_obj = kraken if exchange_name == "Kraken" else kucoin
        if symbol:
            price = fetch_price(exchange_obj, symbol)
            if price:
                prices[exchange_name] = price

    if len(prices) >= 2:
        df = pd.DataFrame(prices.items(), columns=["Exchange", "Price"]).sort_values(by="Price")
        st.dataframe(df, use_container_width=True)
        low = df.iloc[0]
        high = df.iloc[-1]
        spread = high["Price"] - low["Price"]
        profit_percent = (spread / low["Price"]) * 100
        st.success(f"💸 Buy on {low['Exchange']} at {low['Price']:.4f}, sell on {high['Exchange']} at {high['Price']:.4f} → Profit: {profit_percent:.2f}%")
    else:
        st.info(f"Not enough data for {asset} yet.")

# 🔁 Footer
st.caption("🔄 Auto-refreshes every 30 seconds — built with ❤️ by ArbSurfer.")
