from bs4 import BeautifulSoup
import requests

if __name__ == '__main__':
    # ссылка для парсинга
    url_page = 'http://bash.im/'
    # получаем содержимое страницы
    r = requests.get(url_page)
    # преобразуем текст в структуру BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    # находим тег div с id='body'
    body = soup.find('div', id='body')
    if body is None:
        # если нет такого блока, то выходим
        exit()
    # итерируемся по всем div блокам с классом quote
    for item in body.find_all('div', 'quote'):
        # находим блок с рейтингом
        rate_block = item.find('span', 'rating')
        if rate_block is None:
            # если нет, то игнорируем
            continue
        # получаем значение рейтинга
        rate = rate_block.text
        # собираем ссылку на пост
        link = url_page[:-1] + item.find('a', 'id').attrs['href']
        # получаем текст поста
        text = item.find('div', 'text').get_text()
        print('[{}, {}] {}'.format(rate, link, text))
