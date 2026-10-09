# --- PROGRAM TUBERKULOSIS (TB) & KUSTA ---
elif pilih_program == "🩺 Tuberkulosis & Kusta":
  st.subheader("📊 Dashboard Monitoring Tuberkulosis (TBC) & Kusta")
  st.write("**Penanggung Jawab Program:** Muhammad Asdar, SKM., M.Kes")
  st.markdown("---")

  # Masukkan Spreadsheet ID Google Sheets TB Dashboard Anda di sini
  # Contoh: Ambil ID dari link Google Sheets TB Anda
  spreadsheet_id_tb = st.text_input(
      "🔗 Masukkan Spreadsheet ID Google Sheets TB Dashboard:",
      value="",
      placeholder="Contoh: 1X... (Ambil dari URL Google Sheets TB)",
  )

  if spreadsheet_id_tb:
    url_sheets_tb = (
        f"https://docs.google.com/spreadsheets/d/{spreadsheet_id_tb}/export?format=csv"
    )


    @st.cache_data(ttl=600)
    def load_tb_data(url):
      # Berdasarkan gambar, header tabel TB dimulai sekitar baris ke-4 (skiprows=3 atau 4)
      df_raw = pd.read_csv(url, skiprows=3, header=None)
      return df_raw


    try:
      df_full_tb = load_tb_data(url_sheets_tb)

      # Membersihkan dan menamai ulang kolom sesuai struktur gambar
      # Kolom: No, Fasyankes, Target Terduga, Terduga Sesuai Standar, % Penemuan Terduga, Estimasi Kasus, Notifikasi TBC, % Treatment Coverage
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

      # Filter baris valid (buang header teks dan pastikan kolom No berupa angka / baris puskesmas)
      df_tb["No"] = pd.to_numeric(df_tb["No"], errors="coerce")
      df_clean_tb = df_tb.dropna(subset=["No"]).copy()


      # Fungsi pembersih angka / persentase
      def clean_num(val):
        if pd.isna(val) or str(val).strip() in ["", "-", "nan"]:
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


      # Konversi kolom numerik utama
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

      tot_target_terduga = (
          df_clean_tb["Target_Terduga_SPM"].sum()
          if "Target_Terduga_SPM" in df_clean_tb.columns
          else 0
      )
      tot_terduga_standar = (
          df_clean_tb["Terduga_Sesuai_Standar"].sum()
          if "Terduga_Sesuai_Standar" in df_clean_tb.columns
          else 0
      )
      tot_estimasi = (
          df_clean_tb["Estimasi_Kasus_TBC"].sum()
          if "Estimasi_Kasus_TBC" in df_clean_tb.columns
          else
