import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

data = pd.read_csv('out/output_annotated.csv', delimiter='\t', header=None)

tags = data[3]
tag_counts = Counter(tags)
labels = list(tag_counts.keys())
sizes = list(tag_counts.values())
total = sum(sizes)

for label, size in zip(labels, sizes):
    percentage = (size / total) * 100
    print(f"Tag: {label}, Anzahl: {size}, Anteil: {percentage:.2f}%")

plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('Verteilung gemessen an der Gesamtmenge')
plt.axis('equal')
plt.show()