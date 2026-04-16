# Black-Scholes and Greeks Project

Project by Alexsey Chernichenko

# Project Goal

The goal of this project is to build and validate a comprehensive quantitative framework for option pricing and risk analysis. The project begins with the implementation of the Black–Scholes model, including both analytical and numerical computation of option Greeks. It then extends to dynamic hedging through delta hedging simulations, with a focus on analyzing hedging error as a function of rebalancing frequency.

In addition, the project develops a Monte Carlo pricing engine, studies its convergence properties, and applies variance reduction techniques such as control variates to improve efficiency. A detailed comparison between Monte Carlo and Black–Scholes methods is conducted, including pricing consistency and sensitivity analysis with respect to the underlying asset price, Delta (Δ) and Gamma (Γ).

Finally, the project incorporates implied volatility estimation, completing a full pipeline from pricing to market calibration.

# Background

## Black-Scholes model

The Black–Scholes model is a foundational framework in quantitative finance used to price European-style options. It provides a closed-form solution for option prices under a set of simplifying assumptions about market behavior. At its core, the model assumes that the underlying asset price follows a geometric Brownian motion with constant volatility and drift. Beyond that, there are also some additional assumptions: constant risk-free interest rate, frictionless markets (no transaction costs or taxes), no arbitrage opportunities exist and of course that the underlying asset doesn't pay dividends. 

Mathematically speaking, the Black-Scholes model is a a second-order linear partial differential equation (PDE).

$$ \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - rV = 0 $$

Where $V = V (S, t)$ is price of the option (which is either call (C) or put (P)) of the underlying asset $S$ at time $t$, $\sigma$ is volatiltiy of the stock's returns and $r$ is the risk-free interest rate.  

Under these assumptions, the price of a European call option can be expressed analytically.  

$$ C = S N(d_{1}) - K e^{- r (T - t)} N(d_{2}) $$

Where where $S$ is the current stock price, $K$ is the strike price, $T$ is time to maturity and $N(d_{i})$ 
is the standard normal cumulative distribution function. Finally, $d_{1}$ and $d_{2}$ are quantities that are defined as below.

$$ d_{1} = \frac{1}{\sigma \sqrt{T - t}} \bigg[log\bigg(\frac{S}{K}\bigg) + \bigg(r + \frac{\sigma^2}{2}\bigg) (T - t) \bigg]$$

$$ d_{2} = d_{1} - \sigma \sqrt{T - t} $$

Intuitively, $d_{1}$ represents a standardized measure of how far the option is from being in-the-money (ITM) at maturity under the risk-neutral measure, taking into account both the expected growth of the stock price and its volatility. $d_{2}$ is closely related to $d_{1}$, but adjusted downward by a volatility term, which accounts for uncertainty over the remaining time to maturity. It can be interpreted as a standardized measure of terminal moneyness.

The price of a correspondning put option can be derived via the put-call prity.

$$ P = K e^{-r(T - t)} - S + C = K e^{- r (T - t)} N(-d_{2}) - S N(-d_{1}) $$

## The Option Greeks

### Delta ($\Delta$)

Delta measures the sensitivity of the option price to changes in the underlying asset price:

$$ \Delta = \frac{\partial V}{\partial S} $$

Intuitively, Delta represents the hedge ratio, i.e. how many units of the underlying asset are needed to replicate the option’s price changes. For a call option, Delta lies between 0 and 1 whereas it lies between -1 and 0 for a put option.

### Gamma ($\Gamma$)

Gamma measures the rate of change of Delta with respect to the underlying asset price:

$$ \Gamma = \frac{\partial^2 V}{\partial S^2} $$

It captures the curvature of the option price, indicating how stable the Delta hedge is. High Gamma means Delta changes quickly, making hedging more sensitive and requiring more frequent rebalancing.

### Vega ($\nu$)

Vega measures sensitivity to volatility:

$$ \nu = \frac{\partial V}{\partial \sigma} $$

It reflects how much the option price changes when market expectations of volatility change. Options are typically most sensitive to volatility when they are at-the-money (ATM).

### Theta ($\Theta$)

Theta measures sensitivity to time decay:

$$ \Theta = \frac{\partial V}{\partial t} $$

However, in practice one sometimes sets $t$ to zero which then changes the definition.

$$ \Theta = -\frac{\partial V}{\partial T} $$

This convention is also used in the project. Theta measures the rate at which an option loses value as time passes.

### Rho ($\rho$)

Rho measures sensitivity to the risk-free interest rate:

$$ \rho = \frac{\partial V}{\partial r} $$

It is generally less significant in short-dated options but becomes more relevant for longer maturities.

## Delta Hedging

Delta hedging aims to eliminate sensitivity to small changes in the underlying price by constructing a locally risk-free portfolio. A delta-hedged portfolio is formed as:

$$ \Pi = V - \Delta S $$

Using Itô’s lemma, the stochastic term cancels and under continuous rebalancing the portfolio evolves deterministically:

$$ d \Pi = \bigg( \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2}\bigg) dt $$

In the Black–Scholes framework no-arbitrage implies:

$$ d \Pi = r \Pi dt $$

which leads to the Black–Scholes PDE. 

To put it simply, the idea is to offset the option’s exposure to the underlying by taking an opposite position in the stock. Since Delta measures how much the option price moves with the stock, holding $−Δ$ units of the underlying stock cancels the first-order price risk. As the stock price changes, Delta changes as well, so the hedge must be continuously rebalanced. In theory, continuous rebalancing removes all randomness from the portfolio, making it risk-free. In practice, rebalancing is discrete, which introduces hedging error that grows with volatility and lower rebalancing frequency.

## Implied Volatility (IV)

Implied volatility is the volatility parameter that makes the Black–Scholes model match the observed market price of an option. Instead of being directly observed, it is obtained by inverting the pricing formula.
Formally, implied volatility $\sigma_{imp}$ is defined as the solution to:

$$ C_{market} = C_{BS}(S, K, r, T, \sigma_{imp}) $$

Since the Black–Scholes formula is not analytically invertible in $\sigma$, the implied volatility must be computed numerically, typically using root-finding methods such as Newton–Raphson:

$$ \sigma_{n+1} = \sigma_{n} - \frac{C_{BS}(\sigma_{n}) - C_{market}}{\nu(\sigma_{n})} $$

# Methodology

The project follows a structured quantitative approach combining analytical modeling, numerical methods and simulation. First, the Black–Scholes model is implemented, including closed-form pricing and analytical expressions for the Greeks, alongside numerical approximations for validation.

A Monte Carlo framework is then developed to simulate the underlying asset dynamics under the risk-neutral measure. Convergence properties are analyzed and variance reduction techniques, specifically control variates, are applied to improve computational efficiency.

To study risk management, a discrete-time delta hedging strategy is implemented. The hedging performance is evaluated by analyzing the replication error as a function of rebalancing frequency and market parameters.

Finally, implied volatility is computed by numerically inverting the Black–Scholes formula, linking model outputs to observed market prices. Throughout the project, analytical and numerical results are systematically compared to assess accuracy, stability and consistency across methods.

# Structure

# Results

https://black-scholes-and-greeks-project.streamlit.app

# Discussion

# Outlook


