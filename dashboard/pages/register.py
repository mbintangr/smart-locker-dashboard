import streamlit as st

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
    st.session_state.register_email = st.text_input("Email", placeholder="Email", autocomplete="",key="register_email_input")
    st.session_state.register_password = st.text_input("Password", placeholder="Password",autocomplete="", type="password", key="register_password_input")
    st.session_state.register_name = st.text_input("Username", placeholder="Username", key="register_name_input")

    col1, col2 = st.columns([1,6])

    # Register button
    with col1:
        if st.button("Register", key="register_button"):
            email = st.session_state.register_email
            password = st.session_state.register_password
            name = st.session_state.register_name
    
    
    with col2:
        st.page_link("pages/login.py", label="Already have an account ?")