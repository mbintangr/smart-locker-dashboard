import streamlit as st
import requests

API_URL = "https://n8n.mbintangr.com/webhook/create-user"

st.set_page_config(
    page_title="GuaLock",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("#")

with st.container(border=True):
    st.markdown("## Register")
    st.markdown("Silahkan daftar terlebih dahulu untuk menggunakan GuaLock")

    # Input fields
    email = st.text_input("Email", placeholder="Email", key="register_email_input")
    password = st.text_input("Password", placeholder="Password", type="password", key="register_password_input")
    username = st.text_input("Username", placeholder="Username", key="register_name_input")

    col1, col2 = st.columns([1, 6])

    with col1:
        if st.button("Register", key="register_button"):
            if not email or not password or not username:
                st.warning("Semua field wajib diisi.")
            else:
                try:
                    payload = {
                        "email": email,
                        "password": password,
                        "username": username
                    }
                    response = requests.post(API_URL, json=payload)

                    if response.status_code == 201 or response.status_code == 200:
                        st.success("Registrasi berhasil! Silakan login.")
                        st.switch_page("pages/login.py")
                    else:
                        try:
                            error_message = response.json().get("detail", "Registrasi gagal.")
                        except:
                            error_message = "Terjadi kesalahan saat memproses registrasi."
                        st.error(error_message)

                except requests.exceptions.RequestException as e:
                    st.error(f"Network error: {e}")

    with col2:
        st.page_link("pages/login.py", label="Already have an account ?")