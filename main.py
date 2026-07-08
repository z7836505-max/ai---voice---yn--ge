import streamlit as st
import asyncio
from edge_tts import Communicate
import io

# App Setting
st.set_page_config(page_title="AI Voice Generator", page_icon="🎙️")

# CSS - နောက်ခံအရောင်နှင့် ဘောင်လှလှလေးများအတွက်
page_bg_img = """
<style>
/* နောက်ခံအရောင် */
[data-testid="stAppViewContainer"] {
    background-color: #f0f2f6; 
}

/* Input ဖောင်တွေနဲ့ Textarea တွေမှာ ဘောင်ထည့်ခြင်း */
.stTextArea textarea, .stSelectbox [data-baseweb="select"], .stSlider {
    border: 2px solid #ff4b4b !important;
    border-radius: 10px !important;
    padding: 5px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🎙️ AI မြန်မာစာ ဖတ်ခိုင်းမယ်")

# စာရိုက်ရန်
text_data = st.text_area("စာသားကို ဤနေရာတွင် ရိုက်ထည့်ပါ", height=200, placeholder="ဒီမှာ စာရိုက်ပါ...")

# အသံရှင် ရွေးချယ်ရန်
voice_option = st.selectbox("အသံရှင် ရွေးချယ်ပါ", ["နီလာ", "သီဟ"])

# Slider ဖြင့် အမြန်နှုန်းချိန်ညှိရန်
speed_val = st.slider("အသံအမြန်နှုန်း ချိန်ညှိပါ", min_value=-100, max_value=100, value=0, step=10)
rate_str = f"{speed_val:+d}%"

voice_mapping = {
    "နီလာ": "my-MM-NilarNeural",
    "သီဟ": "my-MM-ThihaNeural"
}

# အသံကို RAM ထဲမှာ Process လုပ်ရန်
async def get_audio_bytes(text, voice_code, rate):
    communicate = Communicate(text, voice_code, rate=rate)
    audio_buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    return audio_buffer.getvalue()

# အသံဖန်တီးခြင်း
if st.button("အသံဖန်တီးမည်"):
    if not text_data:
        st.warning("ကျေးဇူးပြု၍ စာသားရိုက်ပေးပါ!")
    else:
        with st.spinner('အသံဖိုင် စတင်ဖန်တီးနေပါပြီ...'):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                audio_bytes = loop.run_until_complete(get_audio_bytes(
                    text_data, 
                    voice_mapping[voice_option], 
                    rate_str
                ))
                
                # Browser မှာ နားထောင်လို့ရမည့် Player
                st.audio(audio_bytes, format="audio/mp3")
                
                # Download လုပ်ရန်
                st.download_button(
                    label="📥 အသံဖိုင် ဒေါင်းလော့ဆွဲရန်",
                    data=audio_bytes,
                    file_name="my_audio.mp3",
                    mime="audio/mp3"
                )
            except Exception as e:
                st.error(f"အမှားတစ်ခုဖြစ်ပေါ်နေသည်: {e}")