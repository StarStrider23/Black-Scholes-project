# Black-Scholes and Greeks Project

Project by Alexsey Chernichenko

# Project Goal

The goal of this project is to build and validate a comprehensive quantitative framework for option pricing and risk analysis. The project begins with the implementation of the Black–Scholes model, including both analytical and numerical computation of option Greeks. It then extends to dynamic hedging through delta hedging simulations, with a focus on analyzing hedging error as a function of rebalancing frequency.

In addition, the project develops a Monte Carlo pricing engine, studies its convergence properties and applies variance reduction techniques such as control variates to improve efficiency. A detailed comparison between Monte Carlo and Black–Scholes methods is conducted, including pricing consistency and sensitivity analysis with respect to the underlying asset price, Delta (Δ) and Gamma (Γ).

Finally, the project incorporates implied volatility estimation, completing a full pipeline from pricing to market calibration.

# Background

## The Black-Scholes model

The Black–Scholes model is a foundational framework in quantitative finance used to price European-style options. It provides a closed-form solution for option prices under a set of simplifying assumptions about market behavior. At its core, the model assumes that the underlying asset price follows a geometric Brownian motion with constant volatility and drift. Beyond that, there are also some additional assumptions: constant risk-free interest rate, frictionless markets (no transaction costs or taxes), no arbitrage opportunities exist and of course that the underlying asset doesn't pay dividends. 

Mathematically speaking, the Black-Scholes model is a a second-order linear partial differential equation (PDE).

$$ \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} + r S \frac{\partial V}{\partial S} - rV = 0 $$

Where $V = V (S, t)$ is price of the option (which is either call (C) or put (P)) of the underlying asset $S$ at time $t$, $\sigma$ is volatiltiy of the stock's returns and $r$ is the risk-free interest rate.  

Under these assumptions, the price of a European call option can be expressed analytically.  

$$ C = S N(d_{1}) - K e^{- r (T - t)} N(d_{2}) $$

Where $S$ is the current stock price, $K$ is the strike price, $T$ is time to maturity and $N(d_{i})$ 
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

All simulations and analyses are conducted for European call options even though the implemented framework supports both calls and puts. However, this restriction is without loss of generality, since results for put options follow directly from put–call parity.

# Structure

# Results

https://black-scholes-and-greeks-project.streamlit.app

## Black-Scholes validation



## Delta Hedging.

Evaluation of the performance of a delta hedging strategy and quantification of hedging error under discrete rebalancing. A delta-hedged portfolio is constructed and rebalanced at discrete time intervals. The replication error is measured at maturity for different rebalancing frequencies.  

<img width="1200" height="600" alt="Hedging Error vs Rebalancing Error" src="https://github.com/user-attachments/assets/027b662f-475e-4c79-8d49-6273ab2f36b9" />  

<img width="1440" height="800" alt="Hedging Error vs rebalancing Frequency, Bins" src="https://github.com/user-attachments/assets/6491f4a3-6b9b-4667-a955-f0e5759e2c3a" />  

Hedging error decreases as the rebalancing frequency increases, approaching zero in the limit of continuous hedging. Residual error arises from discrete rebalancing and is amplified by higher volatility, illustrating the practical limitations of continuous-time assumptions.  

## Monte Carlo Convergence.

Analysis of the convergence of the Monte Carlo estimator and evaluation of the impact of control variates on variance reduction. Simulations are performed under the risk-neutral measure using geometric Brownian motion. The option price is estimated for increasing numbers of simulated paths and results for each number of simulations are averaged across 100 simulation runs to reduce Monte Carlo variability.

<img width="1200" height="600" alt="MC Convergence" src="https://github.com/user-attachments/assets/547ebd68-1918-4e9b-82ea-030ef8e826fe" />  

| Number of simulations |   100  |   500  |  1000  |  5000  |  10000 |  50000 | 100000 |
| --------------------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
|    Standard Error     | 0.0530 | 0.0247 | 0.0181 | 0.0083 | 0.0054 | 0.0028 | 0.0018 |  

