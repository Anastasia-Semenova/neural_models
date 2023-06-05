import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


if __name__ == "__main__":
    data = pd.read_csv("bashkortostan/8_filtered.csv")
    grouped_data = data.groupby("city")
    countries = ["151", "135", "264"]
    counts = grouped_data.size().tolist()

    plt.bar(countries, counts)
    plt.xlabel("City")
    plt.ylabel("Count")
    plt.xticks(countries)
    plt.show()
