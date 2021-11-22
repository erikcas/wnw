import csv
import pandas as pd
import datetime
import time
import sys
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

def tag_data(hashtag, datatweets):
    counts = defaultdict(int)
    for x in datatweets:
        counts[x] += 1
    filename = f'{hashtag}_tweet_graph.csv'
    stand = counts.items()
    pd.DataFrame(stand).to_csv(filename, header=['Tijd', 'Aantal'])

def plot_data(hashtag, datatweets, datum):
    filename = f'{hashtag}_tweet_graph.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        tijd, aantal = [], []
        for row in reader:
            datumtijd = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            try:
                aantallen = int(row[2])
            except ValueError:
                print(f'Geen data voor {datumtijd}')
            else:
                tijd.append(datumtijd)
                aantal.append(aantallen)

    # Plot de aantallen
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(tijd, aantal, c='red')

    # Format plot
    titel = f'{hashtag} tweets per uur sinds {datum}'
    plt.title(titel, fontsize=20)
    plt.xlabel('', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Aantal Tweets', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)

    graphic = f'{hashtag}_tweet_graph.png'
    plt.savefig(graphic)
