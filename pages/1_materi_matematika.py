import streamlit as st
from supabase_client import supabase

# Cek status login pengguna
if 'user' not in st.session_state:
    st.error("⚠️ Anda harus login terlebih dahulu untuk mengakses halaman ini.")
    st.stop() # Menghentikan eksekusi script jika belum login


# Konfigurasi judul halaman
st.set_page_config(page_title="Materi Matematika", page_icon="📚")
st.title("📚 Materi Pelajaran Matematika")
st.write("Berikut adalah kumpulan materi yang dapat Anda pelajari. Materi diambil langsung dari database.")

def load_materials():
    """Mengambil data materi dari tabel 'materials' di Supabase."""
    if not supabase:
        st.error("Koneksi ke Supabase gagal. Tidak dapat memuat materi.")
        return []
    try:
        response = supabase.table('materials').select('title, content').execute()
        return response.data
    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengambil data: {e}")
        return []

# Memuat materi
materials = load_materials()

if not materials:
    st.warning("Belum ada materi yang tersedia. Silakan tambahkan materi di database Supabase Anda pada tabel 'materials'.")
else:
    # Tampilkan setiap materi menggunakan expander
    for i, material in enumerate(materials):
        with st.expander(f"**{i+1}. {material.get('title', 'Tanpa Judul')}**", expanded=False):
            # Gunakan markdown untuk merender konten, termasuk formula LaTeX
            st.markdown(material.get('content', 'Konten tidak tersedia.'), unsafe_allow_html=True)

st.markdown("---")
st.info("Tips: Anda bisa menggunakan format LaTeX untuk menulis rumus matematika di dalam konten materi, contohnya: `$ax^2 + bx + c = 0$`.")
