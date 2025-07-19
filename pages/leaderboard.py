import streamlit as st
from supabase_client import supabase
import pandas as pd

st.set_page_config(page_title="Leaderboard", page_icon="🏆")
st.title("🏆 Leaderboard")
st.write("Peringkat pengguna berdasarkan total skor yang diperoleh dari semua kuis.")

# --- Fungsi untuk mengambil data leaderboard ---
def get_leaderboard():
    try:
        # Menggunakan fungsi database yang sudah kita buat sebelumnya
        return supabase.rpc('get_leaderboard').execute().data
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return []

# --- Tampilan Halaman ---
leaderboard_data = get_leaderboard()

if not leaderboard_data:
    st.info("Belum ada data untuk ditampilkan di leaderboard.")
else:
    df = pd.DataFrame(leaderboard_data)
    df.index = df.index + 1 # Mulai peringkat dari 1
    df.rename(columns={'email': 'Pengguna', 'total_score': 'Total Skor'}, inplace=True)
    
    st.dataframe(
        df,
        use_container_width=True
    )
