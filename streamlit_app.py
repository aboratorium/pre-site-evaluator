import streamlit as st
from utils.load_data import load_benchmark_data
from utils.calc_metrics import calculate_metrics
from utils.go_nogo import calc_go_nogo
from utils.sensitivity import run_sensitivity_analysis
from utils.monte_carlo import run_monte_carlo_simulation
from utils.solver import optimize_project

# === UI SETUP ===
st.set_page_config(page_title="Pre-Site Evaluator", layout="centered")
st.markdown("## 🏗️ Pre-Site Investment Evaluator")
st.markdown("Simulate ROI, cap on land and Go/No-Go recommendation — **MVP 2025**")

st.markdown("---")
st.markdown("### 1. Investment Inputs")

equity = st.number_input("💰 Equity Available (€)", min_value=10000, value=500000, step=10000)

col1, col2 = st.columns(2)
with col1:
    horizon = st.slider("⏳ Project Horizon (Years)", 1, 15, 5)
with col2:
    irr_target = st.slider("🎯 Target IRR (%)", 5.0, 25.0, 15.0, step=0.5)

# IRR context note
with st.expander("ℹ️ What does IRR mean and what's a good target?"):
    st.markdown("""
    **Internal Rate of Return (IRR)** is the annualized return rate a project is expected to generate.  
    - In real estate, a typical **acceptable IRR ranges from 14% to 20%** depending on risk.  
    - For example:
        - Residential → 18–22%  
        - Hospitality → 14–17%  
        - Mixed-Use → 16–20%
    
    A higher IRR = higher risk/return. Make sure to compare with benchmark values below.
    """)

st.info("The model will use these inputs to simulate cash flows and evaluate viability.")

# === DEVELOPMENT TYPE ===
st.markdown("### 2. Development Use Mix")

benchmarks = load_benchmark_data()
dev_type = st.radio("Select development type:", options=list(benchmarks.keys()), index=0,
                    format_func=lambda x: f"{x} (IRR ~ {benchmarks[x]}%)")

# Auto-suggestion for IRR
st.caption(f"📊 Benchmark IRR for **{dev_type}** projects is approx. **{benchmarks[dev_type]}%**")

# === CALCULATION BLOCK ===
st.markdown("### 3. Financial Evaluation")

if st.button("▶️ Run Calculation"):
    st.success("Running simulations...")

    # Placeholder outputs (logic can be extended)
    metrics = calculate_metrics(equity, irr_target, horizon, dev_type)
    recommendation = calc_go_nogo(metrics["irr"], irr_target)

    st.subheader("📈 Financial Metrics")
    st.write(metrics)

    st.markdown("#### ✅ Go/No-Go Recommendation:")
    if recommendation:
        st.success("Go! The project meets target return expectations.")
    else:
        st.error("No-Go. Project IRR is below your target threshold.")

    with st.expander("📊 Sensitivity Analysis"):
        fig = run_sensitivity_analysis()
        st.pyplot(fig)

    with st.expander("🎲 Monte Carlo Simulation"):
        chart = run_monte_carlo_simulation()
        st.altair_chart(chart, use_container_width=True)

    with st.expander("🔍 Solver Recommendation"):
        solution = optimize_project(equity, irr_target)
        st.code(solution)
