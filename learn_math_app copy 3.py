import streamlit as st
from supabase_client import supabase

# Konfigurasi halaman
st.set_page_config(
    page_title="Math Course App",
    page_icon="🧮",
    layout="centered" # Menggunakan layout centered untuk form login
)

def main_app():
    """Fungsi ini akan dijalankan setelah pengguna berhasil login."""
    st.sidebar.success("Anda berhasil login!")
    
    # Tombol Logout di sidebar
    if st.sidebar.button("Logout"):
        # Hapus data sesi pengguna
        del st.session_state['user']
        st.rerun() # Muat ulang aplikasi untuk kembali ke halaman login

    # Konten Halaman Utama setelah login
    st.title(f"Selamat Datang di Aplikasi Pembelajaran Matematika! 🧮")
    st.markdown("---")

    st.header("Navigasi")
    st.write(
        "Gunakan menu di **sidebar sebelah kiri** untuk mengakses halaman **Materi Matematika** atau **Kuis Matematika**."
    )
    st.info("Aplikasi ini dirancang untuk membantu Anda belajar konsep matematika dasar dan menguji pemahaman Anda melalui kuis interaktif.", icon="ℹ️")

    st.image(
        "https://placehold.co/800x300/e2e8f0/475569?text=Ilustrasi+Matematika",
        caption="Belajar matematika menjadi lebih mudah dan menyenangkan."
    )


# --- Logika Autentikasi ---

# Cek apakah pengguna sudah login (berdasarkan data di session_state)
if 'user' not in st.session_state:
    st.title("Selamat Datang! 👋")
    st.write("Silakan login atau daftar untuk melanjutkan.")

    # Membuat dua tab: Login dan Sign Up
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    # --- Tab Login ---
    with login_tab:
        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            login_button = st.form_submit_button("Login")

            if login_button:
                if email and password:
                    try:
                        # Mencoba untuk login menggunakan Supabase
                        session = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })
                        # Simpan data sesi jika berhasil
                        st.session_state['user'] = session.user
                        st.rerun() # Muat ulang aplikasi
                    except Exception as e:
                        st.error(f"Gagal login: Pastikan email dan password benar.")
                else:
                    st.warning("Mohon isi email dan password.")

        # --- BAGIAN BARU: LUPA PASSWORD ---
        st.markdown("---")
        with st.expander("Lupa Password?"):
            with st.form("reset_password_form"):
                st.write("Masukkan email Anda untuk menerima link reset password.")
                reset_email = st.text_input("Email", key="reset_email")
                reset_button = st.form_submit_button("Kirim Link Reset")

                if reset_button:
                    if reset_email:
                        try:
                            # Memanggil fungsi Supabase untuk mengirim email reset
                            supabase.auth.reset_password_for_email(email=reset_email)
                            st.success("Link reset password telah dikirim! Silakan periksa email Anda (termasuk folder spam).")
                        except Exception as e:
                            st.error(f"Gagal mengirim email: {e}")
                    else:
                        st.warning("Mohon masukkan email Anda.")

    # --- Tab Sign Up ---
    with signup_tab:
        with st.form("signup_form"):
            st.subheader("Buat Akun Baru")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            signup_button = st.form_submit_button("Sign Up")

            if signup_button:
                if new_email and new_password:
                    try:
                        # Mencoba untuk mendaftarkan pengguna baru
                        session = supabase.auth.sign_up({
                            "email": new_email,
                            "password": new_password,
                        })
                        # Simpan data sesi jika berhasil
                        st.session_state['user'] = session.user
                        st.success("Pendaftaran berhasil! Anda sekarang sudah login.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal mendaftar: {e}")
                else:
                    st.warning("Mohon isi email dan password.")
else:
    # Jika pengguna sudah login, jalankan aplikasi utama
    main_app()
