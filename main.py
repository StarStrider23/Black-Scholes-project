import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt

from blackscholes.black_scholes import BlackScholes
from monte_carlo.monte_carlo import monte_carlo
from blackscholes.delta_hedging import delta_hedging

# Black-Scholes Model Validation

S = np.linspace(50, 150, 50)
K = 100
r = 0.05
sigma = 0.2
T = 1
steps = 252

bs = BlackScholes(S=S, K=K, r=r, sigma=sigma, T=T)

delta = bs.compute_delta()
delta_num = bs.compute_delta_num()

plt.figure(figsize=(12,6))
plt.plot(S, delta, label="BS Delta")
plt.plot(S, delta_num, '--r', label="Numerical Delta")
plt.xlabel("Underlying price S_0")
plt.ylabel("Delta")
plt.title("Black-Scholes Delta vs Numerical Delta")
plt.legend()
plt.grid(True)
plt.show()

gamma = bs.compute_gamma()
gamma_num = bs.compute_gamma_num()

plt.figure(figsize=(12,6))
plt.plot(S, gamma, label="BS Gamma")
plt.plot(S, gamma_num, '--r', label="Numerical Gamma")
plt.xlabel("Underlying price S_0")
plt.ylabel("Gamma")
plt.title("Black-Scholes Gamma vs Numerical Gamma")
plt.legend()
plt.grid(True)
plt.show()

# # Hedging Error vs Rebalancing Frequency

# steps_list = [10, 25, 50, 100, 252, 500]
# errors = []
# errors_std = []

# n_sim = 10000

# rng = np.random.default_rng(42)

# for steps in steps_list:
#     error = delta_hedging(steps=steps, Z=rng.standard_normal((n_sim, steps)))
#     errors.append(error)
#     errors_std.append(np.std(error))

# plt.figure(figsize=(12,6))
# plt.plot(steps_list, errors_std)
# plt.xlabel("Number of Hedging Steps")
# plt.ylabel("Std of Hedging Error")
# plt.title("Hedging Error vs Rebalancing Frequency")
# plt.grid(True)
# plt.show()

# fig, ax = plt.subplots(2, 3, figsize=(15, 8))
# fig.suptitle('Hedging Error vs Rebalancing Frequency')
# ax[0,0].hist(errors[0], bins=100); ax[0,0].set_title(f"{steps_list[0]} steps")
# ax[0,1].hist(errors[1], bins=100); ax[0,1].set_title(f"{steps_list[1]} steps")
# ax[0,2].hist(errors[2], bins=100); ax[0,2].set_title(f"{steps_list[2]} steps")
# ax[1,0].hist(errors[3], bins=100); ax[1,0].set_title(f"{steps_list[3]} steps")
# ax[1,1].hist(errors[4], bins=100); ax[1,1].set_title(f"{steps_list[4]} steps")
# ax[1,2].hist(errors[5], bins=100); ax[1,2].set_title(f"{steps_list[5]} steps")
# plt.show()

# # Monte Carlo Convergence + control variates

# S = 100
# K = 100
# r = 0.05
# sigma = 0.2
# T = 1
# steps = 252
# n_runs = 100

# sim_list = [100, 500, 1000, 5000, 10000, 50000, 100000]

# bs = BlackScholes(S=S, K=K, r=r, sigma=sigma, T=T)
# price_bs = bs.option_price()

# errors_av = []
# std_av = []

# for i in range(len(sim_list)):
#     opt_prices = []
    
#     for j in range(n_runs):
#         rng = np.random.default_rng(100*i + j)
#         Z = rng.standard_normal((sim_list[i], steps))

#         mc = monte_carlo(S_0=S, r=r, sigma=sigma, steps=steps, n_sim=sim_list[i], 
#                          Z=Z, rng=rng, return_paths=False)
        
#         X = np.exp(-r*T) * np.maximum(mc - K, 0)
#         V = np.mean(X)
#         Y = mc * np.exp(-r * T)
#         exp_val_mc = S

#         beta = np.cov(X, Y)[0, 1] / np.var(Y)

#         V_cv = np.mean(X - beta * (Y - exp_val_mc))
        
#         opt_prices.append(V_cv)
    
#     mean_opt_price = np.mean(opt_prices)
#     errors_av.append(np.sqrt(np.mean((opt_prices - price_bs)**2)))
#     std_av.append(np.std(opt_prices)/np.sqrt(n_runs))

# y = 1 / np.sqrt(sim_list)
# y = y * errors_av[0] / y[0] 

