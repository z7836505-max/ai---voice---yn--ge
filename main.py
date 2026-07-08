import streamlit as st
import asyncio
from edge_tts import Communicate
import io

# App Setting
st.set_page_config(page_title="AI Voice Generator", page_icon="🎙️")
st.title("🎙️ AI မြန်မာစာ ဖတ်ခိုင်းမယ်")

# စာရိုက်ရန်
text_data = st.text_area("စာသားကို ဤနေရာတွင် ရိုက်ထည့်ပါ", height=200, placeholder="ဒီမှာ စာရိုက်ပါ...")

# အသံရှင် ရွေးချယ်ရန်
voice_option = st.selectbox("အသံရှင် ရွေးချယ်ပါ", ["နီလာ", "သီဟ"])
# အသံနှုန်း ရွေးချယ်ရန်
speed_option = st.selectbox("အသံအမြန်နှုန်း ရွေးချယ်ပါ", ["နှေး - 50%", "ပုံမှန်", "မြန် - 50%"])

voice_mapping = {
    "နီလာ": "my-MM-NilarNeural",
    "သီဟ": "my-MM-ThihaNeural"
}

speed_mapping = {
    "နှေး - 50%": "-50%",
    "ပုံမှန်": "+0%",
    "မြန် - 50%": "+50%"
}

# အသံကို RAM ထဲမှာပဲ Process လုပ်ပေးမည့် Function
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
                # ရွေးချယ်ထားတဲ့နှုန်းအတိုင်း အသံထွက်အောင်လုပ်ခြင်း
                audio_bytes = loop.run_until_complete(get_audio_bytes(
                    text_data, 
                    voice_mapping[voice_option], 
                    speed_mapping[speed_option]
                ))
                
                st.audio(audio_bytes, format="audio/mp3")
                
                st.download_button(
                    label="📥 အသံဖိုင် ဒေါင်းလော့ဆွဲရန်",
                    data=audio_bytes,
                    file_name="my_audio.mp3",
                    mime="audio/mp3"
                )
            except Exception as e:
                st.error(f"အမှားတစ်ခုဖြစ်ပေါ်နေသည်: {e}")