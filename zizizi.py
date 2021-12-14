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
min_tahun = int(dataf.min(axis=0)['tahun'])
max_tahun = int(dataf.max(axis=0)['tahun'])
#removing some country
dataf = dataf[dataf['kode_negara'] != "WLD"]
dataf = dataf[dataf['kode_negara'] != "G20"]
dataf = dataf[dataf['kode_negara'] != "EU28"]
dataf = dataf[dataf['kode_negara'] != "OECD"]

st.title("APLIKASI PRODUKSI MINYAK MENTAH DUNIA")
st.subheader("Qoulan Thoyyibah S - Ziyad Dhia Rafi")
st.write("hi")


#soal nomor A
select = st.selectbox("Country :", (i[0] for i in list_negara))
for c in list_negara :
    if c[0] == select:
        set_ccode = c[1]
        break

dataf_countryN = dataf.loc[dataf['kode_negara'] == set_ccode]
print(dataf_countryN) #nanti dihapus
#buat chart
line_countryN = dataf_countryN[["tahun","produksi"]].set_index('tahun')
st.line_chart(line_countryN)


#Nomor B
tahun_min = 1971
tahun_max = 2015
tahun = int(st.number_input("Year : ", min_value=tahun_min, max_value=tahun_max))
b = int(st.number_input("Jumlah produksi terbesar: ", min_value=0, max_value=100))
dataf_year = dataf.loc[dataf['tahun'] == tahun]
dataf_biggest = dataf_year.sort_values('produksi',ascending=False).head(b)
bar_B = dataf_biggest[["kode_negara", "produksi"]].set_index("kode_negara")
st.write('hapus')
st.bar_chart(bar_B)

#Nomor C
dataf['kumulatif'] = dataf.groupby(['kode_negara'])['produksi'].cumsum()
dataf_cml = dataf.drop_duplicates('kode_negara', keep = "last")
dataf_topcml = dataf_cml.sort_values('kumulatif', ascending=False)

bb = int(st.number_input('Berapa angka terbesar?', min_value=1, max_value=100))
bar_topcml = dataf_topcml[['kode_negara', 'produksi']].head(bb)
st.bar_chart(bar_topcml.set_index('kode_negara'))
