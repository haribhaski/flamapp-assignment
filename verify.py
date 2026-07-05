import os
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree
import matplotlib.pyplot as plt


def model(t, theta, M, X):
    envelope = np.exp(M * np.abs(t)) * np.sin(0.3 * t)

    x = t * np.cos(theta) - envelope * np.sin(theta) + X
    y = 42 + t * np.sin(theta) + envelope * np.cos(theta)

    return x, y


os.makedirs("results", exist_ok=True)

df = pd.read_csv("xy_data.csv")

x_obs = df["x"].values
y_obs = df["y"].values
observed_points = np.column_stack([x_obs, y_obs])

theta_deg = 30.0
M = 0.03
X = 55.0

theta = np.radians(theta_deg)

t_dense = np.linspace(6, 60, 20000)
x_dense, y_dense = model(t_dense, theta, M, X)

curve_points = np.column_stack([x_dense, y_dense])

tree = cKDTree(curve_points)
distances, nearest_idx = tree.query(observed_points)

mean_error = np.mean(distances)
max_error = np.max(distances)
rmse = np.sqrt(np.mean(distances ** 2))

print("Independent Verification")
print("theta_deg:", theta_deg)
print("M:", M)
print("X:", X)
print("mean_error:", mean_error)
print("max_error:", max_error)
print("rmse:", rmse)

with open("results/verification.txt", "w") as f:
    f.write("Independent Verification\n")
    f.write(f"theta_deg: {theta_deg}\n")
    f.write(f"M: {M}\n")
    f.write(f"X: {X}\n")
    f.write(f"mean_error: {mean_error}\n")
    f.write(f"max_error: {max_error}\n")
    f.write(f"rmse: {rmse}\n")

plt.figure(figsize=(8, 6))
plt.scatter(x_obs, y_obs, s=18, label="Observed Data")
plt.plot(x_dense, y_dense, linewidth=2, label="Verified Curve")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Independent Verification Plot")
plt.axis("equal")
plt.grid(True)
plt.legend()
plt.savefig("results/verification_plot.png", dpi=300, bbox_inches="tight")
plt.show()

print("\nFiles Generated:")
print("results/verification.txt")
print("results/verification_plot.png")