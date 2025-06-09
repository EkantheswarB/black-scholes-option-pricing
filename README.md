📈 Black-Scholes Option Pricing Dashboard

An interactive Python dashboard for pricing European options, computing Greeks, and visualizing payoff strategies using the Black-Scholes model.
🚀 Features
•	✅ Real-time stock price and expiry data via yfinance
•	📊 Compute Call/Put prices and Greeks (Delta, Gamma, Vega, Theta, Rho)
•	🔍 Estimate Implied Volatility from user-supplied market price
•	📉 Visualize strategy payoffs: Long Call, Long Put, Straddle
•	🧠 Input validation with theoretical price bounds
•	📋 Summary panel with custom/preset input scenarios
•	🔥 2D visualizations and heatmaps for deeper parameter insights
🛠 Tech Stack
•	Python 3.x
•	Streamlit
•	NumPy, SciPy, Matplotlib
•	yFinance API
▶️ Run Locally

1.	Clone this repo:
  git clone https://github.com/EkantheswarB/black-scholes-option-pricing.git
  cd black-scholes-dashboard

2.	Create and activate environment:
  conda create -n blackscholes python=3.11
  conda activate blackscholes
  pip install -r requirements.txt

3.	Run the app:
  streamlit run src/dashboard.py
✅ Example Use Cases
•	Visualizing option price sensitivity to volatility & time
•	Estimating implied volatility for pricing validation
•	Exploring strategy payoffs under varying market conditions
•	Educational tool for understanding options pricing mechanics
📂 Project Structure

black-scholes/
├── src/
│   ├── dashboard.py           # Streamlit GUI
│   ├── black_scholes.py       # Core pricing + Greeks
│   ├── implied_vol.py         # Implied volatility calculation
│   ├── fetch_data.py          # yFinance integrations
│   ├── visualize.py           # Charts, heatmaps, payoff plots
├── requirements.txt
├── README.md

📄 License
This project is open-source under the MIT License.
🙋‍♂️ Author
Ekantheswar Bandarupalli
LinkedIn: https://linkedin.com/in/ekantheswar
GitHub: https://github.com/yourusername
Email: study.ekantheswar@gmail.com