# plt.figure(figsize=(12,6))
# plt.plot(sim_list, y, color='b', label='O(N^{-1/2})')
# plt.errorbar(sim_list, errors_av, yerr=std_av, capsize=3, fmt="o--r", label="MC error")
# plt.xscale("log")
# plt.yscale("log")
# plt.xlabel("Number of simulations")
# plt.ylabel("RMSE")
# plt.title("Monte Carlo Convergence (Log-Log plot)")
# plt.legend()
# plt.grid(True)
# plt.show()

# # Monte Carlo vs Black–Scholes Option Pricing

# S = np.linspace(50, 150, 50)

# bs = BlackScholes(S=S, K=K, r=r, sigma=sigma, T=T)
# bs_opt_prices = bs.option_price()

# rng = np.random.default_rng(42)
# Z = rng.standard_normal((n_sim, steps))

# mc = monte_carlo(S_0=S, r=r, sigma=sigma, T=T, steps=steps, n_sim=10000, Z=Z, rng=rng, return_paths=False)
# mc_opt_prices = np.exp(-r*T) * np.mean(np.maximum(mc - K, 0), axis=1)

# plt.figure(figsize=(12,6))
# plt.plot(S, bs_opt_prices, label='Black–Scholes', linewidth=2)
# plt.plot(S, mc_opt_prices, '--', color='red', label='Monte Carlo', linewidth=2)
# plt.xlabel("Underlying price S_0")
# plt.ylabel("Option price V")
# plt.title("Monte Carlo vs Black–Scholes Option Pricing")
# plt.legend()
# plt.grid(True)
# plt.show()

# error = np.array(mc_opt_prices) - np.array(bs_opt_prices)

# plt.figure(figsize=(12,6))
# plt.plot(S, error)
# plt.axhline(0, linestyle='--', color='red')
# plt.xlabel("Underlying price S_0")
# plt.ylabel("Pricing error (MC - BS)")
# plt.title("Monte Carlo Pricing Error vs Underlying Price")
# plt.grid(True)
# plt.show()

# # Monte Carlo vs Black-Scholes, Delta

# S = np.linspace(50, 150, 50)
# n_sim = 100000
# h=0.2

# bs = BlackScholes(S=S, K=K, r=r, sigma=sigma, T=T)
# bs_delta = bs.compute_delta()

# rng = np.random.default_rng(42)
# Z = rng.standard_normal((n_sim, steps))

# mc_up = monte_carlo(S_0=S + h, r=r, sigma=sigma, steps=steps, n_sim=n_sim, 
#                     Z=Z, rng=rng, return_paths=False)
# mc_down = monte_carlo(S_0=S - h, r=r, sigma=sigma, steps=steps, n_sim=n_sim,
#                       Z=Z, rng=rng, return_paths=False)

# V_up = np.exp(-r*T) * np.mean(np.maximum(mc_up - K, 0), axis=1)
# V_down = np.exp(-r*T) * np.mean(np.maximum(mc_down - K, 0), axis=1)

# mc_delta = (V_up - V_down) / (2 * h)

# plt.figure(figsize=(12,6))
# plt.plot(S, bs_delta, label='Black–Scholes Delta', linewidth=2)
# plt.plot(S, mc_delta, '--', color='red', label='Monte Carlo Delta', linewidth=2)
# plt.xlabel("Underlying price S_0")
# plt.ylabel("Delta")
# plt.title("Monte Carlo vs Black–Scholes Delta")
# plt.legend()
# plt.grid(True)
# plt.show()

# error = np.array(mc_delta) - np.array(bs_delta)

# plt.figure(figsize=(12,6))
# plt.plot(S, error, label="Monte Carlo Delta Error")
# plt.axhline(0, linestyle='--', color='red')
# plt.xlabel("Underlying price S_0")
# plt.ylabel("Delta error (MC - BS)")
# plt.title("Monte Carlo Delta Error vs Underlying Price")
# plt.legend()
# plt.show()

# # Monte Carlo vs Black-Scholes, Gamma 

# S = np.linspace(50, 150, 50)
# n_sim = 50000
# h = 0.5

# bs = BlackScholes(S=S, K=K, r=r, sigma=sigma, T=T)
# bs_gamma = bs.compute_gamma()

# rng = np.random.default_rng(42)
# Z = rng.standard_normal((n_sim, steps), dtype=np.float32)

