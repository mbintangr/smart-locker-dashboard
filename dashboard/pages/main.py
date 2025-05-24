import streamlit as st
import qrcode
import cv2
import io
from pyzbar import pyzbar
from time import sleep
import requests

st.set_page_config(
    page_title="GuaLock",
    layout="wide",
    initial_sidebar_state="expanded"
)


def set_angle(angle, servo_pin):
    """Rotate the servo to a specific angle using gpiozero."""
    from gpiozero import Servo

    servo = Servo(servo_pin, min_pulse_width=0.0005, max_pulse_width=0.0025)

    # Clamp angle between 0 and 180
    angle = max(0, min(180, angle))
    
    # Map angle (0-180) to gpiozero's -1 to 1 range
    normalized = (angle - 90) / 90
    
    servo.value = normalized
    sleep(0.5)
    servo.value = None  # Detach servo

def open_locker(locker_id):
    if locker_id == '1':
        set_angle(90, 18)
    elif locker_id == '2':
        set_angle(90, 23)

def close_locker(locker_id):
    if locker_id == '1':
        set_angle(0, 18)
    elif locker_id == '2':
        set_angle(0, 23)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("pages/login.py")
    st.stop()

def decode_qr_code(frame):
    decoded_objects = pyzbar.decode(frame)
    qr_codes = [obj.data.decode('utf-8') for obj in decoded_objects]
    return qr_codes


# Initialize session state
if "scanning" not in st.session_state:
    st.session_state.scanning = True
if "decoded_message" not in st.session_state:
    st.session_state.decoded_message = None
if "confirming" not in st.session_state:
    st.session_state.confirming = False
if "pending_code" not in st.session_state:
    st.session_state.pending_code = None

@st.fragment
def scan_qr_code():
    st.header("📷 Scan QR Code via Webcam")

    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture image.")
            break

        qr_codes = decode_qr_code(frame)
        stframe.image(frame, channels="BGR")

        if qr_codes:
            current_code = qr_codes[0]
            res = requests.get(
                "https://n8n.mbintangr.com/webhook/checkout",
                data={"id": current_code},
                verify=False
            )
            
            res = res.json()

            if res.get("message") == "Success!":
                open_locker(res.get("locker_id"))
                st.toast("Success! QR Code Valid.", icon="🎉")
            else:
                if res.get("locker_id") == "":
                    st.toast("Failed! QR Code Invalid.", icon="🚫")
                else:
                    close_locker(res.get("locker_id"))
                    st.toast("Failed! QR Code not found.", icon="🚫")
                
            st.rerun()

    cap.release()
    cv2.destroyAllWindows()

st.title("🔲 QR Code Generator & Reader")

with st.sidebar:
    st.title("Welcome, %s" % st.session_state.user_name)
    st.markdown("## Select Mode")
    mode = st.radio("Choose an option:", ("Scan QR Code", "Register Locker"))
    st.divider()
    st.page_link("pages/login.py",label=":material/logout: Logout", use_container_width=True)

if mode == "Register Locker":
    st.header("🧾 Register Locker")
    res = requests.get(url='https://n8n.mbintangr.com/webhook/get-all-user', verify=False)
    res = res.json()
    
    collector = None
    if len(res) > 0:
        users = []
        for user in res:
            if user.get("username"):
                users.append(f'{user.get("username")}')
        if len(users) > 0:
            collector = st.selectbox("Select User", users)
        else:
            st.error("Users not available.")
    else:
        st.error("Users not available.")
        
    res = requests.get(url='https://n8n.mbintangr.com/webhook/get-available-locker', verify=False)
    res = res.json()

    selected_locker = None
    if len(res) > 0:
        available_lockers = []
        for locker in res:
            if locker.get("is_available"):
                available_lockers.append(f'{locker.get("id")}')
        if len(available_lockers) > 0:
            selected_locker = st.selectbox("Select Locker", available_lockers)
        else:
            st.error("No available lockers.")
    else:
        st.error("No available lockers.")
    
    if st.button("Register"):
        if collector and selected_locker:
            res = requests.post(
                url='https://n8n.mbintangr.com/webhook/checkin',
                data={"collector": collector, "locker_id": selected_locker},
                verify=False
            )
            st.toast("Success! Locker Registered.", icon="🎉")
            st.rerun()
        else:
            st.error("Please fill in all fields.")
        

elif mode == "Scan QR Code":
    scan_qr_code()
