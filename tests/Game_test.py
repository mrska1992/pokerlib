import numpy as np

from pokerlib.poker2 import old_poker, Deck as new_deck, poker_objects as po

N_iter = 1000000

N_players = 9

full_deck = np.array(range(52))

for k in range(N_iter):
    np.random.shuffle(full_deck)
    cards = full_deck[:N_players * 2 + 5][:]
    desk = cards[:5]
    players_cards = [
        ','.join(
            po.int_to_card(
                np.hstack(
                    [desk, cards[5 + player_seat*2: 7 + player_seat*2]]
                )
            )
        ) for player_seat in range(N_players)
    ]

    players_points_new = np.array([new_deck(player_cards)['result_points'] for player_cards in players_cards])
    result_new = players_points_new == players_points_new.max()

    players_points_old = np.array([old_poker.Deck(player_cards).check() for player_cards in players_cards])
    result_old = players_points_old == players_points_old.max()

    comparing_result = (result_new == result_old).all()

    if comparing_result is False:
        print cards

    if k % 10000 == 0:
        print k

print 'ready'
