import time
import pyautogui
import pyperclip
import requests
import re
import random

# ------------------------- Configuration -------------------------
OPENROUTER_API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ------------------------- Step 1: Capture Text -------------------------
time.sleep(3)  # Give time to switch to the chat window

# Click the icon to open chat
pyautogui.click(803, 747)
time.sleep(0.5)

# Drag to select chat
pyautogui.moveTo(508, 183)
pyautogui.dragTo(507, 718, duration=0.5, button='left')

# Copy text
pyautogui.hotkey('ctrl', 'c')
time.sleep(0.3)

# Deselect
pyautogui.click(869, 343)

# Get chat history
chat_history = pyperclip.paste()
print("Copied chat history:\n", chat_history)

# ------------------------- Step 2: Check last message sender -------------------------
matches = re.findall(r"\[\d{1,2}:\d{2}, \d{1,2}/\d{1,2}/\d{4}\] ([^:]+):", chat_history)

if not matches:
    print("❌ No sender found in chat history. Exiting.")
    exit()

last_sender = matches[-1].strip()
print(f"Last message from: {last_sender}")

if last_sender.lower() != "mummy jio":
    print("⚠️ Last message is not from Mummy Jio. No reply sent.")
    exit()

# ------------------------- Step 3: Add emotion/tone variation -------------------------
tones = [
    "Use a warm and caring tone, as if talking to your mom, sometimes using emojis like 😊❤️ or 😄.",
    "Use a casual tone — short, relaxed replies like 'haan', 'theek hai', 'abhi karta hoon' with light emojis like 👍🙂.",
    "Sound playful or slightly teasing — like a normal teen texting his mom, e.g., 'arre mummy 😂', 'haan yaar chill 😅'.",
    "Sound polite and calm — no emojis, just simple and respectful language."
]
tone_instruction = random.choice(tones)

# ------------------------- Step 4: Prepare prompt -------------------------
prompt = f"""
You are Shaurya, a 15-year-old Indian student who speaks Hindi and English fluently.
You're chatting casually with your mom ("Mummy Jio") over WhatsApp.
Respond to her latest message only.

Guidelines:
- {tone_instruction}
- Keep it short (1–2 sentences).
- DO NOT include your name, timestamps, or sender labels.
- Reply like a real person, not like an AI.
- Avoid overusing emojis or sounding robotic.

Chat History:
{chat_history}
"""

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are Shaurya, chatting casually with your mom. Be natural, emotional, and human-like."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.9
}

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# ------------------------- Step 5: Get AI Reply -------------------------
response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code == 200:
    ai_reply = response.json()["choices"][0]["message"]["content"].strip()
    
    # Clean possible names/timestamps
    ai_reply = re.sub(r"^.*?:\s*", "", ai_reply)
    ai_reply = re.sub(r"\[\d{1,2}:\d{2}.*?\]", "", ai_reply).strip()
    
    print("\nAI Reply:\n", ai_reply)
else:
    print("Error:", response.status_code, response.text)
    exit()

# ------------------------- Step 6: Auto Send Reply -------------------------
if ai_reply:
    pyperclip.copy(ai_reply)
    time.sleep(0.3)

    pyautogui.click(616, 690)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)
    pyautogui.press('enter')

    print("\n✅ Message sent successfully with natural tone!")




    
