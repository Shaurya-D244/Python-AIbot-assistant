import time
import pyautogui
import pyperclip
import requests
import re

# ------------------------- Configuration -------------------------
OPENROUTER_API_KEY = "API_KEY"
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
# Extract all messages and find the last sender name
matches = re.findall(r"\[\d{1,2}:\d{2}, \d{1,2}/\d{1,2}/\d{4}\] ([^:]+):", chat_history)

if not matches:
    print("❌ No sender found in chat history. Exiting.")
    exit()

last_sender = matches[-1].strip()
print(f"Last message from: {last_sender}")

# Only continue if last message is from Mummy Jio
if last_sender.lower() != "mummy jio":
    print("⚠️ Last message is not from Mummy Jio. No reply sent.")
    exit()

# ------------------------- Step 3: Prepare prompt -------------------------
prompt = f"""
You are Shaurya, a 15-year-old student who speaks Hindi and English fluently.
Respond casually and naturally to the last message from your mom ("Mummy Jio").
Do NOT include your name, timestamps, or any sender labels in your reply.
Only write what Shaurya would actually send in chat — short, natural, and human.

Chat History:
{chat_history}
"""

payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {"role": "system", "content": "You are Shaurya, replying to his mother in Hindi-English mix casually."},
        {"role": "user", "content": prompt}
    ],
    "temperature": 0.7
}

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# ------------------------- Step 4: Get AI Reply -------------------------
response = requests.post(API_URL, headers=headers, json=payload)

if response.status_code == 200:
    ai_reply = response.json()["choices"][0]["message"]["content"].strip()
    
    # Remove any possible name or timestamp if model still adds it
    ai_reply = re.sub(r"^.*?:\s*", "", ai_reply)
    ai_reply = re.sub(r"\[\d{1,2}:\d{2}.*?\]", "", ai_reply).strip()
    
    print("\nAI Reply:\n", ai_reply)
else:
    print("Error:", response.status_code, response.text)
    exit()

# ------------------------- Step 5: Auto Send Reply -------------------------
if ai_reply:
    # Copy reply to clipboard
    pyperclip.copy(ai_reply)
    time.sleep(0.3)

    # Click chatbox and paste
    pyautogui.click(616, 690)
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.3)

    # Press Enter
    pyautogui.press('enter')

    print("\n✅ Message sent successfully!")





