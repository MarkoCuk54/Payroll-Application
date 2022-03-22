import pandas as pd

excelFile = pd.read_excel (r'C:\Users\Marko\Documents\test.xlsx')
for index, row in excelFile.head(n=15).iterrows():
     print(index, row)