import streamlit as st
import requests
import time

st.set_page_config(page_title="ArbSurfer", layout="wide")
st.title("🌊 ArbSurfer: Solana Arbitrage Monitor")

# Get prices
def get_orca_price():
    try:
        resp = requests.get("https://quote-api.jup.ag/v6/quote", params={
            "inputMint": "So11111111111111111111111111111111111111112",  # SOL
            "outputMint": "Es9vMFrzaCERFBn5gdB34dFpgdQT1D9pU8WWvWrtCPSb",  # USDT
            "amount": 10000000,
            "slippage": 1
        })
        data = resp.json()
        return float(data["outAmount"]) / 1e6
    except Exception as e:
        st.error(f"Orca error: {e}")
        return None

def get_raydium_price():
    try:
        data = requests.get("https://api.raydium.io/pairs").json()
        for pair in data:
            if pair["name"] == "SOL/USDT":
                return float(pair["price"])
        return None
    except Exception as e:
        st.error(f"Raydium error: {e}")
        return None

# Refresh every 30 seconds
placeholder = st.empty()
while True:
    with placeholder.container():
        orca = get_orca_price()
        raydium = get_raydium_price()

        if orca and raydium:
            spread = abs(orca - raydium)
            spread_pct = (spread / min(orca, raydium)) * 100

            st.subheader("Current Prices")
            st.metric(label="💧 Orca", value=f"${orca:.4f}")
            st.metric(label="🧪 Raydium", value=f"${raydium:.4f}")
            st.metric(label="📈 Spread %", value=f"{spread_pct:.2f}%")

            if spread_pct >= 0.1:
                st.success("🚨 Arbitrage opportunity detected!")
            else:
                st.warning("⏳ No opportunity above 0.1% right now.")
        else:
            st.error("⚠️ Unable to fetch one or both prices.")

        st.caption("Refreshing in 30s...")
    time.sleep(30)
    placeholder.empty()