# mc_up = monte_carlo(S_0=S + h, r=r, sigma=sigma, steps=steps, n_sim=n_sim,
#                     Z=Z, rng=rng, return_paths=False)
# mc = monte_carlo(S_0=S, r=r, sigma=sigma, steps=steps, n_sim=n_sim,
#                  Z=Z, rng=rng, return_paths=False)
# mc_down = monte_carlo(S_0=S - h, r=r, sigma=sigma, steps=steps, n_sim=n_sim,
#                       Z=Z, rng=rng, return_paths=False)
# V_up = np.exp(-r*T) * np.mean(np.maximum(mc_up - K, 0), axis=1)
# V = np.exp(-r*T) * np.mean(np.maximum(mc - K, 0), axis=1)
# V_down = np.exp(-r*T) * np.mean(np.maximum(mc_down - K, 0), axis=1)

# mc_gamma = (V_up - 2*V + V_down) / h**2

# plt.figure(figsize=(12,6))
# plt.plot(S, bs_gamma, label='Black–Scholes Gamma', linewidth=2)
# plt.plot(S, mc_gamma, '--', color='red', label='Monte Carlo Gamma', linewidth=2)
# plt.xlabel("Underlying price S_0")
# plt.ylabel("Gamma")
# plt.title("Monte Carlo vs Black–Scholes Gamma")
# plt.legend()
# plt.grid(True)
# plt.show()

# error = np.array(mc_gamma) - np.array(bs_gamma)

# plt.figure(figsize=(12,6))
# plt.plot(S, error, label="Monte Carlo Gamma Error")
# plt.axhline(0, linestyle='--', color='red')
# plt.xlabel("Underlying price S_0")
# plt.ylabel("Gamma error (MC - BS)")
# plt.title("Monte Carlo Gamma Error vs Underlying Price")
# plt.legend()
# plt.show()

# # Implied volatility

# irx = "^IRX"
# rf_data = yf.download(irx, "2026-04-15", "2026-04-16")['Close']
# rf_rate = rf_data.iloc[0][irx]
# rf_rate = rf_rate / 100

# asset = "AAPL"
# S = yf.download(asset, "2026-04-15", "2026-04-16")['Close']
# S = S.iloc[0][asset] # S = 266.42999267578125

# # date = ticker.options[7]

# date = open("project_BS/data/option_expiration_date.txt").read()
# date1 = dt.datetime.strptime(date, "%Y-%m-%d").date()

# T = (date1 - dt.datetime.now().date()).days / 365

# # opt = ticker.option_chain(date)
# # calls = opt.calls
# # calls.to_csv("calls_snapshot.csv")

# calls = pd.read_csv("project_BS/data/calls_snapshot.csv")

# calls = calls[(calls['bid'] > 0) & (calls['ask'] > 0)]

# calls['mid'] = (calls['bid'] + calls['ask']) / 2

# calls_atm = calls[(calls['strike'] > S*0.9) & (calls['strike'] < S*1.1)]

# strike_price_atm = np.asarray(calls_atm['strike'])

# call_price_market_atm = np.asarray(calls['mid'])

# def Newton_Raphson(S, K, r, sigma, T, tol=1e-6, max_iter=100):
#     call_price_market = np.asarray(calls_atm['mid'])

#     for _ in range(max_iter):
#         bs = BlackScholes(S, K, r, sigma, T)
#         call_price = bs.option_price(option='call')
#         vega = bs.compute_vega(option='call')

#         price_error = call_price - call_price_market

#         if abs(price_error.any()) < tol:
#             return sigma

#         if vega.any() < 1e-8:
#             break

#         sigma = sigma - price_error / vega
#         sigma = np.maximum(sigma, 1e-6)

#     return sigma

# iv = np.asanyarray(calls_atm['impliedVolatility'])

# nr = Newton_Raphson(S=S, K=strike_price_atm, r=rf_rate, sigma=0.3, T=T)
# print(f"Absolute Error: {abs(nr - iv)}")
# # print(f"Absolute Error Percent: {100*abs((nr - iv) /iv)}")

# plt.figure(figsize=(12,6))
# plt.plot(strike_price_atm, nr, 'o--r', label="Newton-Raphson IV")
# plt.plot(strike_price_atm, iv, color='blue', label="Actual IV")
# plt.axvline(S, linestyle='--', color='black', label='Asset price')
# plt.title('Implied Volatility (IV) Smirk')
# plt.xlabel('Strike prices')
# plt.ylabel('Volatility')
# plt.legend()
# plt.grid(True)
# plt.show()