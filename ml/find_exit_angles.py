import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import csv
from env.car import Car
from env.parking_lot import ParkingLot
from controller.my_controller import ParkingController

results = []

for y_start in np.arange(10.5, 15.5, 0.25):
    for exit_angle in np.arange(10, 61, 0.5):
        car = Car(x=3, y=y_start, heading=0.0)
        lot = ParkingLot()
        ctrl = ParkingController(car, lot, exit_angle_deg=exit_angle)

        for _ in range(700):
            v, s = ctrl.compute_steering()
            car.step(v, s, dt=0.1)
            if lot.is_collision(car) or ctrl.done:
                break

        if lot.is_parked(car):
            results.append([y_start, exit_angle])
            print(f"y={y_start:.1f} → exit_angle={exit_angle}° ✅")
            break  # found gentlest working angle, move to next y
    else:
        print(f"y={y_start:.1f} → no working angle found ❌")

# save results
with open('ml/exit_angles.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['y_start', 'exit_angle_deg'])
    writer.writerows(results)

print(f"\nSaved {len(results)} entries to ml/exit_angles.csv")