# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       azb99                                     		           #
#   Project:      White-Stripes                                                #
#   Description:  IQ2 project                 				           	   	   #
# ---------------------------------------------------------------------------- #

# Notes:
# LED color RED = ERROR
# LED color BLUE = SORT BY COLOR
# LED color PURPLE = SORT BY APRILTAG
# LED color GREEN = NORMAL OPERATION   
# LED flash Green = Entering Sorting Mode
# LED flash Blue = Exiting Sorting Mode
# When in sort by color LED will be the color of the object being handled 
# LED color Gray = LED color Black
# LED off = Transparent object detected or no object detected

# User-End Process
# 1. Initialize the sorting mode
# 2. Drive up to the box (main position)
# 3. Determine which group the object is in based on the selected charecteristic
# 4. Pick up the box and move it to the designated position of the box
# 5. If there is no box detected go to starting position and end program after 1 minute
# 6. Repeat steps 2-5 until step 5 is true

from vex import *

# Configure Robot
controller = Controller()
brain = Brain()
brain_inertial = Inertial()
left_drive_smart = Motor(Ports.PORT1, 1.0, False)
right_drive_smart = Motor(Ports.PORT6, 1.0, True)
drivetrain = SmartDrive(left_drive_smart, right_drive_smart, brain_inertial, 200)
arm = Motor(Ports.PORT10, True)
hand = Motor(Ports.PORT2, True)
distance_sensor = Distance(Ports.PORT7)
led = Touchled(Ports.PORT12)
optical_sensor = Optical(Ports.PORT5)
ai_vision = AiVision(Ports.PORT4, AiVision.ALL_TAGS)

