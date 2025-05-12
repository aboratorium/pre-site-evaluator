import pandas as pd

def run_sensitivity_analysis(metrics: dict) -> pd.DataFrame:
    """
    Simulates a basic sensitivity analysis by showing how changes in key variables
    (like construction cost or revenue) affect the IRR.

    Parameters:
        metrics (dict): A dictionary of calculated financial metrics, including
                        construction cost, revenue, IRR, etc.

    Returns:
        pd.DataFrame: A summary DataFrame of parameter changes and their impact on IRR.
    """
    # Example base values (could be extracted from metrics in advanced version)
    base_cost = 1000000
    base_revenue = 1300000
    base_irr = metrics.get("Simulated IRR (%)", 10)

    # Simulate +10%/-10% changes
    variations = [
        {"Parameter": "Construction Cost", "Change": "+10%", "IRR Impact (%)": round(base_irr - 2.5, 2)},
        {"Parameter": "Construction Cost", "Change": "-10%", "IRR Impact (%)": round(base_irr + 2.5, 2)},
        {"Parameter": "Revenue", "Change": "+10%", "IRR Impact (%)": round(base_irr + 3.0, 2)},
        {"Parameter": "Revenue", "Change": "-10%", "IRR Impact (%)": round(base_irr - 3.0, 2)},
    ]

    return pd.DataFrame(variations)
