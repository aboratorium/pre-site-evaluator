import streamlit as st
from utils.calc_metrics import calculate_metrics
from utils.load_data import load_benchmark_data
from utils.go_nogo import calc_go_nogo
from utils.sensitivity import run_sensitivity_analysis
from utils.monte_carlo import run_monte_carlo_simulation
from utils.solver import optimize_project

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    body {
        background-color: #f8f9fa;
        color: #333;
    }
    .stSlider > div[data-baseweb="slider"] > div {
        background: #ffffff;
        padding: 10px;
        border-radius: 8px;
    }
    .stRadio > div {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 8px;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .info-box {
        background-color: #e9f0fc;
        padding: 1rem;
        border-left: 5px solid #4d7cc1;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- TITLE ---
st.title("🏗️ Pre-Site Investment Evaluator")
st.caption("Simulate ROI, land cap & Go/No-Go decision — MVP 2025")

# === SECTION 1: Investment Inputs ===
st.subheader("1. Investment Inputs")
st.info("📘 Define your initial equity, target IRR (desired return), and project horizon (how many years you plan to hold/build).")

col1, col2 = st.columns([2, 2])

with col1:
    equity_input = st.number_input("💰 Equity Available (€)", value=500000, step=10000)

with col2:
    project_years = st.slider("⏳ Project Horizon (Years)", 1, 20, 5)

target_irr = st.slider("🎯 Target IRR (%)", 5.0, 25.0, 15.0, step=0.5)
st.markdown("<div class='info-box'>ℹ️ <b>IRR (Internal Rate of Return)</b> represents the expected annual return of the project. If unsure, leave the default value or use a market benchmark.</div>", unsafe_allow_html=True)

# === SECTION 2: Development Use Mix ===
st.subheader("2. Development Use Mix")
st.info("📘 Choose the type of development you’re considering. If unsure, the tool will suggest the option with the strongest benchmark IRR.")

dev_options = ["🏠 Residential", "🏨 Hospitality", "🏙️ Mixed-Use", "❓ I’m not sure yet"]
dev_choice = st.radio("", dev_options, index=0)

benchmark_data = load_benchmark_data()
if dev_choice != "❓ I’m not sure yet":
    dev_key = dev_choice.split(" ")[1]
    st.markdown(f"<div class='info-box'>📈 Estimated market IRR for {dev_key}: {benchmark_data[dev_key]}%</div>", unsafe_allow_html=True)
else:
    best_use = max(benchmark_data, key=benchmark_data.get)
    st.markdown(f"<div class='info-box'>🔎 Based on current benchmarks, the most viable option is: <b>{best_use}</b> (IRR: {benchmark_data[best_use]}%)</div>", unsafe_allow_html=True)

# === SECTION 3: Financial Evaluation ===
st.subheader("3. Financial Evaluation")
st.info("📘 These are the key investment metrics based on your inputs, including simulated IRR and max land cost to meet your target.")

if st.button("🚀 Run Evaluation"):
    st.write("📡 Calculating...")

    metrics = calculate_metrics(equity_input, project_years, target_irr, dev_choice)

    st.success("✅ Financial Metrics:")
    for k, v in metrics.items():
        st.markdown(f"**{k}**: {v}")

    st.subheader("🧭 Final Recommendation")
    st.info("📘 The Go / No-Go result helps you understand if the deal meets basic profitability thresholds.")
    decision = calc_go_nogo(metrics)
    st.markdown(f"### ✅ **{decision}**")

    st.subheader("📊 Sensitivity Analysis")
    st.info("📘 Explore how sensitive the result is to changes in core assumptions (like construction costs or rent).")
    sensitivity_df = run_sensitivity_analysis(metrics)
    st.dataframe(sensitivity_df)

    st.subheader("🎲 Monte Carlo Simulation")
    st.info("📘 Run a probabilistic forecast showing likely variations in project return based on uncertain inputs.")
    simulation_results = run_monte_carlo_simulation(metrics)
    st.line_chart(simulation_results)

    st.subheader("🧠 Optimization Results")
    st.info("📘 Suggests better input values (e.g., lower land cost or higher rent) to help your project meet the target return.")
    optimal = optimize_project(metrics)
    for k, v in optimal.items():
        st.markdown(f"**{k}**: {v}")
