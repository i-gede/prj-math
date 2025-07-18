# utils/quiz_data.py

def get_quiz_data():
    """
    Menyediakan daftar soal kuis statis.
    Setiap item adalah dictionary yang berisi:
    - 'question': Teks pertanyaan (bisa menggunakan format LaTeX).
    - 'options': Daftar pilihan jawaban.
    - 'answer': Jawaban yang benar.
    """
    return [
        {
            "question": "Berapakah hasil dari $2 \\times (3+5)$?",
            "options": ["10", "16", "11", "18"],
            "answer": "16"
        },
        {
            "question": "Jika $x - 7 = 10$, berapakah nilai $x$?",
            "options": ["3", "10", "17", "-3"],
            "answer": "17"
        },
        {
            "question": "Apa nama lain dari sudut 90 derajat?",
            "options": ["Sudut Lancip", "Sudut Tumpul", "Sudut Siku-siku", "Sudut Lurus"],
            "answer": "Sudut Siku-siku"
        },
        {
            "question": "Berapakah luas lingkaran dengan jari-jari 7 cm? (gunakan $\\pi = \\frac{22}{7}$)",
            "options": ["154 cm²", "49 cm²", "44 cm²", "77 cm²"],
            "answer": "154 cm²"
        },
        {
            "question": "Sederhanakan bentuk aljabar $5a + 2b - 3a + 5b$.",
            "options": ["$2a + 7b$", "$8a + 7b$", "$2a - 3b$", "$8a - 3b$"],
            "answer": "$2a + 7b$"
        }
    ]

# Catatan:
# Untuk mengambil data dari Supabase, Anda bisa mengubah fungsi ini menjadi seperti ini:
#
# from supabase_client import supabase
#
# def get_quiz_data_from_db():
#     try:
#         response = supabase.table('nama_tabel_kuis').select('*').execute()
#         return response.data
#     except Exception as e:
#         print(f"Gagal mengambil data kuis: {e}")
#         return []
