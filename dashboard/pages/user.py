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
    data=json.dumps({"collector_id": "a"}),
    headers={"Content-Type": "application/json"},
    verify=False  # Set ke True jika menggunakan HTTPS yang valid
)



if response.status_code == 200:
    data = response.json()

# Layout

st.title("Welcome, %s " % st.session_state.user_name)
st.markdown("## Terima kasih sudah menggunakan jasa locker kami")
st.divider()
st.markdown("## Berikut adalah QR Code locker Anda")
st.markdown("Harap simpan QRCode dengan baik dengan cara SS atau klik button Download QRCode")
st.markdown("Berikut adalah Loker yang tersedia")

cols = st.columns(5, gap="large",vertical_alignment="center")  # Ubah jadi 4 atau 5 jika ingin lebih rapat

for idx, item in enumerate(data):
    id_value = item.get("id")
    id_locker = item.get("locker_id")

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
        st.markdown("#")
