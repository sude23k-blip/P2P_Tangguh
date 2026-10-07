import streamlit as st

# Konfigurasi Halaman Utama
st.set_page_config(
    page_title="Portal P2P Dinkes Pangkep", page_icon="🏥", layout="wide"
)

st.title("🏥 Portal Eksekutif Bidang P2P")
st.subheader(
    "Dinas Kesehatan Kabupaten Pangkep | Tahun 2026"
)  # Berdasarkan SK Nomor 7842/Dinkes-PK/P2P/VI/2026

st.markdown("""
Selamat datang di Portal Dashboard Terintegrasi Bidang Pencegahan dan Pengendalian Penyakit (P2P). 
Sistem ini dirancang untuk memantau capaian program dari 3 Tim Kerja secara *real-time* berdasarkan laporan dari seluruh Puskesmas di Kabupaten Pangkep.
""")

st.markdown("---")

# Kartu Navigasi / Menu Akses Cepat per Tim Kerja
st.markdown("### 📂 Pilih Tim Kerja / Bidang Program:")

col1, col2, col3 = st.columns(3)

with col1:
  st.markdown("#### 🦠 1. Tim Kerja P2PM")
  st.write(
      "**Ketua:** Abd. Halim, SKM., M.Kes"
  )  # Berdasarkan SK Tim Kerja[cite: 5]
  st.write("Mencakup: TBC, Kusta, DBD, Malaria, HIV, Diare, ISPA, dll.")
  st.info("👉 Buka menu di sidebar kiri untuk mengakses halaman P2PM.")

with col2:
  st.markdown("#### 🫀 2. Tim Kerja P2PTM & Keswa")
  st.write(
      "**Ketua:** Hj. Sumarti Usman, SKM., M.Kes"
  )  # Berdasarkan SK Tim Kerja[cite: 5]
  st.write(
      "Mencakup: PTM (Hipertensi & DM), Kanker, Obesitas, Kesehatan Jiwa, & KTR"
  )
  st.info("👉 Buka menu di sidebar kiri untuk mengakses halaman P2PTM & Keswa.")

with col3:
  st.markdown("#### 📈 3. Tim Kerja Surveilans & Imunisasi")
  st.write(
      "**Ketua:** Muhammad Anas, SKM., M.Kes"
  )  # Berdasarkan SK Tim Kerja[cite: 5]
  st.write("Mencakup: Data Surveilans Penyakit & Cakupan Imunisasi")
  st.info(
      "👉 Buka menu di sidebar kiri untuk mengakses halaman Surveilans &"
      " Imunisasi."
  )

st.markdown("---")
st.caption(
    "💡 *Tips:* Gunakan menu navigasi di sebelah kiri layar Anda untuk berpindah"
    " antar halaman Tim Kerja."
)