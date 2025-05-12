def load_benchmark_data():
    return {
        "Residential": 17.5,
        "Hospitality": 15.2,
        "Mixed-Use": 16.8
    }

def get_cost_benchmarks():
    return {
        "Residential": {
            "construction_cost_per_m2": 1000,
            "marketing_cost_pct": 5,
            "other_costs_pct": 10
        },
        "Hospitality": {
            "construction_cost_per_m2": 1200,
            "marketing_cost_pct": 6,
            "other_costs_pct": 12
        },
        "Mixed-Use": {
            "construction_cost_per_m2": 1100,
            "marketing_cost_pct": 5.5,
            "other_costs_pct": 11
        }
    }
