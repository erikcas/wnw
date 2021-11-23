import csv
import pandas as pd
import datetime
import time
import sys
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from collections import defaultdict

def tag_data(hashtag, hashtag2, datatweets, datatweets2):
    counts = defaultdict(int)
    for x in datatweets:
        counts[x] += 1
    filename = f'{hashtag}_tweet_graph.csv'
    stand = counts.items()
    pd.DataFrame(stand).to_csv(filename, header=['Tijd', 'Aantal'])

    counts2 = defaultdict(int)
    for x in datatweets2:
        counts2[x] += 1
    filename = f'{hashtag2}_tweet_graph.csv'
    stand = counts2.items()
    pd.DataFrame(stand).to_csv(filename, header=['Tijd', 'Aantal'])

def plot_data(hashtag, hashtag2, datatweets, datatweets2, datum):
    filename = f'{hashtag}_tweet_graph.csv'
    with open(filename) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        tijd, aantal = [], []
        for row in reader:
            datumtijd = (datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') + timedelta(hours=1))
            try:
                aantallen = int(row[2])
            except ValueError:
                print(f'Geen data voor {datumtijd}')
            else:
                tijd.append(datumtijd)
                aantal.append(aantallen)

    filename2 = f'{hashtag2}_tweet_graph.csv'
    with open(filename2) as f:
        reader = csv.reader(f)
        header_row = next(reader)

        tijd2, aantal2 = [], []
        for row in reader:
            datumtijd = (datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') + timedelta(hours=1))
            try:
                aantallen = int(row[2])
            except ValueError:
                print(f'Geen data voor {datumtijd}')
            else:
                tijd2.append(datumtijd)
                aantal2.append(aantallen)

    # Plot de aantallen
    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    ax.plot(tijd, aantal, c='red')
    ax.plot(tijd2, aantal2, c='blue')

    # Format plot
    titel = f'Tweets per uur sinds {datum}\nRood = {hashtag} || Blauw = {hashtag2}'
    plt.title(titel, fontsize=16)
    plt.xlabel('', fontsize=16)
    fig.autofmt_xdate()
    plt.ylabel('Aantal Tweets', fontsize=16)
    plt.tick_params(axis='both', which='major', labelsize=16)

    graphic = f'{hashtag}_vs_{hashtag2}_tweet_graph.png'
    plt.savefig(graphic)
