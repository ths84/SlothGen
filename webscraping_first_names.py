from bs4 import BeautifulSoup
import requests
import openpyxl as xl


def web_scrape_first_names(wb_filename):
    wb = xl.load_workbook(wb_filename)
    sheet = wb.active
    url_root = 'https://www.vorname.com'
    url_part2 = ['maedchennamen', 'jungennamen']
    column = 0
    for part_in_url_part2 in url_part2:
        row = 1
        column += 1
        for url_part3 in range(ord('A'), ord('Z') + 1):
            wb.save(wb_filename)
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
                    female_first_names = soup.find_all('td', class_='name')
                    for name in female_first_names:
                        cell = sheet.cell(row, column)
                        cell.value = name.text
                        row += 1
                        print(f'... {row} ... {cell.value}')
            else:
                print(f'{url_combine} not on server... continuing...')

    wb.save(wb_filename)