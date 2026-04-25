import numpy as np

class ParkingLot:
    def __init__(self):
        #parked cars blocking the space (obstacles)
        #each is (x,y,width,height)
        self.obstacles = [
            (12,7.5,4.0,3.0), #car in front of space
            (21,7.5,4.0,3.0) #car behind space

        ]

        #target parking space
        self.space_x = 16.0
        self.space_y = 7.5
        self.space_width = 5.0
        self.space_height = 3.0

        #curb - bottom wall the car must not hit
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
        #1. center is inside
        in_x = self.space_x< car.x <self.space_x +self.space_width
        in_y = self.space_y<car.y < self.space_y + self.space_height

        #2. heading aligned - should be close to pi (pointing left)
        # or 0(point right).We allow ±15 degrees tolerance
        heading_aligned =(
            abs(car.heading)<np.radians(15) or
            abs(abs(car.heading)-np.pi) <np.radians(15)
        )
        #3. above the curb
        above_curb = car.y > self.curb_y

        return in_x and in_y and heading_aligned and above_curb
    
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