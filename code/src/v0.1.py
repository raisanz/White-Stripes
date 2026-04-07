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
# LED color ORANGE = SORT BY SIZE
# LED color PURPLE = SORT BY APRILTAG
# LED color GREEN = NORMAL OPERATION   
# LED flash Green = Entering Sorting Mode
# LED flash Red = Exiting Sorting Mode
# When in sort by color LED will be the color of the object being handled 
# LED color Gray = LED color Black
# LED off = Transparent object detected or no object detected


from vex import *

# Configure Robot
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

# Initialize Robot
sorting_mode = 1
# arm and hand travel limits (degrees). ARM_MIN should be the lowered/down position,
# ARM_MAX the raised/up position. negative values can prevent movement, so keep
# the lower bound at 0 unless the mechanism really needs to go below its zero
# point. adjust the constants if your gearbox has different stops.
ARM_MIN = 0
ARM_MAX = 900
HAND_OPEN = 0
HAND_CLOSE = 3.75
GRAY = Color(84, 88, 90)

led.set_color(Color.GREEN)

mapped = False
arm.set_position(ARM_MIN, DEGREES)
hand.set_position(HAND_CLOSE, DEGREES)

# Function Definitions
def brain_print(x):
    brain.screen.print(x)
def screen_prep(x = 1, clear = True):
    if clear:
        brain.screen.clear_screen()
    brain.screen.set_cursor(x, 1)
    brain.screen.set_font(FontType.MONO12)
def next_sort_mode():
    global sorting_mode
    sorting_mode += 1
    if sorting_mode > 3:
        sorting_mode = 1 
def sorting():
    brain.buttonLeft.pressed(next_sort_mode)

    while True:
        screen_prep()
        if sorting_mode == 1:
            brain_print("Sort by Color")
            led.set_color(Color.BLUE)
        elif sorting_mode == 2:
            brain_print("Sort by Size")
            led.set_color(Color.ORANGE)
        elif sorting_mode == 3:
            brain_print("Sort by Apriltag")
            led.set_color(Color(85, 33, 207))
        if brain.buttonCheck.pressing():
            led.set_color(Color.GREEN)
            break
        
        wait(20, MSEC)

    screen_prep()
    brain_print("Sort mode: " + str(sorting_mode))
    wait(20, MSEC)
    screen_prep()
def pick_up():
    hand.spin_for(FORWARD, 60, DEGREES)
    drivetrain.drive_for(FORWARD, 4, INCHES)
    hand.spin_for(REVERSE, 40, DEGREES)
    # arm.spin_to_position(ARM_MAX, DEGREES, wait=False)
    arm.spin_for(FORWARD, 250, DEGREES)
    drivetrain.drive_for(REVERSE, 4, INCHES)
def drop_off():
    drivetrain.drive_for(FORWARD, 4, INCHES)
    arm.spin_for(REVERSE, 250, DEGREES)
    hand.spin_for(FORWARD, 40, DEGREES, wait=False)
    drivetrain.drive_for(REVERSE, 4, INCHES)
    hand.spin_for(REVERSE, 60, DEGREES)
def sort_by_color():
    brain.screen.clear_row(1)
    brain.screen.set_cursor(1, 1)
    brain.screen.set_font(FontType.MONO12)
    # brain_print(str(optical_sensor.color()) + " object detected") Does not work

    if optical_sensor.brightness() < 10:
        optical_sensor.set_light(LedStateType.ON)
        optical_sensor.set_light_power(100, PERCENT)

    wait(500, MSEC)

    if distance_sensor.object_distance(INCHES) < 7:
        if optical_sensor.color() == Color.RED:
            brain_print("Red object detected")
            led.set_color(Color.RED)
            return "Red"
        elif optical_sensor.color() == Color.BLUE or optical_sensor.color() == Color.CYAN:
            brain_print("Blue object detected")
            led.set_color(Color.BLUE)
            return "Blue"
        elif optical_sensor.color() == Color.GREEN:
            brain_print("Green object detected")
            led.set_color(Color.GREEN)
            return "Green"
        elif optical_sensor.color() == Color.YELLOW:
            brain_print("Yellow object detected")
            led.set_color(Color.YELLOW)
            return "Yellow"
        elif optical_sensor.color() == Color.WHITE:
            brain_print("White object detected")
            led.set_color(Color.WHITE)
            return "White"
        elif optical_sensor.color() == Color.BLACK:
            brain_print("Black object detected")
            led.set_color(GRAY)
            return "Black"
        elif optical_sensor.color() == Color.PURPLE:
            brain_print("Purple object detected")
            led.set_color(Color.PURPLE)
            return "Purple"
        elif optical_sensor.color() == Color.ORANGE:
            brain_print("Orange object detected")
            led.set_color(Color.ORANGE)
            return "Orange"
        elif optical_sensor.color() == Color.TRANSPARENT:
            brain_print("Transparent object detected")
            led.off()
            return "Transparent"
    else:
        brain_print("No object detected")
        led.off()
        return None
