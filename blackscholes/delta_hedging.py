import numpy as np

from monte_carlo.monte_carlo import monte_carlo
from blackscholes.black_scholes import BlackScholes

def delta_hedging(S_0=100, K=100, r=0.05, sigma=0.2, T=1, steps=252, 
                  n_sim=100000, Z=None, rng=None, return_paths=True, option="call"):
    
    dt = 1/steps
    S = monte_carlo(S_0, r, sigma, T, steps,
                    n_sim, Z, rng, return_paths)
    bs = BlackScholes(S_0, K, r, sigma, T)
    V_0 = bs.option_price(option)
    delta_0 = bs.compute_delta(option)

    B_0 = V_0 - delta_0 * S_0

    B = np.zeros((n_sim, steps+1))
    B[:, 0] = B_0

    t = np.linspace(0, T, steps+1)
    tau = T - t
    tau[-1] = 1e-10

    bs = BlackScholes(S=S[0, :, :], K=K, r=r, sigma=sigma, T=tau)
    delta = bs.compute_delta(option)

    for i in range(1, steps+1):
        B[:, i] = B[:, i-1] * np.exp(r * dt)
        B[:, i] -= (delta[:, i] - delta[:, i-1]) * S[:, :, i].squeeze()

    payoff = np.maximum(S[:, :, -1].squeeze() - K, 0) if option == "call" else np.maximum(K - S[:, :, -1].squeeze(), 0)

    portfolio_value = delta[:, -1] * S[:, :, -1].squeeze() + B[:, -1]

    error = portfolio_value - payoff

    return error
