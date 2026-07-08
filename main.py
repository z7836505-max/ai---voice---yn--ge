import streamlit as st
import asyncio
from edge_tts import Communicate
import io

# App ပုံစံပြင်ဆင်ခြင်း
st.set_page_config(page_title="AI Voice Generator", page_icon="🎙️")

# သင်ပေးပို့လိုက်သော ပုံ၏ Direct Link
IMAGE_URL = "https://i.ibb.co/L9s3Jz1F/image-2a1fb9.jpg" 

# CSS - နောက်ခံပုံ နှင့် အရောင်စုံဘောင်များအတွက်
page_bg_img = f"""
<style>
/* နောက်ခံပုံထည့်ရန် */
[data-testid="stAppViewContainer"] {{
    background-image: url("{IMAGE_URL}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* အရောင်စုံဘောင် (Gradient Border) */
.stTextArea textarea, .stSelectbox [data-baseweb="select"], .stSlider, .stButton button {{
    border: 3px solid transparent !important;
    background-image: linear-gradient(white, white), linear-gradient(to right, #ff00cc, #3333ff, #00ff00);
    background-origin: border-box;
    background-clip: padding-box, border-box;
    border-radius: 15px !important;
    padding: 10px;
    background-color: rgba(255, 255, 255, 0.8) !important;
}}

/* ခေါင်းစဉ်စာသား အရောင် */
h1 {
    color: white;
    text-shadow: 2px 2px 4px #000000;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🎙️ AI မြန်မာစာ ဖတ်ခိုင်းမယ်")

# စာရိုက်ရန်
text_data = st.text_area("စာသားကို ဤနေရာတွင် ရိုက်ထည့်ပါ", height=150)

# အသံရှင် ရွေးချယ်ရန်
voice_option = st.selectbox("အသံရှင် ရွေးချယ်ပါ", ["နီလာ", "သီဟ"])

# Slider ဖြင့် အမြန်နှုန်းချိန်ညှိရန်
speed_val = st.slider("အသံအမြန်နှုန်း ချိန်ညှိပါ", min_value=-100, max_value=100, value=0, step=10)
rate_str = f"{speed_val:+d}%"

voice_mapping = {"နီလာ": "my-MM-NilarNeural", "သီဟ": "my-MM-ThihaNeural"}

# အသံဖန်တီးသည့် Function
async def get_audio_bytes(text, voice_code, rate):
    communicate = Communicate(text, voice_code, rate=rate)
    audio_buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    return audio_buffer.getvalue()

if st.button("အသံဖန်တီးမည်"):
    if not text_data:
        st.warning("စာသားရိုက်ပေးပါဦး!")
    else:
        with st.spinner('အသံဖိုင် စတင်ဖန်တီးနေပါပြီ...'):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_effect_loop(loop)
                audio_bytes = loop.run_until_complete(get_audio_bytes(
                    text_data, voice_mapping[voice_option], rate_str
                ))
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button("📥 ဒေါင်းလော့ဆွဲရန်", data=audio_bytes, file_name="voice.mp3", mime="audio/mp3")
            except Exception as e:
                st.error(f"Error: {e}")