from scipy.optimize import brentq
from black_scholes import bs_call_price, bs_put_price
import numpy as np

def implied_volatility(price, S, K, T, r, option_type='call'):
    def objective(sigma):
        if sigma <= 0:
            return price
        if option_type == 'call':
            return bs_call_price(S, K, T, r, sigma) - price
        elif option_type == 'put':
            return bs_put_price(S, K, T, r, sigma) - price
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    try:
        low_price = bs_call_price(S, K, T, r, 1e-6) if option_type == 'call' else bs_put_price(S, K, T, r, 1e-6)
        high_price = bs_call_price(S, K, T, r, 10.0) if option_type == 'call' else bs_put_price(S, K, T, r, 10.0)

        if not (low_price <= price <= high_price):
            return None

        return brentq(objective, 1e-6, 10.0, maxiter=500)
    except Exception:
        # Brute-force fallback if Brent fails
        sigmas = np.linspace(0.001, 10.0, 10000)
        best_sigma = None
        min_error = float('inf')

        for sigma in sigmas:
            model_price = bs_call_price(S, K, T, r, sigma) if option_type == 'call' else bs_put_price(S, K, T, r, sigma)
            error = abs(model_price - price)
            if error < min_error:
                min_error = error
                best_sigma = sigma

        return best_sigma if min_error < 1e-2 else None
