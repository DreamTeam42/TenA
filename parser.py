from bs4 import BeautifulSoup
import requests
import json
import time

# начальная страница для парсинга
start_url = 'http://realty.dmir.ru/msk/sale/prodazha-gorodskoy-nedvizhimosti-v-moskve/'

# функция парсинга ссылок на объявления
def get_all_urls(url):
    url_list = []
    # получаем html страницы
    page = requests.get(url).text
    # разбираем объявление на теги
    soup = BeautifulSoup(page, 'html.parser')
    # проходим по всем объектам объявлений
    for item in soup.find_all('li', class_='item'):
        # вытаскиваем ссылку на страницу
        ad_url = item.find('a', class_='absItemLink-').attrs['href']
        # добавляем в список
        url_list.append(ad_url)
    return url_list

# функция сбора ссылок на объявления
def get_list():
    # получаем html страницы
    page = requests.get(start_url).text
    # print(page)
    # разбираем объявление на теги
    soup = BeautifulSoup(page, 'html.parser')
    # считаем количество объявлений на странице
    ad_in_page = len(soup.find_all('li', class_='item'))
    # получаем общее количество объявлений
    ad_count = int(soup.find('table', class_='sort-resultlist').tr.th.b.text)
    # print(ad_count)
    # расчитываем количество страниц
    page_count = ad_count // ad_in_page + 1
    # пустой список для записи ссылок
    all_url_pages = []
    for index in range(1, 5):
        # собираем url страницы
        page_to_parse = '{}?page={}'.format(start_url, index)
        # получаем список ссылок и добавлем его
        all_url_pages.extend(get_all_urls(page_to_parse))
        #print(page_to_parse)
    return all_url_pages

# функция парсинга общих параметров
def pars(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    list = {}

    price = soup.find('span', class_='tag').text.strip().strip()
    list['Цена'] = price

    try:
        meter_price = soup.find('li', class_='meterprice').b.text.strip()
        list['Цена за метр'] = meter_price
    except AttributeError:
        list['Цена за метр'] = "не указана"

    count_of_rooms = (soup.find('li', class_='rooms').b.text)
    list['Количество комнат']=count_of_rooms
    all_square = (soup.find('li', class_='square').b.text)
    list['Общая площадь'] = all_square
    try:
        metro = ' '.join([i.strip() for i in soup.find('li', class_='metro').text.split()])
        list['Метро'] = metro
    except AttributeError: list['Метро'] = "нет"

    floor = ' '.join([i.strip() for i in soup.find('li', class_='floor').text.split()])
    list['Этаж'] = floor
    description = soup.find('div', class_='mb20 objectDesc').text
    list['Описание'] = description

    # контактная информация
    try:
        posted = soup.find('a', class_='cap').text.strip()
        list['Разместил'] = posted
        # компания
        if(posted == 'менеджер компании'):
            corp = soup.find_all('dd')[3].text
            list['Компания'] = corp
    except AttributeError: list['Разместил'] = "нет"

    try:
        date = soup.find_all('dd')[4].text
        list['Дата размещения'] = date
    except IndexError: list['Дата размещения'] = soup.find_all('dd')[2].text
    phone = soup.find('div', class_='phone').text
    list['Телефон'] = phone

    # сбор информация по карте
    map_url = soup.find('figure', class_='cardmap').a.attrs['href'][27:].split('|')
    map_info = {}
    for item in map_url:
        ident, value = item.split('=')
        map_info[ident] = value
    # информация по карте
    print(map_info)
    image_urls = []
    for image in soup.find_all('input', class_="_imageViewerMini"):
        image_urls.append(image.attrs['data-full'])
    list['Адрес'] = image_urls

    return list

def main():
    list_url = get_list()
    for index in list_url:
        url = list_url[index]
        index += 1
        pars(url)

    return list


if __name__ == '__main__':
    page = requests.get(start_url).text
    soup = BeautifulSoup(page, 'html.parser')
    ad_count = int(soup.find('table', class_='sort-resultlist').tr.th.b.text)
    main_list = [0]*3
    print('Начал')

    list_url = get_list()
    for index in range(3):
        url = list_url[index]
        main_list[index] = pars(url)

    print('Закончил')

    with open('data.json', 'w', encoding='cp1251') as file:
            json.dump(main_list, file, indent = 2, ensure_ascii = False)

    print('Данные загружены в data.json')
