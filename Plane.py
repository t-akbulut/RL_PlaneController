import math
import pymap3d as pm
from utils import wrap_180
from pymavlink import mavutil
import time
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from utils import *
class Plane:

    _connection_string="udpin:localhost:14550";
    _vehicle = None

    def __init__(self):
        self._vehicle = connect(self._connection_string, wait_ready=True)


    def get_state(self):
        pitch = self._vehicle.attitude.pitch * 180 / math.pi
        vz = self._vehicle.velocity[2] * -1
        va = self._vehicle.airspeed
        d = math.sqrt(self._vehicle.location.local_frame.east**2 + self._vehicle.location.local_frame.north**2) 
        if self._vehicle.location.local_frame.north > 0:
            d *= -1
        h = self._vehicle.location.local_frame.down * -1
        #pitch,as,vz,d,h
        return [pitch,va,vz,d,h];

    def get_reward(self,state):
       
        #pitch reward
        r_p = abs(state[0]-0) * -1
        if(r_p>-8):
            r_p=0
        
        #airspeed reward
        r_va = abs(state[1]-22) * -1

        #vz reward
        r_vz=0
        if(state[4]< 10):
            r_vz = abs(state[2]+1)*3 * -1
        
        #glide slope reward
        slope_angle = state[4]/state[3]
        r_s = abs(slope_angle - 0.05) *5 * -1

        #live reward
        r_l = 0.5

        return r_p + r_va + r_vz + r_s + r_l

    def act(self,action):
        state = self.get_state()
        # action [throttle(0,100),roll(-100,100)]
        self._vehicle.channels.overrides['1'] = int(1500 + action[1] / 100 * 500)
        self._vehicle.channels.overrides['3'] = int(1000 + action[0] / 100 * 1000)
        time.sleep(0.1)
        new_state = self.get_state()
        reward = self.get_reward(new_state)
        return [state,action,new_state,reward]
        



    
    
