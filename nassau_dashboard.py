import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Nassau Candy Dashboard", layout="wide")

st.title("Nassau Candy Distributor")
st.subheader("Product Line Profitability & Margin Performance Analysis")

df = pd.read_csv(r"C:\Users\VEERA RAGHAVAN\Nassau_Candy_Final.csv")

df['Gross Margin %'] = (df['Gross Profit'] / df['Sales']) * 100

st.sidebar.header("Filters")
division = st.sidebar.multiselect(
    "Select Division",
    df['Division'].unique(),
    default=df['Division'].unique(),
    key="division_filter"
)
region = st.sidebar.multiselect(
    "Select Region",
    df['Region'].unique(),
    default=df['Region'].unique(),
    key="region_filter"
)

df_filtered = df[
    df['Division'].isin(division) &
    df['Region'].isin(region)
]

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${df_filtered['Sales'].sum():,.2f}")
col2.metric("Total Gross Profit", f"${df_filtered['Gross Profit'].sum():,.2f}")
col3.metric("Avg Gross Margin %", f"{df_filtered['Gross Margin %'].mean():,.2f}%")

st.markdown("---")

division_margin = df_filtered.groupby('Division')['Gross Margin %'].mean().reset_index()
fig1 = px.bar(division_margin, x='Division', y='Gross Margin %',
              color='Division', title='Average Gross Margin % by Division')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")

division_sales = df_filtered.groupby('Division')[['Sales', 'Gross Profit']].sum().reset_index()
fig2 = px.bar(division_sales, x='Division', y=['Sales', 'Gross Profit'],
              barmode='group', title='Sales vs Gross Profit by Division')
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

region_margin = df_filtered.groupby('Region')['Gross Margin %'].mean().reset_index()
fig3 = px.bar(region_margin, x='Region', y='Gross Margin %',
              color='Region', title='Average Gross Margin % by Region')
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

region_sales = df_filtered.groupby('Region')[['Sales', 'Gross Profit']].sum().reset_index()
fig4 = px.bar(region_sales, x='Region', y=['Sales', 'Gross Profit'],
              barmode='group', title='Sales vs Gross Profit by Region')
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

product_data = df_filtered.groupby(['Product Name', 'Division']).agg({
    'Sales': 'sum',
    'Gross Profit': 'sum',
    'Gross Margin %': 'mean'
}).reset_index()
fig5 = px.scatter(product_data, x='Gross Profit', y='Sales',
                  color='Division', hover_name='Product Name',
                  title='Product Level Sales vs Gross Profit')
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

pareto = df_filtered.groupby('Product Name')['Gross Profit'].sum().reset_index()
pareto = pareto.sort_values('Gross Profit', ascending=False)
fig6 = px.bar(pareto, x='Product Name', y='Gross Profit',
              title='Profit Contribution by Product',
              color='Gross Profit', color_continuous_scale='Blues')
st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

fig7 = px.scatter(df_filtered, x='Cost', y='Sales',
                  color='Division', title='Cost vs Sales by Division', opacity=0.6)
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")

risk_counts = df_filtered['Risk Flag'].value_counts().reset_index()
risk_counts.columns = ['Risk Flag', 'Count']
fig8 = px.pie(risk_counts, names='Risk Flag', values='Count',
              title='Product Risk Flag Distribution',
              color_discrete_map={
                  'Healthy': 'green',
                  'Reprice': 'orange',
                  'Discontinue Review': 'red'
              })
st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

st.dataframe(df_filtered[['Product Name', 'Division', 'Region',
                           'Sales', 'Gross Profit', 'Gross Margin %',
                           'Profit per Unit', 'Risk Flag']])