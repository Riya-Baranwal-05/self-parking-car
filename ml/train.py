import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from ml.correction_net import ExitAngleNet

# load data
df = pd.read_csv('ml/exit_angles.csv')
X = torch.tensor(df['y_start'].values, dtype=torch.float32).unsqueeze(1)
y = torch.tensor(df['exit_angle_deg'].values, dtype=torch.float32).unsqueeze(1)

# normalize inputs and outputs
X_mean, X_std = X.mean(), X.std()
y_mean, y_std = y.mean(), y.std()
X_norm = (X - X_mean) / X_std
y_norm = (y - y_mean) / y_std

# model, loss, optimizer
model = ExitAngleNet()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# train
for epoch in range(1000):
    optimizer.zero_grad()
    pred = model(X_norm)
    loss = criterion(pred, y_norm)
    loss.backward()
    optimizer.step()

    if epoch % 100 == 0:
        print(f"Epoch {epoch} loss: {loss.item():.6f}")

# save model and normalization params
torch.save({
    'model': model.state_dict(),
    'X_mean': X_mean,
    'X_std': X_std,
    'y_mean': y_mean,
    'y_std': y_std
}, 'ml/exit_angle_model.pt')

print("Model saved to ml/exit_angle_model.pt")

# test predictions
print("\nPredictions vs actual:")
model.eval()
with torch.no_grad():
    for i in range(len(X)):
        pred_norm = model(X_norm[i])
        pred = pred_norm * y_std + y_mean
        print(f"y={X[i].item():.2f} → predicted={pred.item():.1f}° actual={y[i].item():.1f}°")