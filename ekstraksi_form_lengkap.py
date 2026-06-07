import ollama
import json

def ekstraksi_anamnesis_komprehensif():
    # 1. BUKU CATATAN DIGITAL (JSON SCHEMA)
    # Ini adalah terjemahan langsung dari formulir .docx Anda ke dalam bahasa mesin
    target_medis = {
        "identitas_dan_keluhan": {
            "usia_menarche_atau_akilbaliq": "",
            "keluhan_utama_yang_dirasakan": [], # Contoh isi: ["Nyeri punggung bawah", "tulang punggung bengkok"]
            "keluhan_lainnya": [], # Contoh isi: ["Kelemahan", "Kesemutan", "Gangguan BAB"]
            "keluhan_paling_mengganggu": "",
            "durasi_keluhan": ""
        },
        "detail_nyeri": {
            "ada_nyeri": False,
            "kualitas_nyeri": "", # Pegal/berat, Ditusuk-tusuk, Seperti tersetrum, Berdenyut
            "sifat_munculnya_nyeri": "", # Tiba-tiba, perlahan, saat tidur, terus menerus, hilang timbul
            "waktu_timbul_utama": "", 
            "pemicu_nyeri": [],
            "pereda_nyeri": []
        },
        "detail_kesemutan": {
            "ada_kesemutan": False,
            "pemicu_kesemutan": [],
            "pereda_kesemutan": []
        },
        "trauma_dan_pengobatan": {
            "akibat_trauma_atau_kecelakaan": False,
            "mekanisme_kejadian": "",
            "pengobatan_yang_sudah_diterima": [] # Obat, Fisioterapi, Korset, Suntikan, dll
        },
        "riwayat_kesehatan_dan_sosial": {
            "riwayat_penyakit_pribadi": [], # Kencing manis, Darah tinggi, Kanker, dll
            "pernah_operasi_tulang_punggung": False,
            "pekerjaan_saat_ini": "",
            "konsumsi_rutin": [] # Rokok, Alkohol, Narkotika
        }
    }

    # 2. PROMPT SISTEM (OTAK AI)
    prompt_sistem = f"""
    Kamu adalah asisten medis ahli untuk dokter spesialis Orthopaedi Spine. 
    Tugasmu adalah membaca cerita atau rekaman percakapan pasien, lalu mengekstrak SEMUA informasi medis ke dalam format JSON yang sangat terstruktur.

    Gunakan struktur JSON persis seperti ini:
    {json.dumps(target_medis, indent=2)}

    ATURAN EKSTRAKSI (SANGAT KETAT):
    1. Jika data tidak disebutkan oleh pasien, isi dengan string kosong "" atau array kosong []. Jangan mengarang data.
    2. Untuk field boolean (seperti "ada_nyeri", "akibat_trauma_atau_kecelakaan"), isi dengan true atau false.
    3. Ekstrak data red flags (kelemahan, gangguan BAB/BAK) dan masukkan ke dalam array "keluhan_lainnya".
    4. OUTPUT HANYA BOLEH JSON VALID. Dilarang memberikan teks sapaan, penjelasan, atau penutup.
    """

    # 3. SIMULASI INPUT PASIEN (Contoh kasus deformitas + radikulopati)
    cerita_pasien = """
    Dok, saya sakit punggung bawah udah sekitar 6 bulan, tapi yang paling ganggu itu kaki kanan saya rasanya kesemutan dan kayak tersetrum, apalagi kalau saya kelamaan duduk di kantor. Kalau dibawa rebahan baru enakan. 
    Dulu sih waktu umur 12 tahun pas baru mens pertama emang dibilang tulang saya agak bengkok, tapi nggak sakit. 
    Sekarang umurnya udah 25 tahun, kerja kantoran duduk terus. Oh ya, saya nggak pernah kecelakaan sih, buang air juga normal lancar. Belum pernah diobatin apa-apa cuma minum paracetamol aja. Saya ada keturunan darah tinggi dari ibu.
    """

    print("Memproses ekstraksi dokumen rekam medis otomatis...\n")
    
    try:
        # 4. MEMANGGIL ENGINE LOKAL (Qwen 3B yang ringan untuk GPU 6GB Anda)
        response = ollama.chat(
            model='qwen2.5:3b',
            messages=[
                {'role': 'system', 'content': prompt_sistem},
                {'role': 'user', 'content': cerita_pasien}
            ],
            format='json'
        )

        # 5. MENCETAK HASIL
        hasil_mentah = response['message']['content']
        hasil_terstruktur = json.loads(hasil_mentah)
        
        print("=== RESUME MEDIS TERSTRUKTUR ===")
        print(json.dumps(hasil_terstruktur, indent=4))
        
    except Exception as e:
        print(f"Terjadi error saat menjalankan AI: {e}")

if __name__ == "__main__":
    ekstraksi_anamnesis_komprehensif()