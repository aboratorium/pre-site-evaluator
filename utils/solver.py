from scipy.optimize import minimize

def solve_optimal_inputs(objective_func, initial_guess, bounds, constraints=()):
    result = minimize(
        objective_func,
        x0=initial_guess,
        bounds=bounds,
        constraints=constraints,
        method='SLSQP'
    )
    return result
