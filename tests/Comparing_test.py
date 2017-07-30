import numpy as np

from pokerlib.poker2 import old_poker, Deck as new_deck, poker_objects as po


def check_equality(card_str):
    deck_old = old_poker.Deck(card_str)
    deck_new = new_deck(card_str)
    old_points = deck_old.check()
    new_points = deck_new['result_points']

    old_result = [int(old_points // 1)] + [int((old_points % 1) % (1./13) ** k // (1./13)**(k+1)) for k in range(4)]
    new_result = [new_points % 13 ** k // 13**(k-1) for k in range(2, 7)[::-1]]

    return (np.array(old_result) == np.array(new_result)).all(), old_result, new_result


card_str = 'Kd,3d,9d,2h,8c,2s,6d'
result, old_result, new_result = check_equality(card_str)
print "old: {0}\nnew: {1}".format(old_result, new_result)


full_deck = np.array(range(52))

for k in range(1000):
    np.random.shuffle(full_deck)
    cards = full_deck[:7][:]
    card_str = ','.join(po.int_to_card(cards))
    try:
        result, old_result, new_result = check_equality(card_str)
        print 'Not equal!!!!!!', card_str
        break
    except:
        print 'Exception!!!!!!', card_str
        raise



