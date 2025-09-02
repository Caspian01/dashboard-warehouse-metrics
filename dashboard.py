# dashboard_kpis.py
import pandas as pd
import streamlit as st
import plotly.express as px

# --- Page Configuration for Better Layout ---
st.set_page_config(layout="wide")

# --- Scenario Selection ---
st.sidebar.title("Scenario Selector")
scenario = st.sidebar.selectbox(
    "Choose Warehouse Scenario",
    ["High Volume", "Low Volume", "Unexpected Spike"]
)

# Map scenario names to file paths
file_map = {
    "High Volume": "high_volume_warehouse_data.csv",
    "Low Volume": "low_volume_warehouse_data.csv",
    "Unexpected Spike": "unexpected_spike_warehouse_data.csv"
}

# --- Load dataset dynamically ---
df = pd.read_csv(file_map[scenario])

# --- Data Preparation ---
df['Date'] = pd.to_datetime(df['Date'])
df['Total_Orders'] = df['Inbound_Orders'] + df['Outbound_Orders']

st.title(f"WTDC - Warehouse Metrics Dashboard ({scenario})")

# --- KPI Section ---
st.subheader("Key Performance Indicators")

total_inbound = df['Inbound_Orders'].sum()
total_outbound = df['Outbound_Orders'].sum()
avg_scan_time = round(df['Avg_Scan_Time_s'].mean(), 2)
inventory_turnover = round(total_outbound / df['Inventory_Level'].mean(), 2)

peak_day_index = df['Total_Orders'].idxmax()
peak_day = df.loc[peak_day_index, 'Date'].strftime('%m/%d/%y')

# KPIs in two rows (3 + 2)
col1, col2, col3 = st.columns(3)
col1.metric("Total Inbound Orders", total_inbound)
col2.metric("Total Outbound Orders", total_outbound)
col3.metric("Avg Scan Time (s)", avg_scan_time)

col4, col5 = st.columns(2)
col4.metric("Inventory Turnover", inventory_turnover)
col5.metric("Peak Day", peak_day)

# --- Optional Date Range Filter ---
st.subheader("Visualizations")

min_date = df['Date'].min().date()
max_date = df['Date'].max().date()

start_date, end_date = st.slider(
    "Select Date Range:",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date)
)

df_filtered = df[(df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)]

# --- Visualizations ---
fig_orders = px.line(
    df_filtered, x='Date', y=['Inbound_Orders', 'Outbound_Orders'],
    title='Inbound vs Outbound Orders Over Time'
)
st.plotly_chart(fig_orders, use_container_width=True)

fig_inventory = px.bar(
    df_filtered, x='Date', y='Inventory_Level',
    title='Inventory Levels per Day'
)
st.plotly_chart(fig_inventory, use_container_width=True)

fig_scan = px.scatter(
    df_filtered, x='Avg_Scan_Time_s', y='Outbound_Orders',
    size='Inbound_Orders', color='Date',
    title='Scan Time vs Orders'
)
st.plotly_chart(fig_scan, use_container_width=True)
