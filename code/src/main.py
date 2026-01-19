# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       azb99                                                        #
# 	Created:      1/18/2026, 11:37:28 AM                                       #
# 	Description:  IQ2 project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Imports
from vex import *
import time

# Brain should be defined by default
brain=Brain()

# Robot configuration code
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT1, 1.0, False)
right_drive_smart = Motor(Ports.PORT6, 1.0, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 200, 173, 76, MM, 1)
arm = Motor(Ports.PORT10, True)
hand = Motor(Ports.PORT4, True)
distance_7 = Distance(Ports.PORT7)
LED = Touchled(Ports.PORT12)


# Main code

# Move Robot
drivetrain.drive_for(FORWARD, 800, MM)

# Give the PC time to connect
time.sleep(2)

buffer = ""

while True:
    # Send request
    brain.serial().write("GET_DATA\n")

    # Read one byte
    raw = brain.serial().read()

    if raw:
        # Convert raw data to a character safely
        if isinstance(raw, int):
            char = chr(raw)          # convert int → character
        else:
            char = raw.decode()      # convert bytes → string

        if char == "\n":
            decoded = buffer.strip()
            buffer = ""

            brain.screen.clear_screen()
            brain.screen.print("API says: " + decoded)
        else:
            buffer += char

    time.sleep(0.05)
