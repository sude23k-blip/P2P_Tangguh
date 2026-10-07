import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Tim P2PTM & Keswa - Dinkes Pangkep", page_icon="🫀", layout="wide"
)

st.title("🫀 Tim Kerja P2PTM & Keswa")
st.write(
    "**Ketua Tim Kerja:** Hj. Sumarti Usman, SKM., M.Kes[cite: 5]"
)  # Berdasarkan SK Tim Kerja[cite: 5]

# Pembagian Tab Program di bawah Tim P2PTM & Keswa
tab_ptm, tab_haji, tab_keswa = st.tabs([
    "📊 PTM (Hipertensi & DM / CKG)",
    "🩺 Kesehatan Haji & Kanker",
    "🧠 Kesehatan Jiwa & KTR",
])

# --- TAB 1: PTM / CKG (Dashboard yang sudah Anda buat sebelumnya) ---
with tab_ptm:
  st.subheader("Monitoring Program Penyakit Tidak Menular (Hipertensi & DM)")
  st.write(
      "**Penanggung Jawab:** Rosdiana Rahman, SKM[cite: 5]"
  )  # Berdasarkan SK PJ Program[cite: 5]

  # Di sini Anda bisa memasukkan kode pembacaan Google Sheets PTM dan grafik yang sudah kita buat sebelumnya!
  st.info(
      "*(Modul grafik CKG Hipertensi dan DM yang sudah kita buat sebelumnya"
      " dapat ditempatkan di tab ini)*"
  )

# --- TAB 2: KESEHATAN HAJI & KANKER ---
with tab_haji:
  st.subheader("Monitoring Kesehatan Haji, Indera, Kanker, dan Obesitas")
  st.write(
      "**Penanggung Jawab:** Ernawati, SKM[cite: 5]"
  )  # Berdasarkan SK PJ Program[cite: 5]
  st.write(
      "Area untuk menghubungkan Google Sheets laporan pemeriksaan kesehatan"
      " jemaah haji dan deteksi dini kanker."
  )

# --- TAB 3: KESEHATAN JIWA & KTR ---
with tab_keswa:
  st.subheader("Monitoring Kesehatan Jiwa & Kawasan Tanpa Rokok (KTR)")
  st.write(
      "**Penanggung Jawab:** Hj. Sumarti Usman, SKM., M.Kes[cite: 5]"
  )  # Berdasarkan SK PJ Program[cite: 5]
  st.write(
      "Area untuk rekapitulasi data ODMK/ODGJ dan pemantauan indikator KTR."
  )