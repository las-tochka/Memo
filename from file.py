import json

dct = {1: '''Царь Колокол.
Самый большой колокол в мире.
Был отлит в 1600 году, но разбился.
Впоследствие был установлен
 в Кремле как экспонат.''',
       2: '''Царь-пушка.
Огнестрельное оружие, что ни разу
 не стреляло. Всю свою жизнь работая экспонатом,
 путешествовала по Москве, пока не осела 
 в Кремле, где и находиться по сей день.''',
       3: '''Московский кремль.
Резиденция Московских царей, позже
правительства. Самое известное место Москвы,
куда толпами съезжаются туристы со всех
стран мира.''',
       4: '''Храм Василия Блаженного.
Уникальный храм, построенный Иваном
Грозным в честь взятия Казани.
Состоит из 11 отдельных церквей, каждая из
 которых имеет свой дизайн и структуру.''',
       5: '''Памятник Минину и Пожарскому.
Мемориал в честь 2 героев, объединивших народ
для борьбы с поляками во времена Смуты.
Этот памятник стоит на красной площади,
главной площади страны.''',
       6: '''Успенский собор.
Собор находится на Соборной площади Кремля
и является одним из древнейших зданий
Москвы. Он издревле служил усыпальницей
для Московских патриархов, а также личной
церковью Московских царей и князей.'''
       }
with open('json_1.json', 'w') as f:
    json.dump(dct, f)