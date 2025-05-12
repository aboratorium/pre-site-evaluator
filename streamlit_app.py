
import streamlit as st
from utils.load_data import load_benchmark_data
from utils.calc_metrics import calculate_metrics
from utils.go_nogo import calc_go_nogo
from utils.sensitivity import perform_sensitivity_analysis
from utils.monte_carlo import run_monte_carlo_simulation
from utils.solver import optimize_project

st.set_page_config(page_title="Pre-Site Investment Evaluator", layout="wide")

# Custom CSS for light theme and improved layout
st.markdown(
    """
    <style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        color: #1c1c1c;
        background-color: #f9f9f9;
    }
    .stSlider > div[data-baseweb="slider"] > div {
        background-color: #d6e4ff !important;
    }
    .stSlider > div[data-baseweb="slider"] > div > div {
        background-color: #1a73e8 !important;
    }
    .stButton>button {
        background-color: #1a73e8;
        color: white;
        border-radius: 4px;
    }
    .stButton>button:hover {
        background-color: #155ab6;
        color: white;
    }
    .block-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 2rem;
        color: #2e3b4e;
    }
    .subtext {
        font-size: 0.85rem;
        color: #666;
        margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏗️ Pre-Site Investment Evaluator")
st.caption("Simulate ROI, cap on land and Go/No-Go recommendation — MVP 2025")

# 1. Investment Inputs
st.markdown('<div class="block-title">1. Investment Inputs</div>', unsafe_allow_html=True)

equity = st.number_input("💰 Equity Available (€)", value=500000, step=10000)

col1, col2 = st.columns(2)
with col1:
    years = st.slider("⏳ Project Horizon (Years)", min_value=1, max_value=15, value=5)
with col2:
    irr_target = st.slider(
        "🎯 Target IRR (%)",
        min_value=5.0,
        max_value=25.0,
        value=15.0,
        step=0.5,
        help="💡 Benchmarks:
- Residential: 18–22%
- Hospitality: 14–17%
- Mixed-Use: 16–20%"
    )

st.info("ℹ️ The model will use these inputs to simulate cash flows and evaluate viability.")

# 2. Development Use Mix
st.markdown('<div class="block-title">2. Development Use Mix</div>', unsafe_allow_html=True)

benchmarks = load_benchmark_data()
selected_type = st.radio(
    "Select development type:",
    list(benchmarks.keys()),
    index=0,
    format_func=lambda x: f"{x} (IRR ~ {benchmarks[x]}%)"
)

# 3. Financial Evaluation
st.markdown('<div class="block-title">3. Financial Evaluation</div>', unsafe_allow_html=True)

if st.button("📊 Run Calculation"):
    with st.spinner("Calculating metrics..."):
        irr_real, cap_land, metrics = calculate_metrics(equity, years, selected_type, irr_target)
        go_decision = calc_go_nogo(irr_real, irr_target)

        st.subheader("📈 Financial Metrics")
        st.metric("IRR (Actual)", f"{irr_real:.2f}%")
        st.metric("Cap on Land (€)", f"{cap_land:,.0f}")
        st.metric("Go / No-Go", "✅ GO" if go_decision else "❌ NO-GO")

        st.markdown("---")
        st.subheader("📌 Explanation")
        st.write("The calculated IRR is compared to your target. The cap on land helps determine the maximum feasible land cost. The decision is based on whether the project exceeds your expected return.")

        st.markdown("---")
        st.subheader("🔍 Optional: Sensitivity Analysis")
        sensitivity_fig = perform_sensitivity_analysis()
        st.plotly_chart(sensitivity_fig)

        st.markdown("🔬 Monte Carlo Simulation (optional)")
        mc_fig = run_monte_carlo_simulation()
        st.plotly_chart(mc_fig)

        st.markdown("🧠 Solver Recommendation (optional)")
        suggestion = optimize_project()
        st.write(suggestion)
