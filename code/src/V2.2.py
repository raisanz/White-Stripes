# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       azb99                                     		           #
#   Project:      White-Stripes                                                #
#   Description:  box sorting project                 	              	   	   #
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

# Initialize Robot
sorting_mode = 1
GRAY = Color(84, 88, 90)
led.set_color(Color.GREEN)

# Function Definitions
# code for printing text to the brain screen
def brain_print(x) -> None:
    brain.screen.print(x)
# code for preping the screen before printing
def screen_prep(x = 1, clear = True) -> None:
    if clear:
        brain.screen.clear_screen()
    brain.screen.set_cursor(x, 1)
    brain.screen.set_font(FontType.MONO12)
# code for the button for changing sorting mode
def next_sort_mode() -> None:
    global sorting_mode
    sorting_mode += 1
    if sorting_mode > 2:
        sorting_mode = 1 
# code for choosing sorting mode
def sorting() -> None:
    brain.buttonLeft.pressed(next_sort_mode)
    controller.buttonFUp.pressed(next_sort_mode)

    while True:
        screen_prep()
        if sorting_mode == 1:
            brain_print("Sort by Color")
            led.set_color(Color.BLUE)
        elif sorting_mode == 2:
            brain_print("Sort by Apriltag")
            led.set_color(Color(85, 33, 207))
        '''elif sorting_mode == 3:
            brain_print("Sort by Size")
            led.set_color(Color.ORANGE)'''
        if brain.buttonCheck.pressing() or controller.buttonFDown.pressing():
            led.set_color(Color.GREEN)
            break
        
        wait(20, MSEC)

    screen_prep()
    brain_print("Sort mode: " + str(sorting_mode))
    wait(20, MSEC)
    screen_prep()
# box pick up code
def pick_up(open_hand = True) -> None:
    if open_hand:
        hand.spin_for(FORWARD, 60, DEGREES)
    drivetrain.drive_for(FORWARD, 4, INCHES)
    hand.spin_for(REVERSE, 40, DEGREES)
    # arm.spin_to_position(ARM_MAX, DEGREES, wait=False)
    arm.spin_for(FORWARD, 250, DEGREES)
    drivetrain.drive_for(REVERSE, 4, INCHES)
# box drop off code
def drop_off() -> None:
    drivetrain.drive_for(FORWARD, 4, INCHES)
    arm.spin_for(REVERSE, 250, DEGREES)
    hand.spin_for(FORWARD, 40, DEGREES, wait=False)
    drivetrain.drive_for(REVERSE, 4, INCHES)
    hand.spin_for(REVERSE, 60, DEGREES)
# code for sorting by color
def sort_by_color():
    brain.screen.clear_row(1)
    brain.screen.set_cursor(1, 1)
    brain.screen.set_font(FontType.MONO12)
    # brain_print(str(optical_sensor.color()) + " object detected") Does not work

    '''if optical_sensor.brightness() < 10:
        optical_sensor.set_light(LedStateType.ON)
        optical_sensor.set_light_power(100, PERCENT)
    '''
    optical_sensor.set_light(LedStateType.ON)
    optical_sensor.set_light_power(100, PERCENT)

    wait(500, MSEC)

    if distance_sensor.object_distance(INCHES) < 7:
        if optical_sensor.color() == Color.RED:
            brain_print("Red object detected")
            led.set_color(Color.RED)
            return "Red"
        elif optical_sensor.color() == Color.BLUE:
            brain_print("Blue object detected")
            led.set_color(Color.BLUE)
            return "Blue"
        elif optical_sensor.color() == Color.GREEN: # or optical_sensor.color() == Color.CYAN
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
        elif optical_sensor.color() == Color.CYAN:
            brain_print("Cyan object detected")
            led.set_color(Color.CYAN)
            return "Cyan"
    else:
        brain_print("No object detected")
        led.off()
        return None
# prints amount of each box sorted
def print_box_count(a, b, c, d = None, e = None, f = None) -> None:
    if sorting_mode == 1:
        screen_prep(2, False)
        brain_print("Red: " + str(a))
        screen_prep(3, False)
        brain_print("Blue: " + str(b))
        screen_prep(4, False)
        brain_print("Green: " + str(c))
    elif sorting_mode == 2:
        screen_prep(2, False)
        brain_print("Tag 0: " + str(a))
        screen_prep(3, False)
        brain_print("Tag 1: " + str(b))
        screen_prep(4, False)
        brain_print("Tag 2: " + str(c))
        screen_prep(5, False)
        brain_print("Tag 3: " + str(d))
        screen_prep(6, False)
        brain_print("Tag 4: " + str(e))
        screen_prep(7, False)
        brain_print("Tag 5: " + str(f))
