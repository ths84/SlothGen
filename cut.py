from bs4 import BeautifulSoup
import requests
import re
import openpyxl as xl


wb = xl.load_workbook('names_db.xlsx')
sheet = wb["sheet1"]

for row in sheet.iter_cols(min_row=1, min_col=3, max_col=3):
    for cell in row:
        if cell.value is not None:
            starting_row = cell.row


print(starting_cell)