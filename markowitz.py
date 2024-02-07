from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt import plotting
import copy
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

# This version of the code follows Medium's implementation using the pypfopt library
# The data used for this version comes from yfinance library
# The values and calculations do not match the excel sheet example

# List of stock tickers
tickers = ['PTON', 'PINS', 'INSP.L', '0H6I.IL', 'ORCP.AQ', 'VOD.L', '0E6H.L', '888.L', 'GGP.L', 'HOTC.L', 'BOO.L', 'EUA.L', 'TSCO.L', 'AAF.L', '0Q1N.IL']

# Download data for each stock
stock_dfs = {ticker: yf.download(ticker, start='2014-12-01', end='2020-01-01')['Adj Close'] for ticker in tickers}

# Concatenate into a dataframe
df = pd.DataFrame(stock_dfs)
print(df)

#calculate expected returns
er = expected_returns.mean_historical_return(df)
print(er)
#Calculate covariance
cov = risk_models.sample_cov(df)
print (cov)
corr = risk_models.cov_to_corr(cov)
print(corr)

#Calculate efficient frontier
ef = EfficientFrontier(er, cov, weight_bounds=(0.05, None))

# Show graph ---- not currently working
fig = plt.figure()
ax = fig.add_subplot(111)
plotting.plot_efficient_frontier(ef, ef_param='risk', ax=ax, show_assets=False)
# Find the tangency portfolio
ef_max_sharpe = EfficientFrontier(er, cov, weight_bounds=(0.05, None))
ef_max_sharpe.max_sharpe(risk_free_rate=0.05)
ret_tangent, std_tangent, _ = ef_max_sharpe.portfolio_performance()
ax.scatter(std_tangent, ret_tangent, marker="*", s=100, c="r", label="Max Sharpe")
# Make graph pretty and save as file--currently disabled
ax.set_title("Efficient Frontier of our portfolio")
ax.legend()
plt.tight_layout()
# plt.savefig("ef_scatter.png", dpi=200)
plt.show()

#Get the optimal weights
weights = ef.max_sharpe()
print(weights)