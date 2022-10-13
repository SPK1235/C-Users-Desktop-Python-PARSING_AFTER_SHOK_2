from parser import parser
from conv_file import conversion_file
import count
import os
import sys
import time

if __name__ == '__main__':
    print('ПАРСИНГ САЙТА "aftershock.news" и смотрим активность комментаторов !!!')
    request_1 = input('Осуществить парсинг ? (да/нет) : ')
    flag_request_1 = False
    while not flag_request_1:
        if request_1 == 'да':
            parser()
            conversion_file()
            flag_request_1 = True
        elif request_1 == 'нет':
            list_file = os.listdir()
            for name in list_file:
                if name == 'output.txt':
                    flag_request_1 = True
                    time_file = time.ctime(os.path.getctime(name))
                    time_file = time.strptime(time_file, "%a %b %d %H:%M:%S %Y")
                    time_file = time.strftime("%d.%m.%Y", time_file)
                    print()
                    print('*' * 100)
                    print()
                    print(f'В системе есть файл "output.txt" за {time_file}')
                    break
            else:
                print()
                print('*' * 100)
                print()
                print('ERROR : НЕТ ФАЙЛА "output.txt" . Дальнейшая работа не возможна !  ')
                sys.exit()
        else:
            flag_request_1 = False
            request_1 = input('Я не понял , так будем парсить или нет ??? (да/нет) : ')
    print()
    print('*' * 100)
    print()
    list_max_30 = count.count_max_30()
    count.intersection_authors_commentators()
    print()
    print('*' * 100)
    print()
    otv = input(f'Выводим график просмотра статей за день за период с {count.data_min} по {count.data_max} ? (да/нет) : ')
    if otv == 'да':
        count.article_views_day()
    print()
    print('*' * 100)
    print()
    request_2 = input('Вывести 30 самых плодовитых авторов ? (да/нет) : ')
    flag_request_2 = False
    while not flag_request_2:
        if request_2 == 'да':
            flag_request_2 = True
            count.number_articles_author()
            print()
            print('*' * 100)
            print()
        elif request_2 == 'нет':
            print()
            print('*' * 100)
            print()
            flag_request_2 = True
        else:
            flag_request_2_1 = False
            print()
            print('*' * 100)
            print()
            request_2_1 = input('Не понял твоего ответа ! Введи да/нет : ')
    request_2_1 = input('Вывести 30-ку самых результативных комментаторов ? (да/нет) : ')
    flag_request_2_1 = False
    list_name_commet = []
    while not flag_request_2_1:
        if request_2_1 == 'да':
            flag_request_2_1 = True
            count.schedule_max_30(list_max_30)
            print()
            print('*' * 100)
            print()
            print('Список 30-ти самых результативных комментатора :')
            print()
            for i in list_max_30:
                tmp = ''
                if i[0] in count.dict_articles_author:
                    tmp = count.dict_articles_author[i[0]]
                    print(f'{i[0]} : {i[1]} комментариев и {tmp} статей')
                else:
                    print(f'{i[0]} : {i[1]} комментариев')
                list_name_commet.append(i[0])
            print()
            print('*' * 100)
            print()
            flag_request_2_1 = True
        elif request_2_1 == 'нет':
            print()
            print('*' * 100)
            print()
            sys.exit()
        else:
            flag_request_2_1 = False
            print()
            print('*' * 100)
            print()
            request_2_1 = input('Не понял твоего ответа ! Введи да/нет : ')
    flag_request_3 = False
    request_3 = input('Введи имя комментатора из списка или "нет" : ')
    while not flag_request_3:
        if request_3 in list_name_commet:
            print()
            print('*' * 100)
            print()
            print(f'График активности {request_3} по дням')
            count.number_author_comments(request_3)
            print()
            print('*' * 100)
            print()
            print(f'График активности {request_3} по дням и часам')
            count.number_author_comments_hour(request_3)
            print()
            print('*' * 100)
            print()
            print('Список 30-ти самых результативных комментатора :')
            print()
            for i in list_max_30:
                tmp = ''
                if i[0] in count.dict_articles_author:
                    tmp = count.dict_articles_author[i[0]]
                    print(f'{i[0]} : {i[1]} комментариев и {tmp} статей')
                else:
                    print(f'{i[0]} : {i[1]} комментариев')
            print()
            print('*' * 100)
            print()
            request_3 = input('Введи имя следующего комментатора из списка или "нет" : ')
        elif request_3 == 'нет':
            print()
            print('*' * 100)
            print()
            sys.exit()
        else:
            print()
            print('*' * 100)
            print()
            request_3 = input('Введи имя комментатора без ошибок : ')


