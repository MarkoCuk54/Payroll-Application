import pandas as pd

excelFile = pd.read_excel (r'C:\Users\Marko\Documents\test.xlsx')
df = pd.DataFrame(excelFile, columns= ['id',"ime", "prezime" ,"sati" ,"satnica"])
