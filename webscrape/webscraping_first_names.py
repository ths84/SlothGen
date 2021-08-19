from bs4 import BeautifulSoup
import requests
import json


def web_scrape_first_names(database_name):
    # Load JSON database
    with open(database_name) as file:
        database = json.load(file)

    url_root = 'https://www.vorname.com'
    url_part2 = ['maedchennamen', 'jungennamen']
    for part_in_url_part2 in url_part2:

        # Loop through all first names starting from 'A' to 'Z'
        for url_part3 in range(ord('A'), ord('Z') + 1):
            url_combine = f'{url_root}/{part_in_url_part2},{chr(url_part3)},1.html'
            response = requests.get(url_combine)
            if response.status_code == 200:
                html_source = requests.get(url_combine).text
                soup = BeautifulSoup(html_source, 'lxml')
                pagination = soup.find('div', class_='pagination')

                # Get all page-urls
                links = [link['href'] for link in pagination.find_all('a', href=True)]

                checker = None
                while checker is None:

                    html_source2 = requests.get(f'{url_root}/{links[-1]}').text
                    soup = BeautifulSoup(html_source2, 'lxml')
                    pagination = soup.find('div', class_='pagination')
                    checker = soup.find('div', class_='next disabled')
                    if checker is None:
                        for link in pagination.find_all('a', href=True):
                            links.append(link['href'])
                    else:
                        break

                # Get all first_names from all page-urls
                for link in links:
                    html_source = requests.get(f'{url_root}/{link}').text
                    soup = BeautifulSoup(html_source, 'lxml')
                    first_names = soup.find_all('td', class_='name')
                    if part_in_url_part2 == 'maedchennamen':
                        for name in first_names:
                            if name.text in database['first_names']['female_first_names']:
                                print(f"... {name.text} already in database ... skipping ...")
                            else:
                                new_name = name.text
                                database['first_names']['female_first_names'].append(new_name)
                                print(f'... 🦥 slothing first names from {url_combine} ... {name.text}')
                    elif part_in_url_part2 == 'jungennamen':
                        for name in first_names:
                            if name.text in database['first_names']['male_first_names']:
                                print(f"... {name.text} already in database ... skipping ...")
                            else:
                                new_name = name.text
                                database['first_names']['male_first_names'].append(new_name)
                                print(f'... 🦥 slothing first names from {url_combine} ... {name.text}')
                    else:
                        print('SlothGen 🦥 encountered an unusual error... Sorry!')
                print(f'Letter {chr(url_part3)} ... DONE.')
            else:
                print(f'{url_combine} not on server... continuing...')

    # Sort all first names alphabetically
    sorted_male_first_names = sorted(database['first_names']['male_first_names'])
    sorted_female_first_names = sorted(database['first_names']['female_first_names'])
    database['first_names']['male_first_names'] = sorted_male_first_names
    database['first_names']['female_first_names'] = sorted_female_first_names

    # Saving JSON database
    with open(database_name, 'w') as file:
        json.dump(database, file, indent=2)