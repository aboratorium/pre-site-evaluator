def calculate_metrics(equity, horizon, irr_target, use_case):
    cap_on_land = equity * 0.6
    simulated_irr = irr_target - 1.5
    go_nogo = simulated_irr > irr_target - 2

    return {
        "Cap on Land (€)": round(cap_on_land, 2),
        "Simulated IRR (%)": round(simulated_irr, 2),
        "Go/No-Go Recommendation": "Go ✅" if go_nogo else "No-Go ❌"
    }