#Qoulan Thoyyibah S
#12220069

import streamlit as st 
import pandas as pd
import json as js

#json
file = js.load(open('kode_negara_lengkap.json'))

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
st.caption("Qoulan Thoyyibah S - 12220069")




#soal nomor A
st.subheader("Grafik Jumlah Produksi Minyak Mentah Negara")
select = st.selectbox("Country :", (i[0] for i in list_negara))
for c in list_negara :
    if c[0] == select:
        set_ccode = c[1]
        break
if not((dataf['kode_negara'] == set_ccode).any()):
    st.write("Data produksi minyak " + select + " tidak ditemukan")
else:
    dataf_countryN = dataf.loc[dataf['kode_negara'] == set_ccode]

    #buat chart
    line_countryN = dataf_countryN[["tahun","produksi"]].set_index('tahun')
    st.line_chart(line_countryN)


#Nomor B
st.subheader("Besar Negara dengan Jumlah Produksi Terbesar")
tahun_min = int(dataf.min(axis=0)['tahun'])
tahun_max = int(dataf.max(axis=0)['tahun'])
tahun = int(st.number_input("Year : ", min_value=tahun_min, max_value=tahun_max))
b = int(st.number_input("Jumlah produksi terbesar: ", min_value=0, max_value=100))
dataf_year = dataf.loc[dataf['tahun'] == tahun]
dataf_biggest = dataf_year.sort_values('produksi',ascending=False).head(b)
bar_B = dataf_biggest[["kode_negara", "produksi"]].set_index("kode_negara")

st.bar_chart(bar_B)



#Nomor C
st.subheader("Besar Negara dengan Jumlah Produksi Terbesar Secara Kumulatif Keseluruhan Tahun")
dataf['kumulatif'] = dataf.groupby(['kode_negara'])['produksi'].cumsum()
dataf_cml = dataf.drop_duplicates('kode_negara', keep = "last")
dataf_topcml = dataf_cml.sort_values('kumulatif', ascending=False)

bb = int(st.number_input('Berapa angka terbesar?', min_value=1, max_value=100))
bar_topcml = dataf_topcml[['kode_negara', 'produksi']].head(bb)
st.bar_chart(bar_topcml.set_index('kode_negara'))

#Nomor D
#kumulatif
st.subheader("Jumlah Produksi Data Kumulatif")
datafnotzero = dataf_topcml[dataf_topcml['kumulatif'] != 0].reset_index(drop=True)

datafnotzero["Nama Negara"] = datafnotzero["kode_negara"]
datafnotzero["Region"] = datafnotzero["kode_negara"]
datafnotzero["Sub Region"] = datafnotzero["kode_negara"]
for i in list_negara:
    datafnotzero["Nama Negara"] = datafnotzero["Nama Negara"].replace([i[1]], i[0])
    datafnotzero["Region"] = datafnotzero["Region"].replace([i[1]], i[3])
    datafnotzero["Sub Region"] = datafnotzero["Sub Region"].replace([i[1]], i[4])

with st.container():
    box1, box2 = st.columns(2)
    with box1 :
        st.success(("Jumlah Produksi Terbesar Kumulatif Tahun "+ str(tahun_max)))
        st.write("Nama Negara : "+ datafnotzero.loc[0, "Nama Negara"])
        st.write("Kode Negara : "+ datafnotzero.loc[0, "kode_negara"])
        st.write("Region : "+ datafnotzero.loc[0, "Region"])
        st.write("Sub-region : "+ datafnotzero.loc[0, "Sub Region"])
        st.write("Produksi terbesar keseluruhan tahun : "+ str(datafnotzero.loc[0, "kumulatif"]))
    with box2 :
        st.warning(("Jumlah Produksi Terkecil Kumulatif Tahun " + str(tahun_max)))
        index_min = len(datafnotzero)-1
        st.write("Nama Negara : "+ datafnotzero.loc[index_min, "Nama Negara"])
        st.write("Kode Negara : "+ datafnotzero.loc[index_min, "kode_negara"])
        st.write("Region : "+ datafnotzero.loc[index_min, "Region"])
        st.write("Sub-region : "+ datafnotzero.loc[index_min, "Sub Region"])
        st.write("Produksi terkecil keseluruhan tahun : "+ str(datafnotzero.loc[index_min, "kumulatif"]))

