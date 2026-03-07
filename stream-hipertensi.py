import pickle
import streamlit as st
import base64
import pandas as pd 
import os            
from datetime import datetime 

# Proses gambar agar dapat masuk ke kotak biru
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

# --- HEADER BANNER BIRU ---
st.markdown(f"""
<style>
.hero {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center 40%;
    height: 420px;
    border-radius: 20px;
    position: relative;
    margin-bottom: 40px;
    overflow: hidden;
}}

.hero::before {{
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(
        to right,
        rgba(13,71,161,0.85), 
        rgba(13,71,161,0.55), 
        rgba(13,71,161,0.2)
    );
    z-index: 1;
}}

.hero-content {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
    color: white;
    z-index: 2;
    width: 100%;
    padding: 0 20px;
}}

.hero h1 {{
    font-size: 64px;
    font-weight: 800;
    margin-bottom: 15px;
}}

.hero p {{
    font-size: 22px;
    opacity: 0.9;
    
}}

.hero p {{
    font-size: 20px;
    opacity: 0.95;
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

<div class="hero">
    <div class="hero-content">
       <h1>Data Mining Prediksi Hipertensi</h1>
        <p style="font-size:18px; opacity:0.9;">
            UPT Puskesmas Palas - Kec. Palas, Kabupaten Lampung Selatan.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("Formulir Input Data Pasien")

# --- INPUT DATA ---
col1, col2, col3 = st.columns(3)

with col1:
    nama_pasien = st.text_input('Nama Lengkap Pasien', placeholder="Masukkan nama pasien...")
    TinggiBadan = st.text_input('Input Tinggi Badan', value='0')
    
    Diastole = st.text_input('Input Diastole (Tekanan Darah Bawah)', value='0')
    LingkarPerut = st.text_input('Input Lingkar Perut', value='0')

with col2:
    jk_pilihan = st.selectbox('Input Jenis Kelamin', ['Perempuan', 'Laki-laki'])
    JenisKelamin = 0 if jk_pilihan == 'Perempuan' else 1
    
    BeratBadan = st.text_input('Input Berat Badan', value='0')
    IMT = st.text_input('Input IMT', value='0')
    
    Merokok = st.selectbox('Input Merokok', ['Tidak', 'Ya'])
    Merokok = 1 if Merokok == 'Ya' else 0

with col3:
    Usia = st.text_input('Input Usia', value='0')
    Sistole = st.text_input('Input Sistole (Tekanan Darah Atas)', value='0')

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
    if Usia == '0' or TinggiBadan == '0' or BeratBadan == '0' or IMT == '0' or LingkarPerut == '0' or Sistole == '0':
        st.warning(f"⚠️ Halo, mohon lengkapi Nama dan data medis untuk diproses, harus diisi dan tidak boleh kosong!")
    else:
        try:
            # Mengambil semua input dan jadikan float
            input_data = [[
                float(JenisKelamin), float(Usia), float(TinggiBadan), 
                float(BeratBadan), float(Sistole),float(Diastole),
                float(IMT), float(HasilIMT),float(LingkarPerut),
                float(Merokok), float(KonsumsiAlkohol)
            ]]
            
            # STANDARISASI
            std_data = scaler.transform(input_data)
            
            # PREDIKSI
            hip_prediction = hipertensi_model.predict(std_data)

            # --- TAMPILKAN HASIL DAN ISI VARIABEL ---
            if hip_prediction[0] == 0:
                hasil_teks = "Tidak Terkena Hipertensi"
                st.success(f'✅ Pasien bernama **{nama_pasien}** diprediksi: **{hasil_teks}**')
            else:
                hasil_teks = "Terkena Hipertensi" 
                st.error(f'🚨 Pasien bernama **{nama_pasien}** diprediksi: **{hasil_teks}**')

            # 3. --- PROSES REKAM DATA KE CSV ---
            # Menyiapkan baris data baru
            # Format: Tanggal-Bulan-Tahun Jam:Menit
            waktu_sekarang = datetime.now().strftime("%d-%m-%Y %H:%M")
            data_baru = {
                'Waktu': [waktu_sekarang],
                'Nama': [nama_pasien],
                'Jenis Kelamin': ['Laki-laki' if JenisKelamin == 1 else 'Perempuan'],
                'Usia': [Usia],
                'Tinggi': [TinggiBadan],
                'Berat': [BeratBadan],
                'Sistole': [Sistole],
                'Diastole': [Diastole],
                'IMT': [IMT],
                'Lingkar Perut': [LingkarPerut],
                'Merokok': ['Ya' if Merokok == 1 else 'Tidak'],
                'Alkohol': ['Ya' if KonsumsiAlkohol == 1 else 'Tidak'],
                'Hasil Prediksi': [hasil_teks]
            }
            df_log = pd.DataFrame(data_baru)
            nama_file = 'rekam_medis.csv'

            # Simpan: Kalau file belum ada buat baru, kalau sudah ada tambah baris di bawahnya
            if not os.path.isfile(nama_file):
                df_log.to_csv(nama_file, index=False)
            else:
                df_log.to_csv(nama_file, mode='a', index=False, header=False)
            
            st.info("💾 Data pemeriksaan telah dicatat ke dalam sistem.")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

            # --- TAMPILKAN TABEL RIWAYAT (Di luar blok tombol) ---
st.markdown("---")
st.markdown("### 📋 Riwayat Pemeriksaan Terakhir")

file_rekam = 'rekam_medis.csv'

if os.path.exists(file_rekam):
    # Membaca data rekam medis agar bisa dilihat di web
    df_riwayat = pd.read_csv(file_rekam)
    
    # Menampilkan 10 data terbaru secara terbalik (yang baru di atas)
    st.dataframe(df_riwayat.tail(10), use_container_width=True)
else:
    st.info("Belum ada riwayat pemeriksaan yang tersimpan.")