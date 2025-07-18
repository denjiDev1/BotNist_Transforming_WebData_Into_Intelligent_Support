import tkinter as tk
from tkinter import scrolledtext, Frame, Label, Toplevel
import requests
import threading
import speech_recognition as sr
import asyncio
import edge_tts
import os
from playsound import playsound

FLASK_API_URL = ""
API_KEY = ""
USER_ID = ""

call_active = False
call_window = None
listening_label = None

# Async TTS using Edge-tts
async def speak_edge(text):
    try:
        communicate = edge_tts.Communicate(text, voice="en-US-EmmaMultilingualNeural")
        await communicate.save("temp_edge.mp3")
        playsound("temp_edge.mp3")
        os.remove("temp_edge.mp3")
    except Exception as e:
        print(f"Speech error: {e}")

def speak_text(text):
    asyncio.run(speak_edge(text))

def send_message(user_input):
    if not user_input:
        return

    chat_display.config(state=tk.NORMAL)
    user_frame = Frame(chat_display, bg="#007AFF", padx=10, pady=5)
    user_label = Label(user_frame, text=user_input, font=("Arial", 12), fg="white", bg="#007AFF", wraplength=250, justify="left")
    user_label.pack(padx=10, pady=5)
    user_frame.pack(anchor="w", padx=10, pady=5, fill=tk.X)
    chat_display.window_create(tk.END, window=user_frame)
    chat_display.insert(tk.END, "\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

    try:
        response = requests.post(FLASK_API_URL, json={"query": user_input, "key": API_KEY, "user_id": USER_ID})
        full_response = response.json().get("response", "No response received")
        # Get only the part before the first empty line (hallucination usually follows)
        # Split response at known ending pattern to exclude hallucinated tail
        delimiters = [
            "Please let me know if you have any other questions or concerns!",
            "Fallback Answer:",
            "Bot:",
            "bot:",
            "user:",
            "User:",
        ]

        # Find first matching delimiter
        for delimiter in delimiters:
            if delimiter in full_response:
                bot_response = full_response.split(delimiter)[0].strip() + f" {delimiter}"
                break
        else:
            # No delimiter found
            bot_response = full_response.strip()


        #split_response = full_response.strip().split("\n\n", 1)
        #bot_response = split_response[0].strip()

    except requests.exceptions.RequestException as e:
        bot_response = "Error: " + str(e)

    chat_display.config(state=tk.NORMAL)
    bot_frame = Frame(chat_display, bg="#34C759", padx=10, pady=5)
    bot_label = Label(bot_frame, text=bot_response, font=("Arial", 12), fg="white", bg="#34C759", wraplength=250, justify="right")
    bot_label.pack(padx=10, pady=5)
    bot_frame.pack(anchor="e", padx=10, pady=5, fill=tk.X)
    chat_display.window_create(tk.END, window=bot_frame)
    chat_display.insert(tk.END, "\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.yview(tk.END)

    if call_active:
        speak_text(bot_response)  # Blocking: waits for speech to finish before continuing

def send_message_from_entry():
    user_input = entry.get().strip()
    entry.delete(0, tk.END)
    send_message(user_input)

def listen_and_send():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        try:
            if listening_label.winfo_exists():
                listening_label.config(text="Listening... Speak now.")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            user_query = recognizer.recognize_google(audio)
            if listening_label.winfo_exists():
                listening_label.config(text="Processing...")
            send_message(user_query)
            if listening_label.winfo_exists():
                listening_label.config(text="Say something or end call.")
        except Exception as e:
            if listening_label and listening_label.winfo_exists():
                listening_label.config(text=f"Error: {e}")


def voice_loop():
    while call_active:
        listen_and_send()

def start_voice_call():
    global call_active, call_window, listening_label
    if call_active:
        return
    call_active = True

    call_window = Toplevel(root)
    call_window.title("Voice Call")
    call_window.geometry("300x150")
    call_window.configure(bg="#f4f4f8")

    listening_label = Label(call_window, text="Say something...", font=("Arial", 12), bg="#f4f4f8", fg="#007AFF")
    listening_label.pack(pady=20)

    cut_button = tk.Button(call_window, text="End Call", font=("Arial", 12), bg="#FF3B30", fg="white", command=end_voice_call)
    cut_button.pack(pady=10)

    threading.Thread(target=voice_loop, daemon=True).start()

def end_voice_call():
    global call_active
    call_active = False
    if call_window:
        call_window.destroy()

# GUI Setup
root = tk.Tk()
root.title("Aesthetic Chatbot")
root.geometry("450x600")
root.configure(bg="#f4f4f8")

header = tk.Label(root, text="Chatbot", font=("Arial", 16, "bold"), fg="#333", bg="#f4f4f8", pady=10)
header.pack()

chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, height=20, font=("Arial", 12), bg="#fff", fg="#333", relief=tk.FLAT, padx=10, pady=10)
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

frame = tk.Frame(root, bg="#f4f4f8")
frame.pack(pady=5, padx=10, fill=tk.X)

entry = tk.Entry(frame, font=("Arial", 12), bg="#fff", fg="#333", relief=tk.FLAT, width=30)
entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
entry.bind("<Return>", lambda event: send_message_from_entry())

send_button = tk.Button(frame, text="Send", font=("Arial", 12, "bold"), bg="#007AFF", fg="white", relief=tk.FLAT, command=send_message_from_entry)
send_button.pack(side=tk.LEFT, padx=5, pady=5)

call_button = tk.Button(root, text="Start Voice Call", font=("Arial", 12), bg="#34C759", fg="white", relief=tk.FLAT, command=start_voice_call)
call_button.pack(pady=10)

root.mainloop()
