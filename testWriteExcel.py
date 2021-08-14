import openpyxl as xl

wb = xl.Workbook()
sheet = wb.active
sheet.title = "sheet1"

for sheet in wb:
    print(sheet.title)

for row in range(1, 10):
    cell = sheet.cell(row, column=1)
    cell.value = 'test'

wb.save('testfile.xlsx')

