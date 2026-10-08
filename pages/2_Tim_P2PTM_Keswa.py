import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Tim P2PTM & Keswa - Dinkes Pangkep", page_icon="🫀", layout="wide"
)

st.title("🫀 Tim Kerja P2PTM & Keswa")
st.write(
    "**Ketua Tim Kerja:** Hj. Sumarti Usman, SKM., M.Kes"
)  # Berdasarkan SK Tim Kerja[cite: 5]
st.markdown("---")

# Pilihan Program di bawah Tim P2PTM & Keswa menggunakan Selectbox / Radio
pilih_program = st.sidebar.radio(
    "Pilih Program Kerja:",
    [
        "📊 PTM (Hipertensi & DM)",
        "🩺 Kes. Haji, Indera, Kanker & Obesitas",
        "🧠 Keswa & KTR",
    ],
)

# --- 1. PROGRAM PTM (HIPERTENSI & DM) ---
if pilih_program == "📊 PTM (Hipertensi & DM)":
  st.subheader("Monitoring Program Penyakit Tidak Menular (Hipertensi & DM)")
  st.write(
      "**Penanggung Jawab Program:** Rosdiana Rahman, SKM"
  )  # Berdasarkan SK PJ[cite: 5]

  # File atau Google Sheets khusus PTM
  default_file_ptm = "data_default_ptm.xlsx"

  uploaded_file = st.file_uploader(
      "📁 Upload file Excel laporan PTM terbaru", type=["xlsx", "csv"]
  )

  # Logika pembacaan data PTM di sini...
  st.info("Area pengolahan data dan grafik khusus program PTM (Hipertensi & DM).")

# --- 2. PROGRAM KESEHATAN HAJI, INDERA, KANKER & OBESITAS ---
elif pilih_program == "🩺 Kes. Haji, Indera, Kanker & Obesitas":
  st.subheader("Monitoring Kesehatan Haji, Indera, Kanker, dan Obesitas")
  st.write(
      "**Penanggung Jawab Program:** Ernawati, SKM"
  )  # Berdasarkan SK PJ[cite: 5]

  # File atau Google Sheets khusus Haji/Kanker
  default_file_haji = "data_default_haji.xlsx"

  uploaded_file_haji = st.file_uploader(
      "📁 Upload file Excel laporan Kes. Haji & Kanker terbaru",
      type=["xlsx", "csv"],
  )

  st.info(
      "Area pengolahan data khusus laporan Kesehatan Haji, Indera, Kanker, dan"
      " Obesitas."
  )

# --- 3. PROGRAM KESEHATAN JIWA & KTR ---
elif pilih_program == "🧠 Keswa & KTR":
  st.subheader("Monitoring Kesehatan Jiwa & Kawasan Tanpa Rokok (KTR)")
  st.write(
      "**Penanggung Jawab Program:** Hj. Sumarti Usman, SKM., M.Kes"
  )  # Berdasarkan SK PJ[cite: 5]

  uploaded_file_keswa = st.file_uploader(
      "📁 Upload file Excel laporan Keswa & KTR terbaru", type=["xlsx", "csv"]
  )

  st.info(
      "Area pengolahan data khusus rekapitulasi Kesehatan Jiwa (ODGJ/ODMK) dan"
      " KTR."
  )
