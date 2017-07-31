prog_name = "AR.Drone Test"
version = 1

##############
### IMPORT ###
##############
import time, sys, os
import ARDroneLib, ARDroneGUI
from ARDroneLog import Log

###############
### GLOBALS ###
###############

gui = None
last_coord=(None,None)
all_coords = dict()


##################
# TEST FUNCTIONS #
##################

def choose_sequence(drone):
    "Choose a test program sequence"
    print "Please choose a test program you want to run:"
    print "1 - Command line test"
    print "2 - GUI Command Test"
    result = raw_input(">")
    if result == "1":
        menu_list(drone)
    elif result == "2":
        print "-> Launching GUI ..."
        command_GUI(drone)

# 1st Test: Command line
def menu_list(drone):
    "List of function you can perform"
    print "Choose your command:"
    print "0 - Emergency"
    print "1 - Hover"
    print "2 - Take Off"
    print "3 - Land"
    print "4 - Forward"
    print "5 - Backward"
    print "6 - Left"
    print "7 - Right"
    print "8 - Calibrate sensors"
    print "a - Reset"
    print "9 - Quit"
    result = ""
    while result != "9":
        result = raw_input(">")
        if result == "0": drone.emergency()
        if result == "1": drone.hover()
        if result == "2": drone.takeoff()
        if result == "3": drone.land()
        if result == "4": drone.forward()
        if result == "5": drone.backward()
        if result == "6": drone.left()
        if result == "7": drone.right()
        if result == "8": drone.calibrate()
        if result == "a": drone.reset()
        if result == "b": drone.set_config(activate_navdata=True)

# 2nd test
def command_GUI(drone):
    "Create a GUI to command the drone"
    global gui
    gui = ARDroneGUI.ControlWindow(default_action=drone.hover)
    # Add command
    gui.add_action("w",drone.forward)
    gui.add_action("s",drone.backward)
    gui.add_action("a",drone.left)
    gui.add_action("d",drone.right)
    gui.add_action("Up",drone.up)
    gui.add_action("Down",drone.down)
    gui.add_action("q",drone.rotate_left)
    gui.add_action("e",drone.rotate_right)
    gui.add_action("Return",drone.takeoff)
    gui.add_action("space",drone.land)
    gui.add_action("p",drone.emergency)
    gui.add_action("t",drone.reset)
    gui.add_action("y",drone.calibrate)
    #gui.add_action("e",lambda arg=drone: drone.animation("flip",("LEFT",)))
    #gui.add_action("j",lambda arg=drone: drone.set_config(record_video=True))
    #gui.add_action("k",lambda arg=drone: drone.set_config(record_video=False))
    # Add info
    gui.add_printable_data("Battery",("navdata_demo","battery_percentage"))
    # gui.add_printable_data("Number of tags",("vision_detect","nb_detected"))
    # gui.add_printable_data("X position",("vision_detect","xc"))
    # gui.add_printable_data("Y position",("vision_detect","yc"))
    # gui.add_printable_data("Width",("vision_detect","width"))
    # gui.add_printable_data("Height",("vision_detect","height"))
    # gui.add_printable_data("Distance",("vision_detect","distance"))
    # gui.add_printable_data("State (!=0)",("navdata_demo","ctrl_state"))
    gui.add_printable_data("Theta",("navdata_demo","theta"))
    gui.add_printable_data("Phi",("navdata_demo","phi"))
    gui.add_printable_data("Psi",("navdata_demo","psi"))
    gui.add_printable_data("Altitude",("navdata_demo","altitude"))
    gui.add_printable_data("x",("navdata_demo","vx"))
    gui.add_printable_data("y",("navdata_demo","vy"))
    gui.add_printable_data("z",("navdata_demo","vz"))
    gui.add_printable_data("latitude",("gps_info","latitude"))
    gui.add_printable_data("longitude",("gps_info","longitude"))
    gui.add_printable_data("elevation",("gps_info","elevation"))
    gui.add_printable_data("hdop",("gps_info","hdop"))
    gui.add_printable_data("data_available",("gps_info","data_available"))
    gui.add_printable_data("zero_validated",("gps_info","zero_validated"))
    gui.add_printable_data("wpt_validated",("gps_info","wpt_validated"))

    drone.set_callback(gui.callback) # Enable the GUI to receive data from the drone
    drone.set_config(activate_navdata=True,detect_tag=1)
    gui.start()


if __name__ == "__main__":
    global drone
    print "> Welcome to " + str(prog_name) + " (r" + str(version) + ")"
    print "> Loading program ..."
    # Create the drone
    try:
        drone = ARDroneLib.Drone("192.168.1.2")
    except IOError:
        wait = raw_input("-> Cannot connect to drone !\n-> Press return to quit...")
        sys.exit()
    try:
        choose_sequence(drone)
    except KeyboardInterrupt:
        drone.stop()
    except:
        drone.stop()
        raise
    else:
        drone.stop()
    print "Test done"