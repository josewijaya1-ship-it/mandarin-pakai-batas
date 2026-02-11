import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Penerjemah Khusus Taiwan", page_icon="🇹🇼", layout="centered")

# --- KONFIGURASI API ---
try:
    # Mengambil API Key dari Secrets Streamlit
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception:
    st.error("API Key belum terpasang di Secrets Streamlit!")
    st.stop()

# Menggunakan model Gemini 1.5 Flash yang stabil
model = genai.GenerativeModel("gemini-1.5-flash")

# --- TAMPILAN UTAMA ---
st.title("🇹🇼 Penerjemah Khusus Mandarin Taiwan")
st.subheader("Input bahasa apapun ➔ Hasil wajib Mandarin Taiwan")

# Perbaikan CSS: Menggunakan unsafe_allow_html=True agar tidak error
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
</style>
""", unsafe_allow_html=True)

# --- LOGIKA INPUT ---
st.info("Masukkan teks dalam bahasa apapun. Sistem hanya akan memberikan hasil dalam Mandarin Taiwan (Traditional Chinese).")

user_input = st.text_area("Masukkan teks di sini:", placeholder="Contoh: Halo, apa kabar?")

if st.button("Terjemahkan Sekarang", use_container_width=True):
    if user_input.strip() == "":
        st.warning("Mohon masukkan teks terlebih dahulu.")
    else:
        with st.spinner("Sedang menerjemahkan..."):
            try:
                # PROMPT KETAT (Agar tidak bisa terjemah ke bahasa lain)
                prompt_instruksi = (
                    "TUGAS: Terjemahkan teks berikut HANYA ke Mandarin Taiwan (Traditional Chinese). "
                    "ATURAN: "
                    "1. Apapun inputnya, hasil HARUS Mandarin Taiwan. "
                    "2. Gunakan aksara TRADITIONAL CHINESE. "
                    "3. Jika user meminta bahasa lain selain Mandarin Taiwan, TOLAK dengan sopan. "
                    "4. Berikan Pinyin dan penjelasan konteks Taiwan. "
                    f"\n\nTeks: '{user_input}'"
                )

                response = model.generate_content(prompt_instruksi)
                
                # Menampilkan Hasil
                st.success("### Hasil Terjemahan (Traditional Chinese)")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan: {e}")

# --- FOOTER ---
st.write("---")
st.caption("Khusus Bahasa Mandarin Taiwan (Traditional Chinese).")
