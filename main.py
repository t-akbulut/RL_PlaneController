from utils import wrap_180
from pymavlink import mavutil
import time
from Plane import *
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from utils import *

import threading
#the_connection = mavutil.mavlink_connection('udpin:localhost:14550')
connection_string="udpin:localhost:14550";
vehicle = connect(connection_string, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

        
    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.commands
    vehicle.armed = True

    while not vehicle.armed:      
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)      
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: #Trigger just below target alt.
            print("Reached target altitude")
            break
        time.sleep(1)


def roll_cmd(roll):
    vehicle.channels.overrides['1'] = int(1500 + roll / 50 * 500)
def pitch_cmd(pitch):
    vehicle.channels.overrides['1'] = 1500 + pitch / 50* 500
def throttle_cmd(throttle):
    vehicle.channels.overrides['1'] = 1000 + throttle / 100* 500

def  navigation():
    vh= vehicle.heading
    ph = math.atan2(vehicle.location.local_frame.east*-1,vehicle.location.local_frame.north*-1) * 180 / math.pi
    heading_error = wrap_180(vh - ph)
   
    print(heading_error)
    roll_command = constrain(heading_error,-10,10)

    roll_cmd(roll_command*-1)
    

def handle_logging():
    yon = 1
    while True:
        
        #roll_cmd(yon * 10)
        navigation()
        time.sleep(1)

if __name__ == "__main__":
    #arm_and_takeoff(5)
    print("Packet Listening OK")
    thread_logging = threading.Thread(target=handle_logging)
    thread_logging.start()
    
    print("Logging OK")
