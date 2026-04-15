# Black-Scholes and Greeks Project

Project by Alexsey Chernichenko

# Project Goal

The goal of this project is to build and validate a comprehensive quantitative framework for option pricing and risk analysis. The project begins with the implementation of the Black–Scholes model, including both analytical and numerical computation of option Greeks. It then extends to dynamic hedging through delta hedging simulations, with a focus on analyzing hedging error as a function of rebalancing frequency.

In addition, the project develops a Monte Carlo pricing engine, studies its convergence properties, and applies variance reduction techniques such as control variates to improve efficiency. A detailed comparison between Monte Carlo and Black–Scholes methods is conducted, including pricing consistency and sensitivity analysis with respect to the underlying asset price, Delta (Δ) and Gamma (Γ).

Finally, the project incorporates implied volatility estimation, completing a full pipeline from pricing to market calibration.

# Background

## Black-Scholes model

The Black–Scholes model is a foundational framework in quantitative finance used to price European-style options. It provides a closed-form solution for option prices under a set of simplifying assumptions about market behavior. At its core, the model assumes that the underlying asset price follows a geometric Brownian motion with constant volatility and drift. Mathematically, the Black-Scholes model is a partial differential equation (PDE) of second order.

$$ \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - rV = 0 $$

Where $V = V (S, t)$ is price of the option of the underlying asset $S$ at time $t$, $\sigma$ is volatiltiy of the stock's returns and r is the risk-free interest rate.    

Under these assumptions, the price of a European call option can be expressed analytically.

$$ C = S_{0} \Phi(d_{1}) - K e^{- r T} \Phi(d_{2}) $$

Where where $S_{0}$ is the current stock price, $K$ is the strike price, $T$ is time to maturity and $\Phi(d)$ 
is the standard normal cumulative distribution function. Finally, $d_{1}$ and $d_{2}$ are quantities that are defined as below.

$$ d_{1} = \frac{1}{\sigma \{T - t}} (log(\frac{S}{K}) + (r + \frac{\sigma^2}{2}) (T - t))$$

$$ d_{2} = d_{1} - \sigma (T - t) $$

# Methodology

# Structure

# Results

https://black-scholes-and-greeks-project.streamlit.app

# Discussion

# Outlook


