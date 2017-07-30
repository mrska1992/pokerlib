from texas_poker import check as texas_check
from poker_objects import *
import itertools as it
from copy import copy

EXPERIMENTAL = False

def check(
        cards_to_check,
        hands_limit=60
):
    if len(cards_to_check) < 4 and not EXPERIMENTAL:
        raise PokerError("Can't check hand with less than 4 cards with Omaha engine. Try probability theory.")

    player_hand4 = cards_to_check[:4]
    all_hands = []

    if len(cards_to_check) in (7, 8, 9):
        desk = cards_to_check[4:]

        for player_hand2 in map(CardList, it.combinations(player_hand4, 2)):
            for desk3 in map(CardList, it.combinations(desk, 3)):
                new_cards_to_check = player_hand2 + desk3
                all_hands.append(texas_check(new_cards_to_check))

    elif len(cards_to_check) == 4:
        for player_hand2 in map(CardList, it.combinations(player_hand4, 2)):
                new_cards_to_check = player_hand2
                all_hands.append(texas_check(new_cards_to_check))
    else:
        desk3 = CardList(cards_to_check[4:])
        for player_hand2 in map(CardList, it.combinations(player_hand4, 2)):
                new_cards_to_check = player_hand2 + desk3
                all_hands.append(texas_check(new_cards_to_check))

    all_hands = np.array(all_hands)
    points = np.array([hand['result_points'] for hand in all_hands])
    all_hands = all_hands[points.argsort()[::-1]][:]
    result = copy(all_hands[0])
    result.update({'all_hands': all_hands[:hands_limit][:]})
    return result
