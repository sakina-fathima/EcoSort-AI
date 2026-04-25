import streamlit as st
from google import genai
from google.genai.types import HttpOptions
from PIL import Image
import time

# --- INITIAL SETUP ---
# Leave it exactly like this in your file:
API_KEY = st.secrets["GOOGLE_API_KEY"]
client = genai.Client(
    api_key = st.secrets["GOOGLE_API_KEY"])

st.set_page_config(page_title="EcoSort AI", page_icon="🌱", layout="wide")

# --- CUSTOM ELEGANT CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    h1 { color: #1b5e20; font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- CLEAN SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3299/3299935.png", width=80)
    st.title("EcoSort AI")
    st.write("---")
    app_mode = st.radio("Menu", ["Dashboard", "Sustainability Goal"])
    st.write("---")

# --- MAIN DASHBOARD ---
if app_mode == "Dashboard":
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("♻️ Smart Waste Classifier")
        st.write("Upload an image to identify the correct disposal method.")
    with col2:
        st.write("") # Keeping layout balanced

    st.divider()

    input_col, output_col = st.columns([1, 1], gap="large")

    with input_col:
        st.subheader("📤 Input")
        option = st.toggle("Switch to Text Search", value=False)

        if not option:
            file = st.file_uploader("Upload waste photo", type=["jpg", "png", "jpeg"])
            if file:
                img = Image.open(file)
                st.image(img, use_container_width=True)
        else:
            text_input = st.text_input("Enter item name", placeholder="e.g. Cardboard box")

    with output_col:
        st.subheader("AI Analysis")
        
        if (not option and file) or (option and text_input):
            if st.button("ANALYZE"):
                with st.spinner("AI is analyzing..."):
                    # --- RETRY LOGIC FOR 503 ERROR ---
                    success = False
                    for attempt in range(3):
                        try:
                            prompt = "Identify this waste. Category, Bin Color, and a Sustainability Tip."
                            if not option:
                                response = client.models.generate_content(model="gemini-2.5-flash", contents=[prompt, img])
                            else:
                                response = client.models.generate_content(model="gemini-2.5-flash", contents=f"{prompt} for {text_input}")
                            
                            st.balloons()
                            st.markdown(f"""
                            <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7d32;">
                                <h4 style="color: #2e7d32; margin:0;">Success!</h4>
                                <p style="color: #333;">{response.text}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            success = True
                            break 
                        except Exception as e:
                            if "503" in str(e):
                                time.sleep(2) # Wait 2 seconds before retrying
                                continue
                            else:
                                st.error(f"Error: {e}")
                                break
                    
                    if not success:
                        st.warning("The AI servers are very busy. Please try again in a few seconds.")
        else:
            st.info("Please provide an input to see results.")

else:
    st.title("SDG 12: Responsible Consumption")
    st.write("This project aims to bridge the gap between waste generation and proper recycling.")
