# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       azb99                                                        #
#   Description:  IQ2 project with AI command (one-time move)                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *
import time

brain = Brain()

# Robot configuration
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT1, 1.0, False)
right_drive_smart = Motor(Ports.PORT6, 1.0, True)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 200, 173, 76, MM, 1)
arm = Motor(Ports.PORT10, True)
hand = Motor(Ports.PORT4, True)
distance_7 = Distance(Ports.PORT7)
LED = Touchled(Ports.PORT12)

# ------------------------------------------------------------
# Only move once
# ------------------------------------------------------------
already_moved = False
buffer = ""

# Give PC time to connect
time.sleep(2)

brain.screen.print("Waiting for AI...")

while True:
    # Ask PC for a command
    brain.serial().write("READY\n")

    # Read one byte
    raw = brain.serial().read()

    if raw:
        # Convert raw data to a character safely
        if isinstance(raw, int):
            char = chr(raw)
        else:
            char = raw.decode()

        if char == "\n":
            command = buffer.strip()
            buffer = ""

            if command:
                brain.screen.clear_screen()
                brain.screen.print("AI says: " + command)

                # Only execute the AI command once
                if not already_moved:
                    parts = command.split()

                    if len(parts) == 2 and parts[0].upper() == "FORWARD":
                        distance = int(parts[1])
                        drivetrain.drive_for(FORWARD, distance, MM)
                        already_moved = True
                        brain.screen.print("Done.")
                    else:
                        brain.screen.print("Invalid cmd")

                else:
                    brain.screen.print("Ignored (already moved)")

        else:
            buffer += char

    time.sleep(0.05)