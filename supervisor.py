# supervisor.py

def cek_kekurangan_data(data):
    """Mengecek form medis sesuai urutan prioritas fase (Rolling Checklist)"""
    
    # FASE 1: Identitas & Keluhan Utama
    # supervisor.py (Ubah bagian Fase 1)

    # FASE 1: Identitas & Keluhan Utama
    if data["nama_pasien"] == "": 
        return "Tanyakan nama pasien. Gunakan kalimat: 'Boleh tahu dengan siapa saya berbicara?'"
    if data["usia"] == "": 
        return "Tanyakan usia pasien. Gunakan kalimat: 'Berapa usia Anda saat ini?'"
    if data["jenis_kelamin"] == "": 
        return "Tanyakan jenis kelamin pasien. Gunakan kalimat: 'Apa jenis kelamin Anda?'"
               
    if data["keluhan_utama"] == "": 
        return "Tanyakan apa keluhan utama yang dirasakan pada tulang belakangnya."
    if data["durasi_keluhan"] == "": 
        return "Tanyakan sudah berapa lama keluhan ini dirasakan."
        
    indikasi_bengkok = ["bengkok", "miring", "asimetris", "skoliosis", "scoliosis", "tinggi sebelah"]
    if any(kata in str(data["keluhan_utama"]).lower() for kata in indikasi_bengkok):
        # PROTEKSI GENDER: Langsung bypass jika laki-laki
        if "laki" in str(data["jenis_kelamin"]).lower():
            data["usia_menarche_atau_akilbaliq"] = "Tidak relevan (Laki-laki)"
        elif data["usia_menarche_atau_akilbaliq"] == "": 
            return "Tanyakan usia saat pasien haid pertama (menarche) atau akil baligh."
    else:
        data["usia_menarche_atau_akilbaliq"] = "Tidak relevan"


    # FASE 2: Red Flags & Neurologis
    if data["kelemahan_atau_kesemutan"] is None: 
        keluhan = str(data["keluhan_utama"]).lower()
        if "leher" in keluhan or "cervical" in keluhan or "tengkuk" in keluhan:
            return "Tanyakan apakah ada rasa kelemahan, kesemutan, atau kebas pada LENGAN/TANGAN dan juga TUNGKAI/KAKI."
        else:
            return "Tanyakan apakah ada rasa kelemahan, kesemutan, atau kebas pada TUNGKAI/KAKI saja."
            
    # LOGIKA CERDAS: Kejar sisi anatomi jika defisit saraf positif
    if str(data["kelemahan_atau_kesemutan"]).lower() not in ["false", "tidak", "none", "tidak ada", "nggak"]:
        if data["sisi_radikuler_kanan_kiri"] == "":
            return "Tanyakan di sisi mana kesemutan atau kelemahan itu dirasakan (apakah kanan, kiri, atau keduanya)."
    else:
        data["sisi_radikuler_kanan_kiri"] = "Tidak relevan"

    if data["gangguan_bab_bak"] is None: 
        return "Tanyakan apakah ada gangguan buang air besar (BAB) atau buang air kecil (BAK)."
    if data["demam_atau_turun_berat_badan"] is None: 
        return "Tanyakan apakah akhir-akhir ini ada demam atau penurunan berat badan drastis."

    # FASE 3: Detail Nyeri & Fungsional
    indikasi_nyeri = ["nyeri", "sakit", "pegal", "ngilu"]
    if any(kata in str(data["keluhan_utama"]).lower() for kata in indikasi_nyeri):
        if data["kualitas_nyeri"] == "": 
            return "Tanyakan rasa nyerinya seperti apa (pegal, ditusuk, tersetrum, atau berdenyut)."
            
        # LOGIKA CERDAS: Skoring VAS
        if data["skor_nyeri_vas"] == "":
            return "Tanyakan berapa skala nyerinya jika diukur dari angka 0 (tidak sakit) sampai 10 (sakit tak tertahankan)."
            
        if data["waktu_muncul_nyeri"] == "": 
            return "Tanyakan kapan nyeri biasanya muncul (pagi, malam, saat aktivitas, dll)."
        if data["pemicu_dan_pereda_nyeri"] == "": 
            return "Tanyakan aktivitas apa yang membuat nyeri memburuk dan apa yang membuatnya membaik."
            
        # LOGIKA CERDAS: Evaluasi Klaudikasio Neurogenik
        if data["kapasitas_fungsional_berjalan"] == "":
            return "Tanyakan perkiraan seberapa jauh (meter) atau berapa lama (menit) pasien sanggup berjalan sebelum nyeri/kesemutan memburuk dan memaksa mereka untuk duduk atau berhenti."
    else:
        data["kualitas_nyeri"] = "Tidak ada keluhan nyeri"
        data["skor_nyeri_vas"] = "0"
        data["waktu_muncul_nyeri"] = "Tidak ada keluhan nyeri"
        data["pemicu_dan_pereda_nyeri"] = "Tidak ada keluhan nyeri"
        data["kapasitas_fungsional_berjalan"] = "Tidak relevan"

    # FASE 4: Pencitraan, Trauma & Pengobatan
    if data["status_pencitraan"] == "":
        return "Tanyakan apakah pasien sudah pernah melakukan pemeriksaan foto Rontgen atau MRI tulang belakang sebelumnya."
    if data["riwayat_trauma_atau_jatuh"] == "": 
        return "Tanyakan apakah keluhan ini berawal dari cedera, jatuh, atau kecelakaan."
    if data["pengobatan_sebelumnya"] == "": 
        return "Tanyakan pengobatan apa saja yang sudah dicoba (obat, fisioterapi, korset, dll)."

    # FASE 5: Riwayat Penyakit & Sosial
    if data["riwayat_penyakit_lain"] == "": 
        return "Tanyakan apakah ada riwayat penyakit penyerta seperti darah tinggi, diabetes, jantung, dll."
    if data["riwayat_operasi"] == "": 
        return "Tanyakan apakah sebelumnya pernah menjalani operasi apa pun."
    if data["pekerjaan_dan_kebiasaan_merokok"] == "": 
        return "Tanyakan apa pekerjaan pasien sehari-hari dan apakah pasien merokok."

    return "SELESAI"