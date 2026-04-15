import numpy as np

from black_scholes import BlackScholes

def monte_carlo(S_0=100, r=0.05, sigma=0.2, T=1.0, steps=252,
    n_sim=10000, Z=None, rng=None, return_paths=True):
    
    dt = T / steps

    S_0 = np.array(S_0 if isinstance(S_0, list) else [S_0]).flatten()

    if Z is None:
        if rng is None:
            rng = np.random.default_rng()
        Z = rng.standard_normal((n_sim, steps))

    drift = (r - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    log_returns = drift + diffusion

    log_S = np.cumsum(log_returns, axis=1)
    log_S = np.hstack([np.zeros((n_sim, 1)), log_S])

    S = S_0[:, None, None] * np.exp(log_S)[None, :, :]

    if return_paths:
        return S
    else:
        return S[:, :, -1]