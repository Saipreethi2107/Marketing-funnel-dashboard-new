import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Marketing Funnel & ROI Dashboard", layout="wide")

st.title("📊 Marketing Funnel & Campaign ROI Analytics")

# Load data
df = pd.read_csv("marketing_funnel_data.csv")

# Filters
col1, col2 = st.columns(2)
channel_filter = col1.multiselect("Channel", df["channel"].unique(), default=df["channel"].unique())
campaign_filter = col2.multiselect("Campaign", df["campaign"].unique(), default=df["campaign"].unique())

filtered = df[(df["channel"].isin(channel_filter)) & (df["campaign"].isin(campaign_filter))]

# KPI metrics
impressions = filtered["impressions"].sum()
clicks = filtered["clicks"].sum()
leads = filtered["leads"].sum()
conversions = filtered["conversions"].sum()
revenue = filtered["revenue"].sum()
cost = filtered["cost"].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Conversion Rate", f"{conversions / clicks:.2%}")
col2.metric("CPA", f"${cost / conversions:,.2f}")
col3.metric("ROI", f"{(revenue - cost) / cost:.2%}")
col4.metric("Revenue", f"${revenue:,.0f}")

# Funnel chart
funnel_df = pd.DataFrame({
    "Stage": ["Impressions", "Clicks", "Leads", "Conversions"],
    "Users": [impressions, clicks, leads, conversions]
})

fig_funnel = px.funnel(funnel_df, x="Users", y="Stage", title="Marketing Funnel")
st.plotly_chart(fig_funnel, use_container_width=True)

# Channel ROI
roi_df = filtered.groupby("channel")[["revenue", "cost"]].sum().reset_index()
roi_df["ROI"] = (roi_df["revenue"] - roi_df["cost"]) / roi_df["cost"]

fig_roi = px.bar(roi_df, x="channel", y="ROI", title="ROI by Channel")
st.plotly_chart(fig_roi, use_container_width=True)

# Attribution
attr_df = filtered.groupby("attribution_model")["conversions"].sum().reset_index()
fig_attr = px.pie(attr_df, names="attribution_model", values="conversions", title="Attribution Model Comparison")
st.plotly_chart(fig_attr, use_container_width=True)
