# 🚗 Self-Parking Car Simulation

A 2D autonomous parallel parking simulation built from scratch in Python.
Implements a bicycle kinematic model and a geometric state machine controller.


## 📽️ Demo
*GIF coming soon*

## 🧠 How the Controller Works

Real parallel parking has exactly 4 steps. Our controller mirrors this precisely:

### Step 1 — APPROACH
Drive forward until the car's rear-left corner is perfectly aligned with the 
top-left corner of the right obstacle car. This position is computed exactly 
using geometry — no guessing.

### Step 2 — ARC 1
Reverse with full right steering until heading reaches 45°. The car follows 
a circular arc determined by the bicycle kinematic model and wheelbase.

### Step 3 — STRAIGHT REVERSE
Reverse straight for exactly 0.8m with wheels straight (heading stays at 45°). 
This is the step most people skip — it creates room for Arc 2 to complete 
without hitting the right obstacle. Mirrors real-world parking step 3.

### Step 4 — ARC 2
Reverse with full left steering until heading returns to 0°. The car swings 
into the space. Stops early if rear gets too close to the curb.

### Step 5 — STRAIGHTEN
Nudge forward or backward to center the car in the space.

## 🧠 What's Inside

| File | What it does |
|------|-------------|
| `env/car.py` | Bicycle kinematic model |
| `env/parking_lot.py` | Parking space, obstacles, collision detection |
| `env/renderer.py` | Live matplotlib visualization |
| `controller/parking_controller.py` | 4-step geometric parking controller |
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


##  Built With
- Python 3.11
- NumPy
- Matplotlib


## 📚 What I Learned
- Bicycle kinematic model from first principles
- State machine controller design
- Constraint-based positioning (aligning car geometry with world coordinates)
- Geometric derivation of parallel parking arcs
- Collision detection using corner positions
- Real-world 4-step parallel parking algorithm


## 🚧 Status
- ✅ Bicycle kinematic model
- ✅ Parking lot with obstacles and collision detection  
- ✅ Live renderer
- ✅ Classical 4-step geometric controller — car parks successfully
- 🔜 Neural correction layer (next)

---
*Built as part of a Shu Ha Ri robotics learning journey.*