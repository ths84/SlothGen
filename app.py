import sys
import random
import timeit
import json

from os import system, name
from dataclasses import dataclass
from pathlib import Path
from webscrape import webscraping_last_names as get_last_names, webscraping_first_names as get_first_names


def select_database():
    clear()
    print(f"""SlothGen 🦥 v0.2 randomly and slowly combines two first names and one last name. ☕️

    [c]reate database
    [l]oad database   
    -----------------
    [h]elp
    [q]uit slothing
    """)
    menu_choice = input(f'🦥 ... ').capitalize()
    if menu_choice == 'C':
        clear()
        print(f'''🦥 >>> Name your database <<<\n''')
        filename = input('🦥 ... (choose a name without file extension): ')
        database_name = f'{filename}.json'
        if Path(database_name).exists():
            print('🦥 ... Sorry, a database with that name already exists.')
            if input("🦥 ... Do you want to overwrite it? [Y/N] ").capitalize() in ('', 'Y', 'Yes'):
                Path(database_name).unlink()
                if Path(database_name.replace('.json', '.pkl')).exists():
                    Path(database_name.replace('.json', '.pkl')).unlink()
            elif input("\n🦥 ... Do you want to use it? [Y/N] ").capitalize() in ('', 'Y', 'Yes'):
                return database_name
            else:
                return None

        # Creating json database template
        create_json_database(database_name)

        # Choosing database built size
        clear()
        print('''🦥 >>> Choose your database build <<<\n     
    [c]omplete          ... building a complete database may take up to 20 min.
    [f]irst names only  ... up to 5 min. 
    [l]ast names only   ... up to 10 min.
    -------------------------------------
    [b]ack to main menu
    [q]uit slothing
            ''')
        database_scope = input('''🦥 ... ''').lower()
        if database_scope == 'c':
            scope = 'full'
            start_scraping(database_name, scope)
        elif database_scope == "f":
            scope = 'first_names_only'
            start_scraping(database_name, scope)
            print(database_name)
            return database_name
        elif database_scope == "l":
            scope = 'last_names_only'
            start_scraping(database_name, scope)
        elif database_scope == 'q':
            sys.exit(0)
        elif database_scope == 'b':
            main()
        else:
            print('Please choose a valid option.')
            return None
        return database_name
    elif menu_choice == 'L':
        clear()
        while True:
            try:
                print(f'''🦥 >>> Load your database <<<\n''')
                database_name = input('🦥 ... Type the name of your database: ')
                if not Path(database_name).is_file():
                    print('Sorry. No file of that name exists.\n')
                elif Path(database_name).is_file():
                    return database_name
            except:
                print('Sorry. That is not a valid option.')
    elif menu_choice == 'Q':
        sys.exit(0)
    elif menu_choice == 'H':
        sloth_help()
    else:
        print('Sorry, that is not a valid input. Try again!')


def sloth_help():
    clear()
    print(f'''🦥 s l o t h   h e l p ☕

SlothGen 🦥 uses a database (.json) to store and load first and last names. After creating or loading 
a database you are able to generate and export names as well as inspect your specific database in a 
number of ways.

Creating a database:    Choose this option if you have never slothed before or want to start fresh.
Loading a database:     Load an existing database (.json) and start slothing.
-----------------------------------------------------------------------------------------------------
Generating names:       Choose to randomly generate a SINGLE or a NUMBER of names.
Exporting names:        Export your generated names in different file types (txt, json etc.).
Inspecting your data:   Various options to evaluate name data after loading or creating a database.

Happy Slothing! 🦥
    ''')
    test = input(f'Hit ENTER to return. ')
    select_database()


