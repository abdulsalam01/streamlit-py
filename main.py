import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

df_csv = pd.read_csv('data/produksi_minyak_mentah.csv')
df_json = pd.read_json('data/kode_negara_lengkap.json')
df_json.to_csv("data/json.csv", index=False)
csv_json = pd.read_csv("data/json.csv")

jumlah_negara = st.number_input(
    'Jumlah Negara', min_value=1, max_value=50, value=5, step=1)

# print-all
df = df_csv.merge(csv_json, left_on='kode_negara', right_on='alpha-3')
df2 = df.nlargest(jumlah_negara, 'produksi')

# select-filter
st.sidebar.header("Pilih Filter:")
name = st.sidebar.multiselect(
    "Pilih Negara:",
    options=df['name'].unique(),
    default=df['name'].unique(),
)

tahun = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=df["tahun"].unique(),
    default=df["tahun"].unique(),
)

region = st.sidebar.multiselect(
    "Pilih Region:",
    options=df["region"].unique(),
    default=df["region"].unique(),
)

# Filter
filter_data = df.query(
    "name == @name & tahun == @tahun & region == @region"
)

filter_data2 = df2.query(
    "name == @name & tahun == @tahun & region == @region"
)


# Chart
data_pertahun = filter_data.groupby(by='name').sum()[['produksi']]
data_pertahun2 = filter_data2.groupby(
    ['name']).sum()[['produksi']]

fig_data = px.bar(
    data_pertahun,
    x=data_pertahun.index,
    y='produksi',
    title="<b>Data Pertahun</b>",
    color_discrete_sequence=["#0083B8"] * len(data_pertahun),
    template="plotly_white",
)
fig_data.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

fig_data2 = px.bar(
    data_pertahun2,
    x=data_pertahun2.index,
    y='produksi',
    title="<b>Data Negara kumulatif tertinggi</b>",
    color_discrete_sequence=["#0083B8"] * len(data_pertahun2),
    template="plotly_white",
)
fig_data2.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


st.plotly_chart(fig_data, use_container_width=True)
st.plotly_chart(fig_data2, use_container_width=True)
st.table(df2)