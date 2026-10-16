import streamlit as st
from google import genai
from PIL import Image
import time

# --- KONFIGURASI HALAMAN & API KEY ---
st.set_page_config(
    page_title="NOBAU VT Studio Official", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi Google GenAI Client resmi
client = None
if "GEMINI_API_KEY" in st.secrets:
    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    except Exception as e:
        st.error(f"⚠️ Gagal menginisialisasi Gemini Client: {e}")

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
    </style>
""", unsafe_allow_html=True)

# --- HEADER APLIKASI ---
st.markdown("# 🚀 NOBAU VT Studio Official — AI Content Generator")
st.markdown("Generator konten TikTok/Reels otomatis multimodal untuk brand resmi **NOBAU DeoFresh**.")
st.markdown("---")

# --- SIDEBAR PANDUAN ---
st.sidebar.markdown("### 📌 Konfigurasi Sistem")
if client:
    st.sidebar.success("API Key aktif & terhubung.")
else:
    st.sidebar.error("⚠️ GEMINI_API_KEY belum disetel!")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📖 Panduan Singkat")
st.sidebar.markdown("1. Pilih menu skenario di tab utama.")
st.sidebar.markdown("2. Upload gambar referensi Pinterest.")
st.sidebar.markdown("3. Klik **Generate Konten**.")

# --- FUNGSI AMAN PAKAI SDK RESMI GOOGLE GENAI ---
def generate_content_safe(client_obj, prompt_text, image_pil):
    if not client_obj:
        return {"error": "GEMINI_API_KEY belum terpasang di Streamlit Secrets!"}
    
    target_model = 'gemini-3.8-flash'
    last_err = None
    
    for attempt in range(3):
        try:
            response = client_obj.models.generate_content(
                model=target_model,
                contents=[prompt_text, image_pil],
                config={
                    "response_mime_type": "application/json",
                    "temperature": 0.4
                }
            )
            return json.loads(response.text)
        except Exception as e:
            last_err = str(e)
            if "503" in last_err or "UNAVAILABLE" in last_err or "429" in last_err:
                time.sleep(3.0)
                continue
            else:
                return {"error": f"API Error: {last_err}"}
                
    return {"error": f"Gagal terhubung ke server setelah beberapa percobaan. Detail: {last_err}"}

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
                try:
                    img_pil = Image.open(uploaded_file_1)
                    system_prompt = f"""
                    Analisis gambar referensi Pinterest yang diberikan. Hasilkan JSON murni yang memuat kunci berikut secara presisi:
                    - "pilar": Pilar konten (Problem-Solution / Personal Care).
                    - "topik": Topik tren TikTok dengan slang fonetik khas (contoh: 'apeuk', 'tengik').
                    - "naskah": Naskah voiceover 8 detik (gaya julid santai khas kreator Indonesia dengan jeda napas natural).
                    - "prompt_image": "Create a natural 9:16 vertical smartphone photograph taken from a close-up personal perspective in a private bedroom, matching the composition, lighting, and aesthetic of the separately uploaded scene reference image. CRITICAL RULE: Ensure only ONE single compact NOBAU DeoFresh spray bottle is held near the creator's clothing or armpit area. Remove any secondary or duplicate bottles. PHOTOGRAPHIC STYLE: Authentic casual smartphone snapshot, natural indoor lighting, natural depth of field with sharp focus on the creator and product. NO CGI, strictly raw photography descriptors."
                    - "prompt_flow": "A continuous 8-second vertical 9:16 smartphone UGC video recorded entirely from a personal close-up perspective in a private bedroom, matching Image 1. IDENTITY: Main female creator, organic sassy Indonesian tone. PRODUCT & ACTION: Holding ONLY ONE NOBAU spray bottle in right hand. 0-3s: Using right thumb to pop off clear cap while speaking opening line. 3-6s: Quick satisfying spray action directed near clothing area with visible fine mist. 6-8s: Relieved expression, bringing bottle close to lens for clear label view."
                    Catatan tambahan kreator: {extra_notes_1}
                    """
                    result = generate_content_safe(client, system_prompt, img_pil)
                    
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
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada proses gambar: {e}")

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
                try:
                    img_pil = Image.open(uploaded_file_2)
                    system_prompt = f"""
                    Analisis gambar referensi Pinterest yang diberikan. Hasilkan JSON murni yang memuat kunci berikut secara presisi:
                    - "pilar": Pilar konten (Relatable Lifestyle & Humor / Problem-Solution).
                    - "topik": Topik tren publik dengan slang khas.
                    - "naskah": Dialog interaktif (Main Creator & Celetohan Teman Dinamis Kasual gaya julid santai).
                    - "prompt_image": "Create a natural 9:16 vertical smartphone photograph at an outdoor cafe table, matching the composition and layout of the uploaded scene reference. CRITICAL RULE: Ensure only ONE single compact NOBAU DeoFresh spray bottle is placed on the table next to coffee cups. Remove secondary or duplicate bottles. PHOTOGRAPHIC STYLE: Authentic casual smartphone snapshot, realistic ambient lighting at dusk, natural depth of field. NO CGI, strictly raw photography descriptors."
                    - "prompt_flow": "A continuous 8-second vertical 9:16 smartphone UGC video recorded at an outdoor cafe table, matching Image 1. IDENTITY: Main creator and friend interacting dynamically with natural Indonesian speech. PRODUCT & ACTION: Holding ONLY ONE NOBAU spray bottle. 0-3s: Friend reacts playfully to odor, main creator pulls out bottle. 3-6s: Quick dynamic spray demonstration in public setting. 6-8s: Both laughing, final hero shot of product label clearly shown."
                    Catatan tambahan kreator: {extra_notes_2}
                    """
                    result = generate_content_safe(client, system_prompt, img_pil)
                    
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
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada proses gambar: {e}")

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
                try:
                    img_pil = Image.open(uploaded_file_3)
                    system_prompt = f"""
                    Analisis gambar referensi Pinterest yang diberikan. Hasilkan JSON murni yang memuat kunci berikut secara presisi:
                    - "pilar": Pilar konten (Workplace Realities & Problem-Solution).
                    - "topik": Topik tren perkantoran / sepatu bau di bawah meja kerja.
                    - "naskah": Naskah Voiceover POV 10 detik (gaya julid santai khas kreator Indonesia dengan jeda napas natural).
                    - "prompt_image": "Create a natural 9:16 vertical smartphone photograph taken from a first-person perspective (POV) sitting at an office desk, matching the composition, laptop layout, and natural indoor lighting of the separately uploaded scene reference image. CRITICAL RULE: OBSTRUCTION & DUPLICATE CLEANUP. Ensure only ONE single compact spray bottle is placed on the desk to the right side near the computer mouse. Remove any secondary or duplicate bottles from the desk surface. PHOTOGRAPHIC STYLE: Authentic casual office smartphone snapshot, realistic indoor lighting, natural depth of field with sharp focus on the laptop and desk setup. NO CGI, strictly raw photography descriptors."
                    - "prompt_flow": "A continuous 10-second vertical 9:16 smartphone UGC video recorded entirely from a first-person perspective (POV) sitting at an office desk, matching Image 1. IDENTITY: First-person POV of main female creator with organic, sassy Indonesian voice tone (gaya julid santai). STATIONARY DESK ENVIRONMENT: Desk background, laptop, and documents remain fully static. PRODUCT & ACTION: Holding ONLY ONE NOBAU spray bottle in right hand. 0-3s: Using right thumb to pop off cap while speaking opening line. 3-6.5s: Smoothly tilting camera downward toward office shoes under desk (directing spray below desk level) and spraying 2 quick mists. 6.5-10s: Bringing bottle upward toward camera lens to show label clearly."
                    Catatan tambahan kreator: {extra_notes_3}
                    """
                    result = generate_content_safe(client, system_prompt, img_pil)
                    
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
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada proses gambar: {e}")