The Monte Carlo estimator converges to the Black–Scholes benchmark as the number of simulations increases. Meanwhile, the Standard Error (SE) decreases with number of simulations. This is partially due to the usage of the so-called control varaites technique. The Black–Scholes analytical price is used as a control variate. The adjusted estimator is constructed to reduce variance without increasing the number of simulations. The convergence rate is consistent with the theoretical $O(N^{-1/2})$ behavior.  

## Monte Carlo vs Black-Scholes Option Pricing.

<img width="1200" height="600" alt="MC vs BS Option Pricing" src="https://github.com/user-attachments/assets/f60922bf-2aa1-432c-9cf7-6eea705bf593" />

<img width="1200" height="600" alt="MC Pricing Error vs Underlying Price" src="https://github.com/user-attachments/assets/4e45a273-598e-4004-91e5-bfb049c3c1a6" />

## Monte Carlo vs Black-Scholes, The Greeks

Comparison of Monte Carlo and Black–Scholes pricing across different market conditions and sensitivities. Option prices and Greeks are evaluated across varying underlying prices. Monte Carlo estimates are compared to analytical Black–Scholes results.

### Delta

<img width="1200" height="600" alt="MC vs BS Delta" src="https://github.com/user-attachments/assets/f0d54b1c-a1ab-48c8-94cd-3314677e830d" />

<img width="1200" height="600" alt="MC Delta Error vs Underlying Price" src="https://github.com/user-attachments/assets/e7d464d8-6ef7-41fc-b004-55822adeadd9" />

### Gamma

<img width="1200" height="600" alt="MC vs BS Gamma" src="https://github.com/user-attachments/assets/8592b790-39c1-46be-a9c5-b4c8481da303" />  
  
<img width="1200" height="600" alt="MC vs BS Gamma Error" src="https://github.com/user-attachments/assets/a77f478e-f908-4fe8-81eb-113a047f01ad" />  
  
Monte Carlo estimates are consistent with Black–Scholes results, validating both implementations. However, Monte Carlo exhibits higher variability, particularly for second-order sensitivities such as Gamma, reflecting the increased difficulty of estimating higher-order derivatives via simulation.

## Implied Volatility

Computation of implied volatility by inverting the Black–Scholes pricing formula. Implied volatility is obtained numerically using an iterative root-finding method, such as Newton–Raphson, applied to match model prices to observed option prices.

The project considered options with prices near the at-the-money (ATM) region, namely $0.9S < K < 1.1S$, with expiration date 2026-05-15, which implies that T = 28 days or T = 0.07671232876712329 years. The closing price at the end of the day (2026-04-15) of the simulation was $S$ = 266.42999267578125 $. The risk-free interest rate was 0.036119999885559084. 
  
<img width="1200" height="600" alt="IV" src="https://github.com/user-attachments/assets/005600d9-037a-42d4-b310-e07eb93f7c10" />  
  
| Strike Price $ | ITM   | Actual $\sigma_{imp}$ | NR $\sigma_{imp}$ |  Absolute error  | Absolute error % |
| -------------- | ----- | --------------------- | ----------------- | ---------------- | ---------------- |
|      240       | True  |       0.38135384      |     0.34410769    |    0.02981965    |       9.77       |
|      245       | True  |       0.35974761      |     0.33263223    |    0.02016357    |       7.54       |
|      250       | True  |       0.3440007       |     0.32293332    |    0.01449942    |       6.12       |
|      255       | True  |       0.32684999      |     0.31221437    |    0.00841760    |       4.48       |
|      260       | True  |       0.31189653      |     0.30322305    |    0.00274007    |       2.78       |
|      265       | True  |       0.30164273      |     0.29711033    |    0.00119512    |       1.50       |
|      270       | False |       0.29590548      |     0.29235877    |    0.00202162    |       1.20       |
|      275       | False |       0.29090065      |     0.28955827    |    0.00411861    |       0.46       |
|      280       | False |       0.28736064      |     0.28696143    |    0.00497072    |       0.14       |
|      285       | False |       0.28601788      |     0.28625329    |    0.00555769    |       0.08       |
|      290       | False |       0.28613995      |     0.28800836    |    0.00719459    |       0.65       |  
  
The numerical procedure converges efficiently to the implied volatility, demonstrating the stability of the implementation. The results highlight how implied volatility serves as a bridge between observed market prices and model parameters.

# Discussion

# Outlook


