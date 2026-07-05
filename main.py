import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("xy_data.csv")

# Dataset Information
print("\nDataset Shape:")
print(df.shape)
print("\nColumns:")
print(df.columns)
print("\nFirst 5 rows:")
print(df.head())
print("\nStatistics:")
print(df.describe())

# Save statistics
with open("results/data_summary.txt", "w") as f:
    f.write("Dataset Shape:\n")
    f.write(str(df.shape))
    f.write("\n\nStatistics:\n")
    f.write(str(df.describe()))

plt.figure(figsize=(8,6))
plt.xlabel("x")
plt.ylabel("y")
plt.title("Original Signal")
plt.axis("equal")
plt.grid(True)

plt.savefig("results/original_signal.png",dpi=300,bbox_inches="tight")

plt.show()
print("\nSaved:")
print("results/original_signal.png")
print("results/data_summary.txt")