import bs4
from bs4 import BeautifulSoup
from urllib.request import urlopen
html = urlopen('http://realty.dmir.ru/').read()
soup = BeautifulSoup(html, 'html.parser')
my_file = open('str.json', 'w')
my_file.write(soup)
my_file.close()