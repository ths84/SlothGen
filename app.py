import sys
import random
import timeit
import datetime
import json
import csv
import pickle

from dataclasses import dataclass
from pathlib import Path
from os import system, name

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
    menu_choice = input(f'🦥 ').capitalize()
    if menu_choice == 'C':
        clear()
        print(f'''🦥 >>> Name your database <<<\n''')
        filename = input('🦥 ... (choose a name without file extension): ')
        # Create name of database
        database_name = f'{filename}.json'
        # Check if database already exists
        if Path(database_name).exists():
            print('🦥 ... Sorry, a database with that name already exists.')
            if input('🦥 ... Do you want to overwrite it? [Y/N] ').capitalize() in ('', 'Y', 'Yes'):
                Path(database_name).unlink()
                if Path(database_name.replace('.json', '.pkl')).exists():
                    Path(database_name.replace('.json', '.pkl')).unlink()
            elif input('\n🦥 ... Do you want to use it? [Y/N] ').capitalize() in ('', 'Y', 'Yes'):
                return database_name
            else:
                return None
        # Creating json database template
        create_json_database(database_name)
        clear()
        # Choosing database built size
        # 'full' = scrape complete names list from web (first and last names)
        # 'first_names_only' = scrape only first names from web
        # 'last_names_only' = scrape only last names from web
        print('''🦥 >>> Choose your database build <<<\n     
   [c]omplete          ... building a complete database may take up to 20 min.
   [f]irst names only  ... up to 5 min. 
   [l]ast names only   ... up to 10 min.
   ---------------------------------------------------------------------------
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
a database you are able to generate, evaluate and work with your name data in a number of ways.

Creating a database:    Choose this option if you have never slothed before or want to start fresh;
                        SlothGen 🦥 scrapes the following websites to create a database:
                        
                        First names from:   https://www.vorname.com
                                            https://www.magicmaman.com
                                            
                        Last names from:    http://www.surnameweb.org
                                            https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen
                                            https://www.familyeducation.com
                                            
Loading a database:     Load an existing database (.json) and start slothing
-----------------------------------------------------------------------------------------------------
Generating names:       Choose to randomly generate a single or a number of names
Exporting names:        Export your generated names in different file types (txt, csv etc.)

Happy Slothing! 🦥
    ''')
    input(f'Hit ENTER to return. ')
    select_database()


