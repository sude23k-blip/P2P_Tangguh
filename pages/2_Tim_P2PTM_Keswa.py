import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Tim P2PTM & Keswa - Dinkes Pangkep", page_icon="🫀", layout="wide"
)

st.title("🫀 Tim Kerja P2PTM & Keswa")
st.write(
    f"**Ketua Tim Kerja:** Hj. Sumarti Usman, SKM., M.Kes[cite: 5]"
)
st.markdown("---")

# Pilihan Program di bawah Tim P2PTM & Keswa menggunakan Selectbox / Radio di Sidebar
pilih_program = st.sidebar.radio(
    "Pilih Program Kerja:",
    [
        "📊 PTM (Hipertensi & DM)",
        "🩺 Kes. Haji, Indera, Kanker & Obesitas",
        "🧠 Keswa & KTR",
    ],
)

# --- 1. PROGRAM PTM (HIPERTENSI & DM / CKG) ---
if pilih_program == "📊 PTM (Hipertensi & DM)":
  st.subheader(
      "Monitoring Program Penyakit Tidak Menular (Hipertensi, Diabetes, Jantung,"
      " Stroke)"
  )
  st.write(
      f"**Penanggung Jawab Program:** Rosdiana Rahman, SKM[cite: 5]"
  )
  st.markdown("---")

  # --- PENGATURAN DATA PTM ---
  default_file_path = "data_default.xlsx"  # Atau file khusus PTM jika ada

  uploaded_file = st.file_uploader(
      "📁 Upload file Excel laporan CKG / PTM terbaru (Opsional - Jika ingin"
      " mengganti data default)",
      type=["xlsx", "csv"],
  )

  data_loaded = False
  df_raw = None

  if uploaded_file is not None:
    try:
      df_raw = pd.read_excel(uploaded_file, sheet_name="Data Agregat CKG")
      st.success("✅ Menggunakan data dari file PTM yang baru di-upload!")
      data_loaded = True
    except:
      try:
        df_raw = pd.read_excel(uploaded_file)
        st.success("✅ Menggunakan data dari file PTM yang baru di-upload!")
        data_loaded = True
      except Exception as e:
        st.error(f"Gagal membaca file yang di-upload: {e}")

  elif os.path.exists(default_file_path):
    try:
      df_raw = pd.read_excel(default_file_path, sheet_name="Data Agregat CKG")
      st.info(
          "ℹ️ Menampilkan data default sistem untuk program PTM (Hipertensi &"
          " DM)."
      )
      data_loaded = True
    except:
      try:
        df_raw = pd.read_excel(default_file_path, sheet_name=0)
        st.info("ℹ️ Menampilkan data default dari sheet pertama.")
        data_loaded = True
      except Exception as e:
        st.error(f"Gagal membaca file default sistem: {e}")
  else:
    st.warning(
        "⚠️ File data default belum ditemukan. Silakan upload file laporan"
        " melalui tombol di atas."
    )

  # Jika data berhasil dimuat, jalankan seluruh analisis CKG Hipertensi & DM
  if data_loaded and df_raw is not None:
    df_original = df_raw.copy()

    # Filter Wilayah
    st.subheader("🔍 Filter Wilayah & Faskes PTM")
    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
      if "Nama Kabupaten Kota" in df_raw.columns:
        kab_list = ["Semua"] + list(df_raw["Nama Kabupaten Kota"].unique())
        pilih_kab = st.selectbox("Kabupaten / Kota:", options=kab_list)
        if pilih_kab != "Semua":
          df_raw = df_raw[df_raw["Nama Kabupaten Kota"] == pilih_kab]
          df_original = df_original[
              df_original["Nama Kabupaten Kota"] == pilih_kab
          ]

    with col_f2:
      if "Nama Kecamatan" in df_raw.columns:
        kec_list = ["Semua"] + list(df_raw["Nama Kecamatan"].unique())
        pilih_kec = st.selectbox("Kecamatan:", options=kec_list)
        if pilih_kec != "Semua":
          df_raw = df_raw[df_raw["Nama Kecamatan"] == pilih_kec]

    with col_f3:
      if "Nama Faskes" in df_raw.columns:
        faskes_list = ["Semua"] + list(df_raw["Nama Faskes"].unique())
        pilih_faskes = st.selectbox("Puskesmas / Faskes:", options=faskes_list)
        if pilih_faskes != "Semua":
          df_raw = df_raw[df_raw["Nama Faskes"] == pilih_faskes]

    df = df_raw
    st.markdown("---")

    # Perhitungan Variabel Utama
    scr_ht = (
        df["Jumlah Orang Diperiksa Tekanan Darah"].sum()
        if "Jumlah Orang Diperiksa Tekanan Darah" in df.columns
        else 0
    )
    tot_ht = (
        df["Jumlah Penderita Hipertensi"].sum()
        if "Jumlah Penderita Hipertensi" in df.columns
        else 0
    )
    prev_ht = (tot_ht / scr_ht * 100) if scr_ht > 0 else 0
    diag_ht = (
        df["Diagnosis Hipertensi"].sum()
        if "Diagnosis Hipertensi" in df.columns
        else 0
    )
    persen_diag_ht = (diag_ht / tot_ht * 100) if tot_ht > 0 else 0
    obat_ht = df["Diberikan Obat"].sum() if "Diberikan Obat" in df.columns else 0
    persen_ht = (obat_ht / tot_ht * 100) if tot_ht > 0 else 0

    scr_dm = (
        df["Jumlah Orang Diperiksa gula darah (Usia ≥ 18 Tahun)"].sum()
        if "Jumlah Orang Diperiksa gula darah (Usia ≥ 18 Tahun)" in df.columns
        else 0
    )
    tot_dm = (
        df["Jumlah Penderita Diabetes"].sum()
        if "Jumlah Penderita Diabetes" in df.columns
        else 0
    )
    prev_dm = (tot_dm / scr_dm * 100) if scr_dm > 0 else 0
    diag_dm = (
        df["Diberikan Diagnosis"].sum()
        if "Diberikan Diagnosis" in df.columns
        else 0
    )
    persen_diag_dm = (diag_dm / tot_dm * 100) if tot_dm > 0 else 0
    obat_dm = (
        df["Diberikan Obat Diabetes"].sum()
        if "Diberikan Obat Diabetes" in df.columns
        else 0
    )
    persen_dm = (obat_dm / tot_dm * 100) if tot_dm > 0 else 0

    # Tampilan Menu Tab di dalam Program PTM
    tab_ptm1, tab_ptm2, tab_ptm3 = st.tabs([
        "📊 Ringkasan & Grafik Kasus",
        "📋 Analisis & Detail",
        "📁 Tabel Data PTM",
    ])

    with tab_ptm1:
      st.subheader("📊 Ringkasan Capaian Hipertensi & Diabetes Melitus")

      st.markdown("##### 🔹 Ringkasan Hipertensi (HT)")
      mc1, mc2, mc3 = st.columns(3)
      with mc1:
        st.metric(
            "Total Penderita Hipertensi",
            f"{tot_ht:,}",
            delta=f"{prev_ht:.1f}% dari {scr_ht:,} diskrining",
        )
      with mc2:
        st.metric(
            "Hipertensi Diberikan Diagnosis",
            f"{diag_ht:,}",
            delta=f"{persen_diag_ht:.1f}% dari penderita",
        )
      with mc3:
        st.metric(
            "Hipertensi Diberikan Obat",
            f"{obat_ht:,}",
            delta=f"{persen_ht:.1f}% dari penderita",
        )

      st.markdown("")
      st.markdown("##### 🔹 Ringkasan Diabetes Melitus (DM)")
      mc4, mc5, mc6 = st.columns(3)
      with mc4:
        st.metric(
            "Total Penderita Diabetes",
            f"{tot_dm:,}",
            delta=f"{prev_dm:.1f}% dari {scr_dm:,} diskrining",
        )
      with mc5:
        st.metric(
            "Diabetes Diberikan Diagnosis",
            f"{diag_dm:,}",
            delta=f"{persen_diag_dm:.1f}% dari penderita",
        )
      with mc6:
        st.metric(
            "Diabetes Diberikan Obat",
            f"{obat_dm:,}",
            delta=f"{persen_dm:.1f}% dari penderita",
        )

      st.markdown("---")

      # Grafik Penderita HT Berdasarkan Kecamatan
      if (
          "Jumlah Penderita Hipertensi" in df.columns
          and "Nama Kecamatan" in df.columns
      ):
        st.subheader("📈 Grafik Penderita Hipertensi Berdasarkan Kecamatan")
        chart_kec_ht = (
            df.groupby("Nama Kecamatan")["Jumlah Penderita Hipertensi"]
            .sum()
            .reset_index()
            .sort_values(by="Jumlah Penderita Hipertensi", ascending=False)
        )
        fig_kec_ht = px.bar(
            chart_kec_ht,
            x="Nama Kecamatan",
            y="Jumlah Penderita Hipertensi",
            text="Jumlah Penderita Hipertensi",
            color="Jumlah Penderita Hipertensi",
            color_continuous_scale="Blues",
        )
        fig_kec_ht.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_kec_ht.update_layout(
            xaxis_tickangle=-45,
            height=400,
            xaxis={"categoryorder": "total descending"},
        )
        st.plotly_chart(fig_kec_ht, use_container_width=True)

    with tab_ptm2:
      st.subheader("📋 Analisis Lanjutan & Alasan Klinis")
      st.info(
          "Modul analisis diagnosis dan alasan pengobatan PTM aktif ditampilkan"
          " di sini."
      )

    with tab_ptm3:
      st.subheader("📁 Tabel Data Detail PTM")
      st.dataframe(df, use_container_width=True)

# --- 2. PROGRAM KESEHATAN HAJI, INDERA, KANKER & OBESITAS ---
elif pilih_program == "🩺 Kes. Haji, Indera, Kanker & Obesitas":
  st.subheader("Monitoring Kesehatan Haji, Indera, Kanker, dan Obesitas")
  st.write(
      f"**Penanggung Jawab Program:** Ernawati, SKM[cite: 5]"
  )
  st.info("Modul laporan kesehatan haji dan deteksi dini kanker aktif.")

# --- 3. PROGRAM KESEHATAN JIWA & KTR ---
elif pilih_program == "🧠 Keswa & KTR":
  st.subheader("Monitoring Kesehatan Jiwa & Kawasan Tanpa Rokok (KTR)")
  st.write(
      f"**Penanggung Jawab Program:** Hj. Sumarti Usman, SKM., M.Kes[cite: 5]"
  )
  st.info("Modul laporan kesehatan jiwa dan KTR aktif.")
