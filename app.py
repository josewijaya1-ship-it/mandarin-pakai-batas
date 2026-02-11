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

# Menggunakan model Gemini 2.5 Flash (Sangat stabil untuk saat ini)
model = genai.GenerativeModel("gemini-2.5-flash")

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
        with st.spinner("Sedang memproses..."):
            try:
                # PROMPT FILTER KETAT (Guardrail)
                prompt_instruksi = (
                    "SISTEM KEAMANAN PENERJEMAH:\n"
                    "1. Periksa apakah user meminta terjemahan ke bahasa selain Mandarin Taiwan (seperti Inggris, Jepang, Korea, dll).\n"
                    "2. Jika user meminta bahasa selain Mandarin Taiwan, JANGAN TERJEMAHKAN. "
                    "Langsung jawab dengan kalimat: 'PERINGATAN: Saya hanya diizinkan menerjemahkan ke Mandarin Taiwan.'\n"
                    "3. Jika user memberikan teks biasa, terjemahkan teks tersebut HANYA ke Mandarin Taiwan (Traditional Chinese).\n"
                    "4. Hasil terjemahan harus menyertakan Pinyin dan cara baca Taiwan.\n"
                    f"\nInput User: '{user_input}'"
                )

                response = model.generate_content(prompt_instruksi)
                hasil_ai = response.text
                
                # LOGIKA PENYARINGAN HASIL
                # Jika AI memberikan jawaban penolakan, tampilkan box merah (error)
                if "PERINGATAN" in hasil_ai or "Maaf" in hasil_ai:
                    st.error(hasil_ai)
                else:
                    # Jika jawaban valid, tampilkan box hijau (success)
                    st.success("### Hasil Terjemahan (Traditional Chinese)")
                    st.markdown(hasil_ai)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")

# --- FOOTER ---
st.write("---")
st.caption("Khusus Bahasa Mandarin Taiwan (Traditional Chinese).")