# code for sorting by apriltag
def sort_by_apriltag():
    brain.screen.clear_row(1)
    brain.screen.set_cursor(1, 1)
    brain.screen.set_font(FontType.MONO12)
    wait(500, MSEC)
    apriltags = ai_vision.take_snapshot(AiVision.ALL_TAGS)

    if apriltags[0].exists:
        apriltag_id = apriltags[0].id
        brain_print("Apriltag with ID:" + str(apriltag_id))
        return apriltag_id
    else:
        brain_print("No apriltag detected")
        return None
# closes program
def end() -> None:
    brain.program_stop()
# lights that indicate the sorting mode has started
'''def sorting_indicator():
    global trigger

    for i in range(3):
        led.set_color(Color.GREEN)
        wait(200, MSEC)
        led.off()
        wait(200, MSEC)
    while True:   
        if trigger:
            trigger = False
            for i in range(3):
                led.set_color(Color.BLUE)
                wait(200, MSEC)
                led.off()
                wait(200, MSEC)
            break
        wait(20, MSEC)
'''
# main code file
def main() -> None:
    # for tracking num of boxes sorted by color
    red = 0
    blue = 0
    green = 0
    # for tracking num of boxes sorted by apriltag
    zero = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0

    controller.buttonEUp.pressed(end)

    led.set_fade(FadeType.OFF)
    for i in range(3):
        led.set_color(Color.GREEN)
        wait(200, MSEC)
        led.off()
        wait(200, MSEC)
    led.set_fade(FadeType.SLOW)

    wait(500, MSEC)
    sorting()
    drivetrain.drive_for(FORWARD, 18, INCHES)
    if sorting_mode == 1:
        red = 0
        blue = 0
        green = 0
        # new code
        print_box_count(red, green, blue)

        while True:
            arm.spin_for(FORWARD, 250, DEGREES)
            drivetrain.drive_for(FORWARD, 4, INCHES)
            color = sort_by_color()
            optical_sensor.set_light(LedStateType.OFF)
            drivetrain.drive_for(REVERSE, 4, INCHES)
            arm.spin_for(REVERSE, 250, DEGREES)
            if color != None and color == "Red" or color == "Blue" or color == "Green":
                pick_up()
                if color == "Red":
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drop_off()
                    red += 1
                    print_box_count(red, green, blue)
                    drivetrain.drive_for(REVERSE, 10, INCHES)
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                elif color == "Blue":
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drop_off()
                    green += 1
                    print_box_count(red, green, blue)
                    drivetrain.drive_for(REVERSE, 10, INCHES)
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                elif color == "Green":
                    drivetrain.drive_for(REVERSE, 15, INCHES)
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drop_off()
                    blue += 1
                    print_box_count(red, green, blue)
                    drivetrain.drive_for(REVERSE, 10, INCHES)
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 15, INCHES)
            else:
                drivetrain.drive_for(REVERSE, 18, INCHES)
                break
    elif sorting_mode == 2:
        print_box_count(zero, one, two, three, four, five)
        while True:
            hand.spin_for(FORWARD, 60, DEGREES)
            id = sort_by_apriltag()
            if id != None and id >= 0 and id <= 5:
                pick_up(False)
                if id == 0:
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    drop_off()
                    zero += 1
                    print_box_count(zero, one, two, three, four, five)
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                elif id == 1:
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                    drop_off()
                    one += 1
                    print_box_count(zero, one, two, three, four, five)
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                elif id == 2:
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drop_off()
                    two += 1
                    print_box_count(zero, one, two, three, four, five)
                    drivetrain.drive_for(REVERSE, 10, INCHES)
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                elif id == 3:
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drop_off()
                    three += 1
                    print_box_count(zero, one, two, three, four, five)
                    drivetrain.drive_for(REVERSE, 10, INCHES)
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                elif id == 4:
                    drivetrain.drive_for(REVERSE, 15, INCHES)
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drop_off()
                    four += 1
                    print_box_count(zero, one, two, three, four, five)
                    drivetrain.drive_for(REVERSE, 10, INCHES)
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 15, INCHES)
                elif id == 5:
                    drivetrain.drive_for(REVERSE, 15, INCHES)
                    drivetrain.turn_for(LEFT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 10, INCHES)
                    drop_off()
                    five += 1
                    print_box_count(zero, one, two, three, four, five)
                    drivetrain.drive_for(REVERSE, 10, INCHES)
                    drivetrain.turn_for(RIGHT, 90, DEGREES)
                    drivetrain.drive_for(FORWARD, 15, INCHES)
            else:
                hand.spin_for(REVERSE, 60, DEGREES)
                drivetrain.drive_for(REVERSE, 18, INCHES)
                break

    led.set_fade(FadeType.OFF)
    for i in range(3):
        led.set_color(Color.BLUE)
        wait(200, MSEC)
        led.off()
        wait(200, MSEC)
    led.set_fade(FadeType.SLOW)

    wait(60, SECONDS)
    led.set_color(Color.RED)
    end()
        

# Main Program
main()