import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


def formation_url(current_page):
    """формирование url страницы"""
    url = 'https://aftershock.news/' + '?q=front&page=' + str(current_page)
    return url


def formation_url_article(node):
    """формирование url статьи"""
    url = 'https://aftershock.news/?q=node/' + str(node)
    return url


def formation_url_commet(url, number):
    """формирование url комментариев"""
    url = url + '&page=' + str(number) + '#comments'
    return url


def date_translation(my_data):
    """формирование даты комментария"""
    date_now = datetime.today().date()
    date_now = date_now.strftime('%d.%m.%Y')
    month_translation = {'Янв': '01', 'Фев': '02', 'Мар': '03', 'Апр': '04', 'Мая': '05', 'Июн': '06', 'Июл': '07',
                         'Авг': '08', 'Сен': '09', 'Окт': '10', 'Ноя': '11', 'Дек': '12',
                         'янв': '01', 'фев': '02', 'мар': '03', 'апр': '04', 'мая': '05', 'июн': '06', 'июл': '07',
                         'авг': '08', 'сен': '09', 'окт': '10', 'ноя': '11', 'дек': '12'}
    if len(my_data) == 5:
        result_data = my_data + ' ' + date_now
    else:
        if len(my_data) == 14:
            my_data = my_data[:6] + '0' + my_data[6:]
        temp = month_translation[my_data[9:12]]
        my_data = my_data[:9] + temp + my_data[12:]
        result_data = datetime.strptime(my_data, '%H:%M-%d/%m/%y')
        result_data = result_data.strftime('%H:%M %d.%m.%Y')
    return result_data


def date_translation_2(my_data):
    """формирование даты публикации статьи"""
    month_translation = {'Янв': '01', 'Фев': '02', 'Мар': '03', 'Апр': '04', 'Мая': '05', 'Июн': '06', 'Июл': '07',
                         'Авг': '08', 'Сен': '09', 'Окт': '10', 'Ноя': '11', 'Дек': '12',
                         'янв': '01', 'фев': '02', 'мар': '03', 'апр': '04', 'мая': '05', 'июн': '06', 'июл': '07',
                         'авг': '08', 'сен': '09', 'окт': '10', 'ноя': '11', 'дек': '12'}
    if len(my_data) == 17:
        my_data = my_data[:8] + '0' + my_data[8:]
    print(f'my_data = {my_data} , len = {len(my_data)}')
    temp = month_translation[my_data[11:14]]
    my_data = my_data[:11] + temp + my_data[14:]
    my_data = list(my_data.split())
    my_data = ''.join(my_data)
    result_data = datetime.strptime(my_data, '%H:%M-%d/%m/%y')
    result_data = result_data.strftime('%d.%m.%Y')
    return result_data


def get_content_page(url, header):
    """получение списка всех id статей на странице, количества просмотров и авторов статей"""
    global dict_author, dict_number_views
    resp = requests.get(url, headers=header)
    list_article_id = []
    try:
        if resp.status_code == 200:
            page = BeautifulSoup(resp.content, "html.parser")
            article_div = page.find_all('div', attrs={'class': 'node node-blog node-teaser'})
            for article in article_div:
                tmp = article.get('id')
                tmp = list(tmp.split('-'))
                list_article_id.append(tmp[1])
                data_div = article.find('span', attrs={'class': 'aft-postdateicon'})
                data_text = data_div.text
                data_text = date_translation_2(data_text)
                views_div = article.find('span', attrs={'class': 'aft-postcounter'})
                views_list = list(views_div.get('title').split())
                views = int(views_list[2])
                if data_text not in dict_number_views:
                    dict_number_views[data_text] = 0
                dict_number_views[data_text] += views
                author_div = article.find('a', attrs={'username user-tooltip'})
                author = author_div.text
                if author not in dict_author:
                    dict_author[author] = 0
                dict_author[author] += 1
            return list_article_id
    except ConnectionResetError:
        print('ERROR !!!')


def get_content_article(url, header):
    """полечение количества страниц с комментариями и получение списка комментаторов с датами"""
    resp = requests.get(url, headers=header)
    number_comments = 0
    number_pages = []
    commets = []
    try:
        if resp.status_code == 200:
            page = BeautifulSoup(resp.content, "html.parser")
            try:
                number_pages_div = page.find('div', attrs={'class': 'aft-pager'})
                number_pages_a = number_pages_div.find_all('a')
                for number in number_pages_a:
                    tmp = number.get('href')
                    number_pages.append(tmp[-1])
                number_pages = list(map(int, number_pages))
                number_pages = max(number_pages)
            except:
                number_pages = 0
            for i in range(number_pages + 1):
                try:
                    url_commet = formation_url_commet(url, i)
                    resp_commet = requests.get(url_commet, headers=header)
                    page = BeautifulSoup(resp_commet.content, "html.parser")
                    blok_commets = page.find('div', attrs={'class': 'aft-comments comment-wrapper'})
                    users = blok_commets.find_all('div', attrs={'class': 'aft-comment aft-postcontent comment'})
                    for user in users:
                        tmp = user.get('data-name')
                        tmp_1 = user.find('span', attrs={'class': 'comment_date'})
                        tmp_1 = tmp_1.text
                        tmp_1 = date_translation(tmp_1)
                        commets.append(tmp + ' ' + tmp_1)
                        number_comments += 1
                    blok_commets = page.find('div', attrs={'class': 'aft-comments comment-wrapper'})
                    users = blok_commets.find_all('div', attrs={'class': 'aft-comment aft-postcontent comment comment-by-node-author'})
                    for user in users:
                        tmp = user.get('data-name')
                        tmp_1 = user.find('span', attrs={'class': 'comment_date'})
                        tmp_1 = tmp_1.text
                        tmp_1 = date_translation(tmp_1)
                        number_comments += 1
                        commets.append(tmp + ' ' + tmp_1)
                except:
                    continue
            print(f'количество комментариев :  {number_comments}')
            return commets
    except ConnectionResetError:
        print('ERROR !!!')


def parser():
    global dict_author, dict_number_views
    print('Осуществляется парсинг сайта "aftershock.news" ')
    many_pages = int(input('Сколько страниц парсить : '))
    current_page = 0  # текущия страница
    header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) Gecko/20100101 Firefox/103.0'}
    write_file_1 = open('output.txt', 'w', encoding='utf-8')
    write_file_2 = open('views_day.json', 'w', encoding='utf-8')
    write_file_3 = open('author.json', 'w', encoding='utf-8')
    list_global_article_id = []
    for i in range(many_pages):
        url = formation_url(current_page)
        list_article_id = get_content_page(url, header)
        for node in list_article_id:
            if node not in list_global_article_id:
                list_global_article_id.append(node)
                url = formation_url_article(node)
                temp = get_content_article(url, header)
                try:
                    for tmp in temp:
                        print(tmp, file=write_file_1)
                except:
                    continue
        current_page += 1
        print(f'обработано страниц : {current_page}')
    print(json.dumps(dict_number_views), file=write_file_2)
    print(json.dumps(dict_author, ensure_ascii=False), file=write_file_3)
    write_file_1.close()
    write_file_2.close()
    write_file_3.close()


dict_author = {}  # список авторов и их количество статей
dict_number_views = {}  # количество посещений в день
#parser()