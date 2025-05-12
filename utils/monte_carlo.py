import numpy as np

def run_monte_carlo(model_func, param_ranges, num_simulations=1000):
    results = []

    for _ in range(num_simulations):
        sample = {
            key: np.random.triangular(*value) if isinstance(value, tuple) else value
            for key, value in param_ranges.items()
        }
        result = model_func(**sample)
        results.append(result)

    return results