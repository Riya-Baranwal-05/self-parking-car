import numpy as np


class ParkingController:
    def __init__(self, car, lot):
        self.car = car
        self.lot = lot
        # target = center of parking space
        self.target_x = lot.space_x + 1/2*lot.space_width
        self.target_y = lot.space_y + 1/2*lot.space_height

        # arc1 exit — car center when rear-left corner 
        # touches obstacle top-left corner at 45°
        angle = np.radians(45)
        obstacle_corner_x = lot.space_x + lot.space_width  # top-left corner of right obstacle x
        obstacle_corner_y = lot.space_y + lot.space_height   # top-left corner of right obstacle y

        self.arc1_exit_x = obstacle_corner_x + (car.length/2)*np.cos(angle) + (car.width/2)*np.sin(angle)   # cx formula
        self.arc1_exit_y = obstacle_corner_y + (car.length/2)*np.sin(angle)  - (car.width/2)*np.cos(angle)   # cy formula

        # approach stops at arc1_exit_x
        self.maneuver_x = self.arc1_exit_x

        # straight reverse distance
        self.straight_distance = 0.8
        self.straight_target_x = None

        # steering
        self.arc1_steering = -car.max_steering   # right
        self.arc2_steering =  car.max_steering  # left

        # state machine
        self.state = "APPROACH"
        self.done  = False


    def compute_steering(self):
        car = self.car
        lot = self.lot

        if self.state == "APPROACH":
            if car.x < self.maneuver_x:
                return 1.0,0.0
            else:
                self.state = "ARC1"
                return 0.0,0.0
            
        elif self.state == "ARC1":
            if abs(np.degrees(car.heading)) < 45:
                return -0.8,-car.max_steering
            else: 
                self.state = "STRAIGHT_REVERSE"
                self.straight_target_x = car.x - 0.8 * np.cos(abs(car.heading))
                return 0.0,0.0
        elif self.state == "STRAIGHT_REVERSE":
            if car.x > self.straight_target_x:
                return -1.0, 0.0
            else:
                self.state = "ARC2"
                rear_y = car.y - (car.length/2)*np.sin(abs(car.heading))
                return 0.0, 0.0
        elif self.state =="ARC2":
            rear_y = car.y - (car.length/2)*np.sin(abs(car.heading))
            if np.degrees(abs(car.heading))> 1 and rear_y > lot.space_y +0.8:
                return -0.8,car.max_steering
            else:
                self.state = "STRAIGHTEN"
                return 0.0,0.0
            
        elif self.state =="STRAIGHTEN":
            if abs(car.x - self.target_x)>0.3:
               direction = -1.0 if car.x>self.target_x else 1.0
               return direction*0.5,0.0
            else:
                self.state = "DONE"
                self.done = True
                return 0.0,0.0
            
        else: 
            return 0.0,0.0

