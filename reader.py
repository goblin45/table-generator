import csv
import pandas as pd

new_dataFrame = pd.read_csv('fruits.csv')
new_excel = pd.ExcelWriter('FruitsInfo.xlsx')
new_dataFrame.to_excel(new_excel, index=False)
new_excel._save()

with open("fruits.csv") as file_obj:

    reader_obj = csv.reader(file_obj)
    for row in reader_obj:
        print(row)
