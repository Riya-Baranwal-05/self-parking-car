from env.car import Car
import numpy as np
import time
from env.parking_lot import ParkingLot
from env.renderer import Renderer
import matplotlib.pyplot as plt
from controller.my_controller import ParkingController

#start the car alongside the road, before the space

car = Car(x=3,y=13,heading=0)
lot = ParkingLot()
renderer = Renderer(world_size=32)
ctrl = ParkingController(car,lot)


print("Starting Parking maneuver...")
print("Intial state:",car.get_state())
print(f"Target: ({ctrl.target_x:.1}, {ctrl.target_y:.1f})")

for step in range(700):
    velocity, steering = ctrl.compute_steering()
    car.step(velocity,steering,dt=0.1)
    renderer.draw(car,lot,title=f"State: {ctrl.state}  |  step {step}")
     # add this block
    if ctrl.state == "ARC2":
        rear_y = car.y - (car.length / 2) * np.sin(car.heading)
        print(f"step {step} | x={car.x:.2f} y={car.y:.2f} | "
              f"heading={np.degrees(car.heading):.1f}° | "
              f"rear_y={rear_y:.2f} | curb={lot.curb_y}")

    if lot.is_collision(car):
        print(f"💥 Collision at step {step}!")
        print(f"   car position: x={car.x:.2f} y={car.y:.2f}")
        print(f"   heading: {np.degrees(car.heading):.1f}°")
        rear_y = car.y - (car.length / 2) * np.sin(car.heading)
        print(f"   rear_y={rear_y:.2f}  curb_y={lot.curb_y}")
        corners = car.get_corners()
        print(f"corners: {corners}")
        for i, (ox, oy, ow, oh) in enumerate(lot.obstacles):
            for corner in corners:
                if ox < corner[0] < ox+ow and oy < corner[1] < oy+oh:
                    print(f"HITTING obstacle {i}: x={ox}-{ox+ow} y={oy}-{oy+oh}")
        if any(c[1] < lot.curb_y for c in corners):
            print(f"HITTING curb")

        break
    if ctrl.done:
        print(f"Final position: x={car.x:.2f} y={car.y:.2f}")
        print(f"Final heading: {np.degrees(car.heading):.1f}°")
        print(f"Final distance to target: {lot.distance_to_target(car):.2f}m")
        print(f"Successfully parked: {lot.is_parked(car)}")
        print(f"car top edge:   {car.y + car.width/2:.2f}")
        print(f"car bot edge:   {car.y - car.width/2:.2f}")
        print(f"space top:      {lot.space_y + lot.space_height:.2f}")
        print(f"space bottom:   {lot.space_y:.2f}")
        break

renderer.close()