import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

data = pd.read_csv('out/output_annotated.csv', delimiter='\t', header=None)
tags = data[3]
redner_fraktionen = data[9]
fraktionen = ["AfD", "CDU/CSU", "FDP", "SPD", "BÜNDNIS 90/DIE GRÜNEN", "DIE LINKE"]
unique_tags = tags.unique()
colors = plt.cm.tab10(range(len(unique_tags)))
tag_color_map = {tag: colors[i] for i, tag in enumerate(unique_tags)}
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

for i, fraktion in enumerate(fraktionen):
    fraktion_tags = tags[redner_fraktionen.str.contains(fraktion, na=False)]
    tag_counts = Counter(fraktion_tags)
    labels = list(tag_counts.keys())
    sizes = list(tag_counts.values())
    total = sum(sizes)
    ax = axes[i]
    if total > 0:
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
                                          colors=[tag_color_map[label] for label in labels])
        ax.set_title(f'Anteil für die Fraktion: {fraktion}')
        ax.axis('equal')
    else:
        ax.text(0.5, 0.5, 'Keine Daten', ha='center', va='center', fontsize=12)
        ax.set_title(f'Anteil für die Fraktion: {fraktion}')
        ax.axis('off')

handles = [plt.Line2D([0], [0], marker='o', color='w', label=tag,
                      markersize=10, markerfacecolor=tag_color_map[tag]) for tag in unique_tags]
fig.legend(handles=handles, title="Legende", loc='center', bbox_to_anchor=(0.5, 0.05), ncol=3)
plt.tight_layout(rect=[0, 0.1, 1, 1])
plt.show()