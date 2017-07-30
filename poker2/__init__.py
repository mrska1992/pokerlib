#coding: utf-8
import numpy as np

import old_poker
import poker_objects
from omaha_poker import check as omaha_check
from texas_poker import check as texas_check

#TODO Убрать дерьмовые кросс-импорты
#TODO Выпилить всякие ненужные проверки на непустоту кардлиста путем наследования от класса "пустой кардлист"
#TODO Тесты нормальные сделать
#TODO Прошерстить код и убрать избыточность, которой дофига
#TODO Неизвестно, зачем это надо, но все-таки надо впилить возможность прогонять карты по одной

EXPERIMENTAL = False


class Deck(poker_objects.CardList):
    def __init__(self, cards, instant_check=True, engine='texas', omaha_hands_limit=10):
        if isinstance(cards, poker_objects.CardList):
            self.cards = cards.cards
        elif isinstance(cards, basestring):
            self.cards = poker_objects.card_to_int(cards.split(','))
        else:
            self.cards = np.asarray(cards)

        self.engine = engine
        self.check_method = {'texas': texas_check, 'omaha': omaha_check}[self.engine]
        self.check_kwargs = {'texas': {}, 'omaha': {'hands_limit': omaha_hands_limit}}[self.engine]

        self.cardlist = poker_objects.CardList(self.cards)
        self.info = dict(cardlist=self.cardlist)
        self.checked = False
        self.omaha_hands_limit = omaha_hands_limit

        # self.combinations = None
        # self.best_combination = None
        # self.result_points = None
        # self.top_five = None
        if instant_check is True:
            self.check()

    def check(self):
        check_result = self.check_method(self.cards, **self.check_kwargs)
        self.info.update(check_result)
        self.checked = True
        return check_result

    def __repr__(self):
        return "Deck[{0}]".format(str(self))

    def __getitem__(self, item):
        if not self.checked:
            self.check()
        try:
            return self.info[item]
        except:
            raise KeyError('Deck instance has not attribute {}'.format(item))

    def __gt__(self, other):
        return self['result_points'] > other['result_points']

    def __lt__(self, other):
        return self['result_points'] < other['result_points']

    def __eq__(self, other):
        return self['result_points'] == other['result_points']

