# main.py
import json
import state
from supervisor import cek_kekurangan_data
from ai_engine import generate_pertanyaan_chat, update_json_siluman

def jalankan_klinik():
    print("=== AUTO-ANAMNESIS ENTERPRISE: SESI BARU DIMULAI ===")
    
    # 1. RESET MEMORI & DATA
    riwayat_percakapan = []
    # Reset data rekam medis ke kondisi awal (kosong)
    for key in state.rekam_medis:
        if state.rekam_medis[key] is None: continue
        state.rekam_medis[key] = ""
    
    # 2. SAPAAN WAJIB DOKTER
    sapaan_awal = "Halo. Saya asisten dokter Phedy. Saya akan bantu untuk pengambilan datanya yah."
    print(f"PA: {sapaan_awal}\n")
    
    # Masukkan sapaan ke dalam sejarah agar AI tidak menyapa lagi di giliran berikutnya
    riwayat_percakapan.append({"role": "AI", "content": sapaan_awal})
    
    while True:
        # Tanya Supervisor apa yang kurang
        instruksi = cek_kekurangan_data(state.rekam_medis)
        
        # Cek apakah form sudah penuh
        if instruksi == "SELESAI":
            print("\nPA: Terima kasih! Datanya sudah lengkap. Dokter akan segera memeriksa Anda.")
            print("\n=== RESUME MEDIS FINAL UNTUK DOKTER ===")
            print(json.dumps(state.rekam_medis, indent=4))
            break
            
        # AI hanya bicara jika giliran ini bukan sapaan awal
        pertanyaan_ai = generate_pertanyaan_chat(instruksi, riwayat_percakapan)
        print(f"PA: {pertanyaan_ai}")
        riwayat_percakapan.append({"role": "AI", "content": pertanyaan_ai})
        
        jawaban_pasien = input("Pasien: ")
        if jawaban_pasien.lower() == 'exit': break
        
        riwayat_percakapan.append({"role": "Pasien", "content": jawaban_pasien})
        
        # Proses background
        teks_obrolan = f"AI bertanya: {pertanyaan_ai}\nPasien menjawab: {jawaban_pasien}"
        print("   [Sistem memproses rekam medis...]")
        state.rekam_medis = update_json_siluman(teks_obrolan, state.rekam_medis)

if __name__ == "__main__":
    jalankan_klinik()