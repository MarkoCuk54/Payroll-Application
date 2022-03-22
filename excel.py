import pandas as pd
ids = []
sati = []
excelFile = pd.read_excel (r'C:\Users\Marko\Documents\test.xlsx')
for index, row in excelFile.head().iterrows():
    ids.append(row["id"])
    sati.append(row["sati"])

