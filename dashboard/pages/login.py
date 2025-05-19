import streamlit as st


# Dummy user credentials for login
users_db = {
    "user1@example.com": {"password": "password123", "name": "User One"},
    "admin@example.com": {"password": "adminpass", "name": "Admin"},
}

st.set_page_config(
    page_title="GuaLock",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
st.session_state.logged_in = False
st.session_state.user_name = ""
st.session_state.login_email = ""
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

# Login form or welcome message
with col2:
    with st.container(border=True):
        if not st.session_state.logged_in:
            st.markdown("## Sign in")
            st.markdown("Sebelum gualock, lock in dulu ya ges")

            # Input fields
            st.session_state.login_email = st.text_input("Email", placeholder="Email", autocomplete="",key="login_email_input")
            st.session_state.login_password = st.text_input("Password", placeholder="Password",autocomplete="", type="password", key="login_password_input")

            # Sign in button
            in1, in2 = st.columns((1.5,6))
            with in1:
                if st.button("Sign in", key="signin_button"):
                    email = st.session_state.login_email
                    password = st.session_state.login_password

                    if email in users_db and users_db[email]["password"] == password:
                        st.session_state.logged_in = True
                        st.session_state.user_name = users_db[email]["name"]
                        st.switch_page("pages/main.py")
                    else:
                        st.error("Invalid email or password. Please try again.")

            # Link to register page
            with in2:
                st.page_link("pages/register.py", label="Doesn't have any account ?")

# Empty column for spacing
with col3:
    st.markdown("#")
