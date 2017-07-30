# -*- coding: utf-8 -*-

import numpy as np

comb_name_dict = {
    0: 'HighCard',
    1: 'Pair',
    2: 'TwoPairs',
    3: 'Set',
    4: 'Straight',
    5: 'Flush',
    6: 'FullHouse',
    7: 'Four',
    8: 'StraightFlush'
    }

str_to_number = dict(zip(list('23456789TJQKA'), range(13)))
str_to_suit = dict(zip(list('cdhs'), range(4)))
number_to_str = dict(zip(range(13), list('23456789TJQKA')))
suit_to_str = dict(zip(range(4), list('cdhs')))

class PokerError(Exception):
    pass


def card_to_int_scalar(card):
    return str_to_number[card[0]]*4 + str_to_suit[card[1]]

def int_to_card_scalar(integer):
    return number_to_str[integer // 4] + suit_to_str[integer % 4]

card_to_int = np.vectorize(card_to_int_scalar)
int_to_card = np.vectorize(int_to_card_scalar)

def to_suits_order_scalar(x, suits_order):
    """
    :param x:  карта
    :param suits_order: порядок мастей
    :return: карта приведенная с новой мастью в соответствии с порядком, так что:
     числовое_представление_карты1 < числовое_представление_карты2 если масть1 идет раньше чем масть2 в suits_order
    """
    return suits_order[x % 4] + 4 * (x // 4)

to_suits_order = np.vectorize(to_suits_order_scalar, excluded=['suits_order'])

def to_13(x, rank):
    if rank in (2, 6):
        return number_to_str[x//13] + ',' + number_to_str[x % 13]
    else:
        return number_to_str[x//13]

class CardList:
    def __init__(self, cards):
        if isinstance(cards, CardList):
            self.cards = cards.cards
        elif isinstance(cards, basestring) and cards != '':
            self.cards = card_to_int(cards.split(','))
        elif isinstance(cards, basestring) and cards == '':
            self.cards = np.array([])
        else:
            self.cards = np.asarray(cards)

    def change_suits(self, suits_order):
        if len(self.cards) > 0:
            self.cards = to_suits_order(self.cards, suits_order)
        else:
            pass

    def __add__(self, other):
        return CardList(list(self.cards) + list(other.cards))

    def __repr__(self):
        return 'CardList[{0}]'.format(','.join(int_to_card(self.cards))) if len(self.cards) > 0 else 'CardList[NoCards]'

    def __str__(self):
        tmp = int_to_card(self.cards) if len(self.cards) > 0 else ''
        return ','.join(tmp)

    def __format__(self, scpecs):
        tmp = int_to_card(self.cards) if len(self.cards) > 0 else ''
        return ','.join(tmp)

    def __getattr__(self, item):
        return getattr(self.cards, item)


class Combination:
    def __init__(self, cards, rank, inner_rank):
        self.cardlist = CardList(cards) if not isinstance(cards, CardList) else cards
        self.name = (
            comb_name_dict[rank] +
            '({0})'.format(to_13(inner_rank, rank))
                     )
        self.rank = rank
        self.inner_rank = inner_rank
        self.base_points = self.rank * 13 ** 6 + self.inner_rank * 13 ** 4

    def change_suits(self, suits_order):
        self.cardlist.change_suits(suits_order=suits_order)

    def __getattr__(self, item):
        return getattr(self.cardlist, item)

    def __repr__(self):
        return self.name

    def __str__(self):
        return "{0} [{1!s}]".format(self.name, self.cardlist)

    def __ge__(self, other):
        return self.base_points >= other.base_points

    def __le__(self, other):
        return self.base_points <= other.base_points

    def __gt__(self, other):
        return self.base_points > other.base_points

    def __lt__(self, other):
        return self.base_points < other.base_points

    def __eq__(self, other):
        return self.base_points == other.base_points



