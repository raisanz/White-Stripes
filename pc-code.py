from dotenv import load_dotenv
import os
import serial
import time

# Load API key from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Confirm it loaded
starred_list = ['*' for char in API_KEY]
API_KEY_STARRED = "".join(starred_list)
print("PC Proxy running. Loaded API key:", API_KEY_STARRED)

# Set current COM port for VEX IQ Brain
Current_COM = "COM8"

# Open serial connection to VEX IQ Brain
# Change COM3 to whatever your Brain uses
serial_port = serial.Serial(Current_COM, 115200, timeout=1)
time.sleep(2)  # Give serial time to initialize

def call_fake_api():
    # Replace this with the real API call later
    return "42"  # pretend the API returned "42"

while True:
    line = serial_port.readline().decode().strip()

    if line:
        print("Robot sent:", line)

    if line == "GET_DATA":
        result = call_fake_api()
        serial_port.write((result + "\n").encode())
        print("Sent back:", result)