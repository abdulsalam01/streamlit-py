import plotly.express as px
import streamlit as st
import pandas as pd

df = pd.read_csv('produksi_minyak_mentah.csv')
df_json = pd.read_json('kode_negara_lengkap.json')
df_merger = {}

for json in df_json.iterrows():
    alpha = json[1]['alpha-3']
    name = json[1]['name']
    region = json[1]['region']
    subregion = json[1]['sub-region']
 
    for row in df.iterrows():
        if row[1]['kode_negara'] == alpha:
            df_merger['name'] = name
            df_merger['alpha-3'] = alpha
            df_merger['region'] = region
            df_merger['sub-region'] = subregion
            df_merger['kode_negara'] = row[1]['kode_negara']
            df_merger['tahun'] = row[1]['tahun']
            df_merger['produksi'] = row[1]['produksi']
   
# print-all
#print(df_merger)

# All Brands
st.sidebar.header("Pilih Filter:")
kode_negara = st.sidebar.multiselect(
    "Pilih Negara:",
    options=df_merger["kode_negara"].unique(),
    default=df_merger["kode_negara"].unique(),   
)

tahun = st.sidebar.multiselect(
    "Pilih Tahun:",
    options=df_merger["tahun"].unique(),
    default=df_merger["tahun"].unique(),   
)

#Filter
filter_data = df_merger.query(
    "kode_negara == @kode_negara & tahun == @tahun"
)

#Chart
data_pertahun = filter_data.groupby(by='kode_negara').sum()[['produksi']]

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