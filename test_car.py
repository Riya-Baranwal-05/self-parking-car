from env.car import Car
import numpy as np
import time
from env.parking_lot import ParkingLot
from env.renderer import Renderer
import matplotlib.pyplot as plt
from controller.parking_controller import ParkingController

#start the car alongside the road, before the space

car = Car(x=3,y=13,heading=0)
lot = ParkingLot()
renderer = Renderer(world_size=32)
ctrl = ParkingController(car,lot)


print("Starting Parking maneuver...")
print("Intial state:",car.get_state())
print(f"Target: ({ctrl.target_x:.1}, {ctrl.target_y:.1f})")

for step in range(300):
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
        break
    if ctrl.done:
        print(f"Final position: x={car.x:.2f} y={car.y:.2f}")
        print(f"Final heading: {np.degrees(car.heading):.1f}°")
        print(f"Final distance to target: {lot.distance_to_target(car):.2f}m")
        print(f"Successfully parked: {lot.is_parked(car)}")
        break

renderer.close()