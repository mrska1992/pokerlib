from pokerlib.poker2 import *

# omaha
full_deck = np.array(range(52))
for N_cards in range(4, 10):
    for k in range(3):
        np.random.shuffle(full_deck)
        cards = full_deck[:N_cards][:]
        card_str = ','.join(poker_objects.int_to_card(cards))
        deck = Deck(card_str, engine='omaha')
        print "N_cards: {0} N_iter: {1}\nDeck: {2}\n{3}".format(
            N_cards, k, deck, deck.info
        )

# texas
full_deck = np.array(range(52))
for N_cards in range(2, 8):
    for k in range(3):
        np.random.shuffle(full_deck)
        cards = full_deck[:N_cards][:]
        card_str = ','.join(poker_objects.int_to_card(cards))
        deck = Deck(card_str, engine='texas')
        print "N_cards: {0} N_iter: {1}\n{2}".format(
            N_cards, k, deck.info
        )


