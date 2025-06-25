import streamlit as st
import matplotlib.pyplot as plt

# Slab Billing Function
def calculate_bill(units):
    if units <= 100:
        return units * 5
    elif units <= 200:
        return 100 * 5 + (units - 100) * 7
    else:
        return 100 * 5 + 100 * 7 + (units - 200) * 10

st.title("Electricity Usage Analyzer (with Slab Billing)")

# Input: Number of days
days = st.number_input("Enter number of days", min_value=1, step=1)
threshold = st.number_input("Enter high usage threshold", min_value=0.0, step=0.1)

# Input: Daily usage
usage = []
if days:
    st.subheader("Enter units consumed each day:")
    for i in range(int(days)):
        unit = st.number_input(f"Day {i + 1}", min_value=0.0, step=0.1, key=i)
        usage.append(unit)

# Button: Analyze
if st.button("Analyze"):
    total = sum(usage)
    avg = total / days
    max_unit = max(usage)
    min_unit = min(usage)
    bill = calculate_bill(total)

    st.subheader("Summary")
    st.write(f"Total Units: {total}")
    st.write(f"Average Usage: {avg:.2f} units/day")
    st.write(f"Highest Usage: {max_unit} units on Day {usage.index(max_unit)+1}")
    st.write(f"Lowest Usage: {min_unit} units on Day {usage.index(min_unit)+1}")
    st.write(f"Estimated Bill (Slab Based): ₹{bill:.2f}")

    # High usage alert
    st.subheader("High Usage Days")
    high_days = [f"Day {i+1}: {u} units" for i, u in enumerate(usage) if u > threshold]
    if high_days:
        for day in high_days:
            st.write(f"⚠️ {day}")
    else:
        st.write("No high usage days found.")

# Button: Show chart
if st.button("Show Chart"):
    st.subheader("Daily Usage Chart")
    fig, ax = plt.subplots()
    ax.bar(range(1, int(days)+1), usage, color='skyblue')
    ax.set_xlabel("Day")
    ax.set_ylabel("Units")
    ax.set_title("Daily Electricity Usage")
    st.pyplot(fig)


