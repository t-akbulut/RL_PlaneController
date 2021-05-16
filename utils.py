def constrain(value, min,max):
    if(value<min):
        return min
    elif(value>max):
        return max
    else:
        return value

def wrap_180(angle):
    angle = angle % 360
    if(angle>180):
        angle = angle-360
    return angle
