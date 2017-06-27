import bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen
html = urlopen('http://realty.dmir.ru/').read()
soup = BeautifulSoup(html, 'html.parser')
print(soup)