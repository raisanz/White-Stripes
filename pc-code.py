from dotenv import load_dotenv
import os
import serial
import time

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Confirm it loaded (starred for safety)
API_KEY_STARRED = "*" * len(API_KEY)
print("PC Proxy running. Loaded API key:", API_KEY_STARRED)

# Set current COM port for VEX IQ Brain
Current_COM = "COM8"

# Open serial connection to VEX IQ Brain
serial_port = serial.Serial(Current_COM, 115200, timeout=0.1)
time.sleep(2)  # Give serial time to initialize

def call_fake_api():
    # Replace this with the real API call later
    return "42"  # pretend the API returned "42"

buffer = ""

while True:
    raw = serial_port.read()  # read ONE byte

    if raw:
        # Convert raw byte safely
        if isinstance(raw, int):
            char = chr(raw)
        else:
            char = raw.decode()

        if char == "\n":
            line = buffer.strip()
            buffer = ""

            print("Robot sent:", line)

            if line == "GET_DATA":
                result = call_fake_api()
                serial_port.write((result + "\n").encode())
                print("Sent back:", result)

        else:
            buffer += char