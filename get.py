from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    # ссылка на объявление
    url_page = 'http://realty.dmir.ru/sale/kvartira-nikolskoe-157829466/'
    r = requests.get(url_page)
    soup = BeautifulSoup(r.text, 'html.parser')
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
    print(image_urls)
