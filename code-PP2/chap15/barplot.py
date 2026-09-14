import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("shopping.csv")
df["Revenue"] = df["UnitPrice"] * df["Quantity"]

sns.barplot(data=df, x="Category", y="Revenue", estimator="mean")
plt.title("카테고리별 평균 매출 (주문당)")
plt.xticks(rotation=45)
plt.show()
