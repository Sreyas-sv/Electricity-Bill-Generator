import streamlit as st
import matplotlib.pyplot as plt

# --- Page config ---
st.set_page_config(page_title="Electricity Usage Analyzer", layout="wide")

# --- Remove top white bar & set background color ---
st.markdown("""
    <style>
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {
        background: none;
    }
    html, body, [data-testid="stApp"] {
        background-color: #C6E2FF;
    }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.markdown("## ⚡ Electricity Usage Analyzer")
st.write("Input daily usage, analyze consumption trends, and calculate slab-wise billing with a modern interface.")

# --- Session state to manage toggles ---
if 'show_chart' not in st.session_state:
    st.session_state.show_chart = False
if 'analyze_clicked' not in st.session_state:
    st.session_state.analyze_clicked = False

# --- Layout: 3 Columns ---
col1, col2, col3 = st.columns([1.2, 1.5, 1.5])

# --- Column 1: Inputs ---
with col1:
    st.markdown("### 🛠️ Input Details")

    num_days = st.number_input("📅 Number of days", min_value=1, max_value=30, value=2, step=1)
    threshold = st.number_input("💡 High usage threshold", min_value=0.0, step=0.1, format="%.2f")

    st.markdown("### 🧮 Enter units consumed each day")
    units = []
    for i in range(num_days):
        units.append(st.number_input(f"Day {i+1}", min_value=0.0, step=0.1, key=f"day_{i}"))

    col_btn1, col_btn2 = st.columns(2)

    if col_btn1.button("🔍 Analyze"):
        st.session_state.analyze_clicked = True

    if col_btn2.button("📊 Show Chart" if not st.session_state.show_chart else "❌ Hide Chart"):
        st.session_state.show_chart = not st.session_state.show_chart

# --- Function to calculate slab-wise bill ---
def calculate_slab_bill(units):
    if units <= 50:
        return units * 3
    elif units <= 200:
        return (50 * 3) + ((units - 50) * 5)
    else:
        return (50 * 3) + (150 * 5) + ((units - 200) * 8)

# --- Column 2: Usage Summary ---
if st.session_state.analyze_clicked:
    with col2:
        total_units = sum(units)
        average_units = total_units / num_days
        estimated_bill = calculate_slab_bill(total_units)
        highest = max(units)
        lowest = min(units)
        high_day = units.index(highest) + 1
        low_day = units.index(lowest) + 1

        st.markdown("### 📈 Usage Summary")
        col_sum1, col_sum2 = st.columns(2)
        with col_sum1:
            st.metric("Total Units", f"{total_units:.2f}")
        with col_sum2:
            st.metric("Estimated Bill", f"₹{estimated_bill:.2f}")

        st.write(f"📊 **Average Usage**: {average_units:.2f} units/day")
        st.write(f"🔺 **Highest Usage**: {highest} units on Day {high_day}")
        st.write(f"🔻 **Lowest Usage**: {lowest} units on Day {low_day}")

        # Slab info (just for reference)
        st.selectbox(
            "📋 Slab Bill Breakdown",
            [
                "Slab A: 0–50 units – ₹3/unit",
                "Slab B: 51–200 units – ₹5/unit",
                "Slab C: 201+ units – ₹8/unit"
            ]
        )

        st.markdown("### 🚨 High Usage Days")
        high_days = [(i+1, u) for i, u in enumerate(units) if u > threshold]
        if high_days:
            for day, val in high_days:
                st.write(f"⚠️ Day {day}: {val} units")
        else:
            st.success("✅ No high usage days.")

# --- Column 3: Chart ---
if st.session_state.show_chart:
    with col3:
        st.markdown("### 📊 Daily Usage Chart")
        fig, ax = plt.subplots()
        ax.bar([f"Day {i+1}" for i in range(num_days)], units, color='skyblue')
        ax.set_ylabel("Units")
        ax.set_xlabel("Day")
        ax.set_title("Daily Electricity Usage")
        st.pyplot(fig)
