import numpy as np

class Car:
    def __init__(self, x=0.0, y= 0.0, heading =0.0):
        #position and orientation
        self.x = x
        self.y = y
        self.heading = heading #angle in radians

        #physical constants
        self.wheelbase = 2.5 #distance between front and rear axle (meters)
        self.max_steering = np.radians(35) #max steering angle
        self.length = 4.0 # total car length for collision drawing
        self.width = 1.8 # total car width

    def step(self, velocity, steering_angle,dt=0.1):
        """ 
        Move the car one timestamp.
        velocity      : speed in m/s (negative = reversing)
        steering_angle: in radians, clamped to max_steering
        dt            : timestep in seconds
        """

        #clamp steering to physical limits
        steering_angle = np.clip(steering_angle,-self.max_steering,self.max_steering)
        #bicycle kinematic model
        self.x +=velocity*np.cos(self.heading)*dt
        self.y +=velocity*np.sin(self.heading)*dt
        self.heading +=(velocity/self.wheelbase)*np.tan(steering_angle)*dt

        #keep heading in [-pi,pi]
        self.heading = (self.heading + np.pi)%(2*np.pi) - np.pi

    def get_corners(self):
        """Returns the 4 corner positions of the car for drawing"""
        cx,cy,h = self.x,self.y,self.heading
        hw,hl= self.width/2,self.length/2
        corners = np.array([[hl,hw],[hl,-hw],[-hl,-hw],[-hl,hw]])

        cos_h,sin_h = np.cos(h),np.sin(h)
        rotation = np.array([[cos_h,-sin_h],[sin_h,cos_h]])
        rotated = (rotation@corners.T).T
        return rotated + np.array([cx,cy])
    
    def get_state(self):
        return np.array([self.x,self.y,self.heading])
    
    def reset(self,x=0.0,y=0.0,heading=0.0):
        self.x,self.y,self.heading=x,y,heading