from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time


pc_user = os.getlogin() # получаем логин юзера

option = webdriver.ChromeOptions()
option.add_argument(r'--user-data-dir=C:\Users\%s\AppData\Local\Google\Chrome\User Data\Default'
                    # путь где лежит файл cookeis
                    %pc_user)
chrome_path = r'C:\chromedriver.exe' # путь к хром драйверу
driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=option)

base_url = 'https://www.olx.kz/rabota/it-telekom-kompyutery/' # ссылка на рубрику


def get_html(url):
    driver.get(url)
    html_source = driver.page_source
    return html_source


def get_page_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    paggination = soup.find('div', class_='pager rel clr')
    return int(paggination.find_all('span', class_="item fleft")[-1].text)


def parser_top(html): # поиск топ объявлений
    soup = BeautifulSoup(html, 'html.parser')
    gold_advert = soup.find('table', class_='fixed offers breakword offers--top redesigned')

    gold_links = []

    for tr in gold_advert.find_all('tr', class_='wrap'):
        for link in tr.find_all('a', class_='marginright5 link linkWithHash detailsLink'):
            if link not in gold_links:
                gold_links.append(link['href'])

    return gold_links


def parser_free(html): # поиск обычных объявлений
    soup = BeautifulSoup(html, 'html.parser')
    free_advert = soup.find('table', class_='fixed offers breakword redesigned')

    free_links = []

    for tr in free_advert.find_all('tr', class_='wrap'):
        for link in tr.find_all('a', class_='marginright5 link linkWithHash detailsLink'):
            if link not in free_links:
                free_links.append(link['href'])

    return free_links


def parse_advert(url): # парсинг объявлений
    driver.get(url)
    driver.find_element_by_xpath('/html/body/div/div[1]/div[3]/main/aside/div[1]/section[2]/div/button').click()
    time.sleep(5)
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    telephone = soup.find('span', class_='css-0').text
    title = soup.find('div', class_='css-mkz7zu').find('h1', class_='css-1oarkq2-Text').text
    job_param = soup.find('ul', class_='css-14j8iip').find_all('p', class_='css-xl6fe0-Text eu5v0x0')
    params_list = []
    for p in job_param:
        params_list.append(p.text)
    params = '\n'.join(params_list)
    content = soup.find('div', class_='css-2t3g1w-Text').text
    print(telephone)
    print(title)
    print(params)
    print(content)
    with open(f'C:\\Users\\{pc_user}\\Desktop\\advert.txt', 'a', encoding='utf-8') as adv:
        adv.write(f'{title.upper()}\n{telephone}\n{params}\nОПИСАНИЕ\n{content}\n\n')
        adv.write('===================================================================\n\n')


def main():
    count_page = get_page_count(get_html(base_url))
    print('Найдено страниц:', count_page)

    link_top = []
    link_free = []
    all_links = []

    for page in range(1, count_page + 1):
        print('Парсинг %d%%' % (page / count_page * 100))
        link_top.extend(parser_top(get_html(base_url + '?page=%d' % page)))
        link_free.extend(parser_free(get_html(base_url + '?page=%d' % page)))

    # делаем из двух списков один
    all_links.extend(link_top)
    for link in link_free:
        if link not in all_links:
            all_links.append(link)

    # парсинг
    for advert in all_links:
        parse_advert(advert)


if __name__ == '__main__':
    main()