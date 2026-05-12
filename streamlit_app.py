import streamlit as st
import pandas as pd
import datetime

# --- APP CONFIG ---
st.set_page_config(page_title="FinanceFlow", layout="wide")
st.title("💰 Monthly Finance Tracker")

# Load existing data or create new
try:
    df = pd.read_csv("finances.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Date", "Category", "Description", "Amount"])

# --- SIDEBAR INPUT ---
st.sidebar.header("Add New Transaction")
with st.sidebar.form("input_form", clear_on_submit=True):
    date = st.date_input("Date", datetime.date.today())
    category = st.selectbox("Category", ["Rent", "Food", "Transport", "Savings", "Utilities", "Other"])
    desc = st.text_input("Description")
    amount = st.number_input("Amount ($)", min_value=0.0, step=0.01)
    submit = st.form_submit_button("Add Record")

if submit:
    new_data = pd.DataFrame([[date, category, desc, amount]], columns=df.columns)
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv("finances.csv", index=False)
    st.success("Transaction Added!")

# --- DASHBOARD CALCULATIONS ---
st.header("Financial Overview")

# Metric Row
total_spent = df["Amount"].sum()
col1, col2 = st.columns(2)
col1.metric("Total Spending", f"${total_spent:,.2f}")
col2.metric("Transactions", len(df))

# Auto-Calculation by Category
st.subheader("Spending by Category")
category_totals = df.groupby("Category")["Amount"].sum()
st.bar_chart(category_totals)

# Raw Data View
with st.expander("View Full Transaction History"):
    st.dataframe(df.sort_values(by="Date", ascending=False), use_container_width=True)
