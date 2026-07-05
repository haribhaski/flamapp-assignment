import os
import pandas as pd
import matplotlib.pyplot as plt

os.makedirs("results", exist_ok=True)

df = pd.read_csv("xy_data.csv")

print("Dataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())

print("\nSummary Statistics:")
print(df.describe())

with open("results/data_summary.txt", "w") as f:
    f.write("Dataset Shape:\n")
    f.write(str(df.shape))

    f.write("\n\nColumns:\n")
    f.write(str(list(df.columns)))

    f.write("\n\nSummary Statistics:\n")
    f.write(str(df.describe()))

plt.figure(figsize=(8, 6))

plt.scatter(
    df["x"],
    df["y"],
    s=20,
    label="Observed Data"
)

plt.xlabel("x")
plt.ylabel("y")
plt.title("Raw Data Points")
plt.axis("equal")
plt.grid(True)
plt.legend()

plt.savefig(
    "results/original_signal.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

print("\nFiles Generated:")
print("results/original_signal.png")
print("results/data_summary.txt")