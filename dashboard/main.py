import streamlit as st
import qrcode
import cv2
import io
from pyzbar import pyzbar

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
        user_choice = st.radio("Is this correct?", ["Yes", "No"], key="confirm_radio")

        if st.button("Submit Confirmation"):
            if user_choice == "Yes":
                st.session_state.decoded_message = st.session_state.pending_code
                st.success(f"✅ Confirmed QR Code: {st.session_state.decoded_message}")
            else:
                st.warning("❌ Rejected QR Code. Please try again.")

            st.session_state.confirming = False
            st.session_state.pending_code = None
            st.session_state.scanning = True
            st.session_state.decoded_message = None
            st.rerun(scope="fragment")


st.title("🔲 QR Code Generator & Reader")

st.sidebar.title("Select Mode")

mode = st.sidebar.radio("Choose an option:", ("Read QR Code", "Generate QR Code"))

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