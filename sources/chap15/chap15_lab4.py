import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("shopping3.csv")

# Revenue 열 추가 (단가 × 수량)
df["Revenue"] = df["UnitPrice"] * df["Quantity"]

# 날짜를 datetime 형식으로 변환
df["OrderDate"] = pd.to_datetime(df["OrderDate"])

# Month(월) 열 추가
df["Month"] = df["OrderDate"].dt.month

monthly = df.groupby("Month")["Revenue"].sum().reset_index()
print(monthly)

plt.figure(figsize=(8, 4))
sns.lineplot(data=monthly, x="Month", y="Revenue", marker="o")
plt.title("Monthly Shopping Revenue Trend (Seaborn)")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.show()

monthly_cat = df.groupby(["Month", "Category"])["Revenue"].sum().reset_index()
print(monthly_cat.head())

# Seaborn으로 여러 선을 한 그래프에 그리기:
plt.figure(figsize=(10, 5))
sns.lineplot(data=monthly_cat, x="Month", y="Revenue", hue="Category", marker="o")
plt.title("Monthly Revenue Trend by Category")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.legend(title="Category")
plt.show()
