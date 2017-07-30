# -*- coding: utf-8 -*-
import numpy as np
from poker_objects import *


EXPERIMENTAL = False

"""
0: HighCard,
1: Pair,
2: TwoPairs,
3: Set,
4: Straight,
5: Flush,
6: FullHouse,
7: Four,
8: StraightFlush
"""


def _kickers_point_counter(kicker):
    return kicker // 4


kickers_point_counter = (
    lambda kickers:
    sum([(kickers[-1 - k] // 4) * (13 ** (len(kickers) - k - 1)) for k in range(len(kickers))])
)


def check(
        cards_to_check,
        return_combinations=True,
        return_best=True,
        return_points=True
):
    """вычисление выигрышных комбинаций,
    возвращаемые объекты зависят от параметов
    """
    if len(cards_to_check) < 2 and not EXPERIMENTAL:
        raise PokerError("Can't check hand with less than 2 cards with Texas engine. Try probability theory.")

    """Вычисление количества вхождений каждой масти"""
    suits = np.bincount(cards_to_check % 4, minlength=4)
    suits_order_tmp = suits.argsort()
    suits_order = dict(zip(suits_order_tmp, range(4)))
    suits_order_r = dict(zip(range(4), suits_order_tmp))

    """Изменяем числовые значения карты с помощью to_suits_order в соответствии с suits_order"""
    cards = to_suits_order(x=cards_to_check, suits_order=suits_order)
    cards.sort()

    """Проверка на наличие флеша"""
    flush_length = suits.max()

    """Инициализация стартовых параметров"""
    same = [-1]
    same_length = 0

    top_pair = []
    top_pair_rank = None
    top_set = []
    top_set_rank = None

    combinations = []
    combinations_len = 0

    if cards[-1] >= 48:
        """Если в наборе есть туз"""
        straight = [cards[-1]]
        straight_length = 1
        prev_number = -1
    else:
        straight = []
        straight_length = 0
        prev_number = None

    """Добавляем флеш"""
    if flush_length >= 5:
        flush = cards[cards % 4 == 3]
    else:
        flush = []

    garbage = []

    """Итерируем по карте"""
    for card, i in zip(cards, range(len(cards))):
        number = card // 4
        if number == prev_number:
            same[same_length] = cards[i - 1]
            same.append(card)
            same_length += 1
            if straight_length > 1:
                straight[-1] = card
        elif same_length > 0:
            (
                same, same_length, top_pair, top_pair_rank,
                top_set, top_set_rank, combinations, combinations_len,
                prev_number
            ) = same_handler(**locals())

        if number - 1 == prev_number:
            straight.append(card)
            straight_length += 1
        else:
            if straight_length >= 5:
                straight_handler(**locals())
            straight_length = 1
            straight = [card]

        prev_number = number

    if same_length > 0:
        (
            same, same_length, top_pair, top_pair_rank, top_set,
            top_set_rank, combinations, combinations_len,
            prev_number
        ) = same_handler(**locals())
        # print 'same finded', combinations
    if straight_length >= 5:
        straight_handler(**locals())
        # print 'straight finded', combinations

    if combinations_len == 0:
        combinations.append(Combination([card], 0, number * 13))

    best_combination = max(combinations)

    if len(best_combination) < 5:
        wtf = best_combination.cardlist.cards
        kickers = np.setdiff1d(cards, wtf)
        kickers = kickers[-(5 - len(best_combination)):]

        top_five = CardList(np.append(best_combination.cards, kickers))
        result_points = (
            best_combination.base_points +
            kickers_point_counter(kickers)
        )
    else:
        kickers = []
        top_five = best_combination.cardlist
        result_points = (
            best_combination.base_points
        )

    for combination in combinations:
        combination.change_suits(suits_order_r)

    best_combination.change_suits(suits_order_r)
    top_five.change_suits(suits_order_r)
    kickers = CardList(kickers)
    kickers.change_suits(suits_order_r)

    return dict(
        combinations=combinations,
        best_combination=best_combination,
        result_points=result_points,
        top_five=top_five,
        kickers=kickers
    )


def straight_handler(straight, straight_length, combinations, combinations_len,
                     flush, flush_length, card, prev_number, **kwargs):
    combinations.append(
        # (cards, combination_rank, inner rank) #
        Combination(straight[-5:], 4, prev_number * 13)
    )
    combinations_len += 1

    if flush_length >= 5:
        have_sf, straight_flush = straight_flush_check(straight, flush, straight_length, flush_length)
        if have_sf:
            combinations.append(
                # (cards, combination_rank, inner rank) #
                Combination(straight_flush[-5:], 8, (straight_flush[-1] // 4 * 13))
            )
            combinations_len += 1


def straight_flush_check(straight, flush, straight_length, flush_length, **kwargs):
    for shift in range(straight_length + 1):
        sample = straight[straight_length - 5 - shift:straight_length - shift]
        intersection = np.intersect1d(sample, flush)
        if len(intersection) == 5:
            return True, sample
    return False, np.array([])


def same_handler(same, same_length, top_pair, top_pair_rank,
                 top_set, top_set_rank, combinations, combinations_len,
                 prev_number, **kwargs):
    if same_length == 1:
        if not (top_set or top_pair):
            combinations.append(
                # (cards, combination_rank, inner rank) #
                Combination(same, 1, prev_number * 13)
            )
            combinations_len += 1
            top_pair = same[:]
            top_pair_rank = prev_number

        elif top_set:
            combinations.append(
                # (cards, combination_rank, inner rank) #
                Combination(same + top_set, 6, top_set_rank * 13 + prev_number)
            )
            combinations_len += 1
            top_pair = same[:]
            top_pair_rank = prev_number

        elif top_pair:
            combinations.append(
                # (cards, combination_rank, inner rank) #
                Combination(top_pair + same, 2, prev_number * 13 + top_pair_rank)
            )
            combinations_len += 1
            top_pair = same[:]
            top_pair_rank = prev_number

    elif same_length == 2:

        if not (top_set or top_pair):
            combinations.append(
                # (cards, combination_rank, inner rank) #
                Combination(same, 3, prev_number * 13)
            )
            combinations_len += 1
            top_set = same[:]
            top_set_rank = prev_number

        elif top_set:
            combinations.append(
                # (cards, combination_rank, inner rank) #
                Combination(top_set[-2:] + same, 6, prev_number * 13 + top_set_rank)
            )
            combinations_len += 1
            top_set = same[:]
            top_set_rank = prev_number

        elif top_pair:
            combinations.append(
                # (cards, combination_rank, inner rank) #
                Combination(top_pair + same, 6, prev_number * 13 + top_pair_rank)
            )
            combinations_len += 1
            top_set = same[:]
            top_set_rank = prev_number
    else:
        combinations.append(
            # (cards, combination_rank, inner rank) #
            Combination(same, 7, prev_number * 13)
        )
        combinations_len += 1

    same = [-1]
    same_length = 0

    return (
        same, same_length, top_pair, top_pair_rank, top_set,
        top_set_rank, combinations, combinations_len, prev_number
    )
