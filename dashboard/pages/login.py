import streamlit as st
import requests

API_LOGIN_URL ="https://n8n.mbintangr.com/webhook/login"

st.set_page_config(
    page_title="GuaLock",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
st.session_state.logged_in = False
st.session_state.user_name = ""
st.session_state.login_username = ""
st.session_state.login_password = ""

st.markdown("#")
# Layout
col1, col2, col3 = st.columns([3, 2, 1], gap="large")


# Welcome text

with col1:
    st.title("Welcome to GuaLock")
    st.markdown("GuaLock adalah solusi modern untuk penyimpanan barang pribadi Anda dengan teknologi keamanan canggih berbasis QR Code. Kami memahami pentingnya keamanan dan kemudahan akses dalam menyimpan barang berharga, oleh karena itu GuaLock hadir sebagai sistem smart locker yang mengutamakan kenyamanan, kecepatan, dan keamanan tinggi.")
    st.markdown("### Apa itu GuaLock?")
    st.markdown("GuaLock adalah sistem Smart Locker inovatif yang memungkinkan Anda menyimpan dan mengambil barang kapan saja dengan metode autentikasi QR Code yang praktis dan aman. Tidak perlu lagi repot membawa kunci fisik atau mengingat kombinasi angka — cukup gunakan QR Code unik yang dikirimkan melalui website kami untuk membuka locker secara otomatis.")

# Login form
with col2:
    with st.container(border=True):
        if not st.session_state.logged_in:
            st.markdown("## Sign in")
            st.markdown("Sebelum gualock, lock in dulu ya ges")

            # Input fields
            username = st.text_input("username", placeholder="username", key="login_username_input")
            password = st.text_input("Password", placeholder="Password", type="password", key="login_password_input")

            col_btn1, col_btn2 = st.columns((1.5, 6))

            with col_btn1:
                if st.button("Sign in", key="signin_button"):
                    if not username or not password:
                        st.warning("Mohon isi username dan password.")
                    else:
                        try:
                            payload = {
                                "username": username,
                                "password": password
                            }
                            response = requests.post(API_LOGIN_URL, json=payload, verify=False)
                            

                            if response.status_code == 200:
                                data = response.json()
                                if data.get("message") == "Logged In!":
                                    st.session_state.logged_in = True
                                    st.session_state.user_name = data.get("username", "User")
                                    st.success(f"Welcome, {st.session_state.user_name}!")
                                    st.switch_page("pages/main.py")
                                else:
                                    st.error("Terjadi kesalahan saat login.")
                            else:
                                try:
                                    err_msg = response.json().get("detail", "Login gagal.")
                                except:
                                    err_msg = "Terjadi kesalahan saat login."
                                st.error(err_msg)

                        except requests.exceptions.RequestException as e:
                            st.error(f"Terjadi masalah koneksi ke server: {e}")

            # Link to register page
            with col_btn2:
                st.page_link("pages/register.py", label="Doesn't have any account ?")

# Spacer column
with col3:
    st.markdown("#")
