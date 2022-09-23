from tika import parser
import re


def pdftotext(filename):
    """
    Функция принимает pdf и возвращает построчный список.
    :param filename: Файл pdf.
    :return: Построчный список.
    """
    raw = parser.from_file(filename)
    text_pdf = raw['content']
    return text_pdf.split("\n")


def razborka(list_text, dict_text):
    """
    Функция разбирает построчный список по шаблону с помощью регулярных выражению.
    :param list_text: Построчный список.
    :param dict_text: Словарь с разобранными значениями.
    :return: Возвращает словарь значений.
    """
    for count_str in range(len(list_text)):
        # print("=",text[count_str])
        if len(list_text[count_str]) > 0 and \
                re.fullmatch(r'[а-яА-Я ]{'+str(len(list_text[count_str]))+r'}', list_text[count_str]) and \
                re.fullmatch(r'[a-zA-Zа-яА-Я *.,-:0-9@ ]{'+str(len(list_text[count_str+1]))+r'}', list_text[count_str+1]) and \
                len(list_text[count_str+1]) > 0 and len(list_text[count_str+2]) == 0 and \
                re.fullmatch(r'[0-9 , ]{'+str(len(list_text[count_str+3]))+r'}', list_text[count_str+3]):
            # print(text[count_str])
            # print(text[count_str + 1])
            # print(text[count_str + 2])
            # print(text[count_str + 3])
            # print("=====")
            try:
                price, _ = list_text[count_str+3].split(' ')
            except:
                price = list_text[count_str+3]
            price = price.replace(',', '.')
            price = price.replace(' ', '')
            if dict_text.get(list_text[count_str+1]):
                dict_text[list_text[count_str + 1]] += float(price)
            else:
                dict_text[list_text[count_str + 1]] = float(price)
    return dict_text


def sort_dict(dict_trat, dict_val):
    """
    Функция сортирует словарь объединяя согласно шаблону в регулярном выражении.
    :param dict_trat: Словарь готовых данных.
    :param dict_val: Словарь шаблонов.
    :return: Сгруппированный словарь
    """
    dict_sort = {}
    for val in dict_val:
        dict_sort[val] = 0
        for trat in dict_trat:
            if re.search(rf"{dict_val[val]}", trat):
                dict_sort[val] += dict_trat[trat]
    return dict_sort


def sort_dict2(dict_trat, dict_val):
    """
    Функция сортирует словарь объединяя согласно шаблона в регулярном выражении.
    :param dict_trat: Словарь готовых данных.
    :param dict_val: Словарь шаблонов.
    :return: Сгруппированный словарь
    """
    dict_sort = {}
    for val in dict_val:
        dict_sort[val] = 0
    for trat in dict_trat:
        flag = False
        for val in dict_val:
            if re.search(rf"{dict_val[val]}", trat):
                flag = True
                dict_sort[val] += dict_trat[trat]
        if not flag:
            print(f"{trat}:{dict_trat[trat]}")
    return dict_sort


def itogo(dict):
    """
    Функция подсчитывает общие затраты по словарю.
    :param dict: Словарь.
    :return: Сумму
    """
    summ = 0
    for _ in dict:
        summ += dict[_]
    return summ


# Создаем словарь
dict_trat = {}
# Получаем текст из первого файла
text = pdftotext('1.pdf')
# Обрабатываем его. Результат сохраняем в словарь.
dict_trat = razborka(text, dict_trat)
# Получаем текст из второго файла
text = pdftotext('2.pdf')
# Обрабатываем его. Результат сохраняем в словарь
dict_trat = razborka(text, dict_trat)
# Создаем словарь шаблонов
dict_val={
    'OZON': 'OZON',
    'Продукты': 'MAGNIT|SHARIFOV|BISKVI|OPTOVICHOK|SVETOFOR|GORKI|NOE BEL|MAKSTER|LENTA|MAKSTER|PEREKRESTOK|SVSH|EVROPA|PYATEROCHKA|Pivtor|AZBUKA VKUSA',
    'Одежда': 'ODEZHD|ZOLLA|GORKI|GRIN|OSTIN',
    'Аптека': 'APTEK|MAKSAVI|OOO VEGA|APTECHNY',
    'Машина': 'AZS|AZK|PARKOMAT|NTER FOR WI|AUTOCLUC|AVTOPASKER|STRELA-AV|VSK|AUTOROOM|AvtoGID|EXIST|PROTEKTOR|AVTOKLYUCH|KAZAKI',
    'ОФИС': 'OFFICE|LEONARD',
    'ФастФуд': 'BURGER|QSR|VINNOE PODV|KAFE|ZAXARENKO|PAW*AVSU|KINOHOD|AVTOSUSHI|PITNICA|BAR|GREEN HAT|PAW*AVSU',
    'РЕМОНТ': 'TORGOVYJ ZAL|SANTEKHNIKA|PRUSAKOV|KHOZTOVAR|BODROVA|KRASKI|OBOI|NAPOLNYEPOKRYTIY|ALLSOFT|PANUKHNIK|STROJTOVAR|RYBAKOVA|PORYADOK|VETTORG',
    'Комуналка': 'SBERBANK ONL@IN PLATEZH',
    'Техника': 'ULTRA|DNS|ALTER|KVANT|BAGIRA',
    'Страховка': 'ALFA',
    'Варя': 'METALLURG',
    'ALIEXPRESS': 'ALIEXPRESS|Aliexpress',
    'Спортмастер': 'SPORTMASTER',
    'Развлечения': 'AKVAPARK|STARYY PARK|ORELKONCERT|LYUBIMOV',
    'Ипотека': 'Agricultural',
    'Корзина': 'MOBILE BANK|ONL@IN KARTA-VKLAD|Tinkoff'
}
# Получаем сгруппированный словарь согласно шаблону
dict_sort = sort_dict2(dict_trat,dict_val)
# Выводим результат
for _ in dict_sort:
    print(f"{_}:{dict_sort[_]:.2f}")
print(f"{(itogo(dict_trat)-itogo(dict_sort)):.2f}")

# Для упорядочивания словаря по увеличению значения ключа
# import  operator
# dict_sort = sorted(dict_trat.items(), key=operator.itemgetter(1))
# for _ in dict_sort:
#      print(f"{_[0]}:{_[1]}")
# print(dict_sort)