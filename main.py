import plotly.express as px
import streamlit as st
import pandas as pd

df_csv = pd.read_csv('produksi_minyak_mentah.csv')
df_json = pd.read_json('kode_negara_lengkap.json')
df_json.to_csv("json.csv", index=False)
csv_json = pd.read_csv("json.csv")


# print-all
df = df_csv.merge(csv_json, left_on='kode_negara', right_on='alpha-3')

# select-filter
st.sidebar.header("Pilih Filter:")
name_negara = st.sidebar.multiselect(
    "Pilih Negara:",
    options=df['name_negara'].unique(),
    default=df['name_negara'].unique(),
)

tahun = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=df["tahun"].unique(),
    default=df["tahun"].unique(),
)

# Filter
filter_data = df.query(
    "name_negara == @name_negara & tahun == @tahun"
)

# Chart
data_pertahun = filter_data.groupby(by='name_negara').sum()[['produksi']]

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

st.plotly_chart(fig_data, use_container_width=True)
