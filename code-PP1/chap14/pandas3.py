import pandas as pd
countries = pd.read_csv("countries.csv")
countries["density"] = countries["population"]/countries["area"]
print(countries)