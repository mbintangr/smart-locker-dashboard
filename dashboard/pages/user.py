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
    id_locker = data[0].get("locker_id")


# Layout

st.title("Welcome, %s " % st.session_state.user_name)
st.markdown("## Terima kasih sudah menggunakan jasa locker kami")
st.divider()
col1, col2, col3 = st.columns([3, 2, 2], gap="large")

with col1:
    st.markdown("## Berikut adalah QR Code locker Anda")
    st.markdown("Harap simpan QRCode dengan baik dengan cara SS atau klik button Download QRCode")
    st.markdown ("Locker kamu adalah Locker Nomor %d" % id_locker)

with col2:
    if isinstance(data, list) and len(data) > 0:
        id_value = data[0].get("id")

    if id_value:
        # Generate QR dari id
        qr_img = qrcode.make(str(id_value))
        buf = io.BytesIO()
        qr_img.save(buf, format="PNG")
        buf.seek(0)

        st.image(buf, caption=f"QR Code untuk Locker: {id_locker} dengan ID {id_value}")
    else:
        st.error("ID tidak ditemukan dalam response.")
