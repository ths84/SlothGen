from bs4 import BeautifulSoup
import requests
import openpyxl as xl


def web_scraping_last_names():
    url = 'https://de.wiktionary.org/wiki/Verzeichnis:Deutsch/Namen/die_häufigsten_Nachnamen_Deutschlands'
    html_source = requests.get(url).text
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(html_source, 'lxml')
        content_block = soup.find('ol')

        wb = xl.load_workbook('names_db.xlsx')
        sheet = wb["sheet1"]
        row = 1
        column = 3
        for name in content_block.find_all('a', title=True):
            cell = sheet.cell(row, column)
            cell.value = name.text
            row += 1
            print(f'... {row} {cell.value}')
    else:
        print(f'{url} not on server... continuing...')

    wb.save('names_db.xlsx')


web_scraping_last_names()