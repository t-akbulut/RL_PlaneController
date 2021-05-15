import math
import pymap3d as pm

class Plane:
    lat          = 0     # deg
    lon          = 0     # deg
    alt          = 0     # msl
    vx           = 0     # m/s
    vy           = 0     # m/s
    vz           = 0     # m/s
    roll         = 0     # deg
    pitch        = 0     # deg
    yaw          = 0     # deg
    airspeed     = 0     # m/s
    groundspeed  = 0     # m/s
    throttle     = 0     # %

    #airfield
    airfield_lat          = -35.3633143     # deg
    airfield_lon          = 149.1652330     # deg
    airfield_alt          = 584.96     # msl
    airfield_heading      = 354     # deg

    def __init__(self):
        pass


    def update_attitude(self, Packet_Attitude):
        self.roll = Packet_Attitude.roll   * 180 / math.pi
        self.pith = Packet_Attitude.pitch  * 180 / math.pi
        self.yaw = Packet_Attitude.yaw     * 180 / math.pi

    def update_positon(self, Packet_GlobalPosition):
        self.lat = Packet_GlobalPosition.lat / 10e6
        self.lon = Packet_GlobalPosition.lon / 10e6
        self.alt = Packet_GlobalPosition.alt / 1000

        
        self.vx = Packet_GlobalPosition.vx / 100
        self.vy = Packet_GlobalPosition.vy / 100
        self.vz = Packet_GlobalPosition.vz / 100
    def update_speed(self, Packet_VfrHud):
        self.airspeed = Packet_VfrHud.airspeed
        self.groundspeed = Packet_VfrHud.groundspeed
        self.throttle = Packet_VfrHud.throtle

    def get_runway_relative_position(self):
        return pm.geodetic2enu(self.lat, self.lon, self.alt, 
                               self.airfield_lat, self.airfield_lon, self.airfield_alt)
    
