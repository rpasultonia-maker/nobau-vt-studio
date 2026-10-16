import streamlit as st
import requests
import json
import base64

# --- KONFIGURASI HALAMAN & API KEY ---
st.set_page_config(
    page_title="NOBAU VT Studio Official", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)
API_KEY = st.secrets.get("GEMINI_API_KEY", "")
if not API_KEY:
    API_KEY = st.sidebar.text_input("Masukkan API Key Google AI Studio", type="password")

# Styling Tambahan untuk Tampilan Modern & Clean
st.markdown("""
    <style>
    .main {
        background-color: #0f1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #ff2b2b;
    }
    .result-box {
        background-color: #1e1e2f;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #33334d;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Konfigurasi API Key
st.sidebar.title("⚙️ Konfigurasi Sistem")
api_key_input = st.sidebar.text_input("Gemini API Key", type="password", placeholder="Masukkan API Key Google AI Studio...")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Panduan Singkat")
st.sidebar.markdown("1. Masukkan API Key Gemini.\n2. Pilih menu skenario di tab utama.\n3. Upload gambar referensi Pinterest.\n4. Klik **Generate Konten**.")

# Judul Utama Aplikasi
st.title("🚀 NOBAU VT Studio Official — AI Content Generator")
st.markdown("Generator konten TikTok/Reels otomatis multimodal untuk brand resmi **NOBAU DeoFresh**.")

# Membuat 3 Tab Utama (Menu Sesuai Permintaan)
tab1, tab2, tab3 = st.tabs(["👤 SOLO UGC", "👥 DUO UGC", "💼 POV OFFICE"])

# ==========================================
# TAB 1: SOLO UGC
# ==========================================
with tab1:
    st.subheader("Skenario 1: SOLO UGC (Privat & Personal — 8 Detik)")
    st.markdown("Fokus pada area privat/personal seperti kamar tidur, depan cermin, atau dapur dengan satu orang pemegang botol.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file_solo = st.file_uploader("Upload Foto Referensi Pinterest (Solo)", type=["jpg", "jpeg", "png"], key="solo_img")
        if uploaded_file_solo:
            st.image(uploaded_file_solo, caption="Preview Gambar Pinterest", use_container_width=True)
            
        extra_notes_solo = st.text_area("Catatan Tambahan / Ide Topik Khusus (Opsional)", placeholder="Misal: Bahas ketiak basah pas bangun tidur...", key="solo_notes")
        generate_btn_solo = st.button("Generate Konten SOLO UGC", key="btn_solo")

    with col2:
        st.markdown("### 📋 Hasil Output Generator")
        if generate_btn_solo:
            if not api_key_input:
                st.error("⚠️ Mohon masukkan Gemini API Key di sidebar terlebih dahulu!")
            elif not uploaded_file_solo:
                st.warning("⚠️ Mohon upload gambar referensi Pinterest terlebih dahulu!")
            else:
                with st.spinner("🤖 AI sedang menganalisis gambar dan meracik skenario Solo UGC..."):
                    try:
                        # Encode gambar ke base64
                        bytes_data = uploaded_file_solo.getvalue()
                        base64_image = base64.b64encode(bytes_data).decode('utf-8')
                        mime_type = uploaded_file_solo.type
                        
                        prompt_solo = f"""
Kamu adalah Creative Director & Trend Analyst khusus konten SOLO UGC untuk brand resmi NOBAU DeoFresh.
Karakter digital utama: Perempuan muda Indonesia ("NOBAU Official").
Catatan tambahan user: {extra_notes_solo}

TUGAS UTAMA:
1. AMATI DAN ANALISIS GAMBAR PINTEREST SOLO (Area privat/personal: Kamar Tidur, Kamar Mandi, Depan Cermin, Dapur, dll).
2. TENTUKAN PILAR & TOPIK: Gunakan ejaan fonetik khas bahasa gaul/slang Indonesia (contoh: tulis "apeuk", bukan "apek"). Pilih varian botol NOBAU yang tepat.
3. BUAT OFFICIAL PROMPT IMAGE:
   "Create a natural 9:16 vertical photograph matching the visual context of the uploaded Pinterest image. Absolute character consistency with master character reference image."
4. BUAT OFFICIAL PROMPT GOOGLE FLOW (8 DETIK SOLO):
   "A continuous 8-second vertical 9:16 smartphone UGC video recorded inside the specified location, recorded from a clean front-facing perspective.
   IDENTITY: Preserve exact facial structure, identity, long dark brown hair, fair skin tone, her original white long-sleeve ribbed v-neck top with her neck completely bare and natural.
   PRODUCT: Holding ONLY ONE compact 100ml NOBAU spray bottle in her right hand.
   STORY & TIMELINE (0-8s): 0-2s Hook, 2-5s Action spraying target area, 5-8s Payoff & CTA.
   DIALOGUE: '[NASKAH_SINGLE_SPEAKER]'
   CONTINUITY: One continuous generation, no camera cuts, clean view."

FORMAT RESPONS WAJIB JSON:
{{
  "pilar": "Pilar Konten",
  "topik": "Topik Tren",
  "naskah": "Naskah voiceover lengkap",
  "prompt_image": "OFFICIAL MASTER PROMPT IMAGE",
  "prompt_flow": "OFFICIAL PROMPT GOOGLE FLOW"
}}
"""
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key_input}"
                        payload = {
                            "contents": [{
                                "parts": [
                                    {"inline_data": {"mime_type": mime_type, "data": base64_image}},
                                    {"text": prompt_solo}
                                ]
                            }],
                            "generationConfig": {"response_mime_type": "application/json"}
                        }
                        
                        response = requests.post(url, json=payload)
                        result_json = response.json()
                        
                        if "candidates" in result_json:
                            raw_text = result_json["candidates"][0]["content"]["parts"][0]["text"]
                            data = json.loads(raw_text)
                            
                            st.session_state['solo_data'] = data
                            st.success("✅ Konten SOLO UGC Berhasil Dibuat!")
                        else:
                            st.error(f"Gagal memproses API: {result_json}")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan sistem: {str(e)}")

                if 'solo_data' in st.locals() or 'solo_data' in st.session_state:
                    res = st.session_state.get('solo_data', {})
                    st.markdown(f"""
                    <div class="result-box">
                        <p><b>Pilar Konten:</b> {res.get('pilar')}</p>
                        <p><b>Topik Tren:</b> {res.get('topik')}</p>
                        <p><b>Naskah Voiceover:</b><br>{res.get('naskah')}</p>
                        <p><b>Official Prompt Image:</b><br><code>{res.get('prompt_image')}</code></p>
                        <p><b>Official Prompt Google Flow:</b><br><code>{res.get('prompt_flow')}</code></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(json.dumps(res, indent=2), language="json")

# ==========================================
# TAB 2: DUO UGC
# ==========================================
with tab2:
    st.subheader("Skenario 2: DUO UGC (Vlog Bareng Teman — 8 Detik)")
    st.markdown("Fokus pada area publik/sosial seperti gym, kafe, tempat nongkrong, atau outdoor dengan format interaksi dua orang.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file_duo = st.file_uploader("Upload Foto Referensi Pinterest (Duo)", type=["jpg", "jpeg", "png"], key="duo_img")
        if uploaded_file_duo:
            st.image(uploaded_file_duo, caption="Preview Gambar Pinterest", use_container_width=True)
            
        extra_notes_duo = st.text_area("Catatan Tambahan / Konteks Nongkrong (Opsional)", placeholder="Misal: Nongkrong habis nge-gym bareng bestie...", key="duo_notes")
        generate_btn_duo = st.button("Generate Konten DUO UGC", key="btn_duo")

    with col2:
        st.markdown("### 📋 Hasil Output Generator")
        if generate_btn_duo:
            if not api_key_input:
                st.error("⚠️ Mohon masukkan Gemini API Key di sidebar terlebih dahulu!")
            elif not uploaded_file_duo:
                st.warning("⚠️ Mohon upload gambar referensi Pinterest terlebih dahulu!")
            else:
                with st.spinner("🤖 AI sedang menganalisis gambar dan meracik skenario Duo UGC..."):
                    try:
                        bytes_data = uploaded_file_duo.getvalue()
                        base64_image = base64.b64encode(bytes_data).decode('utf-8')
                        mime_type = uploaded_file_duo.type
                        
                        prompt_duo = f"""
Kamu adalah Creative Director & Trend Analyst khusus konten DUO UGC (Vlog Bareng Teman) untuk brand resmi NOBAU DeoFresh.
Karakter digital utama: Perempuan muda Indonesia ("NOBAU Official") bersama teman wanitanya.
Catatan tambahan user: {extra_notes_duo}

TUGAS UTAMA:
1. AMATI DAN ANALISIS GAMBAR PINTEREST DUO (Area publik/sosial: Gym, Kafe, Tempat Nongkrong, Outdoor).
2. TENTUKAN PILAR & TOPIK: Gunakan slang fonetik, pilih varian botol NOBAU yang tepat.
3. BUAT OFFICIAL PROMPT IMAGE:
   "Create a natural 9:16 vertical photograph matching the visual context of the uploaded Pinterest image. Absolute character consistency."
4. BUAT OFFICIAL PROMPT GOOGLE FLOW (8 DETIK DUO):
   "A continuous 8-second vertical 9:16 smartphone UGC vlog video recorded inside the location, held in selfie mode by a cheerful female friend. 
   IDENTITY: Main creator (@NoBau Wanita) and friend. 
   PRODUCT: Main creator holds ONE NOBAU spray bottle. 
   STORY: 0-2s Reaction, 2-5s Action spraying, 5-8s Payoff. 
   DIALOGUE: Main Creator: '[NASKAH_UTAMA]' | Friend: '[CELETOHAN_TEMAN_DYNAMIS_KASUAL]'."

FORMAT RESPONS WAJIB JSON:
{{
  "pilar": "Pilar Konten",
  "topik": "Topik Tren",
  "naskah": "Naskah voiceover dialog Duo",
  "prompt_image": "OFFICIAL MASTER PROMPT IMAGE",
  "prompt_flow": "OFFICIAL PROMPT GOOGLE FLOW"
}}
"""
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key_input}"
                        payload = {
                            "contents": [{
                                "parts": [
                                    {"inline_data": {"mime_type": mime_type, "data": base64_image}},
                                    {"text": prompt_duo}
                                ]
                            }],
                            "generationConfig": {"response_mime_type": "application/json"}
                        }
                        
                        response = requests.post(url, json=payload)
                        result_json = response.json()
                        
                        if "candidates" in result_json:
                            raw_text = result_json["candidates"][0]["content"]["parts"][0]["text"]
                            data = json.loads(raw_text)
                            st.session_state['duo_data'] = data
                            st.success("✅ Konten DUO UGC Berhasil Dibuat!")
                        else:
                            st.error(f"Gagal memproses API: {result_json}")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan sistem: {str(e)}")

                if 'duo_data' in st.session_state:
                    res = st.session_state['duo_data']
                    st.markdown(f"""
                    <div class="result-box">
                        <p><b>Pilar Konten:</b> {res.get('pilar')}</p>
                        <p><b>Topik Tren:</b> {res.get('topik')}</p>
                        <p><b>Naskah / Dialog:</b><br>{res.get('naskah')}</p>
                        <p><b>Official Prompt Image:</b><br><code>{res.get('prompt_image')}</code></p>
                        <p><b>Official Prompt Google Flow:</b><br><code>{res.get('prompt_flow')}</code></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(json.dumps(res, indent=2), language="json")

# ==========================================
# TAB 3: POV OFFICE
# ==========================================
with tab3:
    st.subheader("Skenario 3: POV OFFICE (Sudut Pandang Meja Kantor — 10 Detik)")
    st.markdown("Fokus pada sudut pandang orang pertama (POV) di meja kantor: buka tutup botol dengan satu jempol, semprot ke sepatu di bawah meja, dan dokumen *CV Balqia Quondrof*.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded_file_pov = st.file_uploader("Upload Foto Referensi Pinterest (POV Office)", type=["jpg", "jpeg", "png"], key="pov_img")
        if uploaded_file_pov:
            st.image(uploaded_file_pov, caption="Preview Gambar Pinterest", use_container_width=True)
            
        extra_notes_pov = st.text_area("Catatan Tambahan / Isu Kantor (Opsional)", placeholder="Misal: Bau kaki pas kerja seharian pakai pantofel...", key="pov_notes")
        generate_btn_pov = st.button("Generate Konten POV OFFICE", key="btn_pov")

    with col2:
        st.markdown("### 📋 Hasil Output Generator")
        if generate_btn_pov:
            if not api_key_input:
                st.error("⚠️ Mohon masukkan Gemini API Key di sidebar terlebih dahulu!")
            elif not uploaded_file_pov:
                st.warning("⚠️ Mohon upload gambar referensi Pinterest terlebih dahulu!")
            else:
                with st.spinner("🤖 AI sedang menganalisis gambar dan meracik skenario POV Office..."):
                    try:
                        bytes_data = uploaded_file_pov.getvalue()
                        base64_image = base64.b64encode(bytes_data).decode('utf-8')
                        mime_type = uploaded_file_pov.type
                        
                        prompt_pov = f"""
Kamu adalah Creative Director & Trend Analyst khusus konten POV OFFICE untuk brand resmi NOBAU DeoFresh.
Karakter digital utama: Perempuan muda Indonesia ("NOBAU Official").
Catatan tambahan user: {extra_notes_pov}

TUGAS UTAMA:
1. AMATI DAN ANALISIS GAMBAR PINTEREST POV OFFICE (Meja kantor / Office desk dari sudut pandang orang pertama).
2. TENTUKAN PILAR & TOPIK: Pilih varian botol yang tepat untuk foot care/office freshness.
3. BUAT OFFICIAL PROMPT IMAGE:
   "Create a natural 9:16 vertical photograph matching the office desk context of the uploaded Pinterest image."
4. BUAT OFFICIAL PROMPT GOOGLE FLOW (10 DETIK POV OFFICE):
   "A continuous 10-second vertical 9:16 smartphone UGC video recorded entirely from a first-person perspective (POV) sitting at an office desk, strictly matching the reference image. 
   IDENTITY & COSTUME: First-person POV of main female creator (@NoBau Wanita), strictly wearing lower outfit and bare legs from the image. 
   BACKGROUND & PROPS: Stationary desk, laptop, flat stack of documents with 'CV BALQIA QUONDROF' letterhead, NOBAU lanyard fully static. 
   ACTION & SPRAY: Creator holds ONLY ONE NOBAU spray bottle in her right hand. 
   0-3s: Using ONLY her right thumb, she pops off clear cap once; bottle remains uncapped till end. 
   3-6.5s: Smoothly tilts hand and camera DOWNWARD toward shoes under desk (DO NOT spray toward laptop) and sprays 2 quick mists. 
   6.5-10s: Brings uncapped bottle upward to show label clearly. 
   DIALOGUE: '[NASKAH_POV]'."

FORMAT RESPONS WAJIB JSON:
{{
  "pilar": "Pilar Konten",
  "topik": "Topik Tren",
  "naskah": "Naskah voiceover POV",
  "prompt_image": "OFFICIAL MASTER PROMPT IMAGE",
  "prompt_flow": "OFFICIAL PROMPT GOOGLE FLOW"
}}
"""
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key_input}"
                        payload = {
                            "contents": [{
                                "parts": [
                                    {"inline_data": {"mime_type": mime_type, "data": base64_image}},
                                    {"text": prompt_pov}
                                ]
                            }],
                            "generationConfig": {"response_mime_type": "application/json"}
                        }
                        
                        response = requests.post(url, json=payload)
                        result_json = response.json()
                        
                        if "candidates" in result_json:
                            raw_text = result_json["candidates"][0]["content"]["parts"][0]["text"]
                            data = json.loads(raw_text)
                            st.session_state['pov_data'] = data
                            st.success("✅ Konten POV OFFICE Berhasil Dibuat!")
                        else:
                            st.error(f"Gagal memproses API: {result_json}")
                    except Exception as e:
                        st.error(f"Terjadi kesalahan sistem: {str(e)}")

                if 'pov_data' in st.session_state:
                    res = st.session_state['pov_data']
                    st.markdown(f"""
                    <div class="result-box">
                        <p><b>Pilar Konten:</b> {res.get('pilar')}</p>
                        <p><b>Topik Tren:</b> {res.get('topik')}</p>
                        <p><b>Naskah POV:</b><br>{res.get('naskah')}</p>
                        <p><b>Official Prompt Image:</b><br><code>{res.get('prompt_image')}</code></p>
                        <p><b>Official Prompt Google Flow:</b><br><code>{res.get('prompt_flow')}</code></p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.code(json.dumps(res, indent=2), language="json")
