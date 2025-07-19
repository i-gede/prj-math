import streamlit as st
import pandas as pd
from supabase_client import supabase
from datetime import datetime

# Pastikan pengguna sudah login sebelum menjalankan kode halaman apa pun
if 'user' not in st.session_state:
    st.error("⚠️ Anda harus login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()

# --- Fungsi untuk memuat data progres ---
def load_user_progress(user_id):
    """
    Mengambil semua riwayat kuis untuk pengguna tertentu dari Supabase,
    diurutkan dari yang terbaru.
    """
    try:
        response = supabase.table('user_progress').select('*').eq('user_id', user_id).order('completed_at', desc=True).execute()
        return response.data
    except Exception as e:
        st.error(f"Gagal memuat progres: {e}")
        return []

# --- Tampilan Halaman ---
st.set_page_config(page_title="Dashboard Saya", page_icon="📊")
st.title(f"📊 Dashboard Progres Anda")
st.markdown("---")

# Ambil ID pengguna yang sedang login
current_user_id = st.session_state.user.id
progress_data = load_user_progress(current_user_id)

# Cek apakah ada data progres
if not progress_data:
    st.info("Anda belum memiliki riwayat kuis. Silakan selesaikan kuis pertama Anda untuk melihat progres di sini!")
    st.stop()

# --- Tampilan Statistik Utama ---
st.header("Ringkasan Aktivitas")

# Konversi data ke DataFrame Pandas untuk analisis & visualisasi yang mudah
df = pd.DataFrame(progress_data)

# Hitung metrik
total_quizzes = len(df)
average_score = (df['score'].sum() / df['total_questions'].sum()) * 100 if not df.empty else 0
best_score = df['score'].max() if not df.empty else 0
total_questions_in_best_quiz = df.loc[df['score'].idxmax()]['total_questions'] if not df.empty else 0


col1, col2, col3 = st.columns(3)
col1.metric("Total Kuis Dikerjakan", f"{total_quizzes} kali")
col2.metric("Rata-rata Skor", f"{average_score:.1f}%")
col3.metric("Skor Tertinggi", f"{best_score}/{total_questions_in_best_quiz}")

st.markdown("---")

# --- Visualisasi Progres ---
st.header("Grafik Skor Kuis")

# Format tanggal agar lebih mudah dibaca di grafik
df['tanggal'] = pd.to_datetime(df['completed_at']).dt.strftime('%d %b %Y, %H:%M')
df_chart = df.rename(columns={'score': 'Skor'})
df_chart = df_chart.set_index('tanggal')

st.bar_chart(df_chart[['Skor']])

st.markdown("---")

# --- Tabel Riwayat Lengkap ---
st.header("Riwayat Kuis Anda")

# Pilih dan ganti nama kolom untuk ditampilkan
df_display = df[['completed_at', 'quiz_name', 'score', 'total_questions']].copy()
df_display.rename(columns={
    'completed_at': 'Tanggal Selesai',
    'quiz_name': 'Nama Kuis',
    'score': 'Skor Anda',
    'total_questions': 'Total Soal'
}, inplace=True)

# Format tanggal
df_display['Tanggal Selesai'] = pd.to_datetime(df_display['Tanggal Selesai']).dt.strftime('%d %B %Y, %H:%M:%S')


st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True,
)
