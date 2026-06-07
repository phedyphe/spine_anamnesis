# 1. BUKU CATATAN SEMENTARA (State)
# Kita buat versi mini dulu agar mudah dipahami.
# String kosong "" artinya belum diisi. Nilai None artinya belum ditanyakan.
rekam_medis = {
    "keluhan_utama": "",
    "durasi_keluhan": "",
    "ada_nyeri": None
}

# 2. FUNGSI PENGECEK (Sang Supervisor)
def cek_kekurangan_data(data):
    """
    Fungsi ini akan mengecek dari atas ke bawah.
    Ia akan berhenti dan memberikan instruksi begitu menemukan data yang kosong.
    """
    if data["keluhan_utama"] == "":
        return "Instruksi AI: Tanyakan keluhan utama pasien (misal: leher/punggung sakit, tulang bengkok)."
    
    elif data["durasi_keluhan"] == "":
        return "Instruksi AI: Tanyakan sudah berapa lama keluhan tersebut dirasakan."
    
    elif data["ada_nyeri"] is None:
        return "Instruksi AI: Tanyakan apakah ada rasa nyeri."
    
    else:
        return "SELESAI"

# 3. SIMULASI ALUR KERJA
print("=== SIMULASI SUPERVISOR ===")

# Simulasi 1: Pasien baru datang (semua data masih kosong)
instruksi_sekarang = cek_kekurangan_data(rekam_medis)
print(f"Status 1: {instruksi_sekarang}")

# Simulasi 2: Ceritanya AI sudah mengekstrak keluhan utama dari chat pasien
rekam_medis["keluhan_utama"] = "Tulang punggung bengkok"
print("\n(Supervisor melihat pasien sudah menjawab keluhan utama...)")

instruksi_sekarang = cek_kekurangan_data(rekam_medis)
print(f"Status 2: {instruksi_sekarang}")

# Simulasi 3: Ceritanya AI sudah mengekstrak durasi
rekam_medis["durasi_keluhan"] = "Sudah 3 tahun"
rekam_medis["ada_nyeri"] = False # Pasien bilang tidak nyeri
print("\n(Supervisor melihat durasi dan nyeri sudah terjawab...)")

instruksi_sekarang = cek_kekurangan_data(rekam_medis)
print(f"Status 3: {instruksi_sekarang}")