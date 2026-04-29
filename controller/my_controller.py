import numpy as np


class ParkingController:
    def __init__(self, car, lot):
        self.car = car
        self.lot = lot
        # target = center of parking space
        self.target_x = lot.space_x + 1/2*lot.space_width
        self.target_y = lot.space_y + 1/2*lot.space_height
        buffer_y = 0.6   # push car 0.6m lower

        

        # arc1 exit — car center when rear-left corner 
        # touches obstacle top-left corner at 45°
        angle = np.radians(45)
        obstacle_corner_x = lot.space_x + lot.space_width  # top-left corner of right obstacle x
        obstacle_corner_y = lot.space_y + lot.space_height   # top-left corner of right obstacle y

        self.arc1_exit_x = obstacle_corner_x + (car.length/2)*np.cos(angle) + (car.width/2)*np.sin(angle)   # cx formula
        self.arc1_exit_y = obstacle_corner_y + (car.length/2)*np.sin(angle)  - (car.width/2)*np.cos(angle) - buffer_y  # cy formula
        # compute exact straight distance needed to clear right obstacle  # wait, need actual position at arc1 end
        angle = np.radians(45)
        front_right_x = car.x + (car.length/2)*np.cos(abs(car.heading)) + (car.width/2)*np.sin(abs(car.heading))
        # approach stops at arc1_exit_x
        self.maneuver_x = self.arc1_exit_x

        # straight reverse distance
        self.straight_distance = 1.5
        self.straight_target_x = None

        # steering
        self.arc1_steering = -car.max_steering   # right
        self.arc2_steering =  car.max_steering  # left

        # state machine
        self.state = "APPROACH"
        self.done  = False
        print(f"arc1_exit_y with buffer: {self.arc1_exit_y:.3f}")

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
                heading_error = np.radians(45)-abs(car.heading)
                k = car.max_steering / np.radians(30)
                steering = np.clip(k * heading_error, 0, car.max_steering)

                return -0.8, self.arc1_steering
            else: 
                # calculate exact front-right corner position NOW (at 45°)
                front_right_x = car.x \
                    + (car.length/2)*np.cos(abs(car.heading)) \
                    + (car.width/2)*np.sin(abs(car.heading))
                
                # how far do we need to reverse to clear right obstacle?
                right_obstacle_x = lot.space_x + lot.space_width  # = 20.0
                clearance = front_right_x - right_obstacle_x + 0.3  # 0.3m safety buffer
                
                # convert clearance to x movement at current heading
                self.straight_target_x = car.x - clearance * np.cos(abs(car.heading))
                self.state = "STRAIGHT_REVERSE"
                print(f"Arc1 done — front_right_x={front_right_x:.3f}")
                print(f"Clearance needed={clearance:.3f}m")
                print(f"Straight target x={self.straight_target_x:.3f}")
                return 0.0,0.0
        elif self.state == "STRAIGHT_REVERSE":
            if car.x > self.straight_target_x:
                return -1.0, 0.0
            else:
                self.state = "ARC2"
                rear_y = car.y - (car.length/2)*np.sin(abs(car.heading))
                return 0.0, 0.0
        elif self.state == "ARC2":
            rear_y = car.y - (car.length/2)*np.sin(abs(car.heading))
            
            # rear-right corner (the one hitting left obstacle)
            rear_right_x = car.x \
                        - (car.length/2)*np.cos(abs(car.heading)) \
                        + (car.width/2)*np.sin(abs(car.heading))

            corner_safe = rear_right_x > lot.space_x + 0.5  # stay 0.3m from left obstacle

            print(f"  ARC2: heading={np.degrees(car.heading):.1f}° "
                f"rear_right_x={rear_right_x:.3f}")

            if abs(car.heading) > np.radians(1) \
            and rear_y > lot.curb_y + 0.8 \
            and corner_safe:
                k = car.max_steering / np.radians(30)
                steering = np.clip(k * abs(car.heading), 0, car.max_steering)
                return -0.8, self.arc2_steering
               
            else:
                self.nudge_target_x = car.x + 1.5  # pull forward 1.5m
                self.state = "FORWARD_NUDGE"
                print(f"Arc2 paused — pulling forward to finish straightening")
                return 0.0, 0.0
            
        # after ARC2 exits, before STRAIGHTEN
        elif self.state == "FORWARD_NUDGE":
            # pull forward 1.5m to create room
            if car.x < self.nudge_target_x:
                return 0.6, 0.0
            else:
                self.state = "ARC2_FINAL"
                return 0.0, 0.0

        elif self.state == "ARC2_FINAL":
            # finish straightening
            if abs(car.heading) > np.radians(1):
                return -0.5, self.arc2_steering
            else:
                self.state = "STRAIGHTEN"
                return 0.0, 0.0
            
        elif self.state == "STRAIGHTEN":
            if abs(car.x - self.target_x) > 0.3:
                x_error = abs(car.x - self.target_x)
                k = 0.25
                velocity = np.clip(k * x_error, 0.05, 0.5)
                direction = -1.0 if car.x > self.target_x else 1.0
                return direction * velocity, 0.0
            else:
                self.state = "DONE"
                self.done = True
                print("Maneuver complete!")
                return 0.0, 0.0
            
        else: 
            return 0.0,0.0

