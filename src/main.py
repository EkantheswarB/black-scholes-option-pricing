# main.py

import argparse
from black_scholes import black_scholes_all
from implied_vol import implied_volatility


def main():
    parser = argparse.ArgumentParser(description="Black-Scholes Option Pricing Model")
    parser.add_argument('--S', type=float, required=True, help='Current stock price')
    parser.add_argument('--K', type=float, required=True, help='Strike price')
    parser.add_argument('--T', type=float, required=True, help='Time to maturity (in years)')
    parser.add_argument('--r', type=float, required=True, help='Risk-free interest rate')
    parser.add_argument('--sigma', type=float, required=True, help='Volatility (standard deviation)')
    parser.add_argument('--option_type', type=str, choices=['call', 'put'], required=True, help='Option type')
    parser.add_argument('--market_price', type=float, help='Observed market price for IV calculation')

    args = parser.parse_args()

    results = black_scholes_all(args.S, args.K, args.T, args.r, args.sigma, args.option_type)

    print(f"\nBlack-Scholes {args.option_type.capitalize()} Option Pricing:")
    for k, v in results.items():
        print(f"{k.capitalize()}: {v:.4f}")

    if args.market_price:
        iv = implied_volatility(args.market_price, args.S, args.K, args.T, args.r, args.option_type)
        print(f"\nImplied Volatility from Market Price ({args.market_price}): {iv:.4f}" if iv else "Implied Volatility could not be computed.")


if __name__ == '__main__':
    main()
