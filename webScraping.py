from bs4 import BeautifulSoup
import requests
import time
import openpyxl as xl


def web_scrape():
    start = time.time()
    wb = xl.Workbook()
    sheet = wb.active
    sheet.title = "sheet1"
    url_root = 'https://www.vorname.com'
    url_gender = ['maedchennamen', 'jungennamen']
    column = 0
    for url_gender_combine in url_gender:
        row = 1
        column += 1
        for letter in range(ord('A'), ord('Z') + 1):
            url_combine = f'{url_root}/{url_gender_combine},{chr(letter)},1.html'
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
                    female_first_names = soup.find_all('td', class_='name')
                    for name in female_first_names:
                        cell = sheet.cell(row, column)
                        cell.value = name.text
                        row += 1
                        print(f'... {row} ... {cell.value}')
            else:
                print(f'{url_combine} not on server... continuing...')

    wb.save('names_db.xlsx')
    end = time.time()
    print(f'\n{end - start}')


web_scrape()