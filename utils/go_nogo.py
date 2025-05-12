def calc_go_nogo(metrics: dict) -> str:
    """
    Determine Go/No-Go recommendation based on IRR and cap value.
    """
    try:
        irr = float(metrics.get("Simulated IRR (%)", 0))
        cap = float(metrics.get("Cap on Land (€)", 0))
    except (TypeError, ValueError):
        return "❓ Unable to evaluate"

    if irr >= 12.0 and cap <= 300000:
        return "Go ✅"
    elif irr < 10.0 or cap > 350000:
        return "No-Go ❌"
    else:
        return "Further Analysis 🔍"
