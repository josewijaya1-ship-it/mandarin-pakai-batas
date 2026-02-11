 import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Penerjemah Khusus Taiwan", page_icon="🇹🇼", layout="centered")

# --- KONFIGURASI API ---
try:
    # Memastikan API Key diambil dari Secrets Streamlit
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("API Key belum terpasang di Secrets Streamlit!")
    st.stop()

# Menggunakan model Gemini 1.5 Flash (Sangat cepat dan akurat)
model = genai.GenerativeModel("gemini-2.5-flash")

# --- TAMPILAN UTAMA ---
st.title("🇹🇼 Penerjemah Khusus Mandarin Taiwan")
st.subheader("Input bahasa apapun ➔ Hasil wajib Mandarin Taiwan")

# PERBAIKAN: Menggunakan unsafe_allow_html=True
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --- LOGIKA INPUT ---
st.info("Masukkan teks dalam bahasa apapun. Sistem hanya akan memberikan hasil dalam Mandarin Taiwan (Traditional Chinese).")

user_input = st.text_area("Masukkan teks di sini:", placeholder="Contoh: How are you? / Apa kabar?")

if st.button("Terjemahkan Sekarang", use_container_width=True):
    if user_input.strip() == "":
        st.warning("Mohon masukkan teks terlebih dahulu.")
    else:
        with st.spinner("Guru sedang menerjemahkan..."):
            try:
                # PROMPT KETAT (Guardrail)
                prompt_instruksi = (
                    "TUGAS ANDA: Menerjemahkan teks berikut ke Mandarin Taiwan (Traditional Chinese). "
                    "ATURAN KETAT: "
                    "1. Apapun bahasa inputnya, hasil akhir HARUS dalam Bahasa Mandarin yang digunakan di Taiwan. "
                    "2. Gunakan aksara TRADITIONAL CHINESE (Zhongwen). "
                    "3. Jika user meminta diterjemahkan ke bahasa LAIN selain Mandarin Taiwan (misal: 'terjemahkan ke Inggris/Jepang'), "
                    "maka Anda WAJIB MENOLAK dan katakan: 'Maaf, saya hanya diprogram untuk menerjemahkan ke Mandarin Taiwan.' "
                    "4. Berikan Pinyin dan cara baca (Bopomofo/Zhuyin jika perlu). "
                    "5. Jangan berikan jawaban selain hasil terjemahan dan penjelasan singkat tata bahasa Taiwan."
                    f"\n\nTeks yang harus diterjemahkan: '{user_input}'"
                )

                response = model.generate_content(prompt_instruksi)
                
                # Menampilkan Hasil
                st.success("### Hasil Terjemahan (Traditional Chinese)")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# --- FOOTER ---
st.write("---")
st.caption("Dibuat khusus untuk pembelajaran Bahasa Mandarin Taiwan (Traditional Chinese).")
