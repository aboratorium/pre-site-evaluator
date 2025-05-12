def calculate_metrics(equity, horizon, irr_target, use_case):
    # 🔹 Псевдореалистичные допущения (могут позже заменяться на динамические)
    annual_rent_income = 0.12 * equity
    operating_expenses = 0.3 * annual_rent_income
    noi = annual_rent_income - operating_expenses
    annual_debt_service = 0.08 * equity
    distributions = equity * (1 + (irr_target / 100)) ** horizon
    cap_on_land = equity * 0.6
    simulated_irr = irr_target - 1.5
    go_nogo = simulated_irr > irr_target - 2

    # 🔹 Расчёты
    cash_on_cash = (distributions - equity) / equity * 100
    dscr = noi / annual_debt_service

    return {
        "Cap on Land (€)": round(cap_on_land, 2),
        "Simulated IRR (%)": round(simulated_irr, 2),
        "Total Distributions (€)": round(distributions, 2),
        "Net Operating Income (€)": round(noi, 2),
        "Cash-on-Cash Return (%)": round(cash_on_cash, 2),
        "DSCR": round(dscr, 2),
        "Go/No-Go Recommendation": "Go ✅" if go_nogo else "No-Go ❌"
    }
