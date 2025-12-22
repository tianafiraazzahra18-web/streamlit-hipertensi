import pickle
import streamlit as st

#Membaca Model (Load Model)
hipertensi_model = pickle.load(open('hipertensi_model.sav', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

# Membuat dua kolom untuk Logo dan Judul
col_logo, col_judul = st.columns([1, 4])

with col_logo:
    st.image('UPT PALAS.png', width=150) 

with col_judul:
    st.title('UPT Puskesmas Palas')

#Judul WEB
st.title('Data Mining Prediksi Hipertensi Pada UPT Puskesmas Palas')

#Membagi Kolom
col1, col2, col3 = st.columns(3)

with col1:
    JenisKelamin = st.text_input ('Input Jenis Kelamin')

with col2:
    Usia = st.text_input ('Input Usia')

with col3:
    TinggiBadan = st.text_input ('Input Tinggi Badan')

with col1:
    BeratBadan = st.text_input ('Input Berat Badan')

with col2:
    IMT = st.text_input ('Input IMT')

with col3:
    HasilIMT = st.text_input ('Input Hasil IMT')

with col1:
    LingkarPerut = st.text_input ('Input Lingkar Perut')

with col2:
    Merokok = st.text_input ('Input Merokok')

with col3:
    KonsumsiAlkohol =st.text_input ('Input Konsumsi Alkohol')

#Code untuk prediksi
hip_diagnosis = ''

#Membuat Tombol Prediksi
if st.button('Test Prediksi Hipertensi'):
    # Ambil semua input dan jadikan float
    input_data = [[
        float(JenisKelamin), float(Usia), float(TinggiBadan), 
        float(BeratBadan), float(IMT), float(HasilIMT), 
        float(LingkarPerut), float(Merokok), float(KonsumsiAlkohol)
    ]]
    
    # STANDARISASI: Ini kunci agar hasil sama dengan Jupyter!
    std_data = scaler.transform(input_data)
    
    # PREDIKSI: Gunakan data yang sudah di-standarisasi
    hip_prediction = hipertensi_model.predict(std_data)

    # LOGIKA: Sesuaikan dengan Jupyter (0 = Tidak, selain itu = Iya)
    if (hip_prediction[0] == 0):
        st.success('Pasien Tidak Terkena Hipertensi')
    else:
        st.error('Pasien Terkena Hipertensi')