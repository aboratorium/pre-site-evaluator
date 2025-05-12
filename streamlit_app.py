import streamlit as st
from utils.calc_metrics import calculate_metrics
from utils.load_data import load_benchmark_data
from utils.go_nogo import calc_go_nogo
from utils.sensitivity import run_sensitivity_analysis
from utils.monte_carlo import run_monte_carlo_simulation
from utils.solver import optimize_project

# === CONFIGURATION ===
st.set_page_config(page_title="Pre-Site Investment Evaluator", layout="wide")

# === CUSTOM CSS ===
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
        color: #262730;
    }
    .stSlider > div[data-baseweb="slider"] > div {
        background: #e3e4ea;
        padding: 10px;
        border-radius: 8px;
    }
    .stRadio > div {
        background-color: #f0f2f6;
        padding: 12px;
        border-radius: 8px;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .info-box {
        background-color: #e7f0ff;
        padding: 1rem;
        border-left: 5px solid #4a90e2;
        margin-top: 1rem;
        margin-bottom: 1rem;
        border-radius: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# === HEADER ===
st.title("🏗️ Pre-Site Investment Evaluator")
st.caption("Simulate ROI, cap on land and Go/No-Go recommendation — MVP 2025")

# === SECTION 1: Investment Inputs ===
st.subheader("1. Investment Inputs")
col1, col2 = st.columns([2, 2])

with col1:
    equity_input = st.number_input("💰 Equity Available (€)", value=500000, step=5000)

with col2:
    project_years = st.slider("⏳ Project Horizon (Years)", 1, 15, 5)

target_irr = st.slider("🎯 Target IRR (%)", 5.0, 25.0, 15.0, step=0.5)
st.markdown("<div class='info-box'>ℹ️ <b>Tip:</b> IRR (Internal Rate of Return) represents the expected annual return of the project. If unsure, leave the default value or use a market benchmark.</div>", unsafe_allow_html=True)
st.markdown("<div class='info-box'>📊 The model will use these inputs to simulate cash flows and evaluate viability.</div>", unsafe_allow_html=True)

# === SECTION 2: Development Use Mix ===
st.subheader("2. Development Use Mix")
st.write("Select development type:")
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
if st.button("🚀 Run Evaluation"):
    st.write("📡 Calculating financial metrics...")

    metrics = calculate_metrics(equity_input, project_years, target_irr, dev_choice)
    st.success("✅ Metrics calculated!")
    st.write(metrics)

    # Sensitivity Analysis
    st.write("📊 Sensitivity Analysis")
    sensitivity_df = run_sensitivity_analysis(metrics)
    st.dataframe(sensitivity_df)

    # Go/No-Go Recommendation
    st.write("🧭 Go/No-Go Recommendation")
    if isinstance(metrics, dict):
        try:
            decision = calc_go_nogo(metrics)
            st.markdown(f"**{decision}**")
        except Exception as e:
            st.error(f"❌ Unable to calculate recommendation: {e}")
    else:
        st.warning("⚠️ Metrics format invalid. Cannot evaluate recommendation.")

    # Monte Carlo Simulation
    st.write("🎲 Monte Carlo Simulation")
    simulation_results = run_monte_carlo_simulation(metrics)
    st.line_chart(simulation_results)

    # Optimization Suggestion
    st.write("🧠 Optimization Suggestion")
    optimal = optimize_project(metrics)
    st.json(optimal)
