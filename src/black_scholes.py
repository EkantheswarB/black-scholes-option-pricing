# black_scholes.py

import numpy as np
from scipy.stats import norm

def d1(S, K, T, r, sigma):
    return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

def d2(S, K, T, r, sigma):
    return d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

def bs_call_price(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)
    return S * norm.cdf(D1) - K * np.exp(-r * T) * norm.cdf(D2)

def bs_put_price(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)
    return K * np.exp(-r * T) * norm.cdf(-D2) - S * norm.cdf(-D1)

def call_delta(S, K, T, r, sigma):
    return norm.cdf(d1(S, K, T, r, sigma))

def put_delta(S, K, T, r, sigma):
    return norm.cdf(d1(S, K, T, r, sigma)) - 1

def gamma(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    return norm.pdf(D1) / (S * sigma * np.sqrt(T))

def vega(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    return S * norm.pdf(D1) * np.sqrt(T)

def call_theta(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)
    term1 = - (S * norm.pdf(D1) * sigma) / (2 * np.sqrt(T))
    term2 = - r * K * np.exp(-r * T) * norm.cdf(D2)
    return term1 + term2

def put_theta(S, K, T, r, sigma):
    D1 = d1(S, K, T, r, sigma)
    D2 = d2(S, K, T, r, sigma)
    term1 = - (S * norm.pdf(D1) * sigma) / (2 * np.sqrt(T))
    term2 = r * K * np.exp(-r * T) * norm.cdf(-D2)
    return term1 + term2

def call_rho(S, K, T, r, sigma):
    D2 = d2(S, K, T, r, sigma)
    return K * T * np.exp(-r * T) * norm.cdf(D2)

def put_rho(S, K, T, r, sigma):
    D2 = d2(S, K, T, r, sigma)
    return -K * T * np.exp(-r * T) * norm.cdf(-D2)

def black_scholes_all(S, K, T, r, sigma, option_type='call'):
    if option_type == 'call':
        return {
            'price': bs_call_price(S, K, T, r, sigma),
            'delta': call_delta(S, K, T, r, sigma),
            'gamma': gamma(S, K, T, r, sigma),
            'vega': vega(S, K, T, r, sigma),
            'theta': call_theta(S, K, T, r, sigma),
            'rho': call_rho(S, K, T, r, sigma)
        }
    elif option_type == 'put':
        return {
            'price': bs_put_price(S, K, T, r, sigma),
            'delta': put_delta(S, K, T, r, sigma),
            'gamma': gamma(S, K, T, r, sigma),
            'vega': vega(S, K, T, r, sigma),
            'theta': put_theta(S, K, T, r, sigma),
            'rho': put_rho(S, K, T, r, sigma)
        }
    else:
        raise ValueError("option_type must be 'call' or 'put'")
