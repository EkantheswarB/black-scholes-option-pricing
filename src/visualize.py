# visualize.py

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from black_scholes import bs_call_price, bs_put_price


def plot_option_price_vs_volatility(S, K, T, r, option_type='call'):
    sigmas = np.linspace(0.01, 1.0, 100)
    prices = []

    for sigma in sigmas:
        if option_type == 'call':
            prices.append(bs_call_price(S, K, T, r, sigma))
        else:
            prices.append(bs_put_price(S, K, T, r, sigma))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(sigmas, prices, color='blue', linewidth=2)
    ax.set_title(f'{option_type.capitalize()} Option Price vs Volatility')
    ax.set_xlabel('Volatility (σ)')
    ax.set_ylabel('Option Price')
    ax.grid(True)
    plt.tight_layout()
    plt.close(fig)
    print(f"[DEBUG] Volatility range: {sigmas}")
    print(f"[DEBUG] Option prices: {prices[:5]} ... {prices[-5:]}")
    return fig


def plot_option_price_vs_strike(S, T, r, sigma, option_type='call'):
    Ks = np.linspace(0.5 * S, 1.5 * S, 100)
    prices = []

    for strike in Ks:
        if option_type == 'call':
            prices.append(bs_call_price(S, strike, T, r, sigma))
        else:
            prices.append(bs_put_price(S, strike, T, r, sigma))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(Ks, prices, label=f'{option_type.capitalize()} Price')
    ax.set_xlabel('Strike Price (K)')
    ax.set_ylabel('Option Price')
    ax.set_title(f'{option_type.capitalize()} Option Price vs Strike Price')
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.close(fig)
    return fig


def generate_price_heatmap(K, T, r, option_type='call', spot_range=(80, 120), vol_range=(0.05, 0.5), resolution=20):
    spot_prices = np.linspace(spot_range[0], spot_range[1], resolution)
    volatilities = np.linspace(vol_range[0], vol_range[1], resolution)
    Z = np.zeros((len(volatilities), len(spot_prices)))

    for i, sigma in enumerate(volatilities):
        for j, S in enumerate(spot_prices):
            if option_type == 'call':
                Z[i, j] = bs_call_price(S, K, T, r, sigma)
            else:
                Z[i, j] = bs_put_price(S, K, T, r, sigma)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(Z, xticklabels=np.round(spot_prices, 1), yticklabels=np.round(volatilities, 2),
                cmap='viridis', ax=ax)
    ax.set_xlabel('Spot Price (S)')
    ax.set_ylabel('Volatility (σ)')
    ax.set_title(f'{option_type.capitalize()} Option Price Heatmap')
    plt.tight_layout()
    plt.close(fig)
    return fig