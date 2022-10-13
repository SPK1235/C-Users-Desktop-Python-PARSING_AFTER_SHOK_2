import time
import matplotlib.pyplot as plt
import json
import copy


def count_max_30():
    """считывает файл "output.txt"
    и создает 30-ку комментаторов по количеству комментаторов """
    global data_min, data_max, list_comments
    read_file = open('output.txt', 'r', encoding='utf-8')
    count_commet = {}
    list_max_30 = []
    number_iterations = 0
    for line in read_file:
        temporary = list(line.split())
        name = ' '.join(temporary[:-2])
        if number_iterations == 0:
            temporary_data = time.strptime(temporary[-1], "%d.%m.%Y")
            data_max = temporary_data
            data_min = temporary_data
            number_iterations += 1
            count_commet[name] = 1
        else:
            temporary_data = time.strptime(temporary[-1], "%d.%m.%Y")
            if temporary_data > data_max:
                data_max = temporary_data
            if temporary_data < data_min:
                data_min = temporary_data
            if name not in count_commet:
                count_commet[name] = 1
            elif name in count_commet:
                count_commet[name] += 1
    data_min = time.strftime('%d.%m.%y', data_min)
    data_max = time.strftime('%d.%m.%y', data_max)
    sorted_tuple = sorted(count_commet.items(), key=lambda x: x[1], reverse=True)
    list_comments = copy.deepcopy(list(sorted_tuple))
    for i in range(30):
        list_max_30.append(sorted_tuple[i])
    return list_max_30


def schedule_max_30(list_max_30):
    """Построение графика 30-ки комментаторов и их количества комментариев"""
    global data_min, data_max
    name = []
    col_commet = []
    for i in list_max_30:
        name.append(i[0])
        col_commet.append(i[1])
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.ylabel('Число комментариев')
    plt.xlabel('Nickname комментатора')
    plt.title(f'30-ка комментаторов с {data_min} по {data_max}')
    ax.bar(name, col_commet, color='blue')
    """y_point = (max(col_commet) * 3 / 100)
    for i in range(len(name)):
        x_point = i - 0.1
        ax.text(x_point, y_point, f'{name[i]}', color='black').set_rotation(90)
    for i in range(len(name)):
        if len(str(col_commet[i])) <= 3:
            x_point = i - 0.2
        else:
            x_point = i - 0.3
        y_point = col_commet[i] + (max(col_commet) * 2.5 / 100)
        ax.text(x_point, y_point, f'{col_commet[i]}', color='black').set_rotation(0)"""
    for label in ax.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(90)
        label.set_fontsize(6)
    plt.show()


def number_author_comments(name):
    """Построение графика количества комментариев автора под ником 'name' по числам"""
    global data_min, data_max, list_weekend_22
    read_file = open('conv_commet.json', 'r', encoding='utf-8')
    list_authors_comments = read_file.read()
    dict_authors_comments = json.loads(list_authors_comments)
    author_comments = dict_authors_comments[name]
    comments_data = {}
    for data in author_comments:
        temporary_data = time.strptime(data, "%H:%M %d.%m.%Y")
        temporary_data = time.strftime("%d.%m.%Y", temporary_data)
        if temporary_data not in comments_data:
            comments_data[temporary_data] = 0
        comments_data[temporary_data] += 1
    col_comments = []
    data = []
    for key, value in comments_data.items():
        data.append(key)
        col_comments.append(value)
    col_comments_working_day = []
    col_comments_week_day = []
    for i in range(len(data)):
        if data[i] in list_weekend_22:
            col_comments_week_day.append(col_comments[i])
            col_comments_working_day.append(0)
        else:
            col_comments_working_day.append(col_comments[i])
            col_comments_week_day.append(0)
    fig_1 = plt.figure()
    ax_1 = fig_1.add_subplot()
    ax_1.set_ylabel('Число комментариев в день')
    ax_1.set_xlabel('Даты активности')
    ax_1.set_title(f'Активность {name} с {data_min} по {data_max}')
    ax_1.bar(data, col_comments_working_day, color='blue')
    ax_1.bar(data, col_comments_week_day, color='red')
    for label in ax_1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(90)
        label.set_fontsize(5)
    plt.show()


def number_author_comments_hour(name):
    """Построение графика количества комментариев автора под ником 'name' по числам и часам"""
    global data_min, data_max, list_weekend_22
    read_file = open('conv_commet.json', 'r', encoding='utf-8')
    list_authors_comments = read_file.read()
    dict_authors_comments = json.loads(list_authors_comments)
    author_comments = dict_authors_comments[name]
    comments_data = {}
    data = []
    for dt in author_comments:
        temporary_data = time.strptime(dt, "%H:%M %d.%m.%Y")
        temporary_time_hour = int(time.strftime("%H", temporary_data))
        temporary_time_minute = int(time.strftime("%M", temporary_data)) / 60
        temporary_time = temporary_time_hour + temporary_time_minute
        temporary_time = round(temporary_time, 2)
        temporary_data = time.strftime("%d.%m.%Y", temporary_data)
        if temporary_data not in comments_data:
            comments_data[temporary_data] = []
        comments_data[temporary_data].append(temporary_time)
        if temporary_data not in data:
            data.append(temporary_data)
    fig_1 = plt.figure()
    ax_1 = fig_1.add_subplot()
    ax_1.set_ylabel('Время в часах')
    ax_1.set_xlabel('Даты активности')
    ax_1.set_title(f'Активность {name} с {data_min} по {data_max}')
    n = 1
    for i in range(len(data)):
        for dt in comments_data[data[i]]:
            if data[i] in list_weekend_22:
                ax_1.scatter(data[i], dt, color='red')
            else:
                ax_1.scatter(data[i], dt, color='blue')
            print(f'n = {n}')
            n += 1
    for label in ax_1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(90)
        label.set_fontsize(5)
    plt.show()