def start_scraping(database_name, scope):
    if scope == 'full':
        clear()
        print('🦥 SlothGen slowly started building your database ...')
        start_timer = timeit.default_timer()
        get_first_names.scraping_first_names_vornamedotcom(database_name)
        get_first_names.scraping_first_names_magicmamandotcom(database_name)
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
    print(f'''🦥 [Booted database: '{name_register.database_name}' | Last updated: {name_register.timestamp.year}/{name_register.timestamp.month}/{name_register.timestamp.day}] 
   [Male 1st names: {len(name_register.male_first_names)} | Female 1st names: {len(name_register.female_first_names)} | Last names: {len(name_register.last_names)}]
   [Gender: {name_register.gender} | Export format: {name_register.export_format}]
    
   META
   [g]ender           ... set gender for generator
   [f]ormat           ... set file format for export
   =================================================
    
   GENERATING AND EXPORTING NAMES     
   [s]single          ... generates a single name
   [l]list            ... generates a list of names
   [e]xport           ... exports a list of names  
   =================================================
   
   [b]ack to main menu
   [q]uit slothing''')
    while get_more_names is True:
        menu_choise = input("\n🦥 ").capitalize()
        if menu_choise == 'S':
            name_register.create_random_name()
        elif menu_choise == "G":
            while True:
                set_gender = input('[F]emale, [m]ale, [u]ndefined or [r]andom: ').lower()
                if set_gender == 'f':
                    name_register.gender = 'female'
                    create_random_names(name_register)
                elif set_gender == 'm':
                    name_register.gender = 'male'
                    create_random_names(name_register)
                elif set_gender == 'u':
                    name_register.gender = 'undefined'
                    create_random_names(name_register)
                elif set_gender == 'r':
                    name_register.gender = 'random'
                    create_random_names(name_register)
                else:
                    print('Please choose a valid option.\n')
        elif menu_choise == "F":
            while True:
                set_export_format = input('Choose file format: [t]xt, [c]sv ... ').lower()
                if set_export_format == 't':
                    name_register.export_format = 'txt'
                elif set_export_format == 'c':
                    name_register.export_format = 'csv'
                else:
                    print('Please choose a valid option.')
                create_random_names(name_register)
        # elif menu_choise == 'A':
        #     while True:
        #         set_gender = input(
        #             'Are you adding [f]emale, [m]ale, [u]ndefined or [l]ast names? '
        #             '\nType [b] to step back ... ').lower()
        #         if set_gender == 'f':
        #             new_user_names = input(
        #                 'Type the name(s) you want to add (separate names using whitespaces): ').split(' ')
        #             for i in new_user_names:
        #                 if i in name_register.female_first_names:
        #                     print(f'{i} already in database.\n')
        #                 else:
        #                     name_register.female_first_names.append(i)
        #                     name_register.saving_database()
        #                     print(f'{i} was added to >>> female 1st names.\n')
        #         elif set_gender == 'm':
        #             new_user_names = input(
        #                 'Type the name(s) you want to add (separate names using whitespaces): ').split(' ')
        #             for i in new_user_names:
        #                 if i in name_register.male_first_names:
        #                     print(f'{i} already in database.\n')
        #                 else:
        #                     name_register.male_first_names.append(i)
        #                     print(f'{i} was added to >>> male 1st names.\n')
        #         elif set_gender == 'u':
        #             print('Reminder @Thomas: implement non-gender names!!\n')
        #         elif set_gender == 'l':
        #             new_user_names = input(
        #                 'Type the name(s) you want to add (separate names using whitespaces): ').split(' ')
        #             for i in new_user_names:
        #                 if i in name_register.last_names:
        #                     print(f'{i} already in database.\n')
        #                 else:
        #                     name_register.last_names.append(i)
        #                     print(f'{i} was added to >>> last names.\n')
        #         elif set_gender == 'b':
        #             create_random_names(name_register)
        elif menu_choise == 'Q':
            sys.exit(0)
        elif menu_choise == 'B':
            main()
        elif menu_choise == 'E':
            xcount = int(input(f'How many names do you want to export? '))
            name_register.export_random_names(xcount)
        # elif menu_choise == 'U':
        #     while True:
        #         scope = str(input(f'Do you want to update [a]ll or only [f]irst or [l]ast names?'
        #                           f'\nType [b] to step back ... ')).lower()
        #         if scope == 'f':
        #             scope = 'first_names_only'
        #             start_scraping(name_register.database_name, scope)
        #             name_register.timestamp = datetime.datetime.now()
        #             input(f'Press ENTER to continue.')
        #             create_random_names(name_register)
        #         elif scope == 'a':
        #             scope = "full"
        #             start_scraping(name_register.database_name, scope)
        #             name_register.timestamp = datetime.datetime.now()
        #             input(f'Press ENTER to continue.')
        #             create_random_names(name_register)
        #         elif scope == 'l':
        #             scope = 'last_names_only'
        #             start_scraping(name_register.database_name, scope)
        #             name_register.timestamp = datetime.datetime.now()
        #             input(f'Press ENTER to continue.')
        #             create_random_names(name_register)
        #         elif scope == 'b':
        #             create_random_names(name_register)
        #         else:
        #             print(f'Please choose a valid option.')
        elif menu_choise == 'L':
            while True:
                try:
                    xcount = int(input('\n🦥 Generate how many names? '))
                    if xcount > 0:
                        break
                except:
                    print("Please choose a valid option.")
            start_timer = timeit.default_timer()
            print('\nStarted slothing ... 🦥\n')
            for x in range(0, xcount):
                name_register.create_random_name()
            duration_seconds = int(timeit.default_timer() - start_timer)
            print(f'\n(SlothGen 🦥 took {duration_seconds} seconds to generate {xcount} names.)\n')
            input(f'Press ENTER to continue.')
            create_random_names(name_register)
        else:
            print('Please choose a valid option.')


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


