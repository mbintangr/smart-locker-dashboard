import streamlit as st
import requests
import json
import qrcode
import io

st.set_page_config(
    page_title="GuaLock",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# Login Logic
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/login.py")
    st.stop()

# APi Calling
API_URL = "https://n8n.mbintangr.com/webhook/get-collector-data"

response = requests.request(
    "GET",
    API_URL,
    data=json.dumps({"collector_id": st.session_state.user_name}),
    headers={"Content-Type": "application/json"},
    verify=False  # Set ke True jika menggunakan HTTPS yang valid
)


if response.status_code == 200:
    if len(response.json()) == 0:
        data = []
        st.error("Data Locker Kosong")
    else:
        data = response.json()

# Layout
with st.sidebar:
    st.page_link("pages/login.py",label=":material/logout: Logout", use_container_width=True)
st.title("Welcome, %s " % st.session_state.user_name)
st.markdown("Terima kasih sudah menggunakan jasa locker kami 🙏🏻")
# st.divider()

cols = st.columns(5, gap="large",vertical_alignment="center")  # Ubah jadi 4 atau 5 jika ingin lebih rapat

for idx, item in enumerate(data):
    id_value = item.get("id")
    id_locker = item.get("locker_id")
    if id_value is not None:
        st.markdown("## Berikut adalah QR Code locker Anda")
        st.markdown("Harap simpan QR Code dengan baik dengan cara Screenshot")
        st.markdown("Berikut adalah Loker yang tersedia")
        
        qr_img = qrcode.make(str(id_value))
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)

        col = cols[idx % 2]
        with col:
            with st.container(border=True):
                st.image(buf, caption=f"QR Code Locker: {id_locker}", width=265)
                st.caption(f"ID: {id_value}")

        if (idx + 1) % 2 == 0 and (idx + 1) < len(data):
            cols = st.columns(3)
    else:
        st.warning('Anda belum memiliki locker')
