# dashboard.py

import streamlit as st
from black_scholes import black_scholes_all
from implied_vol import implied_volatility
from fetch_data import get_stock_price, get_expiry_dates
from visualize import plot_option_price_vs_volatility, plot_option_price_vs_strike, generate_price_heatmap
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Black-Scholes Option Pricing", layout="centered")
st.title("📈 Black-Scholes Option Pricing Model")

st.sidebar.header("Choose a Stock and Expiry")
ticker = st.sidebar.text_input("Enter Stock Ticker (e.g., AAPL)", value="AAPL").upper()

expiry_dates = get_expiry_dates(ticker)
expiry = st.sidebar.selectbox("Select Expiry Date", expiry_dates) if expiry_dates else None

stock_price = get_stock_price(ticker) if ticker else None
if stock_price:
    st.success(f"📡 Live Stock Price for {ticker}: ${stock_price:.2f}")
else:
    st.warning("⚠️ Live stock price unavailable. Using manual input.")

st.sidebar.header("Custom Parameters")

preset = st.sidebar.selectbox("🎯 Choose Preset Scenario", options=["Custom", "Tech Stock (High Volatility)", "Long-dated OTM Put", "ATM Call with 3M Maturity"])

if preset != "Custom":
    if preset == "Tech Stock (High Volatility)":
        S, K, T, r, sigma = 150, 140, 0.5, 0.03, 0.6
    elif preset == "Long-dated OTM Put":
        S, K, T, r, sigma = 80, 100, 2, 0.02, 0.25
    elif preset == "ATM Call with 3M Maturity":
        S, K, T, r, sigma = 100, 100, 0.25, 0.05, 0.18
else:
    S = st.sidebar.number_input("Stock Price (S)", min_value=0.0, value=100.0)
    K = st.sidebar.number_input("Strike Price (K)", min_value=0.0, value=100.0)
    T = st.sidebar.number_input("Time to Maturity (T in years)", min_value=0.01, value=1.0)
    r = st.sidebar.number_input("Risk-free Rate (r)", min_value=0.0, value=0.05)
    sigma = st.sidebar.number_input("Volatility (σ)", min_value=0.01, value=0.2)

calculate_iv = st.sidebar.checkbox("Estimate Implied Volatility")
call_market_price = put_market_price = None
if calculate_iv:
    call_market_price = st.sidebar.number_input("Call Market Price", min_value=0.0, value=10.0)
    put_market_price = st.sidebar.number_input("Put Market Price", min_value=0.0, value=10.0)

if S and K and T and r and sigma:
    call_results = black_scholes_all(S, K, T, r, sigma, 'call')
    put_results = black_scholes_all(S, K, T, r, sigma, 'put')

    st.markdown("---")
    st.markdown("### 📋 Summary of Inputs")
    st.write(f"**Stock Price (S):** {S}")
    st.write(f"**Strike Price (K):** {K}")
    st.write(f"**Time to Maturity (T):** {T} years")
    st.write(f"**Risk-Free Rate (r):** {r}")
    st.write(f"**Volatility (σ):** {sigma}")

    st.markdown("---")
    st.subheader("Call and Put Option Pricing and Greeks")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📘 Call Option")
        st.write(f"**Option Price:** {call_results['price']:.4f}")
        st.write(f"Delta: {call_results['delta']:.4f}")
        st.write(f"Gamma: {call_results['gamma']:.4f}")
        st.write(f"Vega: {call_results['vega']:.4f}")
        st.write(f"Theta: {call_results['theta']:.4f}")
        st.write(f"Rho: {call_results['rho']:.4f}")
        if calculate_iv and call_market_price:
            low = black_scholes_all(S, K, T, r, 1e-6, 'call')['price']
            high = black_scholes_all(S, K, T, r, 10.0, 'call')['price']
            if not (low <= call_market_price <= high):
                st.error(f"Market price (${call_market_price}) out of theoretical range: {low:.2f}–{high:.2f}")
            else:
                call_iv = implied_volatility(call_market_price, S, K, T, r, 'call')
                if call_iv:
                    st.success(f"Implied Volatility: {call_iv:.4f}")
                else:
                    st.error("Implied Volatility could not be computed.")

    with col2:
        st.markdown("### 📕 Put Option")
        st.write(f"**Option Price:** {put_results['price']:.4f}")
        st.write(f"Delta: {put_results['delta']:.4f}")
        st.write(f"Gamma: {put_results['gamma']:.4f}")
        st.write(f"Vega: {put_results['vega']:.4f}")
        st.write(f"Theta: {put_results['theta']:.4f}")
        st.write(f"Rho: {put_results['rho']:.4f}")
        if calculate_iv and put_market_price:
            low = black_scholes_all(S, K, T, r, 1e-6, 'put')['price']
            high = black_scholes_all(S, K, T, r, 10.0, 'put')['price']
            if not (low <= put_market_price <= high):
                st.error(f"Market price (${put_market_price}) out of theoretical range: {low:.2f}–{high:.2f}")
            else:
                put_iv = implied_volatility(put_market_price, S, K, T, r, 'put')
                if put_iv:
                    st.success(f"Implied Volatility: {put_iv:.4f}")
                else:
                    st.error("Implied Volatility could not be computed.")

    st.markdown("---")
    st.subheader("💡 Strategy Payoff at Expiry")
    strategy = st.selectbox("Choose Strategy", ["None", "Long Call", "Long Put", "Straddle"])

    if strategy != "None":
        spot_prices = np.linspace(0.5 * S, 1.5 * S, 200)
        if strategy == "Long Call":
            payoff = np.maximum(spot_prices - K, 0) - call_results['price']
        elif strategy == "Long Put":
            payoff = np.maximum(K - spot_prices, 0) - put_results['price']
        elif strategy == "Straddle":
            payoff = np.maximum(spot_prices - K, 0) + np.maximum(K - spot_prices, 0) - (call_results['price'] + put_results['price'])

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(spot_prices, payoff, label=f"Payoff – {strategy}")
        ax.axhline(0, color='black', linestyle='--')
        ax.axvline(S, color='blue', linestyle=':', label='Spot Price')
        ax.set_xlabel("Spot Price at Expiry")
        ax.set_ylabel("Profit / Loss")
        ax.set_title(f"{strategy} Payoff")
        ax.legend()
        st.pyplot(fig)