def start_scraping(database_name, scope):
    if scope == 'full':
        clear()
        print('🦥 SlothGen slowly started building your database ...')
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
        print(f'\nSlothGen 🦥 successfully created your database in {duration_seconds // 60} minutes and '
              f'{duration_seconds % 60} seconds.')
    elif scope == 'first_names_only':
        clear()
        print('SlothGen slowly started building your database ... 🦥')
        start_timer = timeit.default_timer()
        # Scrape first names only
        get_first_names.scraping_first_names_vornamedotcom(database_name)
        get_first_names.scraping_first_names_magicmamandotcom(database_name)
        duration_seconds = int(timeit.default_timer() - start_timer)
        clear()
        print(f'\nSlothGen 🦥 successfully created your database in {duration_seconds // 60} minutes and '
              f'{duration_seconds % 60} seconds.')
    elif scope == "last_names_only":
        clear()
        print('🦥 SlothGen slowly started building your database ...')
        start_timer = timeit.default_timer()
        # Scrape last names only
        get_last_names.scraping_last_names_surnameweb(database_name)
        get_last_names.scraping_last_names_wikipedia(database_name)
        get_last_names.scraping_last_names_familyeducationdotcom(database_name)
        duration_seconds = int(timeit.default_timer() - start_timer)
        clear()
        print(f'\nSlothGen 🦥 successfully created your database in {duration_seconds // 60} minutes and '
              f'{duration_seconds % 60} seconds.')


def create_random_names(name_register):
    clear()
    get_more_names = True
    print('''🦥 >>> Generating random names <<<\n     
    [s]single          ... generates a single name.
    [l]list            ... generates a list of names. 
    -------------------------------------------------
    [b]ack to main menu
    [q]uit slothing''')
    while get_more_names is True:
        roll_dice = input("\n🦥 ... ").capitalize()
        if roll_dice == 'S':
            name_register.create_random_name()
        elif roll_dice == 'Q':
            sys.exit(0)
        elif roll_dice == 'B':
            main()
        elif roll_dice == 'L':
            while True:
                try:
                    xcount = int(input('\n🦥 Generate how many names? '))
                    if xcount > 0:
                        break
                except:
                    print("That's not a valid option!")
            start_timer = timeit.default_timer()
            print('\nStarted slothing ... 🦥')
            for x in range(0, xcount):
                name_register.create_random_name()
            duration_seconds = int(timeit.default_timer() - start_timer)
            print(f'\n(SlothGen 🦥 took {duration_seconds} seconds to generate {xcount} names.)')
            print('''\n🦥 >>> Generating random names <<<\n     
    [s]single          ... generates a single name.
    [l]list            ... generates a list of names. 
    -------------------------------------------------
    [b]ack to main menu
    [q]uit slothing''')
        else:
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
    print(f'''\nSlothGen 🦥 found {len(database['first_names']['male_first_names'])} male and 
    {len(database['first_names']['female_first_names'])} female first names. SlothGen found 
    {len(database['last_names'])} last names too.''')


@dataclass
class NameRegister:
    def __init__(self, database_name):
        self.database_name = database_name
        self._read_names(database_name)

    def _read_names(self, database_name):
        with open(database_name) as file:
            database = json.load(file)
        self.male_first_names = list(set(database['first_names']['male_first_names']))
        self.female_first_names = list(set(database['first_names']['female_first_names']))
        self.last_names = list(set(database['last_names']))

    def create_random_name(self):
        print(f'{random.choice(self.male_first_names)} {random.choice(self.female_first_names)} '
              f'{random.choice(self.last_names)}')

    def pickle(self):
        import pickle
        with open(self.database_name.replace('.json', '.pkl'), "wb") as fout:
            pickle.dump(self, fout)


def main():
    database_name = None
    while database_name is None:
        database_name = select_database()

    if Path(database_name.replace('.json', '.pkl')).exists():
        import pickle
        with open(database_name.replace('.json', '.pkl'), "rb") as fin:
            name_register = pickle.load(fin)
    else:
        name_register = NameRegister(database_name)
        name_register.pickle()

    while True:
        create_random_names(name_register)


if __name__ == '__main__':
    main()