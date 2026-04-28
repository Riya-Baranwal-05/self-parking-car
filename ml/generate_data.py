import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import numpy as np
from env.car import Car
from env.parking_lot import ParkingLot
from controller.my_controller import ParkingController
import csv

all_data = []
for y_start in np.arange(10.5,15.0,0.1):
    car = Car(x=3,y=y_start,heading=0.0)
    lot = ParkingLot()
    ctrl = ParkingController(car,lot)

    car_target_x = lot.space_x + lot.space_width/2
    car_target_y = lot.space_y + lot.space_height/2
    car_target_heading = 0.0
    run_data = []
    for step in range(700):
        velocity, steering = ctrl.compute_steering()
        x_error = abs(car_target_x - car.x)
        y_error = abs(car_target_y - car.y)
        heading_error = abs(car_target_heading- car.heading)
        run_data.append([x_error,y_error,heading_error,velocity,steering])
        car.step(velocity,steering,dt=0.1)
        if lot.is_collision(car):
            break
        if lot.is_parked(car):
            break
        if ctrl.done:
            break

    parked = lot.is_parked(car)
    all_data.append((run_data,parked))

with open('ml/training_data.csv','w',newline='') as f:
    writer = csv.writer(f)
    #header row
    writer.writerow(['x_error','y_error','heading_error','velocity','steering','parked'])

    for run_data, parked in all_data:
        for step_data in run_data:
            writer.writerow(step_data + [parked])

