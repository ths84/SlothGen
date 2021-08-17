import random
import datetime
import time
import openpyxl as xl
import webscraping_first_names as get_first_names
import webscraping_last_names as get_last_names
from pathlib import Path


def rng_intro():
    print(f"""
SlothGen 🦥 randomly and slowly combines two first names and one last name. ☕️

First names from: https://www.vorname.com
Last names from:  https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen
                  https://www.familyeducation.com
    """)


def convert_timedelta(duration):
    seconds = duration.seconds
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return minutes, seconds


def stats(wb_filename):
    wb = xl.load_workbook(wb_filename)
    sheet = wb['sheet1']

    for column in range(1, sheet.max_column + 1):
        compare_row = sheet.min_row
        for row in range(1, sheet.max_row + 1):
            cell = sheet.cell(row, column)
            if cell.value is not None and column == 1:
                if row >= compare_row:
                    stats.max_row_firstname = row
                else:
                    break
            elif cell.value is not None and column == 2:
                if row >= compare_row:
                    stats.max_row_lastname = row
                else:
                    break


def create_random_name(wb_filename, xcount):
    wb = xl.load_workbook(wb_filename)
    sheet = wb['sheet1']

    # Get max non empty cell numbers for columns 1 - 2
    for column in range(1, sheet.max_column + 1):
        compare_row = sheet.min_row
        for row in range(1, sheet.max_row + 1):
            cell = sheet.cell(row, column)
            if cell.value is not None and column == 1:
                if row >= compare_row:
                    stats.max_row_firstname = row
                else:
                    break
            elif cell.value is not None and column == 2:
                if row >= compare_row:
                    stats.max_row_lastname = row
                else:
                    break

    # Get random cell numbers for column 1 - 2
    dice_first_name = random.randint(1, stats.max_row_firstname)
    dice_second_name = random.randint(1, stats.max_row_firstname)
    dice_last_name = random.randint(1, stats.max_row_lastname)

    # Set random cells for column 1 - 2
    cell_first_name = sheet.cell(dice_first_name, 1)
    cell_second_name = sheet.cell(dice_second_name, 1)
    cell_last_name = sheet.cell(dice_last_name, 2)

    print(f'{cell_first_name.value} {cell_second_name.value} {cell_last_name.value}')


rng_intro()

is_input_valid = False
while is_input_valid is False:
    result = input("🦥 [C]reate or [W]ork with existing database? [Q] to stop slothing... ").capitalize()
    if result == 'C':
        is_input_valid = True
        filename = input('🦥 Name your database: ')
        wb_filename = f'{filename}.xlsx'

        wb = xl.Workbook()
        sheet = wb.active
        sheet.title = "sheet1"
        wb.save(wb_filename)

        print('SlothGen slowly started building your database ... 🦥')

        start_log = datetime.datetime.now()
        # Scrape first names (female + male) from vornamen.com
        get_first_names.web_scrape_first_names(wb_filename)
        # Scrape last names (German) from wikipedia.de
        get_last_names.scraping_last_names_wikipedia(wb_filename)
        # Scrape last names from familyeducation.com
        get_last_names.scraping_last_names_familyeducationdotcom(wb_filename)

        end_log = datetime.datetime.now()
        duration = end_log - start_log
        minutes, seconds = convert_timedelta(duration)
        print('\nSlothGen 🦥 successfully created your database in {} minutes and {} seconds.'.format(minutes, seconds))
    elif result == 'W':
        is_input_valid = True
        is_filename_valid = False
        while is_filename_valid is False:
            wb_filename = input('Type the name of your database with file extension (example: database.xlsx): ')
            if Path(wb_filename).is_file():
                is_filename_valid = True
            else:
                is_filename_valid = False
                print('Sorry. No file of that name exists.\n')
    elif result == 'Q':
        exit()
    else:
        is_input_valid = False
        print('Please choose [C]reate or [W]ork.')

stats(wb_filename)
print(f'\nSlothGen 🦥 found {stats.max_row_firstname} first names and {stats.max_row_lastname} last names in your database.')

get_more_names = True
is_roll_dice_input_valid = False

while get_more_names is True:
    roll_dice = input("\n🦥 Generate [S]ingle name, [N]umber of names or [Q]uit? ").capitalize()
    if roll_dice == 'S':
        xcount = 1
        is_roll_dice_input_valid = True
        create_random_name(wb_filename, xcount)
    elif roll_dice == 'Q':
        is_roll_dice_input_valid = True
        get_more_names = False
    elif roll_dice == 'N':
        start = time.time()
        is_roll_dice_input_valid = True
        is_xcount_corret = False
        while is_xcount_corret is False:
            try:
                xcount = int(input('\n🦥 Generate how many names? '))
                is_xcount_corret = True
                print('Started slothing ... 🦥')
                for x in range(1, xcount + 1):
                    create_random_name(wb_filename, xcount)
            except ValueError:
                print('\nPlease enter a valid number.')
        duration = time.time() - start
        print('\n(SlothGen 🦥 took %.0f seconds to generate your names.)' % duration)
    else:
        is_roll_dice_input_valid = False
        print('Please press [N] or [Q].')