from pymavlink import mavutil
import time
from Plane import *
import threading
plane = Plane()
the_connection = mavutil.mavlink_connection('udpin:localhost:14550')





def handle_received_packet():
    while True:
        try:
            istenenpaketler = ["ATTITUDE","GLOBAL_POSITION_INT","VFR_HUD"]
            pakage = the_connection.recv_match(type=istenenpaketler)
            if pakage.name == "ATTITUDE":
                plane.update_attitude(pakage)
            if pakage.name == "GLOBAL_POSITION_INT":
                plane.update_positon(pakage)
            if pakage.name == "VFR_HUD":
                plane.update_speed(pakage)
                
        except:
            pass
        time.sleep(0.1)

def handle_logging():
    while True:
        print(plane.alt)
        time.sleep(1)


if __name__ == "__main__":
    the_connection.wait_heartbeat()
    print("Connection OK")
    thread_received_packet = threading.Thread(target=handle_received_packet)
    thread_received_packet.start()
    print("Packet Listening OK")
    thread_logging = threading.Thread(target=handle_logging)
    thread_logging.start()
    print("Logging OK")
