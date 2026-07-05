import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution, minimize, minimize_scalar


def model(t, theta, M, X):
    envelope = np.exp(M * np.abs(t)) * np.sin(0.3 * t)

    x = t * np.cos(theta) - envelope * np.sin(theta) + X
    y = 42 + t * np.sin(theta) + envelope * np.cos(theta)

    return x, y


def curve_loss(params, observed_x, observed_y):
    theta_deg, M, X = params
    theta = np.radians(theta_deg)

    distances = []

    for x_i, y_i in zip(observed_x, observed_y):

        def point_distance(t):
            px, py = model(t, theta, M, X)
            return (px - x_i) ** 2 + (py - y_i) ** 2

        result = minimize_scalar(
            point_distance,
            bounds=(6, 60),
            method="bounded"
        )

        distances.append(np.sqrt(result.fun))

    return np.mean(distances)


os.makedirs("results", exist_ok=True)
os.makedirs("plots", exist_ok=True)

df = pd.read_csv("xy_data.csv")

x_obs = df["x"].values
y_obs = df["y"].values

bounds = [
    (0, 50),
    (-0.05, 0.05),
    (0, 100)
]

result = differential_evolution(
    curve_loss,
    bounds=bounds,
    args=(x_obs, y_obs),
    seed=42,
    maxiter=40,
    popsize=10,
    polish=False
)

local = minimize(
    curve_loss,
    result.x,
    args=(x_obs, y_obs),
    method="Nelder-Mead"
)

theta_deg, M, X = local.x
final_loss = local.fun

print("Estimated Parameters")
print("theta_deg:", theta_deg)
print("theta_rad:", np.radians(theta_deg))
print("M:", M)
print("X:", X)
print("loss:", final_loss)

with open("results/final_result.txt", "w") as f:
    f.write("Estimated Parameters\n")
    f.write(f"theta_deg: {theta_deg}\n")
    f.write(f"theta_rad: {np.radians(theta_deg)}\n")
    f.write(f"M: {M}\n")
    f.write(f"X: {X}\n")
    f.write(f"loss: {final_loss}\n")

t_dense = np.linspace(6, 60, 2000)
x_pred, y_pred = model(t_dense, np.radians(theta_deg), M, X)

plt.figure(figsize=(8,6))
plt.scatter(df["x"],df["y"],s=20,color="red",label="Observed Data")
plt.plot(x_pred,y_pred,color="blue",linewidth=2,label="Approximated Curve")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Observed vs Approximated Curve")
plt.axis("equal")
plt.grid(True)
plt.legend()

plt.savefig("results/fitted_curve.png", dpi=300, bbox_inches="tight")
plt.show()

print("Saved:")
print("results/final_result.txt")
print("results/fitted_curve.png")