import pandas as pd

excelFile = pd.read_excel (r'C:\Users\Marko\Documents\test.xlsx')
for index, row in excelFile.head().iterrows():
     print(row[0], row[3], row[4])