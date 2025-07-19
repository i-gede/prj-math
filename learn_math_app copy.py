import streamlit as st
from supabase_client import supabase

# Konfigurasi halaman
st.set_page_config(
    page_title="Math Course App",
    page_icon="🧮",
    layout="wide"
)

# Judul dan deskripsi utama
st.title("Selamat Datang di Aplikasi Pembelajaran Matematika! 🧮")
st.markdown("---")

st.header("Navigasi")
st.write(
    "Gunakan menu di **sidebar sebelah kiri** untuk mengakses halaman **Materi Matematika** atau **Kuis Matematika**."
)
st.info("Aplikasi ini dirancang untuk membantu Anda belajar konsep matematika dasar dan menguji pemahaman Anda melalui kuis interaktif.", icon="ℹ️")

# Menampilkan gambar sebagai ilustrasi
st.image(
    "https://placehold.co/800x300/e2e8f0/475569?text=Ilustrasi+Matematika",
    caption="Belajar matematika menjadi lebih mudah dan menyenangkan."
)

# Cek status koneksi Supabase untuk debugging
st.sidebar.header("Status Koneksi")
if supabase:
    st.sidebar.success("Berhasil terhubung ke Supabase.")
else:
    st.sidebar.error("Gagal terhubung ke Supabase. Periksa file .env dan koneksi internet Anda.")

