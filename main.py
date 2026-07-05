import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("xy_data.csv")

os.makedirs("data", exist_ok=True)

plt.figure(figsize=(8, 6))
plt.scatter(df["x"], df["y"], s=12)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Original Signal")
plt.axis("equal")
plt.grid(True)

plt.savefig("data/original_signal.png", dpi=300, bbox_inches="tight")
plt.show()

print("Saved plot at: data/original_signal.png")