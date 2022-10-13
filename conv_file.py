import time
import json


def conversion_file():
    """считывает файл "output.txt"
    и создает словарь с именами и временем комментария с записью в файл "conv_commet.txt """
    read_file = open('output.txt', 'r', encoding='utf-8')
    write_file = open('conv_commet.json', 'w', encoding='utf-8')
    dict_commet = {}
    dict_commet_2 = {}
    for line in read_file:
        temporary = list(line.split())
        name = ' '.join(temporary[:-2])
        data_commet = ' '.join(temporary[-2:])
        if name not in dict_commet:
            dict_commet[name] = []
            dict_commet[name].append(data_commet)
        elif name in dict_commet:
            dict_commet[name].append(data_commet)
    for key in dict_commet:
        temporary = dict_commet[key]
        temporary = sorted(temporary, key=lambda x: time.mktime(time.strptime(x, "%H:%M %d.%m.%Y")))
        dict_commet_2[key] = temporary
    print(json.dumps(dict_commet_2), file=write_file)
    read_file.close()
    write_file.close()


