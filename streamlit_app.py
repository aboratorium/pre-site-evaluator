import streamlit as st
from utils.load_data import load_benchmark_data
from utils.calc_metrics import calculate_metrics
from utils.go_nogo import calc_go_nogo
from utils.sensitivity import run_sensitivity_analysis
from utils.monte_carlo import run_monte_carlo_simulation
from utils.solver import solve_optimal_inputs  # <-- корректный импорт

# --- Custom Styling ---
st.set_page_config(page_title="Pre-Site Evaluator", layout="wide")

st.markdown(
    """
    <style>
    body {
        background-color: #f9f9f9;
        color: #222;
    }
    .stSlider > div {
        background: #dee2e6;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- App Title ---
st.title("🏗️ Pre-Site Investment Evaluator")
st.caption("Simulate ROI, cap on land and Go/No-Go recommendation — MVP 2025")

# --- Section 1: Investment Inputs ---
st.header("1. Investment Inputs")

equity = st.number_input("💰 Equity Available (€)", min_value=10000, step=50000, value=500000)

col1, col2 = st.columns(2)
with col1:
    horizon = st.slider("⏳ Project Horizon (Years)", 1, 15, 5)
with col2:
    target_irr = st.slider("🎯 Target IRR (%)", 5.0, 25.0, 15.0, step=0.5)
    st.caption("ℹ️ Tip: Set a realistic IRR target based on market benchmarks.")

st.info("The model will use these inputs to simulate cash flows and evaluate viability.")

# --- Section 2: Development Mix ---
st.header("2. Development Use Mix")
benchmark_data = load_benchmark_data()

project_type = st.radio("Select development type:", list(benchmark_data.keys()))
st.caption(f"📊 Estimated market IRR for {project_type}: {benchmark_data[project_type]}%")

# --- Section 3: Evaluation ---
st.header("3. Financial Evaluation")

if st.button("📈 Run Calculation"):
    irr = benchmark_data[project_type]
    result = calculate_metrics(equity, horizon, irr)

    st.subheader("📊 Financial Metrics")
    st.write(result)

    cap_land = result.get("Cap on Land", "N/A")
    st.metric("🔹 Cap on Land (€)", f"{cap_land:,.0f}" if isinstance(cap_land, (int, float)) else cap_land)

    st.subheader("🚦 Go / No-Go Recommendation")
    recommendation = calc_go_nogo(result.get("IRR", 0), target_irr)
    st.success(f"Recommendation: **{recommendation}**")

    st.subheader("📉 Sensitivity Analysis")
    sens = run_sensitivity_analysis(equity, horizon, irr)
    st.dataframe(sens)

    st.subheader("🎲 Monte Carlo Simulation")
    mc_result = run_monte_carlo_simulation(equity, horizon, irr)
    st.write(mc_result)

    st.subheader("🧠 Solver Optimization")
    st.write("Running optimization based on target IRR and constraints...")
    optimal = solve_optimal_inputs(
        objective_func=lambda x: abs(x[0] * 0.18 - target_irr),  # Dummy
        initial_guess=[1.0],
        bounds=[(0.1, 2.0)]
    )
    st.write("Optimal factor:", optimal.x[0])

st.markdown("---")
st.caption("Prototype powered by Streamlit · Python · Staiger & ULI methods")
