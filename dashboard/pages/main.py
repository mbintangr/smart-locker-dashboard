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

# def get_distance(locker_id):
#     from gpiozero import DistanceSensor
    
#     if locker_id == '1':
#         us = DistanceSensor(echo=12, trigger=16, max_distance=2.0)
#         distance = us.distance * 100
#     elif locker_id == '2':
#         us = DistanceSensor(echo=6, trigger=19, max_distance=2.0)
#         distance = us.distance * 100
    
#     return distance

def get_distance(locker_id):
    import RPi.GPIO as GPIO
    import time

    GPIO.setmode(GPIO.BCM)

    if locker_id == '1':
        TRIG = 16
        ECHO = 12
    elif locker_id == '2':
        TRIG = 19
        ECHO = 6

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)
    time.sleep(0.1)

    # Send 10us pulse to trigger
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo to start
    pulse_start = time.time()
    timeout = time.time() + 0.04
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if pulse_start > timeout:
            return 999  # Timeout

    # Wait for echo to end
    pulse_end = time.time()
    timeout = time.time() + 0.04
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if pulse_end > timeout:
            return 999  # Timeout

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # cm
    distance = round(distance, 2)

    GPIO.cleanup()

    return distance

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
            if get_distance(selected_locker) < 30:
                print(get_distance(selected_locker))
                res = requests.post(
                    url='https://n8n.mbintangr.com/webhook/checkin',
                    data={"collector": collector, "locker_id": selected_locker},
                    verify=False
                )
                st.toast("Success! Locker Registered.", icon="🎉")
                close_locker(selected_locker)
        else:
            st.error("Please fill in all fields.")
        st.rerun()
        

elif mode == "Scan QR Code":
    scan_qr_code()
