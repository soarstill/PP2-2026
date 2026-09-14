import csv
import matplotlib.pyplot as plt

f = open('ages.csv')
data = csv.reader(f)
header = next(data)

for row in data:
    if '서울특별시' in row[0]: 
        print(row)
f.close()
input()