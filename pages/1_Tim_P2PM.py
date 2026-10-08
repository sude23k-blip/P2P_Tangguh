import pandas as pd
import plotly.express as px
import streamlit as st

# --- DI DALAM BLOK PROGRAM POPM KECACINGAN ---
if pilih_program == "🐛 POPM Kecacingan":
  st.subheader(
      "📊 Analisis Indikator Penting POPM Kecacingan - Kabupaten Pangkep"
  )
  st.write(
      "Analisis mendalam cakupan sasaran, pemberian obat, kelompok umur, dan"
      " identifikasi Puskesmas dengan capaian terendah."
  )
  st.markdown("---")

  # Konfigurasi Link Google Sheets (Pastikan GID sesuai dengan tab Pangkep)
  SPREADSHEET_ID = "1kqVS5KJX-BwmVw9AJ6ysrRaLooxO7qgYmpH4v57agWE"
  GID_PANGKEP = (
      "657728817"  # GID khusus tab Pangkep dari link spreadsheet Anda
  )
  url_sheets = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/export?format=csv&gid={GID_PANGKEP}"


  @st.cache_data(ttl=600)
  def load_popm_data(url):
    df_raw = pd.read_csv(url, header=None)
    return df_raw


  try:
    df_full = load_popm_data(url_sheets)

    # Pilihan Periode Laporan
    pilih_periode = st.selectbox(
        "Pilih Periode Analisis:",
        ["Periode I Tahun 2026", "Periode II Tahun 2026"],
    )

    # Ekstraksi baris berdasarkan tabel Periode I dan II
    idx_p1 = df_full[
        df_full.apply(
            lambda row: row.astype(str).str.contains("PERIODE I TAHUN").any(),
            axis=1,
        )
    ].index
    idx_p2 = df_full[
        df_full.apply(
            lambda row: row.astype(str).str.contains("PERIODE II TAHUN").any(),
            axis=1,
        )
    ].index

    if not idx_p1.empty and not idx_p2.empty:
      row_p1 = idx_p1[0]
      row_p2 = idx_p2[0]

      if pilih_periode == "Periode I Tahun 2026":
        df_clean = df_full.iloc[row_p1 + 4 : row_p2 - 3].copy()
      else:
        df_clean = df_full.iloc[row_p2 + 4 :].copy()

    # Pembersihan Data Utama Puskesmas
    if df_clean.shape[1] > 2:
      df_clean = df_clean.dropna(subset=[df_clean.columns[1]])
      df_clean.columns = [
          "NO",
          "PUSKESMAS",
          "Pos_Jml",
          "Pos_Dapat",
          "TK_Jml",
          "TK_Dapat",
          "SD_Jml",
          "SD_Dapat",
          "Total_Sasaran",
          "S1_4_Tot",
          "S1_4_L",
          "S1_4_P",
          "S5_6_Tot",
          "S5_6_L",
          "S5_6_P",
          "S7_12_Tot",
          "S7_12_L",
          "S7_12_P",
          "Tot_Capaian",
          "J_S1_4_Tot",
          "J_S1_4_L",
          "J_S1_4_P",
          "J_S5_6_Tot",
          "J_S5_6_L",
          "J_S5_6_P",
          "J_S7_12_Tot",
          "J_S7_12_L",
          "J_S7_12_P",
          "POPM_Cacing_Pct",
      ][: df_clean.shape[1]]

      df_clean["NO"] = pd.to_numeric(df_clean["NO"], errors="coerce")
      df = df_clean.dropna(subset=["NO"]).copy()

      # Konversi kolom numerik penting
      numeric_cols = [
          "Total_Sasaran",
          "Tot_Capaian",
          "POPM_Cacing_Pct",
          "Pos_Jml",
          "Pos_Dapat",
          "TK_Jml",
          "TK_Dapat",
          "SD_Jml",
          "SD_Dapat",
      ]
      for col in numeric_cols:
        if col in df.columns:
          df[col] = (
              df[col].astype(str).str.replace(",", ".").astype(float)
          )

      # --- 1. KARTU INDIKATOR UTAMA (METRICS) ---
      st.markdown(f"### 📌 Ringkasan Indikator Utama - {pilih_periode}")

      total_sasaran_kab = (
          df["Total_Sasaran"].sum() if "Total_Sasaran" in df.columns else 0
      )
      total_capaian_kab = (
          df["Tot_Capaian"].sum() if "Tot_Capaian" in df.columns else 0
      )
      avg_cakupan = (
          (total_capaian_kab / total_sasaran_kab * 100)
          if total_sasaran_kab > 0
          else 0
      )

      # Cari Puskesmas dengan cakupan tertinggi dan terendah
      best_pkm = (
          df.loc[df["POPM_Cacing_Pct"].idxmax()]["PUSKESMAS"]
          if not df.empty
          else "-"
      )
      best_pct = (
          df["POPM_Cacing_Pct"].max() if not df.empty else 0
      )
      low_pkm = (
          df.loc[df["POPM_Cacing_Pct"].idxmin()]["PUSKESMAS"]
          if not df.empty
          else "-"
      )
      low_pct = (
          df["POPM_Cacing_Pct"].min() if not df.empty else 0
      )

      m1, m2, m3, m4 = st.columns(4)
      with m1:
        st.metric("Total Sasaran Anak", f"{int(total_sasaran_kab):,}")
      with m2:
        st.metric("Total Anak Minum Obat", f"{int(total_capaian_kab):,}")
      with m3:
        st.metric(
            "Cakupan Kabupaten",
            f"{avg_cakupan:.2f}%",
            delta="Target 100%",
            delta_color="off",
        )
      with m4:
        st.metric(
            "Cakupan Tertinggi", f"{best_pct:.1f}%", delta=f"{best_pkm}"
        )

      st.markdown("---")

      # --- 2. ANALISIS KELOMPOK SASARAN (Posyandu, TK/PAUD, SD/MI) ---
      st.markdown(
          "### 🏫 Analisis Cakupan Berdasarkan Tempat Pelaksanaan (Fasilitas)"
      )
      col_f1, col_f2, col_f3 = st.columns(3)

      with col_f1:
        pos_sas = df["Pos_Jml"].sum() if "Pos_Jml" in df.columns else 0
        pos_cap = df["Pos_Dapat"].sum() if "Pos_Dapat" in df.columns else 0
        pos_pct = (pos_cap / pos_sas * 100) if pos_sas > 0 else 0
        st.metric(
            "Sasaran Posyandu (Anak Usia 1-6 Tahun)",
            f"{int(pos_cap):,} / {int(pos_sas):,}",
            delta=f"{pos_pct:.1f}%",
        )

      with col_f2:
        tk_sas = df["TK_Jml"].sum() if "TK_Jml" in df.columns else 0
        tk_cap = df["TK_Dapat"].sum() if "TK_Dapat" in df.columns else 0
        tk_pct = (tk_cap / tk_sas * 100) if tk_sas > 0 else 0
        st.metric(
            "Sasaran TK / PAUD",
            f"{int(tk_cap):,} / {int(tk_sas):,}",
            delta=f"{tk_pct:.1f}%",
        )

      with col_f3:
        sd_sas = df["SD_Jml"].sum() if "SD_Jml" in df.columns else 0
        sd_cap = df["SD_Dapat"].sum() if "SD_Dapat" in df.columns else 0
        sd_pct = (sd_cap / sd_sas * 100) if sd_sas > 0 else 0
        st.metric(
            "Sasaran SD / MI (Usia 7-12 Tahun)",
            f"{int(sd_cap):,} / {int(sd_sas):,}",
            delta=f"{sd_pct:.1f}%",
        )

      st.markdown("---")

      # --- 3. REKOMENDASI OTOMATIS & EVALUASI PROGRAM ---
      st.markdown("### ⚠️ Evaluasi & Puskesmas Perlu Perhatian Khusus")
      st.write(
          f"Berdasarkan data {pilih_periode}, Puskesmas dengan capaian terendah"
          f" yang memerlukan intervensi/sweeping obat cacing adalah **{low_pkm}**"
          f" dengan cakupan sebesar **{low_pct:.2f}%**."
      )

      # Tabel Puskesmas dengan Capaian di Bawah 95% (Indikator Peringatan Dini)
      df_warning = df[df["POPM_Cacing_Pct"] < 95.0].sort_values(
          by="POPM_Cacing_Pct", ascending=True
      )
      if not df_warning.empty:
        st.warning(
            f"Terdapat {len(df_warning)} Puskesmas dengan cakupan di bawah target"
            " min. 95%:"
        )
        st.dataframe(
            df_warning[["PUSKESMAS", "Total_Sasaran", "Tot_Capaian", "POPM_Cacing_Pct"]],
            use_container_width=True,
        )
      else:
        st.success(
            "🎉 Luar biasa! Seluruh Puskesmas di Kabupaten Pangkep mencapai"
            " cakupan di atas 95% pada periode ini."
        )

      # --- 4. GRAFIK PERBANDINGAN CAKUPAN PUSKESMAS ---
      st.markdown("---")
      st.subheader("📈 Grafik Peringkat Cakupan POPM Kecacingan Per Puskesmas")
      df_sorted = df.sort_values(by="POPM_Cacing_Pct", ascending=False)

      fig = px.bar(
          df_sorted,
          x="PUSKESMAS",
          y="POPM_Cacing_Pct",
          text=df_sorted["POPM_Cacing_Pct"].apply(lambda x: f"{x:.2f}%"),
          color="POPM_Cacing_Pct",
          color_continuous_scale="Tealgrn",
      )
      fig.update_traces(textposition="outside")
      fig.update_layout(
          xaxis_tickangle=-45,
          height=480,
          yaxis_title="Cakupan (%)",
          yaxis_ticksuffix="%",
          xaxis={"categoryorder": "total descending"},
      )
      st.plotly_chart(fig, use_container_width=True)

  except Exception as e:
    st.error(f"Gagal memproses analisis indikator POPM Kecacingan: {e}")
