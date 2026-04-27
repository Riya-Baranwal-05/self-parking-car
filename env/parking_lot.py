import numpy as np

class ParkingLot:
    def __init__(self):
        # parked cars blocking the space
        self.obstacles = [
            (10, 7.5, 4.0, 3.0),   # left obstacle  x=10 to 14
            (20, 7.5, 4.0, 3.0),   # right obstacle x=20 to 24
        ]

        # space is 1.5 × car length = 6.0m wide
        self.space_x      = 14.0   # start of space
        self.space_y      = 7.5    # bottom of space
        self.space_width  = 6.0    # 1.5 × 4.0m car length
        self.space_height = 3.0    # fits car width 1.8m with buffer

        self.curb_y = 7.0

    def get_parking_space(self):
        return(self.space_x,self.space_y,self.space_width,self.space_height)
    
    def is_parked(self,car):
        """ 
        Return True if the car is succesfully parked.
        Check 3 things:
        1. Car center is inside the parking space
        2. Car is heading roughly straight (aligned with space)
        3. Car is not touching the curb
        
        """
        #car center must be within space
        in_x = self.space_x < car.x < self.space_x + self.space_width
        in_y = self.space_y + car.width/2 < car.y < self.space_y + self.space_height - car.width/2 + 0.1

        # above curb
        above_curb = car.y - (car.width/2) > self.curb_y

        # heading straight
        heading_aligned = abs(car.heading) < np.radians(5)

        return in_x and in_y and above_curb and heading_aligned
    
    def is_collision(self,car):
        """
        Return True if the car has hit an obstacle or the curb
        """
        corners = car.get_corners()

        # check curb
        if np.any(corners[:,1]<self.curb_y):
            return True
        # check each obstacle 
        for (ox,oy,ow,oh) in self.obstacles:
            for (cx,cy) in corners:
                if ox < cx < ox+ow and oy < cy <oy +oh:
                    return True
                
        return False
    
    def distance_to_target(self,car):
        """
        How far is te car center from the ideal parking position?
        Useful as a reward signal later for neural network
        
        """

        target_x = self.space_x +self.space_width/2
        target_y = self.space_y +self.space_height/2
        return np.sqrt((car.x-target_x)**2 +(car.y-target_y)**2)