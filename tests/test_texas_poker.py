import pytest

from pokerlib.poker2 import Combination
from pokerlib.poker2 import Deck


@pytest.mark.parametrize("cards, expected", [
    ('2h,4s,4d,8c,9c', Combination('4s,4d', 1, 2*13)),
    ('2h,4s,3c,8c,9c', Combination('4s,4d', 1, 2*13)),
])
def test_best_combination(cards, expected):
    deck = Deck(cards)
    assert deck.info['best_combination'] == expected



