import sys
sys.path.append('.')
import torch
import numpy as np
from env.car import Car
from env.parking_lot import ParkingLot
from env.renderer import Renderer
from controller.my_controller import ParkingController
from ml.correction_net import ExitAngleNet

# load neural net
checkpoint = torch.load('ml/exit_angle_model.pt')
model = ExitAngleNet()
model.load_state_dict(checkpoint['model'])
model.eval()

X_mean, X_std = checkpoint['X_mean'], checkpoint['X_std']
y_mean, y_std = checkpoint['y_mean'], checkpoint['y_std']

# predict exit angle for unseen y=12.6
y_start = 12.6
x = torch.tensor([[y_start]])
x_norm = (x - X_mean) / X_std
with torch.no_grad():
    pred_angle = (model(x_norm) * y_std + y_mean).item()

print(f"Neural net predicts: {pred_angle:.1f}° for y={y_start}")

# run simulation
car = Car(x=3, y=y_start, heading=0.0)
lot = ParkingLot()
renderer = Renderer(world_size=32)
ctrl = ParkingController(car, lot, exit_angle_deg=pred_angle)

print("Starting neural net guided parking...")

for step in range(700):
    velocity, steering = ctrl.compute_steering()
    car.step(velocity, steering, dt=0.1)
    renderer.draw(car, lot, title=f"Neural Net | y_start={y_start} | State: {ctrl.state}")

    if lot.is_collision(car):
        print(f"💥 Collision!")
        break

    if ctrl.done:
        print(f"Final position: x={car.x:.2f}  y={car.y:.2f}")
        print(f"Final heading:  {np.degrees(car.heading):.1f}°")
        print(f"Successfully parked: {lot.is_parked(car)}")
        break

renderer.close()