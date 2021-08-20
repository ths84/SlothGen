from bs4 import BeautifulSoup
import requests
import re
import json


def scraping_last_names_surnameweb(database_name):
    # Load JSON database
    with open(database_name) as file:
        database = json.load(file)

    url_root = 'http://www.surnameweb.org/registry/'
    html_source = requests.get(url_root).text
    response = requests.get(url_root)
    if response.status_code == 200:
        soup = BeautifulSoup(html_source, 'lxml')
        found_urls = soup.find_all('a', href=True)
        all_urls = []
        for i in found_urls:
            url_part2 = i.text
            if len(i.text) == 6:
                url_combined = f'{url_root}{url_part2}'
                all_urls.append(url_combined)

        for url in all_urls:
            html_source = requests.get(url).text
            soup = BeautifulSoup(html_source, 'lxml')
            section = soup.find('blockquote')
            if "Surname" in section.text:
                last_name = section.text
                last_name_cleaned = re.sub(r'\sSurname', '', last_name)
                if "," in last_name_cleaned:
                    last_name_cleaned = re.sub(r'\s,\s', '', last_name_cleaned)
                last_name_cleaned = last_name_cleaned.split()

                for name in last_name_cleaned:
                    if name in database['last_names']:
                        print(f"... {name} already in database ... skipping ...")
                    else:
                        database['last_names'].append(name)
                        print(f'... 🦥 slothing last names from {url} ... {name}')

    else:
        print(f'{url_root} not on server... continuing...')

    # Sort names alphabetically
    sorted_last_names = sorted(database['last_names'])
    database['last_names'] = sorted_last_names

    # Saving JSON database
    with open(database_name, 'w') as file:
        print('DONE ... SAVING.')
        json.dump(database, file, indent=2)


def scraping_last_names_wikipedia(database_name):
    # Load JSON database
    with open(database_name) as file:
        database = json.load(file)

    url = 'https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen/die_häufigsten_Nachnamen_Deutschlands'
    html_source = requests.get(url).text
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(html_source, 'lxml')
        content_block = soup.find('ol')

        for name in content_block.find_all('a', title=True):
            if name.text in database['last_names']:
                print(f"... {name.text} already in database ... skipping ...")
            else:
                new_name = name.text
                database['last_names'].append(new_name)
                print(f'... 🦥 slothing last names from {url} ... {name.text}')
    else:
        print(f'{url} not on server... continuing...')

    # Sort names alphabetically
    sorted_last_names = sorted(database['last_names'])
    database['last_names'] = sorted_last_names

    # Saving JSON database
    with open(database_name, 'w') as file:
        print('DONE ... SAVING.')
        json.dump(database, file, indent=2)


def scraping_last_names_familyeducationdotcom(database_name):
    # Load JSON database
    with open(database_name) as file:
        database = json.load(file)

    url_root = 'https://www.familyeducation.com/baby-names/browse-names/surname'
    for url_appendix in range(ord('a'), ord('z') + 1):
        url_combine = f'{url_root}/{chr(url_appendix)}'
        html_source = requests.get(url_combine).text
        response = requests.get(url_combine)
        if response.status_code == 200:
            soup = BeautifulSoup(html_source, 'lxml')

            # Find page links on site for set surname starting with url_appendix
            pagination = soup.find('ul', {'class': 'pager__items js-pager__items pagination'})

            if pagination is not None:
                # Get page links from first site for set surname starting with url_appendix
                links = [link['href'] for link in pagination.find_all('a', href=True)]
                for i in range(1, 3):
                    del links[-1]

                # Get last available page link for set surname starting with url_appendix
                pagination_last = soup.find('li', {'class': 'pager__item pager__item--last hide-li'})
                last_page_url = pagination_last.find('a', href=True)
                links.append(last_page_url['href'])

                # Fill in missing page links
                first_string = links[-2]
                last_string = links[-1]
                num_first_string = int(re.search(r'\d+', first_string).group())
                num_last_string = int(re.search(r'\d+', last_string).group())

                missing_links = []
                for i in range(num_first_string, num_last_string):
                    missing_links.append(f'?page={i}')

                in_links = set(links)
                in_missing_links = set(missing_links)
                in_links_but_not_in_missing_links = in_missing_links - in_links
                complete_links = links + list(in_links_but_not_in_missing_links)

                # Get names from all pages for set surname
                for link in complete_links:
                    html_source = requests.get(f'{url_root}/{chr(url_appendix)}{link}').text
                    soup = BeautifulSoup(html_source, 'lxml')
                    section = soup.find('section', {'id': 'block-fentheme-content'})
                    names_list = section.find_all('a', {'href': re.compile("/baby-names/name-meaning/")})
                    for name in names_list:
                        if name.text in database['last_names']:
                            print(f"... {name.text} already in database ... skipping ...")
                        else:
                            new_name = name.text
                            database['last_names'].append(new_name)
                            print(f'... 🦥 slothing last names from {url_combine} ... {name.text}')
                print(f'Letter {chr(url_appendix).capitalize()} ... DONE.')
            else:
                print(f'No pagination found on site; continuing to scrape ...')
                html_source = requests.get(f'{url_root}/{chr(url_appendix)}').text
                soup = BeautifulSoup(html_source, 'lxml')
                section = soup.find('section', {'id': 'block-fentheme-content'})
                names_list = section.find_all('a', {'href': re.compile("/baby-names/name-meaning/")})
                for name in names_list:
                    if name.text in database['last_names']:
                        print(f"... {name.text} already in database ... skipping ...")
                    else:
                        new_name = name.text
                        database['last_names'].append(new_name)
                        print(f'... 🦥 slothing last names from {url_combine} ... {name.text}')
                print(f'Letter {chr(url_appendix).capitalize()} ... DONE ... SAVING.')

        else:
            print(f'{url_root} not on server... continuing...')

    # Sort names alphabetically
    sorted_last_names = sorted(database['last_names'])
    database['last_names'] = sorted_last_names

    # Saving JSON database
    with open(database_name, 'w') as file:
        print('DONE ... SAVING.')
        json.dump(database, file, indent=2)