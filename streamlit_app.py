import streamlit as st
from utils.load_data import load_benchmark_data

st.set_page_config(page_title="Pre-Site Evaluator", layout="wide")

st.title("🏗️ Pre-Site Real Estate Evaluator")

st.markdown("## 1. 💰 Investment Parameters")
equity = st.number_input("Available Equity (€)", min_value=50000, value=300000, step=10000)
horizon = st.slider("Project Duration (Years)", 1, 15, 5)
target_irr = st.slider("Target IRR (%)", 5.0, 25.0, 15.0)

st.markdown("## 2. 🏘️ Development Function")
dev_type = st.radio(
    "Select Development Type",
    ["Residential", "Hospitality", "Mixed-Use"],
    help="Each has different IRR benchmarks and construction durations"
)

st.markdown("## 3. 📊 Model Explanation")
st.info("This tool uses cash flow modeling and DCF to simulate return scenarios.
"
        "All IRR values are calculated using realistic assumptions and benchmark data.")

# Load benchmark and display example
benchmarks = load_benchmark_data()
if dev_type in benchmarks:
    st.metric(f"📈 Market IRR (avg) for {dev_type}", f"{benchmarks[dev_type]}%")

st.markdown("---")
st.markdown("Built with ❤️ to make real estate analysis accessible.")