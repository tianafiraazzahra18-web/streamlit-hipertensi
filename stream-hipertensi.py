import pickle
import streamlit as st
import base64

# Proses gambar agar dapat masuk ke kotak pink
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Nama file GAMBAR
img_base64 = get_base64('UPT PALAS.png')

# Membaca Model (Load Model)
hipertensi_model = pickle.load(open('hipertensi_model.sav', 'rb'))
scaler = pickle.load(open('scaler.sav', 'rb'))

st.set_page_config(layout="wide", page_title="Prediksi Hipertensi")

# --- HEADER BANNER PINK ---
st.markdown(f"""
    <style>
    .main-header {{
        background-color: #42A5F5;
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
        background-color: #42A5F5;
        color: white;
        border-radius: 10px;
        font-weight: bold;
        width: 100%;
        height: 3em;
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

st.markdown("Formulir Input Data Pasien")

# --- INPUT DATA ---
col1, col2, col3 = st.columns(3)

with col1:
    jk_pilihan = st.selectbox('Input Jenis Kelamin', ['Perempuan', 'Laki-laki'])
    JenisKelamin = 0 if jk_pilihan == 'Perempuan' else 1
    
    BeratBadan = st.text_input('Input Berat Badan', value='0')
    LingkarPerut = st.text_input('Input Lingkar Perut', value='0')

with col2:
    Usia = st.text_input('Input Usia', value='0')
    IMT = st.text_input('Input IMT', value='0')
    
    Merokok = st.selectbox('Input Merokok', ['Tidak', 'Ya'])
    Merokok = 1 if Merokok == 'Ya' else 0

with col3:
    TinggiBadan = st.text_input('Input Tinggi Badan', value='0')
    
    HasilIMT = st.selectbox('Input Hasil IMT', ['Ideal', 'Lebih', 'Obesitas', 'Kurang', 'Gemuk'])
    # Konversi Hasil IMT ke Angka
    imt_map = {'Ideal': 0, 'Lebih': 1, 'Obesitas': 2, 'Kurang': 3, 'Gemuk': 4}
    HasilIMT = imt_map[HasilIMT]

    KonsumsiAlkohol = st.selectbox('Input Konsumsi Alkohol', ['Tidak', 'Ya'])
    KonsumsiAlkohol = 1 if KonsumsiAlkohol == 'Ya' else 0

st.markdown("---")

#TOMBOL PREDIKSI DENGAN VALIDASI
if st.button('Test Prediksi Hipertensi'):
    # VALIDASI: Cek jika ada data yang masih '0'
    if Usia == '0' or TinggiBadan == '0' or BeratBadan == '0' or IMT == '0' or LingkarPerut == '0':
        st.warning("⚠️ Mohon maaf, semua data (Usia, Tinggi, Berat, IMT, Lingkar Perut) harus diisi dan tidak boleh 0!")
    else:
        try:
            # Ambil semua input dan jadikan float
            input_data = [[
                float(JenisKelamin), float(Usia), float(TinggiBadan), 
                float(BeratBadan), float(IMT), float(HasilIMT), 
                float(LingkarPerut), float(Merokok), float(KonsumsiAlkohol)
            ]]
            
            # STANDARISASI
            std_data = scaler.transform(input_data)
            
            # PREDIKSI
            hip_prediction = hipertensi_model.predict(std_data)

            # TAMPILKAN HASIL
            if hip_prediction[0] == 0:
                st.success('✅ Pasien Tidak Terkena Hipertensi')
            else:
                st.error('🚨 Pasien Terkena Hipertensi')
        
        except Exception as e:
            st.error(f"Terjadi kesalahan input: {e}")