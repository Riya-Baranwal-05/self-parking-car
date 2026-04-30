from env.car import Car
import numpy as np
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

for step in range(700):
    velocity, steering = ctrl.compute_steering()
    car.step(velocity,steering,dt=0.1)
    renderer.draw(car,lot,title=f"State: {ctrl.state}  |  step {step}")

    if lot.is_collision(car):
        print(f"Collision at step {step}!")
        break
    if ctrl.done:
        print(f"Final position: x={car.x:.2f} y={car.y:.2f}")
        print(f"Final heading: {np.degrees(car.heading):.1f}°")
        print(f"Successfully parked: {lot.is_parked(car)}")
        break

renderer.close()