def item_count_color(color, r = 0, g = 0, b = 0):
    if color != None: 
        if color == "Red":
            r += 1
            return r
        elif color == "Blue":
            b += 1
            return b
        elif color == "Green":
            g += 1
            return g
def print_color_count(r, g, b):
    screen_prep(2, False)
    brain_print("Red: " + str(r))
    screen_prep(3, False)
    brain_print("Blue: " + str(b))
    screen_prep(4, False)
    brain_print("Green: " + str(g))
# Not doing sort by size anymore
def sort_by_apriltag():
    screen_prep()
    apriltags = ai_vision.take_snapshot(AiVision.ALL_TAGS)

    if apriltags[0].exists:
        apriltag_id = apriltags[0].id
        brain_print("Apriltag with ID:" + str(apriltag_id))
def end():
    brain.program_stop()

# Initialize robot pose; use the named constants so that changing the
# limits isn't forgotten.
#arm.set_position(ARM_MIN, DEGREES)
#hand.set_position(HAND_CLOSE, DEGREES)

# Main Program

# Home program
for i in range(3):
    led.set_color(Color.GREEN)
    wait(200, MSEC)
    led.off()
    wait(200, MSEC)


sorting()
if sorting_mode == 1:
    red = 0
    blue = 0
    green = 0
    # new code
    print_color_count(red, green, blue)
    
    drivetrain.drive_for(FORWARD, 18, INCHES)
    while True:
        arm.spin_for(FORWARD, 250, DEGREES)
        color = sort_by_color()
        optical_sensor.set_light(LedStateType.OFF)
        if color != None and color == "Red" or color == "Blue" or color == "Green":
            arm.spin_for(REVERSE, 250, DEGREES)
            pick_up()
        else:
            arm.spin_for(REVERSE, 250, DEGREES)
        
        if color == "Red":
            drivetrain.turn_for(RIGHT, 90, DEGREES)
            drivetrain.drive_for(FORWARD, 10, INCHES)
            drop_off()
            red = item_count_color(color, red, green, blue)
            print_color_count(red, green, blue)
            drivetrain.drive_for(REVERSE, 10, INCHES)
            drivetrain.turn_for(LEFT, 90, DEGREES)
        elif color == "Blue":
            drivetrain.turn_for(LEFT, 90, DEGREES)
            drivetrain.drive_for(FORWARD, 10, INCHES)
            drop_off()
            blue = item_count_color(color, red, green, blue)
            print_color_count(red, green, blue)
            drivetrain.drive_for(REVERSE, 10, INCHES)
            drivetrain.turn_for(RIGHT, 90, DEGREES)
        elif color == "Green":
            drivetrain.drive_for(REVERSE, 15, INCHES)
            drivetrain.turn_for(RIGHT, 90, DEGREES)
            drivetrain.drive_for(FORWARD, 10, INCHES)
            drop_off()
            green = item_count_color(color, red, green, blue)
            print_color_count(red, green, blue)
            drivetrain.drive_for(REVERSE, 10, INCHES)
            drivetrain.turn_for(LEFT, 90, DEGREES)
            drivetrain.drive_for(FORWARD, 15, INCHES)
        else:
            drivetrain.drive_for(REVERSE, 18, INCHES)
            break
else:
    pass

for i in range(3):
    led.set_color(Color.BLUE)
    wait(200, MSEC)
    led.off()
    wait(200, MSEC)
# end()
