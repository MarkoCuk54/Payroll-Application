import pandas as pd
id = []
sati = []
excelFile = pd.read_excel (r'C:\Users\Marko\Documents\test.xlsx')
for index, row in excelFile.head().iterrows():
    id.append(row["id"])
    sati.append(row["sati"])