def article_views_day():
    """считывает файл "views_day.json"
    и создает график общего просмотра статей за день"""
    global data_min, data_max
    read_file = open('views_day.json', 'r', encoding='utf-8')
    views_day = read_file.read()
    dict_views_day = json.loads(views_day)
    list_views_day = dict_views_day.items()
    list_views_day = sorted(list_views_day, key=lambda x: time.mktime(time.strptime(x[0], "%d.%m.%Y")))
    dict_views_day = dict(list_views_day)
    data = list(dict_views_day.keys())
    views = list(dict_views_day.values())
    fig_1 = plt.figure()
    ax_1 = fig_1.add_subplot()
    ax_1.set_ylabel('Число просмотров в день')
    ax_1.set_xlabel('Даты активности')
    ax_1.set_title(f'График общего просмотра статей за день с {data_min} по {data_max}')
    ax_1.bar(data, views, color='blue')
    for label in ax_1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(90)
        label.set_fontsize(5)
    plt.show()


def number_articles_author():
    """считывает файл "author.json"
    и создает График 30 самых результативных авторов за выбранный период"""
    global data_min, data_max
    read_file = open('author.json', 'r', encoding='utf-8')
    dict_articles_author = json.loads(read_file.read())
    list_articles_author = dict_articles_author.items()
    list_articles_author = sorted(list_articles_author, key=lambda x: x[1], reverse=True)
    dict_articles_author = dict(list_articles_author[:30])
    author = list(dict_articles_author.keys())
    number = list(dict_articles_author.values())
    fig_1 = plt.figure()
    ax_1 = fig_1.add_subplot()
    ax_1.set_ylabel('Количество статей')
    ax_1.set_xlabel('Автор')
    ax_1.set_title(f'График 30 самых результативных авторов с {data_min} по {data_max}')
    ax_1.bar(author, number, color='blue')
    for label in ax_1.xaxis.get_ticklabels():
        label.set_color('black')
        label.set_rotation(90)
        label.set_fontsize(6)
    plt.show()


def intersection_authors_commentators():
    global data_min, data_max, list_comments, dict_articles_author
    dict_comments = dict(list_comments)
    set_comments = set(dict_comments.keys())
    print(f'За период с {data_min} по {data_max} количество комментаторов = {len(set_comments)}')
    read_file = open('author.json', 'r', encoding='utf-8')
    dict_articles_author = json.loads(read_file.read())
    set_articles_author = set(dict_articles_author.keys())
    print(f'За период с {data_min} по {data_max} количество авторов = {len(set_articles_author)}')
    set_intersection = set_comments & set_articles_author
    print(f'Из них , авторов которые комментируют = {len(set_intersection)}')


data_max = ''
data_min = ''
list_comments = []
dict_articles_author = {}
list_weekend_22 = ['01.01.2022', '02.01.2022', '03.01.2022', '04.01.2022', '05.01.2022', '06.01.2022', '07.01.2022',
                   '08.01.2022', '09.01.2022', '15.01.2022', '16.01.2022', '22.01.2022', '23.01.2022', '29.01.2022',
                   '30.01.2022', '05.02.2022', '06.02.2022', '12.02.2022', '13.02.2022', '19.02.2022', '20.02.2022',
                   '23.02.2022', '26.02.2022', '27.02.2022', '06.03.2022', '07.03.2022', '08.03.2022', '12.03.2022',
                   '13.03.2022', '19.03.2022', '20.03.2022', '26.03.2022', '27.03.2022', '02.04.2022', '03.04.2022',
                   '09.04.2022', '10.04.2022', '16.04.2022', '17.04.2022', '23.04.2022', '24.04.2022', '30.04.2022',
                   '01.05.2022', '02.05.2022', '03.05.2022', '07.05.2022', '08.05.2022', '09.05.2022', '10.05.2022',
                   '14.05.2022', '15.05.2022', '21.05.2022', '22.05.2022', '28.05.2022', '29.05.2022', '04.06.2022',
                   '05.06.2022', '11.06.2022', '12.06.2022', '13.06.2022', '18.06.2022', '19.06.2022', '25.06.2022',
                   '26.06.2022', '02.07.2022', '03.07.2022', '09.07.2022', '10.07.2022', '16.07.2022', '17.07.2022',
                   '23.07.2022', '24.07.2022', '30.07.2022', '31.07.2022', '06.08.2022', '07.08.2022', '13.08.2022',
                   '14.08.2022', '20.08.2022', '21.08.2022', '27.08.2022', '28.08.2022', '03.09.2022', '04.09.2022',
                   '10.09.2022', '11.09.2022', '17.09.2022', '18.09.2022', '24.09.2022', '25.09.2022', '01.10.2022',
                   '02.10.2022', '08.10.2022', '09.10.2022', '15.10.2022', '16.10.2022', '22.10.2022', '23.10.2022',
                   '29.10.2022', '30.10.2022', '04.11.2022', '05.11.2022', '06.11.2022', '12.11.2022', '13.11.2022',
                   '19.11.2022', '20.11.2022', '26.11.2022', '27.11.2022', '03.12.2022', '04.12.2022', '10.12.2022',
                   '11.12.2022', '17.12.2022', '18.12.2022', '24.12.2022', '25.12.2022', '31.12.2022']

"""count_max_30()
intersection_authors_commentators()"""
