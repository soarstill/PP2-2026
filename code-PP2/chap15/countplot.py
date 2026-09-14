import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv("shopping.csv")
df["Revenue"] = df["UnitPrice"] * df["Quantity"]

sns.countplot(data=df, x="Category")
plt.title("카테고리별 주문 건수")
plt.xticks(rotation=45)
plt.show()
