import random
import timeit
import json
import openpyxl as xl
from webscrape import webscraping_last_names as get_last_names, webscraping_first_names as get_first_names
from pathlib import Path


def rng_intro():
    print(f"""
SlothGen 🦥 randomly and slowly combines two first names and one last name. ☕️

First names from: https://www.vorname.com
Last names from:  https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen
                  https://www.familyeducation.com
    """)


def create_json_database(database_name):
    data = {}
    first_names = {}
    last_names = []
    first_names['male_first_names'] = []
    first_names['male_first_names'].append('Thomas')
    first_names['female_first_names'] = []
    first_names['female_first_names'].append('Maria')
    last_names.append('Schmidt')
    data['first_names'] = first_names
    data['last_names'] = last_names

    with open(database_name, 'w') as file:
        json.dump(data, file, indent=2)


def stats(database_name):
    with open(database_name) as file:
        database = json.load(file)

    print(f'''\nSlothGen 🦥 found {len(database['first_names']['male_first_names'])} male and {len(database['first_names']['female_first_names'])} female first names. SlothGen found {len(database['last_names'])} last names too.''')


def create_random_name(database_name, xcount):
    with open(database_name) as file:
        database = json.load(file)

    # Get max number of names of each category (male_first_names, female_first_names, last_names) first
    max_male_first_names = len(database['first_names']['male_first_names'])
    max_female_first_names = len(database['first_names']['female_first_names'])
    max_last_names = len(database['last_names'])

    # Get random number for each name category
    dice_female_first_name = random.randint(0, max_female_first_names - 1)
    dice_male_first_name = random.randint(0, max_male_first_names - 1)
    dice_last_name = random.randint(0, max_last_names - 1)

    # Set random cells for column 1 - 2
    print(f'''{database['first_names']['male_first_names'][dice_male_first_name]} {database['first_names']['female_first_names'][dice_female_first_name]} {database['last_names'][dice_last_name]}''')


rng_intro()
is_input_valid = False
while is_input_valid is False:
    result = input("🦥 [C]reate or [W]ork with existing database? [Q] to stop slothing... ").capitalize()
    if result == 'C':
        is_input_valid = True
        filename = input('🦥 Name your database: ')
        database_name = f'{filename}.json'

        create_json_database(database_name)

        print('SlothGen slowly started building your database ... 🦥')

        start_timer = timeit.default_timer()
        # Scrape first names (female + male) from vornamen.com
        get_first_names.web_scrape_first_names(database_name)
        # Scrape last names (German) from wikipedia.de
        get_last_names.scraping_last_names_wikipedia(database_name)
        # Scrape last names from familyeducation.com
        get_last_names.scraping_last_names_familyeducationdotcom(database_name)

        duration_seconds = int(timeit.default_timer() - start_timer)
        print(f'\nSlothGen 🦥 successfully created your database in {duration_seconds//60} minutes and {duration_seconds%60} seconds.')
    elif result == 'W':
        is_input_valid = True
        is_filename_valid = False
        while is_filename_valid is False:
            database_name = input('Type the name of your database with file extension (example: database.xlsx): ')
            if Path(database_name).is_file():
                is_filename_valid = True
            else:
                is_filename_valid = False
                print('Sorry. No file of that name exists.\n')
    elif result == 'Q':
        exit()
    else:
        is_input_valid = False
        print('Please choose [C]reate or [W]ork.')

stats(database_name)

get_more_names = True
is_roll_dice_input_valid = False

while get_more_names is True:
    roll_dice = input("\n🦥 Generate [S]ingle name, [N]umber of names or [Q]uit? ").capitalize()
    if roll_dice == 'S':
        xcount = 1
        is_roll_dice_input_valid = True
        create_random_name(database_name, xcount)
    elif roll_dice == 'Q':
        is_roll_dice_input_valid = True
        get_more_names = False
    elif roll_dice == 'N':
        start_timer = timeit.default_timer()
        is_roll_dice_input_valid = True
        is_xcount_corret = False
        while is_xcount_corret is False:
            try:
                xcount = int(input('\n🦥 Generate how many names? '))
                is_xcount_corret = True
                print('Started slothing ... 🦥')
                for x in range(1, xcount + 1):
                    create_random_name(database_name, xcount)
            except ValueError:
                print('\nPlease enter a valid number.')
        duration_seconds = int(timeit.default_timer() - start_timer)
        print(f'\nSlothGen 🦥 took {duration_seconds//60} minutes and {duration_seconds%60} seconds to generate your names.')
    else:
        is_roll_dice_input_valid = False
        print('Please press [N] or [Q].')