
import streamlit as st
from utils.calc_metrics import calculate_metrics
from utils.go_nogo import calc_go_nogo
from utils.load_data import get_cost_benchmarks

st.set_page_config(page_title="Pre-Site Investment Evaluator", layout="wide")

st.title("🏗️ Pre-Site Investment Evaluator")
st.markdown("Simulate ROI, cap on land and Go/No-Go recommendation — MVP 2025")

# 1. Investment Inputs
st.header("1. Investment Inputs")
equity = st.number_input("💰 Equity Available (€)", value=500000, step=10000)
project_horizon = st.slider("⏳ Project Horizon (Years)", 1, 15, 5)
target_irr = st.slider("🎯 Target IRR (%)", 5.0, 25.0, 15.0)

st.info("ℹ️ The model will use this information to simulate cash flows and evaluate viability.")

# 2. Development Use Mix
st.header("2. Development Use Mix")
use_type = st.radio("Select development type:", ["🏘 Residential (IRR ~ 18–22%)", "🏨 Hospitality (IRR ~ 14–17%)", "🏙 Mixed-Use (IRR ~ 16–20%)"])

# 3. Financial Evaluation
st.header("3. Financial Evaluation")
if st.button("🔍 Run Calculation"):
    cap_on_land, metrics = calculate_metrics(equity, project_horizon, target_irr, use_type)
    
    st.subheader("🏷️ Cap on Land")
    st.success(f"Maximum land acquisition price: €{cap_on_land:,.0f}")

    st.subheader("📊 Financial Metrics")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("IRR", f"{metrics['irr']:.2%}")
    col2.metric("NPV", f"€{metrics['npv']:,.0f}")
    col3.metric("MIRR", f"{metrics['mirr']:.2%}")
    col4.metric("P(Gain)", f"{metrics['p_gain']:.1%}")

    st.subheader("🚦 Recommendation")
    go_nogo = calc_go_nogo(metrics, target_irr)
    if go_nogo:
        st.success("✅ Recommendation: GO")
    else:
        st.error("❌ Recommendation: NO-GO")

st.caption("Prototype powered by Streamlit · Python · Staiger & ULI methods")
