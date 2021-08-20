from os import system, name
import random
import timeit
import json
from webscrape import webscraping_last_names as get_last_names, webscraping_first_names as get_first_names
from pathlib import Path


def sloth_menu():
    print(f"""
SlothGen 🦥 randomly and slowly combines two first names and one last name. ☕️

    [M]ANAGE MY DATABASE        [S]LOTH HELP!
    [G]ENERATE ME SOME NAMES    [T]IP OF THE DAY
                                [A]BOUT THE SLOTH
    """)
    menu_choice = input(f'What do you want SlothGen 🦥 to do? ').capitalize()
    if menu_choice == 'M':
        sloth_menu_manage_database()
    else:
        print('HELP!!')


def sloth_menu_manage_database():
    is_input_valid = False
    while is_input_valid is False:
        print(f"""
    [C]REATE A FRESH DATABASE        [S]LOTH HELP!
    [O]OPEN YOUR EXISTING DATABASE
    [G]ET SOME STATS    
                
    [B]ACK TO MAIN MENU
            """)
        result = input('''🦥 ... ''').capitalize()
        if result == 'C':
            is_input_valid = True
            filename = input('\n🦥 ... Name your database: ')
            database_name = f'{filename}.json'
            create_json_database(database_name)

            database_scope = input('\n🦥 ... Build [C]OMPLETE database? Or just [F]IRST or [L]AST names? ').lower()
            if database_scope == 'c':
                clear()
                print('\n🦥 SlothGen slowly started building your database ...')
                start_timer = timeit.default_timer()
                # Scrape first names
                get_first_names.scraping_first_names_vornamedotcom(database_name)
                get_first_names.scraping_first_names_magicmamandotcom(database_name)
                # Scrape last names
                get_last_names.scraping_last_names_surnameweb(database_name)
                get_last_names.scraping_last_names_wikipedia(database_name)
                get_last_names.scraping_last_names_familyeducationdotcom(database_name)
                duration_seconds = int(timeit.default_timer() - start_timer)
                clear()
                print(f'\nSlothGen 🦥 successfully created your database in {duration_seconds // 60} minutes and {duration_seconds % 60} seconds.')
                stats(database_name)
                sloth_menu()
            elif database_scope == "f":
                clear()
                print('\nSlothGen slowly started building your database ... 🦥')
                start_timer = timeit.default_timer()
                # Scrape first names only
                get_first_names.scraping_first_names_vornamedotcom(database_name)
                get_first_names.scraping_first_names_magicmamandotcom(database_name)
                duration_seconds = int(timeit.default_timer() - start_timer)
                print(f'\nSlothGen 🦥 successfully created your database in {duration_seconds // 60} minutes and {duration_seconds % 60} seconds.')
                stats(database_name)
                sloth_menu()
            elif database_scope == "l":
                clear()
                print('\n🦥 SlothGen slowly started building your database ...')
                start_timer = timeit.default_timer()
                # Scrape last names only
                get_last_names.scraping_last_names_surnameweb(database_name)
                get_last_names.scraping_last_names_wikipedia(database_name)
                get_last_names.scraping_last_names_familyeducationdotcom(database_name)
                duration_seconds = int(timeit.default_timer() - start_timer)
                print(f'\nSlothGen 🦥 successfully created your database in {duration_seconds // 60} minutes and {duration_seconds % 60} seconds.')
                stats(database_name)
                sloth_menu()
        elif result == 'O':
            is_input_valid = True
            is_filename_valid = False
            while is_filename_valid is False:
                database_name = input('Type the name of your database with file extension (example: database.json): ')
                if Path(database_name).is_file():
                    sloth_menu_generate_names(database_name)
                else:
                    is_filename_valid = False
                    print('Sorry. No file of that name exists.\n')
        elif result == 'Q':
            exit()
        else:
            is_input_valid = False
            print('Please choose [C]REATE, [O]PEN or [Q]UIT.')


def sloth_menu_generate_names(database_name):
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
            exit()
        elif roll_dice == 'N':
            is_roll_dice_input_valid = True
            is_xcount_corret = False
            while is_xcount_corret is False:
                try:
                    xcount = int(input('\n🦥 Generate how many names? '))
                    is_xcount_corret = True
                    start_timer = timeit.default_timer()
                    print('Started slothing ... 🦥')
                    for x in range(1, xcount + 1):
                        create_random_name(database_name, xcount)
                    duration_seconds = int(timeit.default_timer() - start_timer)
                    print(
                        f'\nSlothGen 🦥 took {duration_seconds // 60} minutes and {duration_seconds % 60} seconds to generate {xcount} names.')
                except ValueError:
                    print('\nPlease enter a valid number.')
        else:
            is_roll_dice_input_valid = False
            print('Please press [N] or [Q].')


def clear():
    # Windows
    if name == 'nt':
        _ = system('cls')

    # Mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


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


sloth_menu()

