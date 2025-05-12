def calc_go_nogo(irr, target_irr):
    """
    Простое правило: если IRR >= целевого, даём рекомендацию Go.
    """
    if irr is None:
        return "⚠️ Недостаточно данных"
    if irr >= target_irr:
        return "✅ GO — проект соответствует требованиям"
    else:
        return "❌ NO-GO — доходность ниже цели"