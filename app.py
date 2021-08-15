import random
import time
import openpyxl as xl
import webscraping_first_names as get_first_names
import webscraping_last_names as get_last_names

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


result = input("[C]reate or [W]ork with existing database? ").capitalize()

if result == 'C':
    filename = input('Name your database: ')
    wb_filename = f'{filename}.xlsx'

    start = time.process_time()
    wb = xl.Workbook()
    sheet = wb.active
    sheet.title = "sheet1"
    wb.save(wb_filename)

    # Scrape first names (female + male) from vornamen.com
    get_first_names.web_scrape_first_names(wb_filename)
    # Scrape last names (German) from wikipedia.de
    get_last_names.scraping_last_names_wikipedia(wb_filename)
    # Scrape last names from familyeducation.com
    get_last_names.scraping_last_names_familyeducationdotcom(wb_filename)

    end = time.time()
    print(time.process_time() - start)

elif result == 'W':
    print('Thanks!')



