import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("failures.csv", parse_dates=["Month"])
    df["Month"] = df["Month"].dt.strftime("%Y-%m")  # Format for better display
    return df

df = load_data()

# Title
st.title("MTA Rail Car MDBF Visualization")

# Sidebar Filters
st.sidebar.header("Filters")
divisions = st.sidebar.multiselect("Select Division:", options=df["Division"].unique(), default=df["Division"].unique())
car_classes = st.sidebar.multiselect("Select Car Class:", options=df["Car Class"].unique(), default=df["Car Class"].unique())

# Filter Data
filtered_df = df[(df["Division"].isin(divisions)) & (df["Car Class"].isin(car_classes))]

# Line Chart for MDBF Over Time
st.subheader("Mean Distance Between Failures (MDBF) Over Time")
fig_mdbf = px.line(filtered_df, x="Month", y="MDBF", color="Car Class", markers=True, title="MDBF Trends")
st.plotly_chart(fig_mdbf, use_container_width=True)

# Bar Chart for 12-Month Average MDBF
st.subheader("12-Month Average MDBF by Car Class")
fig_avg_mdbf = px.bar(filtered_df, x="Car Class", y="12-Month Average MDBF", color="Car Class",
                       title="12-Month Average MDBF", text_auto=True)
st.plotly_chart(fig_avg_mdbf, use_container_width=True)

# Display Data Table
st.subheader("Filtered Data")
st.dataframe(filtered_df)