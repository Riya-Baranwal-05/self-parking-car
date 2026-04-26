import numpy as np

class ParkingController:
    def __init__(self, car, lot):
        self.car = car
        self.lot = lot

        self.target_x = lot.space_x + lot.space_width / 2   # = 17.0
        self.target_y = lot.space_y + lot.space_height / 2  # = 9.0

        # approach: drive until rear-left corner aligns with 
        # top-left corner of right obstacle at exactly 45°
        angle = np.radians(45)
        obstacle_corner_x = lot.space_x + lot.space_width   # = 20.0
        obstacle_corner_y = lot.space_y + lot.space_height  # = 10.5

        # exact car center when rear-left corner = (20.0, 10.5) at 45°
        self.arc1_exit_x = obstacle_corner_x \
                         + (car.length/2)*np.cos(angle) \
                         + (car.width/2)*np.sin(angle)
        self.arc1_exit_y = obstacle_corner_y \
                         + (car.length/2)*np.sin(angle) \
                         - (car.width/2)*np.cos(angle)

        # approach stops when car reaches this x
        self.maneuver_x = self.arc1_exit_x

        # straight reverse: exactly 1.2m
        self.straight_distance = 0.8
        self.straight_target_x = None   # set when straight reverse starts

        # steering
        self.arc1_steering = -car.max_steering   # full right
        self.arc2_steering =  car.max_steering   # full left

        self.state = "APPROACH"
        self.done  = False

        print(f"Arc 1 exit target: x={self.arc1_exit_x:.3f}  y={self.arc1_exit_y:.3f}")
        print(f"Approach stops at: x={self.maneuver_x:.3f}")

    def compute_steering(self):
        car = self.car
        lot = self.lot

        # ── APPROACH: drive forward ────────────────────────────────
        if self.state == "APPROACH":
            if car.x < self.maneuver_x:
                return 1.0, 0.0
            else:
                self.state = "ARC1"
                print(f"APPROACH done — x={car.x:.3f} y={car.y:.3f}")
                print("Starting Arc 1 — reverse right")
                return 0.0, 0.0

        # ── ARC1: reverse right until 45° ─────────────────────────
        elif self.state == "ARC1":
            heading_deg = abs(np.degrees(car.heading))
            
            print(f"  ARC1: heading={heading_deg:.1f}° "
                f"x={car.x:.3f} y={car.y:.3f}")

            # exit when heading hits 45° — that's it
            # position is determined by physics, not us
            if heading_deg < 45:
                return -0.8, self.arc1_steering
            else:
                self.straight_target_x = car.x - self.straight_distance * np.cos(abs(car.heading))
                self.state = "STRAIGHT_REVERSE"
                print(f"Arc 1 done — heading={heading_deg:.1f}° "
                    f"x={car.x:.3f} y={car.y:.3f}")
                print(f"Reversing straight to x={self.straight_target_x:.3f}")
                return 0.0, 0.0

        # ── STRAIGHT REVERSE: reverse 1.2m straight ───────────────
        elif self.state == "STRAIGHT_REVERSE":
            # measure distance travelled since straight reverse started
            # use x as proxy — but account for diagonal movement
            # straight_target_x was set as car.x - 1.2*cos(heading)
            print(f"  STRAIGHT: x={car.x:.3f} "
                f"target={self.straight_target_x:.3f}")

            if car.x > self.straight_target_x:
                return -0.8, 0.0
            else:
                self.state = "ARC2"
                print(f"Straight done — x={car.x:.3f} y={car.y:.3f} "
                    f"heading={np.degrees(car.heading):.1f}°")
                return 0.0, 0.0

        # ── ARC2: reverse left until straight ─────────────────────
        elif self.state == "ARC2":
            rear_y = car.y - (car.length/2) * np.sin(abs(car.heading))
            print(f"  ARC2: heading={np.degrees(car.heading):.1f}° "
                  f"x={car.x:.3f} y={car.y:.3f} rear_y={rear_y:.3f}")

            if abs(car.heading) > np.radians(5) and rear_y > lot.curb_y + 0.8:
                return -0.8, self.arc2_steering
            else:
                self.state = "STRAIGHTEN"
                print(f"Arc 2 done — heading={np.degrees(car.heading):.1f}° "
                      f"x={car.x:.3f} y={car.y:.3f}")
                return 0.0, 0.0

        # ── STRAIGHTEN: nudge to center x ─────────────────────────
        elif self.state == "STRAIGHTEN":
            print(f"  STRAIGHTEN: x={car.x:.3f} target={self.target_x:.3f}")
            if abs(car.x - self.target_x) > 0.3:
                direction = 1.0 if car.x < self.target_x else -1.0
                return direction * 0.5, 0.0
            else:
                self.state = "DONE"
                self.done  = True
                print("Maneuver complete!")
                return 0.0, 0.0

        # ── DONE ──────────────────────────────────────────────────
        else:
            return 0.0, 0.0