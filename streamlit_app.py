import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from numpy_financial import irr, npv

st.set_page_config(page_title="🏗️ Pre-Site Investment Evaluator", layout="wide")
st.title("🏗️ Pre-Site Investment Evaluator")
st.caption("Simulate ROI, cap on land and Go/No-Go recommendation — MVP 2025")

# --- Step 1: Inputs ---
st.header("1. Investment Inputs")
col1, col2, col3 = st.columns(3)
with col1:
    equity = st.number_input("💰 Equity Available (€)", 50000, 5000000, 500000, step=50000)
with col2:
    horizon = st.slider("⏳ Project Horizon (Years)", 1, 15, 5)
with col3:
    target_irr = st.slider("🎯 Target IRR (%)", 5.0, 25.0, 15.0, step=0.5)

st.markdown("ℹ️ The model will use this information to simulate cash flows and evaluate viability.")

# --- Step 2: Select Scenario ---
st.header("2. Development Use Mix")
scenario = st.radio("Select development type:", [
    "🏘️ Residential (IRR ~ 18–22%)", 
    "🏨 Hospitality (IRR ~ 14–17%)", 
    "🏢 Mixed-Use (IRR ~ 16–20%)"
])

# --- Step 3: Calculations ---
st.header("3. Financial Evaluation")
if st.button("🧮 Run Calculation"):
    # Assumed project cash flows (demo)
    annual_income = 0.18 * equity
    cashflows = [-equity] + [annual_income] * (horizon - 1) + [equity * 1.3]  # simple return

    irr_value = irr(cashflows)
    discount_rate = target_irr / 100
    npv_value = npv(discount_rate, cashflows)

    land_cap_limit = 0.2 * equity  # Dummy logic: max 20% of equity into land

    st.subheader("📊 Financial Metrics")
    st.markdown(f"- IRR: **{irr_value*100:.2f}%**")
    st.markdown(f"- NPV: **€{npv_value:,.0f}** at {target_irr:.1f}% discount")
    st.markdown(f"- Suggested Max Land Cost (Cap on Land): **€{land_cap_limit:,.0f}**")

    go_status = "✅ Go" if irr_value >= discount_rate else "❌ No-Go"
    st.subheader(f"🔎 Recommendation: {go_status}")

    st.markdown("---")
    st.markdown("📉 IRR Distribution (Simulated)")

    # Monte Carlo simulation (demo)
    mc_irr = np.random.normal(loc=irr_value, scale=0.03, size=1000)
    fig, ax = plt.subplots()
    ax.hist(mc_irr, bins=30, alpha=0.7)
    ax.axvline(discount_rate, color='red', linestyle='--', label='Target IRR')
    ax.set_title("Simulated IRR Distribution")
    ax.legend()
    st.pyplot(fig)

st.caption("Prototype powered by Streamlit · Python · Staiger & ULI methods")