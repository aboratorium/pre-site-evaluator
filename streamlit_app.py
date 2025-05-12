import streamlit as st
from utils.load_data import load_benchmark_data
from utils.calc_metrics import calculate_metrics
from utils.go_nogo import calc_go_nogo

# ——— Apply Custom Styling ———
def inject_custom_css():
    st.markdown("""
        <style>
            .stApp {
                background-color: #ffffff;
            }
            .stSlider > div > div {
                background: #1d4ed8 !important;
            }
            .stButton>button {
                background-color: #1d4ed8;
                color: white;
                border-radius: 4px;
            }
            .block-container {
                padding: 2rem 2rem 2rem 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# ——— Title & Intro ———
st.title("🏗️ Pre-Site Investment Evaluator")
st.caption("Simulate ROI, cap on land and Go/No-Go recommendation — MVP 2025")

# ——— 1. Investment Inputs ———
st.header("1. Investment Inputs")

equity = st.number_input("💰 Equity Available (€)", min_value=10000, value=500000, step=10000)
horizon = st.slider("⏳ Project Horizon (Years)", 1, 15, value=5)
target_irr = st.slider("🎯 Target IRR (%)", 5.0, 25.0, value=15.0, step=0.5)

st.info("ℹ️ The model will use these inputs to simulate cash flows and evaluate viability.")

# ——— 2. Development Use Mix ———
st.header("2. Development Use Mix")

benchmark_data = load_benchmark_data()

selected_mix = st.radio("Select development type:", list(benchmark_data.keys()))
benchmark_irr = benchmark_data[selected_mix]

st.markdown(f"📊 **Benchmark IRR for {selected_mix}: ~ {benchmark_irr:.1f}%**  \n_(Based on historical data and regional trends)_")

# ——— 3. Financial Evaluation ———
st.header("3. Financial Evaluation")

if st.button("📉 Run Calculation"):
    metrics = calculate_metrics(
        equity_amount=equity,
        project_years=horizon,
        irr_target=target_irr,
        dev_type=selected_mix
    )
    recommendation = calc_go_nogo(metrics)

    st.subheader("📊 Financial Metrics")
    st.write(metrics)

    st.subheader("🚦 Go / No-Go Recommendation")
    st.success("✅ GO: Project meets target criteria") if recommendation else st.error("🚫 NO-GO: Project below target thresholds")

# ——— Footer ———
st.caption("Prototype powered by Streamlit · Python · Staiger & ULI methods")
