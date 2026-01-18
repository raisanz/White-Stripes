# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       azb99                                                        #
# 	Created:      1/18/2026, 11:37:28 AM                                       #
# 	Description:  IQ2 project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

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


# Python now drops into REPL
