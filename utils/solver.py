from scipy.optimize import minimize

def optimize_project(metrics):
    """
    Простая заглушка для демонстрации оптимизации. Можно расширить.
    """
    def objective(x):
        # Пример: минимизировать отрицательный IRR (максимизировать IRR)
        equity, years = x
        return -(equity / (1 + years))  # условная функция

    bounds = [(100000, 1000000), (1, 15)]
    initial_guess = [metrics["equity"], metrics["years"]]

    result = minimize(objective, x0=initial_guess, bounds=bounds, method='SLSQP')
    
    return {
        "optimized_equity": round(result.x[0]),
        "optimized_years": int(result.x[1]),
        "success": result.success
    }
