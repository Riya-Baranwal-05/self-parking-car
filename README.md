# 🚗 Self-Parking Car Simulation

A 2D autonomous parallel parking simulation built from scratch in Python.
Implements a bicycle kinematic model and a geometric state machine controller.


## 📽️ Demo
*GIF coming soon*

## 🧠 What's Inside

| File | What it does |
|------|-------------|
| `env/car.py` | Bicycle kinematic model — real car physics |
| `env/parking_lot.py` | Parking space, obstacles, collision detection |
| `env/renderer.py` | Live matplotlib visualization |
| `controller/parking_controller.py` | Geometric two-arc parking controller |
| `test_car.py` | Main simulation runner |

## 🚀 How to Run

```bash
pip install numpy matplotlib
python test_car.py
```

##  How it Works

The car uses a **bicycle kinematic model**:
- Position (x, y) and heading θ updated each timestep
- Steering angle clamped to physical limits (±35°)
- Turning radius derived from: `R = wheelbase / tan(steering_angle)`

The parking controller is a **state machine** with 4 stages:
1. `APPROACH` — drive forward past the space
2. `ARC1` — reverse with right steering (geometric arc)
3. `ARC2` — reverse with left steering (snap heading back)
4. `STRAIGHTEN` — nudge to center of space

##  Built With
- Python 3.11
- NumPy
- Matplotlib

##  What I Learned
- Bicycle kinematic model from first principles
- State machine controller design
- Geometric derivation of parallel parking arcs
- Collision detection in 2D simulation

##  Status
Classical geometric controller working.
Neural correction layer coming next.

---
*Built as part of a Shu Ha Ri robotics learning journey.*