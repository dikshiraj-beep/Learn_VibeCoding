import streamlit as st

st.set_page_config(page_title="Simple Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Simple Calculator")
st.write("Enter two numbers, choose an operation, and hit Calculate.")

col1, col2 = st.columns(2)
with col1:
    num1 = st.number_input("First number", value=0.0, format="%f")
with col2:
    num2 = st.number_input("Second number", value=0.0, format="%f")

operation = st.selectbox(
    "Operation",
    ("Addition", "Subtraction", "Multiplication", "Division"),
)

if st.button("Calculate"):
    if operation == "Addition":
        result = num1 + num2
    elif operation == "Subtraction":
        result = num1 - num2
    elif operation == "Multiplication":
        result = num1 * num2
    else:  # Division
        if num2 == 0:
            st.error("Cannot divide by zero. Please enter a non-zero second number.")
            result = None
        else:
            result = num1 / num2

    if result is not None:
        st.success(f"Result: {result}")
