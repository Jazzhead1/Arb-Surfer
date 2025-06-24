import streamlit as st
import requests

st.set_page_config(page_title="ArbSurfer", layout="wide")
st.title("🌊 ArbSurfer: Solana Arbitrage Monitor (SOL/USDT)")

def get_orca_price():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get("https://quote-api.jup.ag/v6/quote", params={
            "inputMint": "So11111111111111111111111111111111111111112",  # SOL
            "outputMint": "Es9vMFrzaCERFBn5gdB34dFpgdQT1D9pU8WWvWrtCPSb",  # USDT
            "amount": 10000000,  # 0.01 SOL
            "slippage": 1
        }, headers=headers)
        response.raise_for_status()
        out_amount = float(response.json()["outAmount"])
        return out_amount / 1e6
    except Exception as e:
        st.error(f"❌ Error fetching Orca price from Jupiter: {e}")
        return None

def get_raydium_price():
    try:
        response = requests.get("https://api.raydium.io/pairs")
        response.raise_for_status()
        for pair in response.json():
            if pair.get("name") == "SOL/USDT":
                return float(pair["price"])
        st.warning("⚠️ Raydium pair SOL/USDT not found")
        return None
    except Exception as e:
        st.error(f"❌ Error fetching Raydium price: {e}")
        return None

if st.button("🔄 Refresh"):
    st.experimental_rerun()

orca_price = get_orca_price()
raydium_price = get_raydium_price()

if orca_price and raydium_price:
    spread = abs(orca_price - raydium_price)
    spread_pct = (spread / min(orca_price, raydium_price)) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("💧 Orca", f"${orca_price:.4f}")
    col2.metric("🧪 Raydium", f"${raydium_price:.4f}")
    col3.metric("📈 Spread", f"{spread_pct:.2f}%")

    if spread_pct >= 0.1:
        st.success("🚨 Arbitrage opportunity detected!")
    else:
        st.info("📉 No significant arbitrage at this time.")
else:
    st.warning("⚠️ Could not load both prices.")
