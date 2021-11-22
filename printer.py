import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

def print_table(hashtag, sorttweets, top=10):
    counts = defaultdict(int)
    for x in sorttweets:
        counts[x] += 1
    stand = sorted(counts.items(), reverse=True, key=lambda tup: tup[1])[:top]
    plt.style.use('classic')
    df = pd.DataFrame(stand)

    #fig, ax = plt.subplots()
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots(1, 1)
    plt.axis('off')
    tab = ax.table(cellText=df.values, loc='center', colLabels = ('Naam', 'Aantal'))
    tab.auto_set_font_size(False)
    tab.set_fontsize(10)
    fig.tight_layout()

    #plt.show()
    filename = f'{hashtag}_tweet_top10.png'
    plt.savefig(filename)
