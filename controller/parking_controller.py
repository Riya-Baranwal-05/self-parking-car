import numpy as np
from env.car import Car
from env.parking_lot import ParkingLot

class ParkingController:
    def __init__(self,car,lot):
        self.car = car
        self.lot = lot
        # where we want to end up
        self.target_x = lot.space_x + lot.space_width  / 2
        self.target_y = lot.space_y + lot.space_height / 2

        # start maneuver just past the space
        self.maneuver_x = lot.space_x + lot.space_width + 2.0

        # will be computed at maneuver start
        self.arc1_steering = None
        self.arc2_steering = None

        self.state = "APPROACH"
        self.done  = False


    def compute_arc_steering(self):
        
        car = self.car
        lot = self.lot

        #how far the car needs to drop in y to enter the space
        #arc 1 takes car halfway down , arc 2 finishes it
        total_drop = car.y - self.target_y
        half_drop = total_drop/2

        #horizontal travel during one arc(roughly)
        #car moves backward, so delta_x is negative

        delta_x = 4.0

        #turning radius from circle geometry
        #R = (dy² + dx²) / (2 * dy)
        R = (half_drop**2 + delta_x**2)/(2*half_drop)

        # clamp R to realistic car limits
        # our wheelbase is 2.5m, max steering 35° → min R = 2.5/tan(35°) = 3.57m
        min_R = car.wheelbase / np.tan(car.max_steering)
        R = max(R, min_R + 1.0)  # add 1m buffer above minimum

        #steering angle from wheelbase and radius
        #steering = arctan(L/R)
        steering = np.arctan(car.wheelbase/R)

        print(f"Computed geometry:")
        print(f"total y drop needed: {total_drop:.2f}m")
        print(f"turning radius R : {R:.2f}m")
        print(f" steering angle  :{np.degrees(steering):.1f}°")

        #Arc 1 steers one way , Arc2 the opposite
        self.arc1_steering= -steering #right (into space)
        self.arc2_steering= steering # left (straighten)

        # store arc 1 exit y at the moment maneuver begins
        # car should have dropped 60% of total_drop before switching
        self.arc1_exit_y_stored = car.y - (total_drop * 0.6)
        print(f"  Arc 1 will exit at y : {self.arc1_exit_y_stored:.2f}")

    def compute_steering(self):
        """
        State machine-returns(velocity, steering_angle) for current step.
        States: Approach -> Align -> ARC1 -> ARC2 ->Straighten ->Done
        
        """
        car = self.car
        lot = self.lot

        #--Approach:drive forward alongside the space -----------
        if self.state == "APPROACH":
            if car.x<self.maneuver_x:
                return 1.0,0.0 #drive straight forward
            else: 
                self.compute_arc_steering()
                self.state ="ARC1"
                print("Starting Arc 1 - reverse right")
                return 0.0 ,0.0
        
        #--Arc 1: reverse with right steering-----------
        elif self.state =="ARC1":
            # exit when car has dropped halfway to target y
            # exit when car has dropped 60% of the way to target y
            # leave 40% for Arc 2 to finish with
            arc1_exit_y = self.target_y + (car.y - self.target_y) * 0.4
            # but we need to store the INITIAL y, not current car.y
            if car.y > self.arc1_exit_y_stored:
                return -0.8, self.arc1_steering
            else:
                self.state ="ARC2"
                print("Starting Arc 2- reverse left")
                return 0.0,0.0
            
        #--Arc 2: reverse with left steering--------------
        elif self.state == "ARC2":
            if abs(car.heading) > np.radians(5):
                return -0.5, self.arc2_steering
            else:
                self.state = "STRAIGHTEN"
                print(f"Arc 2 done — heading={np.degrees(car.heading):.1f}° y={car.y:.2f}")
                return 0.0, 0.0
            
        #--STRAIGHTEN:nudge forward to center in space-------------
        elif self.state == "STRAIGHTEN": 
            if abs(car.x-self.target_x)>0.3:
                #move forward or backward to center
                direction = 1.0 if car.x <self.target_x else -1.0
                return direction*0.5,0.0
            else:
                self.state = "Done"
                self.done = True
                print("Maneuver complete!")
                return 0.0,0.0
            

        #--Done-----------------------------------------------------
        else:
            return 0.0,0.0
            