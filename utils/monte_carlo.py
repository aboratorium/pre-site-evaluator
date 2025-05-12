import numpy as np
import pandas as pd

def run_monte_carlo_simulation(metrics: dict, simulations: int = 500) -> pd.DataFrame:
    """
    Run Monte Carlo simulation on the projected IRR based on metrics.
    Returns a DataFrame of simulated IRR outcomes.
    """
    try:
        # Attempt to extract and convert IRR from metrics dictionary
        base_irr = float(metrics.get("Simulated IRR (%)", 0)) / 100  # Convert from % to decimal
        if base_irr <= 0:
            raise ValueError("IRR must be a positive number")
    except Exception:
        # Fallback to a default average IRR if extraction fails
        base_irr = 0.12  # 12% average as a safe fallback

    # Generate samples with normal distribution
    irr_samples = np.random.normal(loc=base_irr, scale=0.03, size=simulations)
    
    # Clamp values between 0% and 100% for realism
    irr_samples = np.clip(irr_samples, 0, 1)

    # Convert to percentage format for display
    return pd.DataFrame({
        "Simulated IRR (%)": np.round(irr_samples * 100, 2)
    })
