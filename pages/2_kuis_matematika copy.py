import streamlit as st
from utils.quiz_data import get_quiz_data

# Cek status login pengguna
if 'user' not in st.session_state:
    st.error("⚠️ Anda harus login terlebih dahulu untuk mengakses halaman ini.")
    st.stop() # Menghentikan eksekusi script jika belum login


# Konfigurasi judul halaman
st.set_page_config(page_title="Kuis Matematika", page_icon="📝")
st.title("📝 Kuis Matematika Interaktif")
st.write("Uji pemahaman Anda dengan menjawab pertanyaan-pertanyaan berikut!")

# --- Inisialisasi Session State ---
# Session state digunakan untuk menyimpan state antar-interaksi pengguna
if 'questions' not in st.session_state:
    st.session_state.questions = get_quiz_data()

if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'user_answers' not in st.session_state:
    st.session_state.user_answers = [None] * len(st.session_state.questions)

# --- Fungsi untuk me-reset kuis ---
def restart_quiz():
    """Mengatur ulang semua state kuis ke nilai awal."""
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.user_answers = [None] * len(st.session_state.questions)

# --- Logika Utama Kuis ---
questions = st.session_state.questions
current_q_index = st.session_state.current_question

# Cek apakah kuis sudah selesai
if current_q_index >= len(questions):
    st.success(f"🎉 Kuis Selesai! Skor Akhir Anda: **{st.session_state.score} / {len(questions)}**")
    
    # Tampilkan review jawaban
    st.subheader("Review Jawaban Anda")
    for i, q in enumerate(questions):
        user_ans = st.session_state.user_answers[i]
        correct_ans = q['answer']
        if user_ans == correct_ans:
            st.markdown(f"**Soal {i+1}:** {q['question']} - **Benar** (Jawaban Anda: {user_ans})")
        else:
            st.markdown(f"**Soal {i+1}:** {q['question']} - **Salah** (Jawaban Anda: {user_ans}, Jawaban Benar: {correct_ans})")

    # Tombol untuk mengulang kuis
    if st.button("Ulangi Kuis", type="primary"):
        restart_quiz()
        st.rerun()

else:
    # Tampilkan pertanyaan saat ini
    question_item = questions[current_q_index]
    
    # Progress bar
    st.progress((current_q_index + 1) / len(questions), text=f"Pertanyaan {current_q_index + 1} dari {len(questions)}")
    
    # Tampilkan pertanyaan
    st.subheader(f"Pertanyaan {current_q_index + 1}:")
    st.markdown(f"### {question_item['question']}")

    # Tampilkan pilihan jawaban
    user_choice = st.radio(
        "Pilih salah satu jawaban:",
        options=question_item['options'],
        index=None,  # Tidak ada pilihan default
        key=f"q_{current_q_index}"
    )

    # Tombol untuk submit jawaban
    if st.button("Submit Jawaban", key=f"submit_{current_q_index}"):
        if user_choice is not None:
            # Simpan jawaban pengguna
            st.session_state.user_answers[current_q_index] = user_choice
            
            # Cek apakah jawaban benar
            if user_choice == question_item['answer']:
                st.session_state.score += 1
                st.success("Jawaban Anda Benar! 👍")
            else:
                st.error(f"Jawaban Anda Salah. Jawaban yang benar adalah: **{question_item['answer']}**")
            
            # Lanjut ke pertanyaan berikutnya
            st.session_state.current_question += 1
            st.rerun() # Rerun script untuk menampilkan pertanyaan selanjutnya
        else:
            st.warning("Anda harus memilih satu jawaban sebelum melanjutkan.")

