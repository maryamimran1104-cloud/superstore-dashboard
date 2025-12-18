# -*- coding: utf-8 -*-
"""
Created on Thu Dec 18 19:40:51 2025

@author: DELL
"""

import streamlit as st
import plotly.express as px
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

st.title("📊 Superstore Sales Dashboard")
st.write("This dashboard helps analyze sales, profit, and performance across regions and categories.")

@st.cache_data
def load_data():
    df = pd.read_csv("superstore.csv")
    return df

df = load_data()

st.subheader("📄 Dataset Preview")
st.dataframe(df.head())

# Fix missing values
df.fillna(0, inplace=True)

# Convert Order Date to datetime
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Add new columns
df['Year'] = df['Order Date'].dt.year
df['Month'] = df['Order Date'].dt.month_name()
df['Profit %'] = (df['Profit'] / df['Sales']) * 100

st.sidebar.header("🔍 Filters")

start_date = st.sidebar.date_input(
    "Start Date",
    df['Order Date'].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df['Order Date'].max()
)

product_category = st.sidebar.multiselect(
    "Product Category",
    df['Product Category'].unique(),
    default=df['Product Category'].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df['Region'].unique(),
    default=df['Region'].unique()
)

filtered_df = df[
    (df['Order Date'] >= pd.to_datetime(start_date)) &
    (df['Order Date'] <= pd.to_datetime(end_date)) &
    (df['Product Category'].isin(product_category)) &
    (df['Region'].isin(region))
]

# ------------------ KPI METRICS ------------------
st.subheader("📌 Key Performance Indicators")

c1, c2, c3 = st.columns(3)
c1.metric("Total Sales", f"${filtered_df['Sales'].sum():,.0f}")
c2.metric("Total Profit", f"${filtered_df['Profit'].sum():,.0f}")
c3.metric("Average Order Value", f"${filtered_df['Sales'].mean():,.0f}")

category_sales = (
    filtered_df
    .groupby('Product Category')['Sales']
    .sum()
    .reset_index()
)

fig2 = px.bar(
    category_sales,
    x='Product Category',
    y='Sales',
    title="Sales by Product Category"
)

st.plotly_chart(fig2, use_container_width=True)

monthly_sales = (
    filtered_df
    .groupby('Order Date')['Sales']
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x='Order Date',
    y='Sales',
    title="Sales Trend Over Time"
)

st.plotly_chart(fig1, use_container_width=True)
region_sales = (
    filtered_df
    .groupby('Region')['Sales']
    .sum()
    .reset_index()
)

fig3 = px.pie(
    region_sales,
    names='Region',
    values='Sales',
    title="Sales by Region"
)

st.plotly_chart(fig3, use_container_width=True)
top10 = (
    filtered_df
    .groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.subheader("🏆 Top 10 Products by Sales")
st.dataframe(top10)
