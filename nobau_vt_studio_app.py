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

# Langsung ambil API Key secara otomatis dari Streamlit Secrets
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("⚠️ GEMINI_API_KEY belum disetel di Streamlit Secrets! Harap masukkan di menu Settings -> Secrets di dashboard Streamlit Cloud.")
    st.stop()

# --- STYLING TAMBAHAN (UI MODERN) ---
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
        color: #ffffff;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER APLIKASI ---
st.markdown("# 🚀 NOBAU VT Studio Official — AI Content Generator")
st.markdown("Generator konten TikTok/Reels otomatis multimodal untuk brand resmi **NOBAU DeoFresh**.")
st.markdown("---")

# --- SIDEBAR PANDUAN ---
st.sidebar.markdown("### 📌 Konfigurasi Sistem")
st.sidebar.success("API Key aktif otomatis dari sistem.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Panduan Singkat")
st.sidebar.markdown("1. Pilih menu skenario di tab utama.")
st.sidebar.markdown("2. Upload gambar referensi Pinterest.")
st.sidebar.markdown("3. Klik **Generate Konten**.")

# --- FUNGSI PEMANGGIL GEMINI API (GEMINI 3.8 FLASH OPTIMIZED) ---
def call_gemini_multimodal(prompt_text, uploaded_image):
    # Menggunakan model gemini-3.8-flash dengan konfigurasi payload yang dioptimalkan
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.8-flash:generateContent?key={API_KEY}"
    
    parts = [{"text": prompt_text}]
    
    if uploaded_file is not None or uploaded_image is not None:
        image_bytes = uploaded_image.getvalue()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        parts.append({
            "inline_data": {
                "mime_type": uploaded_image.type,
                "data": encoded_image
            }
        })
        
    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {
            "response_mime_type": "application/json",
            "temperature": 0.7
        }
    }
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code == 200:
            res_json = response.json()
            content_text = res_json['candidates'][0]['content']['parts'][0]['text']
            return json.loads(content_text)
        else:
            return {"error": f"API Error ({response.status_code}): {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# --- TAB MENU UTAMA ---
tab1, tab2, tab3 = st.tabs(["🔥 SOLO UGC", "👥 DUO UGC", "🏢 POV OFFICE"])

# ================= SKENARIO 1: SOLO UGC =================
with tab1:
    st.markdown("### Skenario 1: SOLO UGC (Privat & Personal — 8 Detik)")
    st.markdown("Fokus pada area privat/personal seperti kamar tidur, depan cermin, atau dapur dengan satu orang pemegang botol.")
    
    uploaded_file_1 = st.file_uploader("Upload Foto Referensi Pinterest (Solo)", type=["jpg", "png", "jpeg"], key="solo_img")
    extra_notes_1 = st.text_area("Catatan Tambahan / Ide Topik Khusus (Opsional)", placeholder="Misal: Bahas ketiak basah pas bangun tidur...", key="solo_note")
    
    if st.button("Generate Konten Solo", key="btn_solo"):
        if not uploaded_file_1:
            st.warning("⚠️ Harap upload foto referensi Pinterest terlebih dahulu!")
        else:
            with st.spinner("🤖 Gemini 3.8 sedang meracik naskah & Master Prompt AppSheet Solo UGC..."):
                system_prompt = f"""
                Bertindaklah sebagai Senior TikTok Content Strategist untuk brand 'NOBAU DeoFresh' (produk deodorizing spray multiguna).
                Analisis gambar referensi Pinterest yang diberikan. Buatlah paket konten video pendek berdurasi 8 detik dengan format JSON murni yang menggunakan kuncian standar AppSheet berikut:
                - "pilar": Pilar konten (Problem-Solution, Edukasi, atau Unboxing).
                - "topik": Topik tren TikTok dengan slang fonetik khas (contoh: 'apeuk', 'tengik').
                - "naskah": Naskah voiceover 8 detik (Hook 0-2s, Aksi Semprot 2-5s, Payoff/CTA 5-8s).
                - "prompt_image": Master Prompt Image terstruktur ketat gaya AppSheet: "Photorealistic close-up UGC style in a private bedroom, young creator holding a sleek minimalist NOBAU DeoFresh spray bottle near armpit/clothing area, natural morning sunlight, highly detailed texture, 8k resolution, cinematic aesthetic."
                - "prompt_flow": Prompt Google Flow terstruktur detik AppSheet: "0-3s: Creator looking annoyed at body odor source in mirror, holding NOBAU DeoFresh. 4-5s: Quick satisfying one-thumb spray action with visible fine mist. 6-8s: Relieved confident expression, smooth product hero close-up shot with clean fresh vibe."
                Catatan tambahan dari kreator: {extra_notes_1}
                """
                result = call_gemini_multimodal(system_prompt, uploaded_file_1)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.markdown("### 📋 Hasil Output Generator")
                    st.markdown(f"**📌 Pilar Konten:** {result.get('pilar', '-')}")
                    st.markdown(f"**🔥 Topik / Slang:** {result.get('topik', '-')}")
                    st.markdown(f"**🎙️ Naskah Voiceover (8 Detik):**\n{result.get('naskah', '-')}")
                    
                    st.markdown("**🎨 Master Prompt Image:**")
                    st.code(result.get('prompt_image', '-'), language="text")
                    
                    st.markdown("**🎬 Prompt Google Flow (Video):**")
                    st.code(result.get('prompt_flow', '-'), language="text")

# ================= SKENARIO 2: DUO UGC =================
with tab2:
    st.markdown("### Skenario 2: DUO UGC (Publik & Sosial — 8 Detik)")
    st.markdown("Fokus pada area publik seperti gym, kafe, atau hangout bareng teman dengan interaksi dinamis.")
    
    uploaded_file_2 = st.file_uploader("Upload Foto Referensi Pinterest (Duo)", type=["jpg", "png", "jpeg"], key="duo_img")
    extra_notes_2 = st.text_area("Catatan Tambahan / Ide Topik Khusus (Opsional)", placeholder="Misal: Diledekin temen pas habis nge-gym...", key="duo_note")
    
    if st.button("Generate Konten Duo", key="btn_duo"):
        if not uploaded_file_2:
            st.warning("⚠️ Harap upload foto referensi Pinterest terlebih dahulu!")
        else:
            with st.spinner("🤖 Gemini 3.8 sedang meracik naskah & Master Prompt AppSheet Duo UGC..."):
                system_prompt = f"""
                Bertindaklah sebagai Senior TikTok Content Strategist untuk brand 'NOBAU DeoFresh'.
                Analisis gambar referensi Pinterest yang diberikan. Buatlah paket konten video duo berdurasi 8 detik dengan format JSON murni yang menggunakan kuncian standar AppSheet berikut:
                - "pilar": Pilar konten.
                - "topik": Topik tren dengan slang khas.
                - "naskah": Dialog interaktif (Main Creator & Celetohan Teman Dinamis Kasual).
                - "prompt_image": Master Prompt Image terstruktur ketat gaya AppSheet: "Photorealistic UGC style in a vibrant public cafe/gym, two young friends interacting dynamically, main creator holding a sleek NOBAU DeoFresh spray bottle, warm natural lighting, highly detailed, 8k resolution."
                - "prompt_flow": Prompt Google Flow terstruktur detik AppSheet: "0-3s: Friend reacting playfully to sweat/odor, main creator smiling while pulling out NOBAU DeoFresh. 4-6s: Quick dynamic spray demonstration in public setting. 7-8s: Both laughing and nodding, final hero shot of product next to coffee cup or gym gear."
                Catatan tambahan dari kreator: {extra_notes_2}
                """
                result = call_gemini_multimodal(system_prompt, uploaded_file_2)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.markdown("### 📋 Hasil Output Generator")
                    st.markdown(f"**📌 Pilar Konten:** {result.get('pilar', '-')}")
                    st.markdown(f"**🔥 Topik / Slang:** {result.get('topik', '-')}")
                    st.markdown(f"**🎙️ Naskah Dialog (8 Detik):**\n{result.get('naskah', '-')}")
                    
                    st.markdown("**🎨 Master Prompt Image:**")
                    st.code(result.get('prompt_image', '-'), language="text")
                    
                    st.markdown("**🎬 Prompt Google Flow (Video):**")
                    st.code(result.get('prompt_flow', '-'), language="text")

# ================= SKENARIO 3: POV OFFICE =================
with tab3:
    st.markdown("### Skenario 3: POV OFFICE (Sudut Pandang Meja Kerja — 10 Detik)")
    st.markdown("Fokus pada meja kantor / office desk dari sudut pandang POV dengan properti khusus.")
    
    uploaded_file_3 = st.file_uploader("Upload Foto Referensi Pinterest (POV Office)", type=["jpg", "png", "jpeg"], key="pov_img")
    extra_notes_3 = st.text_area("Catatan Tambahan / Ide Topik Khusus (Opsional)", placeholder="Misal: Bau sepatu di bawah meja kerja kantor...", key="pov_note")
    
    if st.button("Generate Konten POV Office", key="btn_pov"):
        if not uploaded_file_3:
            st.warning("⚠️ Harap upload foto referensi Pinterest terlebih dahulu!")
        else:
            with st.spinner("🤖 Gemini 3.8 sedang meracik Master Prompt AppSheet POV Office..."):
                system_prompt = f"""
                Bertindaklah sebagai Senior TikTok Content Strategist untuk brand 'NOBAU DeoFresh'.
                Analisis gambar referensi Pinterest yang diberikan. Buatlah paket konten video POV Office berdurasi 10 detik dengan format JSON murni yang menggunakan kuncian standar AppSheet berikut:
                - "pilar": Pilar konten.
                - "topik": Topik tren perkantoran/sepatu bau.
                - "naskah": Naskah Voiceover POV (Satu jempol uncap botol sekali, kamera miring ke bawah menyemprot sepatu di bawah meja, latar dokumen CV).
                - "prompt_image": Master Prompt Image terstruktur ketat gaya AppSheet: "First-person POV shot across an office desk, messy paperwork, laptop, sleek NOBAU DeoFresh spray bottle placed prominently on desk, moody professional office lighting, photorealistic 8k."
                - "prompt_flow": Prompt Google Flow terstruktur detik AppSheet: "0-3s: POV looking down at office desk and shoes, handling work stress. 4-6s: One hand uncapping NOBAU DeoFresh with a single thumb, tilting camera down sharply to spray shoes under the desk. 7-10s: Relief expression, clean desk hero shot with product."
                Catatan tambahan dari kreator: {extra_notes_3}
                """
                result = call_gemini_multimodal(system_prompt, uploaded_file_3)
                
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.markdown("### 📋 Hasil Output Generator")
                    st.markdown(f"**📌 Pilar Konten:** {result.get('pilar', '-')}")
                    st.markdown(f"**🔥 Topik / Slang:** {result.get('topik', '-')}")
                    st.markdown(f"**🎙️ Naskah POV (10 Detik):**\n{result.get('naskah', '-')}")
                    
                    st.markdown("**🎨 Master Prompt Image:**")
                    st.code(result.get('prompt_image', '-'), language="text")
                    
                    st.markdown("**🎬 Prompt Google Flow (Video):**")
                    st.code(result.get('prompt_flow', '-'), language="text")
