import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# Step 1: Load Data from CSV
# ------------------------------

df = pd.read_csv("students.csv")

print("\n--- Original Data ---")
print(df)

# ------------------------------
# Step 2: Feature Engineering
# ------------------------------

df["Total"] = df[["Math", "Science", "English"]].sum(axis=1)
df["Average"] = df["Total"] / 3

# Pass / Fail (Pass if average >= 40)
df["Result"] = np.where(df["Average"] >= 40, "Pass", "Fail")

# Grade System
def assign_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    else:
        return "D"

df["Grade"] = df["Average"].apply(assign_grade)

# Ranking (1 = highest)
df["Rank"] = df["Total"].rank(ascending=False, method="min")

# ------------------------------
# Step 3: Insights
# ------------------------------

print("\n--- Top 3 Students ---")
print(df.sort_values("Rank").head(3)[["Student", "Total", "Rank"]])

print("\nClass Average:", df["Average"].mean())

print("\nSubject-wise Average:")
print(df[["Math", "Science", "English"]].mean())

print("\nPass Percentage:",
      (df["Result"].value_counts(normalize=True) * 100)["Pass"], "%")

# ------------------------------
# Step 4: Visualization
# ------------------------------

plt.figure(figsize=(15,10))

# 1️⃣ Total Marks Bar Chart
plt.subplot(2,2,1)
plt.bar(df["Student"], df["Total"])
plt.xticks(rotation=45)
plt.title("Total Marks by Student")

# 2️⃣ Subject Average
plt.subplot(2,2,2)
df[["Math","Science","English"]].mean().plot(kind="bar")
plt.title("Subject-wise Average")

# 3️⃣ Grade Distribution
plt.subplot(2,2,3)
df["Grade"].value_counts().plot(kind="pie", autopct="%1.1f%%")
plt.title("Grade Distribution")

# 4️⃣ Marks Trend
plt.subplot(2,2,4)
plt.plot(df["Student"], df["Average"], marker="o")
plt.xticks(rotation=45)
plt.title("Average Marks Trend")

plt.tight_layout()
plt.show()