import streamlit as st
from supabase_client import supabase

# Pastikan pengguna sudah login sebelum menjalankan kode halaman apa pun
if 'user' not in st.session_state:
    st.error("⚠️ Anda harus login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()

# --- Expander di Sidebar untuk Filter Kelas ---
# Expander ini akan muncul di sidebar dan bisa dibuka/ditutup
with st.sidebar.expander("📖 Pilih Kelas Materi", expanded=True):
    grade_options = {
        "Semua Kelas": None,
        "Kelas 7": 7,
        "Kelas 8": 8,
        "Kelas 9": 9,
        "Kelas 10": 10,
        "Kelas 11": 11,
        "Kelas 12": 12,
    }
    selected_grade_label = st.selectbox(
        "Pilih tingkat kelas:",
        options=list(grade_options.keys()), # Tampilkan nama kelas sebagai pilihan
        label_visibility="collapsed" # Sembunyikan label "Pilih tingkat kelas:" agar lebih rapi
    )

# Dapatkan angka kelas berdasarkan label yang dipilih
selected_grade_value = grade_options[selected_grade_label]


# --- Fungsi untuk memuat data materi berdasarkan kelas ---
def load_materials(grade=None):
    """
    Mengambil data materi dari Supabase.
    Jika 'grade' diberikan, maka akan memfilter berdasarkan kelas tersebut.
    """
    if not supabase:
        st.error("Koneksi ke Supabase gagal. Tidak dapat memuat materi.")
        return []
    try:
        query = supabase.table('materials').select('title, content, grade')
        
        # Jika kelas tertentu dipilih (bukan "Semua Kelas"), tambahkan filter
        if grade is not None:
            query = query.eq('grade', grade)
            
        response = query.order('title').execute()
        return response.data
    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengambil data: {e}")
        return []

# --- Tampilan Halaman Utama ---
st.title("📚 Materi Pelajaran Matematika")
st.header(f"{selected_grade_label}")
#st.write("Berikut adalah kumpulan materi yang dapat Anda pelajari. Materi diambil langsung dari database.")

# Memuat materi berdasarkan kelas yang dipilih di sidebar
materials = load_materials(selected_grade_value)

if not materials:
    st.warning(f"Belum ada materi yang tersedia untuk {selected_grade_label}. Silakan tambahkan materi di database Supabase Anda.")
else:
    # Tampilkan setiap materi menggunakan expander
    for i, material in enumerate(materials):
        with st.expander(f"**{i+1}. {material.get('title', 'Tanpa Judul')}**", expanded=False):
            st.markdown(material.get('content', 'Konten tidak tersedia.'), unsafe_allow_html=True)

st.markdown("---")
st.info("Tips: Anda bisa menggunakan format LaTeX untuk menulis rumus matematika di dalam konten materi, contohnya: `$ax^2 + bx + c = 0$`.")
