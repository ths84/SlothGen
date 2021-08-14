from bs4 import BeautifulSoup
import requests

url_root = 'https://www.vorname.com'
for letter in range(ord('A'), ord('Z') + 1):
    url_combine = f'{url_root}/maedchennamen,{chr(letter)},1.html'
    response = requests.get(url_combine)
    if response.status_code == 200:

    print(response.status_code)

    html_source = requests.get(url_combine).text
    soup = BeautifulSoup(html_source, 'lxml')





