





from bs4 import BeautifulSoup

no_new_url = False
set_new_url = f'{url_root}/{links[0]}'
while no_new_url is False:
    for link in links:
        if set_new_url == f'{url_root}/{links[-1]}':
            no_new_url = True
        else:
            html_source = requests.get(f'{url_root}/{link}').text
            soup = BeautifulSoup(html_source, 'lxml')
            female_first_names = soup.find_all('td', class_='name')
            set_new_url = f'{url_root}/{link}'
            for name in female_first_names:
                print(name.text)













with open('Home.html', 'r') as html_file:
    content = html_file.read()

    # New instance of BeautifulSoup with Home.html as argument
    # soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify())
    #names_in_html_tags = soup.find_all('h5')
    #for name in names_in_html_tags:
    #    output = name.text
    #    print(output.strip())

    soup = BeautifulSoup(content, 'lxml')

    html_first_names = soup.find_all('td', class_='name')

    for name in html_first_names:
        print(name.text)






for column in range(1, sheet.max_column + 1):
    for row in range(1, sheet.max_row + 1):
        cell = sheet.cell(row, column)
        if cell.value is not None and column == 1:
            first_name = cell.value
        elif cell.value is not None and column == 2:
            middle_name = cell.value
        elif cell.value is not None and column == 3:
            last_name = cell.value
        else:
            break




