import random
import openpyxl as xl


def process_workbook():
    wb = xl.load_workbook('tab_namen.xlsx')
    sheet = wb['sheet1']

    # Get max non empty cell numbers for columns 1 - 3
    for column in range(1, sheet.max_column + 1):
        compare_row = sheet.min_row
        for row in range(1, sheet.max_row + 1):
            cell = sheet.cell(row, column)
            if cell.value is not None and column == 1:
                if row >= compare_row:
                    max_row_firstname = row
                else:
                    break
            elif cell.value is not None and column == 2:
                if row >= compare_row:
                    max_row_secondname = row
                else:
                    break
            elif cell.value is not None and column == 3:
                if row >= compare_row:
                    max_row_lastname = row
                else:
                    break

    # Get random cell numbers for column 1 - 3
    dice_first_name = random.randint(1, max_row_firstname)
    dice_second_name = random.randint(1, max_row_secondname)
    dice_last_name = random.randint(1, max_row_lastname)

    # Set random cells for column 1 - 3
    cell_first_name = sheet.cell(dice_first_name, 1)
    cell_second_name = sheet.cell(dice_second_name, 2)
    cell_last_name = sheet.cell(dice_last_name, 3)

    print(f'{cell_first_name.value} {cell_second_name.value} {cell_last_name.value}')


process_workbook()