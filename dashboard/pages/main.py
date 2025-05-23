import streamlit as st
import qrcode
import cv2
import io
from pyzbar import pyzbar
from gpiozero import Servo
import time
from time import sleep

st.set_page_config(
    page_title="GuaLock",
    layout="wide",
    initial_sidebar_state="expanded"
)


def set_angle(angle):
    """Rotate the servo to a specific angle using gpiozero."""

    SERVO_PIN = 18
    servo = Servo(SERVO_PIN, min_pulse_width=0.0005, max_pulse_width=0.0025)

    # Clamp angle between 0 and 180
    angle = max(0, min(180, angle))
    
    # Map angle (0-180) to gpiozero's -1 to 1 range
    normalized = (angle - 90) / 90
    
    servo.value = normalized
    sleep(0.5)
    servo.value = None  # Detach servo

def open_locker():
    set_angle(90)

def close_locker():
    set_angle(0)

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
if "door_state" not in st.session_state:
    st.session_state.door_state = False
    
@st.fragment
def scan_qr_code():

    if st.session_state.scanning and not st.session_state.confirming:
        cap = cv2.VideoCapture(0)
        stframe = st.empty()

        while st.session_state.scanning and not st.session_state.confirming:
            ret, frame = cap.read()
            if not ret:
                st.write("Failed to capture image.")
                break

            qr_codes = decode_qr_code(frame)
            stframe.image(frame, channels="BGR")

            if qr_codes:
                current_code = qr_codes[0]
                if current_code != st.session_state.decoded_message:
                    st.session_state.confirming = True
                    st.session_state.pending_code = current_code
                    break

        cap.release()
        cv2.destroyAllWindows()

    if st.session_state.confirming:
        st.info(f"Detected QR Code: `{st.session_state.pending_code}`")
        open_locker_choice = st.radio("Open the locker?", ["Yes", "No"], key="confirm_radio")

        if st.button("Open Locker", key="open_locker_button"):
            if open_locker_choice == "Yes":
                st.session_state.decoded_message = st.session_state.pending_code
                open_locker()
                # time.sleep(3)
                # close_locker()
                st.success(f"✅ Opened Locker ID: {st.session_state.decoded_message}")
            else:
                st.warning("❌ Rejected QR Code. Please try again.")

            st.session_state.confirming = False
            st.session_state.pending_code = None
            st.session_state.scanning = True
            st.session_state.decoded_message = None
            st.rerun(scope="fragment")

        close_locker_choice = st.radio("Close the locker?", ["Yes", "No"], key="confirm_radio")
        if st.button("Close Locker", key="close_locker_button"):
            if close_locker_choice == "Yes":
                st.session_state.decoded_message = st.session_state.pending_code
                close_locker()
                st.success(f"✅ Closed Locker ID: {st.session_state.decoded_message}")
            else:
                st.warning("❌ Rejected QR Code. Please try again.")

            st.session_state.confirming = False
            st.session_state.pending_code = None
            st.session_state.scanning = True
            st.session_state.decoded_message = None
            st.rerun(scope="fragment")

st.title("🔲 QR Code Generator & Reader")

with st.sidebar:
    st.title("Welcome, %s" % st.session_state.user_name)
    st.markdown("## Select Mode")
    mode = st.radio("Choose an option:", ("Read QR Code", "Generate QR Code"))
    st.divider()
    st.page_link("pages/login.py",label=":material/home: Logout", use_container_width=True)



if mode == "Generate QR Code":
    st.header("🧾 Generate QR Code")
    qr_text = st.text_input("Enter text or URL:")
    if st.button("Generate"):
        if qr_text:
            qr_img = qrcode.make(qr_text)

            # Convert to BytesIO
            buf = io.BytesIO()
            qr_img.save(buf, format="PNG")
            buf.seek(0)

            st.image(buf, caption="Generated QR Code")
            
            qr_img.save("qr_code.png")
            with open("qr_code.png", "rb") as file:
                st.download_button("Download QR Code", file, file_name="qr_code.png")
        else:
            st.warning("Please enter some text.")

elif mode == "Read QR Code":
    st.header("📷 Scan QR Code via Webcam")
    scan_qr_code()
