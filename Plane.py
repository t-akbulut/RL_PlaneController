import math
import pymap3d as pm
from utils import wrap_180
from pymavlink import mavutil
import time
from dronekit import connect, VehicleMode, LocationGlobal, LocationGlobalRelative
from utils import *
import numpy as np
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
        #pitch,as,vz,h
        state = [pitch,va,vz,h]
        state = np.reshape(state, [1, np.shape(state)[0]])
        return state

    def get_touch(self):
        h = self._vehicle.location.local_frame.down * -1;
        if h < 1:
            return True
        return False
    def get_reward(self,state):
       
        #pitch reward
        [pitch,va,vz,h] = state[0]

        r_p = abs(pitch+8) * -1 
        if(pitch>0):
            r_p=-7
        
        #airspeed reward
        r_va = 0
        if va<20:
            r_va = -5
            
        #vz reward
        r_vz=0
        if vz>0:
            r_vz = -50
        elif h<40:
            r_vz = vz

        if(h<5):
            r_vz += vz*10
        #glide slope reward
       

        #live reward
        r_l = - 0.5

        return r_l+ r_va + r_vz

    def act(self,action):
        state = self.get_state()
        [pitch,va,vz,h] = state[0]
        # action [0:pitch_down,1:pitch_up]
        if(action==0):
            self._vehicle.channels.overrides['2'] = int(1700)
        elif action==1:
            self._vehicle.channels.overrides['2'] = int(1500)
        elif action==2:
            self._vehicle.channels.overrides['2'] = int(1200)

        if h >10:
            self._vehicle.channels.overrides['3'] = int(1300)

        time.sleep(0.5)
        new_state = self.get_state()
        reward = self.get_reward(new_state)
        return [state,action,new_state,reward]
        
    def get_flight_mode(self):
        return self._vehicle.mode.name


    
    
