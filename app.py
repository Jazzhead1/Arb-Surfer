import streamlit as st
import requests

st.set_page_config(page_title="ArbSurfer", layout="wide")
st.title("🌊 ArbSurfer: Solana Arbitrage Monitor")

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
        st.error(f"❌ Orca error: {e}")
        return None

def get_raydium_price():
    try:
        data = requests.get("https://api.raydium.io/pairs").json()
        for pair in data:
            if pair["name"] == "SOL/USDT":
                return float(pair["price"])
        return None
    except Exception as e:
        st.error(f"❌ Raydium error: {e}")
        return None

if st.button("🔄 Refresh Prices"):
    st.experimental_rerun()

orca_price = get_orca_price()
raydium_price = get_raydium_price()

if orca_price and raydium_price:
    spread = abs(orca_price - raydium_price)
    spread_pct = (spread / min(orca_price, raydium_price)) * 100

    st.subheader("💱 Prices")
    col1, col2, col3 = st.columns(3)
    col1.metric("💧 Orca", f"${orca_price:.4f}")
    col2.metric("🧪 Raydium", f"${raydium_price:.4f}")
    col3.metric("📈 Spread", f"{spread_pct:.2f}%")

    if spread_pct >= 0.1:
        st.success("🚨 Arbitrage opportunity detected!")
    else:
        st.info("⏳ No significant arbitrage at the moment.")
else:
    st.warning("⚠️ One or both price sources failed.")

st.caption("Click refresh to check again.")
