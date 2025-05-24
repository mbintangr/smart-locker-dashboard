import streamlit as st

pages = {
    "Account Management":
    [
        st.Page("pages/login.py", title="Logout", icon=":material/home:"),
        st.Page("pages/register.py"),
        st.Page("pages/main.py"),
        st.Page("pages/user.py")
    ]
}



pg = st.navigation(pages, position="hidden")
pg.run()