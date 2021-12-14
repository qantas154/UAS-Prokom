#Qoulan Thoyyibah S
#12220069

import streamlit as st 
import pandas as pd
import json as js

#json
file = js.load(open('kode_negara_lengkap.json'))
print(file) #nanti dihapus

#initialize
list_negara = []

#bikin list negara
for negara in file:
    nama = negara.get('name')
    code = negara.get('alpha-3')
    ccode = negara.get('country-code')
    region = negara.get('region')
    sub_region = negara.get('sub-region')
    list_negara.append([nama,code,ccode,region,sub_region])
print(list_negara) #nanti dihapus

#buka csv
dataf = pd.read_csv('produksi_minyak_mentah.csv')
#removing some country
dataf = dataf[dataf['kode_negara'] != "WLD"]
dataf = dataf[dataf['kode_negara'] != "G20"]
dataf = dataf[dataf['kode_negara'] != "EU28"]
dataf = dataf[dataf['kode_negara'] != "OECD"]

st.title("APLIKASI PRODUKSI MINYAK MENTAH DUNIA")
st.subheader("Qoulan Thoyyibah S - Ziyad Dhia Rafi")



