# ai_engine.py
import json
from langchain_ollama import ChatOllama

# =====================================================================
# 1. INISIALISASI LLM (LANGCHAIN)
# =====================================================================
# Mesin Chatbot: Suhu 0.2 (Konsisten, klinis, tidak berhalusinasi), dibatasi 120 token
llm_chat = ChatOllama(
    model="qwen2.5:3b",      
    temperature=0.2,         
    num_predict=120,         
)

# Mesin Ekstraktor JSON: Suhu 0.0 (Sangat kaku dan deterministik)
llm_json = ChatOllama(
    model="qwen2.5:3b",
    temperature=0.0,
    format="json" 
)

# =====================================================================
# 2. FUNGSI CHAT PA SENIOR
# =====================================================================
def generate_pertanyaan_chat(instruksi_supervisor, riwayat_percakapan):
    """Menghasilkan kalimat PA Senior menggunakan LangChain dan memori Sliding Window"""
    
    # Ambil 10 baris obrolan terakhir untuk mencegah VRAM Overload
    riwayat_terbaru = riwayat_percakapan[-10:] if len(riwayat_percakapan) > 10 else riwayat_percakapan
    
    teks_transkrip = ""
    for chat in riwayat_terbaru:
        teks_transkrip += f"{chat['role']}: {chat['content']}\n"

    """Menghasilkan kalimat PA Senior menggunakan LangChain"""
    
    # 1. Tentukan apakah ini giliran pertama
    is_first_turn = len(riwayat_percakapan) == 0
    
    # 2. Buat instruksi tambahan khusus untuk giliran pertama
    instruksi_tambahan = ""
    if is_first_turn:
        instruksi_tambahan = "JANGAN PERNAH MENYAPA. JANGAN PERNAH MEMPERKENALKAN DIRI. JANGAN PERNAH MENGUCAPKAN BASA-BASI. LANGSUNG TANYAKAN KELUHAN UTAMA PASIEN."

    # 3. Ambil riwayat percakapan
    riwayat_terbaru = riwayat_percakapan[-10:] if len(riwayat_percakapan) > 10 else riwayat_percakapan
    teks_transkrip = ""
    for chat in riwayat_terbaru:
        teks_transkrip += f"{chat['role']}: {chat['content']}\n"
    
    # 4. Susun Prompt dengan variabel yang sudah bersih
    system_prompt = f"""
    Kamu adalah seorang Physician Assistant (PA) Senior di bidang Bedah Ortopedi Tulang Belakang 
    (Orthopedic Spine Surgery) dengan pengalaman klinis lebih dari 20 tahun. Tugas utamamu adalah 
    melakukan anamnesis kepada pasien sebelum mereka bertemu dengan Dokter Bedah Utama.

    GAYA KOMUNIKASI & NADA (TONE):

    1. Profesional & Klinis: Gunakan bahasa yang sopan namun terarah.
    2. Singkat & Padat: Jangan menggunakan kalimat basa-basi. Tunjukkan empati melalui validasi singkat.
    3. Tidak Menggurui: Jangan pernah memberikan diagnosis atau saran pengobatan. Tugasmu HANYA bertanya.

    ATURAN MUTLAK DARI DOKTER (SANGAT KETAT):
    1. HANYA BOLEH BERTANYA SATU (1) PERTANYAAN SAJA PER GILIRAN. (WAJIB PATUH)
       - Jika instruksi supervisor berisi lebih dari satu poin pertanyaan/kalimat, kamu WAJIB hanya mengambil kalimat PERTAMA saja.
       - Abaikan instruksi setelah kalimat pertama. Jangan pernah menggabungkan pertanyaan.
       - Contoh: Jika disuruh tanya "Tangan dan kaki", kamu HANYA boleh tanya "Tangan".
       - Jangan menggabungkan pertanyaan menjadi "Tangan dan kaki". Itu TIDAK BOLEH.
       - Jangan menggabungkan pertanyaan dengan kalimat lain seperti "Tangan, dan juga umur". Itu TIDAK BOLEH.
    2. LANGSUNG keluarkan ucapanmu. DILARANG KERAS menulis awalan "AI:", "PA:", atau "Pasien:".
    3. JANGAN PERNAH mengarang jawaban pasien.
    4. Jika pasien mulai kesal (misal: "tadi saya sudah jawab"), MINTA MAAF dengan sopan lalu ganti cara bertanya.
    5. Jika pasien bertanya balik, jawab dengan singkat lalu kembali ke tugas medis.
    6. LANGSUNG tanyakan informasi medis yang dibutuhkan sesuai tugas.

    RIWAYAT OBROLAN:
    {teks_transkrip}

    TUGAS UTAMAMU SAAT INI (Gali informasi ini sekarang juga): 
    {instruksi_supervisor}
    """
    
    # Menjalankan prompt menggunakan LangChain
    response = llm_chat.invoke(system_prompt)
    hasil = response.content
    
    # Pembersih darurat jika AI masih membandel
    if hasil.startswith("AI:"):
        hasil = hasil.replace("AI:", "", 1).strip()
    elif hasil.startswith("PA:"):
        hasil = hasil.replace("PA:", "", 1).strip()
        
    return hasil

# =====================================================================
# 3. FUNGSI EKSTRAKTOR JSON
# =====================================================================
def update_json_siluman(percakapan_baru, data_sekarang):
    """Mengekstrak data medis di background menggunakan LLM LangChain Format JSON"""
    
    system_prompt = f"""
    Kamu adalah AI Data Entry Medis.
    Tugasmu memperbarui JSON berdasarkan obrolan terbaru.
    
    JSON Saat Ini:
    {json.dumps(data_sekarang, indent=2)}
    
    PANDUAN KLINIS (CONTOH CARA MENGISI):
    - Jika pasien bilang "kanan", "kiri", atau "dua-duanya" saat ditanya kesemutan, masukkan ke key "sisi_radikuler_kanan_kiri".
    - Jika pasien bilang "bahu" atau "leher", masukkan ke key "keluhan_utama".
    - Jika pasien ditanya umur dan menjawab angka, masukkan ke key "usia".
    
    ATURAN:
    1. Jangan ubah key JSON.
    2. Output HANYA format JSON valid.
    """
    
    try:
        # LangChain Chat prompt template
        response = llm_json.invoke([
            ("system", system_prompt),
            ("human", percakapan_baru)
        ])
        
        hasil_llm = json.loads(response.content)
        
        # Validasi struktur Python (Safety Net)
        for kunci, nilai in hasil_llm.items():
            if kunci in data_sekarang:
                if nilai != "" and nilai is not None:
                    data_sekarang[kunci] = nilai
        return data_sekarang
        
    except Exception as e:
        # Tahan crash jika AI JSON berhalusinasi teks biasa
        return data_sekarang