def clear():
    # Windows
    if name == 'nt':
        _ = system('cls')
    # Mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


@dataclass
class NameRegister:
    def __init__(self, database_name):
        self.database_name = database_name
        self.gender = 'random'
        self.export_format = 'txt'
        self.timestamp = datetime.datetime.now()
        self._read_names(database_name)

    def _read_names(self, database_name):
        with open(database_name) as file:
            database = json.load(file)
        self.male_first_names = list(set(database['first_names']['male_first_names']))
        self.female_first_names = list(set(database['first_names']['female_first_names']))
        self.first_names = list(set(database['first_names']))
        self.last_names = list(set(database['last_names']))

    def create_random_name(self):
        if self.gender == 'male':
            print(f'{random.choice(self.male_first_names)} {random.choice(self.male_first_names)} '
                  f'{random.choice(self.last_names)}')
        elif self.gender == 'female':
            print(f'{random.choice(self.female_first_names)} {random.choice(self.female_first_names)} '
                  f'{random.choice(self.last_names)}')
        elif self.gender == 'undefined':
            print(f'{random.choice(self.male_first_names)} {random.choice(self.female_first_names)} '
                  f'{random.choice(self.last_names)}')
        elif self.gender == 'random':
            dice = random.choice(self.first_names)
            if dice == 'male_first_names':
                print(f'{random.choice(self.male_first_names)} {random.choice(self.male_first_names)} '
                      f'{random.choice(self.last_names)}')
            elif dice == 'female_first_names':
                print(f'{random.choice(self.female_first_names)} {random.choice(self.female_first_names)} '
                      f'{random.choice(self.last_names)}')
            else:
                print('Random error.')

    def export_random_names(self, xcount):
        export_list = []
        for i in range(0, xcount):
            if self.gender == 'male':
                set_name = f'{random.choice(self.male_first_names)} {random.choice(self.male_first_names)} ' \
                           f'{random.choice(self.last_names)}'
                export_list.append(set_name)
            elif self.gender == 'female':
                set_name = f'{random.choice(self.female_first_names)} {random.choice(self.female_first_names)} ' \
                           f'{random.choice(self.last_names)}'
                export_list.append(set_name)
            elif self.gender == 'undefined':
                set_name = f'{random.choice(self.male_first_names)} {random.choice(self.female_first_names)} ' \
                           f'{random.choice(self.last_names)}'
                export_list.append(set_name)
            elif self.gender == 'random':
                dice = random.choice(self.first_names)
                if dice == 'male_first_names':
                    set_name = f'{random.choice(self.male_first_names)} {random.choice(self.male_first_names)} ' \
                               f'{random.choice(self.last_names)}'
                    export_list.append(set_name)
                elif dice == 'female_first_names':
                    set_name = f'{random.choice(self.female_first_names)} {random.choice(self.female_first_names)} ' \
                               f'{random.choice(self.last_names)}'
                    export_list.append(set_name)
        # Export as 'txt' and 'csv'
        if self.export_format == 'txt':
            file_name = f'{self.database_name}.txt'
            txtout = open(file_name, 'w')
            for i in export_list:
                txtout.write(i + '\n')
            txtout.close()
            print(f'Exported {len(export_list)} names to {file_name}.')
        elif self.export_format == 'csv':
            file_name = f'{self.database_name}.csv'
            with open(file_name, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for i in export_list:
                    writer.writerow([i])
            print(f'Exported {len(export_list)} names to {file_name}.')

    def pickle(self):
        with open(self.database_name.replace('.json', '.pkl'), "wb") as fout:
            pickle.dump(self, fout)


def main():
    database_name = None
    while database_name is None:
        database_name = select_database()

    if Path(database_name.replace('.json', '.pkl')).exists():
        with open(database_name.replace('.json', '.pkl'), "rb") as fin:
            name_register = pickle.load(fin)
    else:
        name_register = NameRegister(database_name)
        name_register.pickle()

    while True:
        create_random_names(name_register)


if __name__ == '__main__':
    main()