#sama dengan nol
st.subheader("Jumlah Produksi Data Nol Kumulatif")
datafzero = dataf_topcml[dataf_topcml['kumulatif'] == 0].reset_index(drop=True)
datafzero["Nama Negara"] = datafzero["kode_negara"]
datafzero["Region"] = datafzero["kode_negara"]
datafzero["Sub Region"] = datafzero["kode_negara"]
for z in list_negara:
    datafzero["Nama Negara"] = datafzero["Nama Negara"].replace([z[1]], z[0])
    datafzero["Region"] = datafzero["Region"].replace([z[1]], z[3])
    datafzero["Sub Region"] = datafzero["Sub Region"].replace([z[1]], z[4])

datafzero2 = datafzero[["Nama Negara", "kode_negara", "Region", "Sub Region"]]
datafzero2 = datafzero2.rename(columns={'kode_negara' : 'Kode'})
datafzero2.index += 1
st.table(datafzero2)

#Per Tahun
st.subheader("Jumlah Produksi Data Pada Tahun Tertentu")
pertahun = int(st.slider("Year : ", min_value=tahun_min, max_value=tahun_max))

datafpertahun = dataf.loc[dataf['tahun'] == pertahun]
datafpertahunnozero = datafpertahun.loc[dataf['produksi'] != 0]

datafpertahunsorted = datafpertahunnozero.sort_values("produksi", ascending=False).reset_index(drop=True)

datafpertahunsorted["Nama Negara"] = datafpertahunsorted["kode_negara"]
datafpertahunsorted["Region"] = datafpertahunsorted["kode_negara"]
datafpertahunsorted["Sub Region"] = datafpertahunsorted["kode_negara"]
for i in list_negara:
    datafpertahunsorted["Nama Negara"] = datafpertahunsorted["Nama Negara"].replace([i[1]], i[0])
    datafpertahunsorted["Region"] = datafpertahunsorted["Region"].replace([i[1]], i[3])
    datafpertahunsorted["Sub Region"] = datafpertahunsorted["Sub Region"].replace([i[1]], i[4])

with st.container():
    box1, box2 = st.columns(2)
    with box1 :
        st.success(("Jumlah Produksi Terbesar Pada Tahun "+ str(pertahun)))
        st.write("Nama Negara : "+ datafpertahunsorted.loc[0, "Nama Negara"])
        st.write("Kode Negara : "+ datafpertahunsorted.loc[0, "kode_negara"])
        st.write("Region : "+ datafpertahunsorted.loc[0, "Region"])
        st.write("Sub-region : "+ datafpertahunsorted.loc[0, "Sub Region"])
        st.write("Produksi terbesar keseluruhan tahun : "+ str(datafpertahunsorted.loc[0, "kumulatif"]))
    with box2 :
        st.warning(("Jumlah Produksi Terkecil Pada Tahun "+ str(pertahun)))
        index_min = len(datafpertahunsorted)-1
        st.write("Nama Negara : "+ datafpertahunsorted.loc[index_min, "Nama Negara"])
        st.write("Kode Negara : "+ datafpertahunsorted.loc[index_min, "kode_negara"])
        st.write("Region : "+ datafpertahunsorted.loc[index_min, "Region"])
        st.write("Sub-region : "+ datafpertahunsorted.loc[index_min, "Sub Region"])
        st.write("Produksi terkecil keseluruhan tahun : "+ str(datafpertahunsorted.loc[index_min, "kumulatif"]))

#sama dengan nol
st.subheader("Jumlah Produksi Data Nol Pada Tahun Tertentu")
datafpertahunzero =  datafpertahun.loc[datafpertahun['produksi'] == 0].reset_index(drop=True)
datafpertahunzero["Nama Negara"] = datafpertahunzero["kode_negara"]
datafpertahunzero["Region"] = datafpertahunzero["kode_negara"]
datafpertahunzero["Sub Region"] = datafpertahunzero["kode_negara"]
for z in list_negara:
    datafpertahunzero["Nama Negara"] = datafpertahunzero["Nama Negara"].replace([z[1]], z[0])
    datafpertahunzero["Region"] = datafpertahunzero["Region"].replace([z[1]], z[3])
    datafpertahunzero["Sub Region"] = datafpertahunzero["Sub Region"].replace([z[1]], z[4])

datafpertahunzero2 = datafpertahunzero[["Nama Negara", "kode_negara", "Region", "Sub Region"]]
datafpertahunzero2 = datafpertahunzero2.rename(columns={'kode_negara' : 'Kode'})
datafpertahunzero2.index += 1
st.table(datafpertahunzero2)


