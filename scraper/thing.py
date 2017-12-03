import pandas as pd
category = []
csv_series = pd.read_csv('sources.csv')
websites = csv_series.head().websites
categories = csv_series.head().type

print(websites)
