import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("shopping3.csv")
df["Revenue"] = df["UnitPrice"] * df["Quantity"]

df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["Month"] = df["OrderDate"].dt.month
monthly = df.groupby("Month")["Revenue"].sum()
sns.lineplot(x=monthly.index, y=monthly.values, marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.show()
