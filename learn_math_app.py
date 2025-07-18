import streamlit as st
from supabase_client import supabase

# Konfigurasi halaman
st.set_page_config(
    page_title="Math Course App",
    page_icon="🧮",
    layout="centered"
)

def main_app():
    """Fungsi ini akan dijalankan setelah pengguna berhasil login."""
    st.sidebar.success("Anda berhasil login!")
    
    if st.sidebar.button("Logout"):
        del st.session_state['user']
        st.query_params.clear() # Hapus parameter dari URL saat logout
        st.rerun()

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

# Ambil parameter dari URL
params = st.query_params
access_token = params.get("access_token")

# --- KONDISI 1: Ada token reset password di URL ---
if access_token:
    st.title("Atur Ulang Password Anda")
    
    try:
        # --- PERBAIKAN UTAMA DI SINI ---
        # Mengganti None dengan string kosong "" untuk refresh token.
        supabase.auth.set_session(str(access_token), "")

        with st.form("update_password_form"):
            st.write("Silakan masukkan password baru Anda di bawah ini.")
            new_password = st.text_input("Password Baru", type="password")
            confirm_password = st.text_input("Konfirmasi Password Baru", type="password")
            update_button = st.form_submit_button("Update Password")

            if update_button:
                if not new_password or not confirm_password:
                    st.warning("Mohon isi kedua kolom password.")
                elif new_password != confirm_password:
                    st.error("Password tidak cocok. Silakan coba lagi.")
                else:
                    # Setelah sesi diatur, kita bisa langsung update password
                    supabase.auth.update_user(
                        {"password": new_password}
                    )
                    st.success("Password berhasil diperbarui! Silakan login dengan password baru Anda.")
                    # Hapus parameter dari URL dan bersihkan sesi
                    st.query_params.clear()
                    supabase.auth.sign_out() # Membersihkan sesi sementara
                    st.rerun()

    except Exception as e:
        st.error(f"Gagal memproses link: Link tidak valid atau sudah kedaluwarsa. Silakan minta link baru.")


# --- KONDISI 2: Pengguna sudah login ---
elif 'user' in st.session_state:
    main_app()

# --- KONDISI 3: Halaman login/signup normal ---
else:
    st.title("Selamat Datang! 👋")
    st.write("Silakan login atau daftar untuk melanjutkan.")

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            login_button = st.form_submit_button("Login")

            if login_button:
                try:
                    session = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state['user'] = session.user
                    st.rerun()
                except Exception:
                    st.error("Gagal login: Pastikan email dan password benar.")
        
        with st.expander("Lupa Password?"):
            with st.form("reset_password_form"):
                reset_email = st.text_input("Email untuk reset", key="reset_email")
                if st.form_submit_button("Kirim Link Reset"):
                    supabase.auth.reset_password_for_email(email=reset_email)
                    st.success("Link reset telah dikirim! Periksa email Anda.")

    with signup_tab:
        with st.form("signup_form"):
            st.subheader("Buat Akun Baru")
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_password")
            if st.form_submit_button("Sign Up"):
                try:
                    session = supabase.auth.sign_up({"email": new__email, "password": new_password})
                    st.session_state['user'] = session.user
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal mendaftar: {e}")
