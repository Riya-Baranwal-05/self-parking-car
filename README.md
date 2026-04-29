# 🚗 Self-Parking Car Simulation

A 2D autonomous parallel parking simulation built from scratch in Python.
Implements a bicycle kinematic model and a geometric state machine controller.


## 📽️ Demo
*GIF coming soon*

Good — here's the updated README with all the math added. Replace your current README.md with this:

markdown
# 🚗 Self-Parking Car Simulation

A 2D autonomous parallel parking simulation built from scratch in Python.
Implements a bicycle kinematic model and a geometric state machine controller.

![Status](https://img.shields.io/badge/status-in%20progress-yellow)
![Python](https://img.shields.io/badge/python-3.11-blue)

## 📽️ Demo
*GIF coming soon — see assets/ folder for daily progress recordings*

## 🧠 How the Controller Works

Real parallel parking has exactly 7 steps. Our controller mirrors this precisely:

### Step 1 — APPROACH
Drive forward until the car's rear-left corner is perfectly aligned with the
top-left corner of the right obstacle. Position computed exactly from geometry.

### Step 2 — ARC 1
Reverse with full right steering until heading reaches 45°.

### Step 3 — STRAIGHT REVERSE
Reverse straight (wheels straight) until the front-right corner clears the
right obstacle. Distance calculated dynamically — not hardcoded.

### Step 4 — ARC 2
Reverse with full left steering until rear-right corner approaches left obstacle.
Monitored in real time using corner position formula.

### Step 5 — FORWARD NUDGE
Pull forward 1.5m to create room for final straightening. Mirrors real driving.

### Step 6 — ARC 2 FINAL
Small final reverse-left arc to bring heading to 0°.

### Step 7 — STRAIGHTEN
Nudge to center x of parking space.
APPROACH → ARC1 → STRAIGHT_REVERSE → ARC2
→ FORWARD_NUDGE → ARC2_FINAL → STRAIGHTEN → DONE


## 📐 The Math

### Bicycle Kinematic Model
x_new = x + v × cos(θ) × dt
y_new = y + v × sin(θ) × dt
θ_new = θ + (v / L) × tan(δ) × dt

v = velocity (negative = reversing)
θ = heading angle (radians)
L = wheelbase = 2.5m
δ = steering angle (max ±35°)


### Corner Position Formula
Any corner of the car at heading θ from center (cx, cy):
forward direction:      x += cos(θ),  y += sin(θ)
left perpendicular:     x -= sin(θ),  y += cos(θ)
right perpendicular:    x += sin(θ),  y -= cos(θ)

rear-left corner:
x = cx - (L/2)×cos(θ) - (W/2)×sin(θ)
y = cy - (L/2)×sin(θ) - (W/2)×cos(θ)

rear-right corner:
x = cx - (L/2)×cos(θ) + (W/2)×sin(θ)
y = cy - (L/2)×sin(θ) - (W/2)×cos(θ)


### Arc 1 Entry — Constraint-Based Positioning
We want rear-left corner = top-left corner of right obstacle at 45°.
Working backwards from corner to car center:
cx = obstacle_x + (L/2)×cos(45°) + (W/2)×sin(45°) = 22.051m
cy = obstacle_y + (L/2)×sin(45°) + (W/2)×cos(45°) = 12.550m


### Straight Reverse Distance — Dynamic Calculation
After Arc1, calculate exactly how far to reverse to clear right obstacle:
front_right_x = car.x + (L/2)×cos(θ) + (W/2)×sin(θ)
clearance = front_right_x - right_obstacle_x + 0.3m
straight_target_x = car.x - clearance × cos(θ)


### Arc 2 Safety — Rear-Right Corner Check
Stop Arc2 before rear-right corner hits left obstacle:
rear_right_x = car.x - (L/2)×cos(θ) + (W/2)×sin(θ)
stop when: rear_right_x < space_x + 0.3m


### Turning Radius
R = wheelbase / tan(steering_angle) = 2.5 / tan(35°) = 3.57m minimum

## 🧠 Neural Net — ExitAngleNet

The classical controller works from one fixed starting position (y=13).
The neural net extends this to any starting y.

**How it works:**
1. Search script finds the correct Arc1 exit angle for each starting y
2. Small MLP (1→16→16→1) trains on these (y_start, exit_angle) pairs
3. At test time: net predicts exit angle → controller uses it → parks!

**Architecture:**
input: y_start (1 number)
hidden: 16 → ReLU → 16 → ReLU
output: exit_angle_deg (1 number)

**Results:**
- Trains to loss < 0.0001 in 1000 epochs
- Generalizes to unseen starting positions
- y=12.6 (never seen) → predicted 38.5° → Successfully parked: True ✅

## 🗂️ File Structure

| File | What it does |
|------|-------------|
| `env/car.py` | Bicycle kinematic model |
| `env/parking_lot.py` | Parking space, obstacles, collision detection |
| `env/renderer.py` | Live matplotlib visualization |
| `controller/parking_controller.py` | Original geometric controller |
| `controller/my_controller.py` | Rewritten from scratch — full understanding |
| `test_car.py` | Main simulation runner |
| `ml/correction_net.py` | ExitAngleNet neural network architecture |
| `ml/find_exit_angles.py` | Search script to find working exit angles |
| `ml/train.py` | Training script |
| `ml/exit_angles.csv` | Training data |
| `ml/exit_angle_model.pt` | Trained model weights |

## 🚀 How to Run

```bash
pip install numpy matplotlib
python test_car.py
```

## 🔧 Built With
- Python 3.11
- NumPy
- Matplotlib

## 📚 What I Learned
- Bicycle kinematic model from first principles
- State machine controller design
- Constraint-based positioning
- Dynamic clearance calculation from corner geometry
- Real-time corner monitoring during maneuvers
- Real-world 7-step parallel parking algorithm
- Git workflow and daily commit habits

## 🚧 Status
- ✅ Bicycle kinematic model
- ✅ Parking lot with obstacles and collision detection
- ✅ Live renderer
- ✅ Classical geometric controller
- ✅ Rewritten controller from scratch (my_controller.py)
- ✅ Neural net — ExitAngleNet predicts arc1 exit angle from starting position
- ✅ Car parks successfully from unseen starting positions using neural net

---
*Built as part of a Shu Ha Ri robotics learning journey.*


