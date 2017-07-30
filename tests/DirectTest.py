from pokerlib.poker2 import *

void_cards = poker_objects.CardList('')


TEST_SET = [
    'Ac,2c,3c,4c,5c,6s,9d'
]



for test in TEST_SET:
    incards = Deck(test)
    output = incards.info
    print output, '\n'
