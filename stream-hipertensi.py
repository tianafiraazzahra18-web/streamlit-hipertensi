import pickle
import streamlit as st
import base64

#Proses gambar agar dapat masuk ke kotak pink
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

#Nama file GAMBAR
img_base64 = get_base64('UPT PALAS.png')

#Membaca Model (Load Model)
hipertensi_model = pickle.load(open('hipertensi_model.sav', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

st.set_page_config(layout="wide")

# --- HEADER BANNER PINK ---
st.markdown(f"""
    <style>
    .main-header {{
        background-color: #F06292; 
        padding: 30px; 
        border-radius: 15px; 
        display: flex; 
        align-items: center; 
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    .header-text {{
        color: white;
        font-family: 'sans-serif';
    }}
    .stButton>button {{
        background-color: #F06292;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }}
    </style>
    
    <div class="main-header">
        <img src="data:image/png;base64,{img_base64}" style="width: 300px; border-radius: 10px; margin-right: 25px; border: 2px solid white;">
        <div class="header-text">
            <h1 style="margin: 0; font-size: 32px;">Data Mining Prediksi Hipertensi</h1>
            <p style="margin: 0; font-size: 18px;">UPT Puskesmas Palas - Kec. Palas Lampung Selatan</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Judul Kecil di atas form
st.markdown("Formulir Input Data Pasien")

#Membagi Kolom
col1, col2, col3 = st.columns(3)

with col1:
   JenisKelamin = st.selectbox ('Input Jenis Kelamin', ['Perempuan', 'Laki-laki'])
if JenisKelamin == 'Perempuan':
    JenisKelamin = 0
else:
    JenisKelamin = 1
        
with col2:
    Usia = st.text_input ('Input Usia', value='0')

with col3:
    TinggiBadan = st.text_input ('Input Tinggi Badan', value='0')

with col1:
    BeratBadan = st.text_input ('Input Berat Badan', value='0')

with col2:
    IMT = st.text_input ('Input IMT', value='0')

with col3:
    HasilIMT = st.selectbox('Input Hasil IMT', ['Ideal', 'Lebih', 'Obesitas', 'Kurang', 'Gemuk'])
    if HasilIMT == 'Ideal':
        HasilIMT = 0
    elif HasilIMT == 'Lebih':
        HasilIMT = 1
    elif HasilIMT == 'Obesitas':
        HasilIMT = 2
    elif HasilIMT == 'Kurang':
        HasilIMT = 3
    else: 
        HasilIMT = 4

with col1:
    LingkarPerut = st.text_input ('Input Lingkar Perut', value='0')

with col2:
    Merokok = st.selectbox ('Input Merokok', ['Tidak', 'Ya'])
    Merokok = 1 if Merokok == 'Ya' else 0

with col3:
    KonsumsiAlkohol = st.selectbox('Input Konsumsi Alkohol', ['Tidak', 'Ya'])
    KonsumsiAlkohol = 1 if KonsumsiAlkohol == 'Ya' else 0

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