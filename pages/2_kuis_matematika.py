import streamlit as st
from utils.quiz_data import get_quiz_data
from supabase_client import supabase

# Pastikan pengguna sudah login sebelum menjalankan kode halaman apa pun
if 'user' not in st.session_state:
    st.error("⚠️ Anda harus login terlebih dahulu untuk mengakses halaman ini.")
    st.stop()

def initialize_quiz_state():
    """
    Fungsi ini memastikan semua variabel yang dibutuhkan kuis ada di session state.
    Ini adalah cara yang lebih tangguh untuk mencegah error.
    """
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = get_quiz_data()
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    # Pastikan user_answers diinisialisasi dengan panjang yang benar
    if 'user_answers' not in st.session_state or len(st.session_state.user_answers) != len(st.session_state.quiz_questions):
         st.session_state.user_answers = [None] * len(st.session_state.quiz_questions)
    if 'progress_saved' not in st.session_state:
        st.session_state.progress_saved = False

# Panggil fungsi inisialisasi di awal script
initialize_quiz_state()

def save_progress(user_id, score, total_questions):
    """Menyimpan hasil kuis ke tabel user_progress di Supabase."""
    try:
        data_to_insert = {
            "user_id": user_id,
            "score": score,
            "total_questions": total_questions,
            "quiz_name": "Kuis Matematika Dasar"
        }
        supabase.table("user_progress").insert(data_to_insert).execute()
        st.toast("Progres Anda telah disimpan!", icon="💾")
    except Exception as e:
        st.error(f"Gagal menyimpan progres: {e}")

def restart_quiz():
    """Mengatur ulang semua state kuis ke nilai awal."""
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.user_answers = [None] * len(st.session_state.quiz_questions)
    st.session_state.progress_saved = False
    st.rerun()

# --- Tampilan Halaman ---
st.title("📝 Kuis Matematika Interaktif")
st.write("Uji pemahaman Anda dengan menjawab pertanyaan-pertanyaan berikut!")
st.markdown("---")

# --- Logika Utama Kuis ---
questions = st.session_state.quiz_questions
current_q_index = st.session_state.current_question

if current_q_index >= len(questions):
    # Tampilan setelah kuis selesai
    st.success(f"🎉 Kuis Selesai! Skor Akhir Anda: **{st.session_state.score} / {len(questions)}**")

    # Simpan progres jika belum disimpan untuk sesi ini
    if not st.session_state.progress_saved:
        user_id = st.session_state.user.id
        save_progress(user_id, st.session_state.score, len(questions))
        st.session_state.progress_saved = True

    # Tampilkan review jawaban
    st.subheader("Review Jawaban Anda")
    for i, q in enumerate(questions):
        user_ans = st.session_state.user_answers[i]
        correct_ans = q['answer']
        if user_ans == correct_ans:
            st.markdown(f"**Soal {i+1}:** {q['question']} - **Benar** (Jawaban Anda: {user_ans})")
        else:
            st.markdown(f"**Soal {i+1}:** {q['question']} - **Salah** (Jawaban Anda: {user_ans}, Jawaban Benar: {correct_ans})")

    if st.button("Ulangi Kuis", type="primary"):
        restart_quiz()
else:
    # Tampilan saat kuis sedang berjalan
    question_item = questions[current_q_index]
    
    st.progress((current_q_index + 1) / len(questions), text=f"Pertanyaan {current_q_index + 1} dari {len(questions)}")
    
    st.subheader(f"Pertanyaan {current_q_index + 1}:")
    st.markdown(f"### {question_item['question']}")

    user_choice = st.radio(
        "Pilih salah satu jawaban:",
        options=question_item['options'],
        index=None,
        key=f"q_{current_q_index}"
    )

    if st.button("Submit Jawaban", key=f"submit_{current_q_index}"):
        if user_choice is not None:
            st.session_state.user_answers[current_q_index] = user_choice
            if user_choice == question_item['answer']:
                st.session_state.score += 1
                st.success("Jawaban Anda Benar! 👍")
            else:
                st.error(f"Jawaban Anda Salah. Jawaban yang benar adalah: **{question_item['answer']}**")
            
            st.session_state.current_question += 1
            st.rerun()
        else:
            st.warning("Anda harus memilih satu jawaban sebelum melanjutkan.")
