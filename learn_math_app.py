import streamlit as st
from supabase_client import supabase
import requests 
import json

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
        st.query_params.clear() 
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

params = st.query_params
access_token = params.get("access_token")

# --- KONDISI 1: Ada token reset password di URL ---
if access_token:
    st.title("Atur Ulang Password Anda")

    with st.form("update_password_form"):
        st.write("Untuk keamanan, silakan masukkan kembali email Anda dan password baru.")
        # --- PERUBAHAN UTAMA: Tambahkan input email ---
        email = st.text_input("Email Anda")
        new_password = st.text_input("Password Baru", type="password")
        confirm_password = st.text_input("Konfirmasi Password Baru", type="password")
        update_button = st.form_submit_button("Update Password")

        if update_button:
            if not email or not new_password or not confirm_password:
                st.warning("Mohon isi semua kolom.")
            elif len(new_password) < 6:
                st.warning("Password harus terdiri dari minimal 6 karakter.")
            elif new_password != confirm_password:
                st.error("Password tidak cocok. Silakan coba lagi.")
            else:
                try:
                    # --- SOLUSI FINAL: Gunakan verify_otp dengan email dan token ---
                    session = supabase.auth.verify_otp({
                        "token": str(access_token),
                        "type": "recovery",
                        "email": email
                    })
                    
                    # Jika verify_otp berhasil, sesi menjadi aktif
                    # dan kita bisa langsung update password
                    supabase.auth.update_user(
                        {"password": new_password}
                    )
                    
                    st.success("Password berhasil diperbarui! Silakan login dengan password baru Anda.")
                    st.query_params.clear()
                    supabase.auth.sign_out() # Bersihkan sesi sementara
                    st.balloons()
                    st.rerun()

                except Exception as e:
                    st.error(f"Gagal memperbarui password. Pastikan email benar dan link belum kedaluwarsa.")
                    st.error(f"Pesan teknis: {e}")


# --- KONDISI 2 & 3 (Login, Signup, dll tidak berubah) ---
elif 'user' in st.session_state:
    main_app()
else:
    st.title("Selamat Datang! 👋")
    st.write("Silakan login atau daftar untuk melanjutkan.")
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
    with login_tab:
        with st.form("login_form"):
            st.subheader("Login")
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            if st.form_submit_button("Login"):
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
                    session = supabase.auth.sign_up({"email": new_email, "password": new_password})
                    st.session_state['user'] = session.user
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal mendaftar: {e}")
