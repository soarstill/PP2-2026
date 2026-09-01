import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("titanic.csv")
df["Age"].fillna(df["Age"].median(), inplace=True)
df["Embarked"].fillna(df["Embarked"].mode()[0], inplace=True)

sns.barplot(data=df, x="Sex", y="Survived")
plt.title("Survival Rate by Sex")
plt.show()

sns.barplot(data=df, x="Pclass", y="Survived")
plt.title("Survival Rate by Passenger Class")
plt.show()

sns.histplot(data=df, x="Age", hue="Survived", multiple="stack")
plt.title("Age Distribution of Survivors and Non-Survivors")
plt.show()

sns.catplot(data=df, x="Pclass", y="Survived", hue="Sex", kind="bar")
plt.title("Survival Rate by Sex and Passenger Class")
plt.show()
