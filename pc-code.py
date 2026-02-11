from google import genai
from dotenv import load_dotenv
import os
import serial
import time

# -----------------------------
# 1. Gemini setup
# -----------------------------
load_dotenv()
API_KEY = os.getenv("API_KEY")

client = genai.Client(api_key=API_KEY)
MODEL = "gemini-2.5-flash"

# -----------------------------
# 2. Serial setup (controller ↔ PC)
# -----------------------------
SERIAL_PORT = "COM11"   # change to your controller's COM port
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

print("PC proxy running. AI will command robot to move 1 meter.")

# -----------------------------
# 3. Main loop
# -----------------------------
while True:
    try:
        if ser.in_waiting > 0:
            robot_msg = ser.readline().decode(errors="ignore").strip()
            if not robot_msg:
                continue

            print(f"[Robot → PC] {robot_msg}")

            # -----------------------------
            # 4. Ask Gemini what to do
            # -----------------------------
            prompt = """
You are controlling a robot.  
Always respond ONLY with a command in this exact format:

FORWARD 1000

This means: move forward 1000 millimeters (1 meter).
Do not add extra words. Do not explain. Only output the command.
"""

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            ai_reply = (response.text or "").strip()
            print(f"[AI → PC] {ai_reply}")

            # -----------------------------
            # 5. Send command back to robot
            # -----------------------------
            ser.write((ai_reply + "\n").encode())

    except KeyboardInterrupt:
        print("Exiting PC proxy.")
        break
    except Exception as e:
        print(f"[ERROR] {e}")
        try:
            ser.write(b"AI_ERROR\n")
        except:
            pass
        time.sleep(1)

ser.close()