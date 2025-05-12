import numpy as np
import pandas as pd
import altair as alt

def run_monte_carlo_simulation(n_simulations=500):
    np.random.seed(42)
    irr_samples = np.random.normal(loc=0.16, scale=0.03, size=n_simulations)
    irr_samples = np.clip(irr_samples, 0, 0.35)

    df = pd.DataFrame({'Simulated IRR': irr_samples * 100})
    chart = alt.Chart(df).mark_bar().encode(
        alt.X("Simulated IRR", bin=alt.Bin(maxbins=30), title="IRR (%)"),
        y="count()"
    ).properties(
        title="Monte Carlo Simulation of IRR",
        width=600,
        height=300
    )
    return chart
