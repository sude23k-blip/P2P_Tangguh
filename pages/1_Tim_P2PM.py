import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Tim P2PM - Dinkes Pangkep", page_icon="🦠", layout="wide"
)

st.title("🦠 Tim Kerja P2 Penyakit Menular (P2PM)")
st.write("**Ketua Tim Kerja:** Halim, SKM., M.Kes")
st.markdown("---")

pilih_program = st.sidebar.radio(
    "Pilih Program Kerja P2PM:",
    [
        "🐛 POPM Kecacingan",
        "🦟 Malaria, DBD & Filariasis",
        "🩺 Tuberkulosis & Kusta",
        "💉 Diare & HIV",
    ],
)

# --- 1. PROGRAM POPM KECACINGAN ---
if pilih_program == "🐛 POPM Kecacingan":
  # (Kode POPM Kecacingan yang sudah kita buat sebelumnya tetap di sini...)
  st.subheader(
      "📊 Analisis Indikator Penting POPM Kecacingan - Kabupaten Pangkep"
  )
  # ... (biarkan bagian POPM tetap seperti sebelumnya)

# --- 2. PROGRAM TUBERKULOSIS (TB) & KUSTA ---
elif pilih_program == "🩺 Tuberkulosis & Kusta":
  st.subheader("📊 Dashboard Monitoring Tuberkulosis (TBC) & Kusta")
  st.write("**Penanggung Jawab Program:** Muhammad Asdar, SKM., M.Kes")
  st.markdown("---")

  # Konfigurasi Link Google Sheets TB Dashboard (Sheet2 / GID 1080277873)
  SPREADSHEET_ID_TB = "1rtiP7ksaIixLTenoQxlrPzl3njHGOu6KQOohVCM4S3k"
  GID_TB = "1080277873"
  url_sheets_tb = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID_TB}/export?format=csv&gid={GID_TB}"


  @st.cache_data(ttl=600)
  def load_tb_data(url):
    # Berdasarkan gambar, tabel data TB dimulai pada baris ke-5 (skiprows=4)
    df_raw = pd.read_csv(url, skiprows=4, header=None)
    return df_raw


  try:
    df_full_tb = load_tb_data(url_sheets_tb)

    # Ambil baris data utama (dari baris 1 sampai baris total Pangkep)
    df_tb = df_full_tb.dropna(subset=[df_full_tb.columns[1]]).copy()
    df_tb.columns = [
        "No",
        "Fasyankes",
        "Target_Terduga_SPM",
        "Terduga_Sesuai_Standar",
        "Persen_Terduga_SPM",
        "Estimasi_Kasus_TBC",
        "Notifikasi_TBC",
        "Persen_Treatment_Coverage",
    ][: df_tb.shape[1]]

    # Filter baris yang memiliki nomor valid (Puskesmas/RS/Klinik)
    df_tb["No"] = pd.to_numeric(df_tb["No"], errors="coerce")
    df_clean_tb = df_tb.dropna(subset=["No"]).copy()


    # Fungsi pembersih angka
    def clean_num(val):
      if pd.isna(val) or str(val).strip() in ["", "-", "nan", "PANGKEP"]:
        return 0.0
      val_str = (
          str(val)
          .replace("%", "")
          .replace(".", "")
          .replace(",", ".")
          .strip()
      )
      try:
        return float(val_str)
      except:
        return 0.0


    for col in [
        "Target_Terduga_SPM",
        "Terduga_Sesuai_Standar",
        "Estimasi_Kasus_TBC",
        "Notifikasi_TBC",
    ]:
      if col in df_clean_tb.columns:
        df_clean_tb[col] = df_clean_tb[col].apply(
            lambda x: float(
                str(x).replace(".", "").replace(",", ".").strip()
            )
            if str(x).strip() not in ["", "-", "nan"]
            else 0.0
        )

    st.success("✅ Berhasil terhubung live ke Google Sheets TB Dashboard!")

    # --- 1. KARTU RINGKASAN INDIKATOR UTAMA TB ---
    st.markdown("### 📌 Ringkasan Capaian TBC Kabupaten Pangkep")

    tot_target_terduga = df_clean_tb["Target_Terduga_SPM"].sum()
    tot_terduga_standar = df_clean_tb["Terduga_Sesuai_Standar"].sum()
    tot_estimasi = df_clean_tb["Estimasi_Kasus_TBC"].sum()
    tot_notifikasi = df_clean_tb["Notifikasi_TBC"].sum()

    pct_terduga_kab = (
        (tot_terduga_standar / tot_target_terduga * 100)
        if tot_target_terduga > 0
        else 0
    )
    pct_treatment_cov = (
        (tot_notifikasi / tot_estimasi * 100) if tot_estimasi > 0 else 0
    )

    tb1, tb2, tb3, tb4 = st.columns(4)
    with tb1:
      st.metric("Total Terduga Sesuai Standar", f"{int(tot_terduga_standar):,}")
    with tb2:
      st.metric("Cakupan SPM Terduga", f"{pct_terduga_kab:.1f}%")
    with tb3:
      st.metric("Total Notifikasi Kasus TBC", f"{int(tot_notifikasi):,}")
    with tb4:
      st.metric("Treatment Coverage", f"{pct_treatment_cov:.1f}%")

    st.markdown("---")

    # --- 2. TABEL DATA RINCI FASYANKES ---
    st.subheader("📋 Tabel Data Penemuan & Notifikasi TBC per Fasyankes")
    st.dataframe(df_clean_tb, use_container_width=True)

    # --- 3. GRAFIK NOTIFIKASI KASUS TBC PER FASYANKES ---
    if "Fasyankes" in df_clean_tb.columns and "Notifikasi_TBC" in df_clean_tb.columns:
      st.markdown("---")
      st.subheader("📈 Grafik Notifikasi Kasus TBC per Fasyankes")
      df_tb_sorted = df_clean_tb.sort_values(
          by="Notifikasi_TBC", ascending=False
      )

      fig_tb = px.bar(
          df_tb_sorted,
          x="Fasyankes",
          y="Notifikasi_TBC",
          text="Notifikasi_TBC",
          color="Notifikasi_TBC",
          color_continuous_scale="Reds",
      )
      fig_tb.update_traces(texttemplate="%{text:,}", textposition="outside")
      fig_tb.update_layout(
          xaxis_tickangle=-45,
          height=500,
          yaxis_title="Jumlah Notifikasi Kasus",
          xaxis={"categoryorder": "total descending"},
      )
      st.plotly_chart(fig_tb, use_container_width=True)

  except Exception as e:
    st.error(f"Gagal memproses Google Sheets TB Dashboard: {e}")

# --- 3. PROGRAM LAIN DI BAWAH P2PM ---
elif pilih_program == "🦟 Malaria, DBD & Filariasis":
  st.subheader("Monitoring Program Malaria, DBD, dan Filariasis")
  st.write("**Penanggung Jawab Program:** Abdul Halim, SKM., M.Kes")
  st.info("Modul laporan siap dihubungkan ke Google Sheets.")

elif pilih_program == "💉 Diare & HIV":
  st.subheader("Monitoring Program Diare & HIV")
  st.write("**Penanggung Jawab Program:** Marliati, SKM")
  st.info("Modul laporan siap dihubungkan ke Google Sheets.")
