import ollama
import json

def jalankan_anamnesis():
    # 1. Target output: Parameter deformitas yang wajib ada
    target_medis = {
        "identitas": {"usia": "", "jenis_kelamin": ""},
        "kurva_deformitas": {
            "sadar_sejak_kapan": "",
            "keluhan_kosmetik": ""
        },
        "red_flags": {
            "nyeri_punggung": False,
            "kelemahan_motorik_kaki": False,
            "gangguan_bab_bak": False
        }
    }

    # 2. Simulasi suara/ketikan pasien
    cerita_pasien = """
    Dok, anak saya perempuan umurnya 14 tahun. Saya baru sadar bahunya tinggi sebelah 
    kira-kira 4 bulan yang lalu pas fitting baju seragam. Anaknya sih nggak ngeluh 
    sakit punggung atau lemes kakinya, pipis juga biasa aja. Cuma dia malu kalau 
    pakai baju ketat karena kelihatan miring.
    """

    # 3. Prompt untuk AI Qwen
    prompt_dokter = f"""
    Anda adalah asisten AI untuk dokter spesialis Orthopaedi Spine. 
    Ekstrak cerita pasien berikut ke dalam format JSON persis seperti struktur ini:
    {json.dumps(target_medis, indent=2)}

    Aturan:
    1. Ekstrak data red flags menjadi true/false.
    2. Jika tidak ada info, isi dengan "".
    3. Output HANYA JSON murni tanpa kata pengantar apapun.
    """

    print("AI sedang memproses cerita pasien...\n")
    
    # 4. Eksekusi AI secara offline
    response = ollama.chat(
        model='qwen2.5:3b',
        messages=[
            {'role': 'system', 'content': prompt_dokter},
            {'role': 'user', 'content': cerita_pasien}
        ],
        format='json'
    )

    # 5. Tampilkan hasil JSON yang rapi
    hasil_json = json.loads(response['message']['content'])
    print(json.dumps(hasil_json, indent=4))

# Jalankan fungsi
if __name__ == "__main__":
    jalankan_anamnesis()