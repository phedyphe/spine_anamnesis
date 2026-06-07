# state.py

rekam_medis = {
    # FASE 1: Identitas & Keluhan Utama
    "nama_pasien": "",
    "usia": "",
    "jenis_kelamin": "",
    
    "keluhan_utama": "",
    "durasi_keluhan": "",
    "usia_menarche_atau_akilbaliq": "",
    
    # FASE 2: Red Flags & Neurologis
    "kelemahan_atau_kesemutan": None,
    "sisi_radikuler_kanan_kiri": "", # Metrik: Lateralisasi (Kanan/Kiri/Bilateral)
    "gangguan_bab_bak": None,
    "demam_atau_turun_berat_badan": None,
    
    # FASE 3: Detail Nyeri & Fungsional
    "kualitas_nyeri": "",
    "skor_nyeri_vas": "", # Metrik: Visual Analogue Scale (0-10)
    "waktu_muncul_nyeri": "",
    "pemicu_dan_pereda_nyeri": "",
    "kapasitas_fungsional_berjalan": "", # Metrik: Neurogenic Claudication Distance
    
    # FASE 4: Pencitraan, Trauma & Pengobatan
    "status_pencitraan": "", # Metrik: Ketersediaan MRI/X-Ray
    "riwayat_trauma_atau_jatuh": "",
    "pengobatan_sebelumnya": "",
    
    # FASE 5: Riwayat Penyakit & Sosial
    "riwayat_penyakit_lain": "",
    "riwayat_operasi": "",
    "pekerjaan_dan_kebiasaan_merokok": ""
}