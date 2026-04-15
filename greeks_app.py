import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

from black_scholes import BlackScholes

st.title("Black-Scholes Numerical Greeks Explorer")

S = st.slider("Stock Price (S)", 50.0, 150.0, 100.0)
K = st.slider("Strike (K)", 50.0, 150.0, 100.0)
r = st.slider("Interest Rate (r)", 0.0, 0.1, 0.05)
sigma = st.slider("Volatility (σ)", 0.05, 0.5, 0.2)
T = st.slider("Maturity (T)", 0.01, 2.0, 1.0)

h_values = np.logspace(-8, -1, 60)

model = BlackScholes(S, K, r, sigma, T)

delta = model.compute_delta()
gamma = model.compute_gamma()
vega = model.compute_vega()
theta = model.compute_theta()
rho = model.compute_rho()

delta_num = model.compute_delta_num(h=h_values)
gamma_num = model.compute_gamma_num(h=h_values)
vega_num = model.compute_vega_num(h=h_values)
theta_num = model.compute_theta_num(h=h_values)
rho_num = model.compute_rho_num(h=h_values)

delta_errors = abs(delta - delta_num)
gamma_errors = abs(gamma - gamma_num)
vega_errors = abs(vega - vega_num)
theta_errors = abs(theta - theta_num)
rho_errors = abs(rho - rho_num)

show_delta = st.checkbox("Show Delta", True)
show_gamma = st.checkbox("Show Gamma", True)
show_vega = st.checkbox("Show Vega", False)
show_theta = st.checkbox("Show Theta", False)
show_rho = st.checkbox("Show Rho", False)

fig, ax = plt.subplots()

if show_delta:
    ax.loglog(h_values, delta_errors, label="Delta Error")

if show_gamma:
    ax.loglog(h_values, gamma_errors, label="Gamma Error")

if show_vega:
    ax.loglog(h_values, vega_errors, label="Vega Error")

if show_theta:
    ax.loglog(h_values, theta_errors, label="Theta Error")

if show_rho:
    ax.loglog(h_values, rho_errors, label="Rho Error")

ax.set_xlabel("Log of step size h")
ax.set_ylabel("Log of error")

if show_delta or show_gamma or show_vega or show_theta or show_rho:
    ax.legend(bbox_to_anchor=(1.0, 1.0))

ax.grid(True)

st.pyplot(fig)