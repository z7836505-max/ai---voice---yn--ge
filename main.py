import os
import sys
import asyncio
import tkinter as tk
from tkinter import ttk, messagebox
from edge_tts import Communicate
from moviepy.editor import VideoFileClip, AudioFileClip

# FFmpeg လမ်းကြောင်း သတ်မှတ်ခြင်း (သင့် ကုဒ်ဟောင်းအတိုင်း ထိန်းသိမ်းထားပါသည်)
os.environ["IMAGEIO_FFMPEG_EXE"] = "ffmpeg"

# ----------------------------------------------------
# ၁။ AI အသံဖိုင် ထုတ်ပေးမည့် လုပ်ဆောင်ချက် (Function)
# ----------------------------------------------------
def generate_premium_voice():
    # စာရိုက်ကွက်ထဲက စာသားကို ယူခြင်း
    text_data = text_box.get("1.0", tk.END).strip()
    
    # Dropdown က ရွေးချယ်လိုက်တဲ့ အသံအမည်ကို ယူခြင်း
    voice_selection = voice_dropdown.get()

    if not text_data:
        messagebox.showwarning("သတိပေးချက်", "ကျေးဇူးပြု၍ အသံပြောင်းမည့် မြန်မာစာသားကို ရိုက်ထည့်ပါ!")
        return

    # Dropdown စာသားအလိုက် Microsoft ရဲ့ Premium AI အသံကုဒ်ကို ပြောင်းလဲခြင်း
    if "နီလာ" in voice_selection:
        selected_voice = "my-MM-NilarNeural"  # ကြည်လင်ပြတ်သားသော အမျိုးသမီးသံ
    elif "သီဟ" in voice_selection:
        selected_voice = "my-MM-ThihaNeural"  # သဘာဝကျပြီး Smooth ဖြစ်သော အမျိုးသားသံ
    else:
        selected_voice = "my-MM-NilarNeural"

    status_label.config(text="အသံဖိုင် ထုတ်လုပ်နေပါသည်... ခေတ္တစောင့်ပါ...")
    root.update()

    # edge-tts အတွက် နောက်ကွယ်ကနေ အလုပ်လုပ်ပေးမည့် async စနစ်
    async def run_tts():
        communicate = Communicate(text_data, selected_voice)
        await communicate.save("output.mp3")

    try:
        asyncio.run(run_tts())
        status_label.config(text="အဆင်သင့်")
        messagebox.showinfo("အောင်မြင်ပါသည်", "✨ ပိုမိုစမုခ်ဖြစ်သော AI အသံဖိုင် 'output.mp3' ထွက်လာပါပြီ။")
    except Exception as e:
        status_label.config(text="Error ဖြစ်သွားပါသည်")
        messagebox.showerror("Error", f"အကြောင်းရင်း: {e}")

# ----------------------------------------------------
# ၂။ Desktop Application UI ပိုင်း (Window ထည်ဆောက်ခြင်း)
# ----------------------------------------------------
root = tk.Tk()
root.title("AI Voice Generator")
root.geometry("450x450")
root.configure(bg="#f5f5f5")

# ခေါင်းစဉ်စာတန်း
header_label = tk.Label(root, text="AI Voice Generator", font=("Helvetica", 16, "bold"), bg="#f5f5f5", fg="#333333")
header_label.pack(pady=15)

# အသံရွေးချယ်ရန် Dropdown အကွက်
select_label = tk.Label(root, text="အသံရှင် ရွေးချယ်ပါ -", font=("Pyidaungsu", 11), bg="#f5f5f5")
select_label.pack(pady=5)

voice_dropdown = ttk.Combobox(root, font=("Pyidaungsu", 10), width=32, state="readonly")
# Dropdown ထဲတွင် အသံသစ်နှစ်ခုကို ထည့်သွင်းထားခြင်း
voice_dropdown['values'] = ("နီလာ (Premium AI - ကြည်လင်သောအမျိုးသမီးသံ)", "သီဟ (Premium AI - စမုခ်ဖြစ်သောအမျိုးသားသံ)")
voice_dropdown.current(0)  # Default အနေနဲ့ နီလာ ကို ရွေးထားမည်
voice_dropdown.pack(pady=5)

# စာရိုက်ရန် Text Box
text_box = tk.Text(root, font=("Pyidaungsu", 11), width=45, height=8, bd=1, relief="solid")
text_box.pack(pady=15)

# အသံဖိုင်ထုတ်မည့် ခလုတ် (Button)
process_button = tk.Button(root, text="အသံဖိုင်ထုတ်မည်", font=("Pyidaungsu", 11, "bold"), command=generate_premium_voice, bg="#4CAF50", fg="white", activebackground="#45a049", padx=15, pady=6, bd=0)
process_button.pack(pady=10)

# အခြေအနေပြ စာတန်း
status_label = tk.Label(root, text="အဆင်သင့်", font=("Pyidaungsu", 11), bg="#f5f5f5", fg="#666666")
status_label.pack(pady=5)

root.mainloop()