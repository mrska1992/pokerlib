import random as rd
from multiprocessing import Pool


class suit:
    """
    ['s','h','c','d','*']
    1) suit(int), example: suit(0) = s
    2) suit(str), example: suit('h'), suit('hearts')
    """

    def __init__(self, x):
        sd = {'s': 0, 'h': 1, 'c': 2, 'd': 3}
        sdl = ['spades', 'hearts', 'clubs', 'diamonds']
        sdt = ['s', 'h', 'c', 'd', '*']
        if type(x) == int:
            self.i = suit(sdt[x]).i
        elif type(x) == str and len(x) == 1:
            if x == '*':
                self.i = -1
            else:
                self.i = sd[x]
        elif type(x) == str and len(x) > 1:
            self.i = sdl.index(x)

    def __repr__(self, short=True):
        sdl = ['spades', 'hearts', 'clubs', 'diamonds']
        sdt = ['s', 'h', 'c', 'd', '*']
        return sdt[self.i] if short else sdl[self.i]

    def __str__(self, short=True):
        sdl = ['spades', 'hearts', 'clubs', 'diamonds']
        sdt = ['s', 'h', 'c', 'd', '*']
        return sdt[self.i] if short else sdl[self.i]

    def __eq__(self, suit2):
        return self.i == suit2.i or self.i == -1 or suit2.i == -1


class number(int):
    """
    1) number(int), example: number(10) <=> Q
    2) number(str), example: number('Q')
    """

    def __init__(self, x):
        nd = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
        if type(x) == str:
            self.i = nd[x]
        elif type(x) == int:
            self.i = x

    def __repr__(self):
        ndt = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        return ndt[self.i]

    def __str__(self):
        ndt = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        return ndt[self.i]

    def __add__(self, x):
        return number((self.i + x) % 13)

    def __sub__(self, x):
        return number((self.i - x) % 13)


class Card:
    def __init__(self, x=None, y=None):
        nd = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}
        sd = {'s': 0, 'h': 1, 'c': 2, 'd': 3}
        if isinstance(x, number) and isinstance(y, suit):
            self.n = x
            self.s = y
        else:
            if y == None and x != None:
                if type(x) == int:  # example: card(47)
                    if x in range(52):
                        S = x // 13
                        N = x % 13
                    else:
                        S = N = None
                elif type(x) == str:
                    if len(x) > 3:  # example: card('10 of diamonds')
                        n = x[:x.index(' ')]
                        s = x[x.index(' ') + 4: x.index(' ') + 5]
                    elif len(x) <= 3:  # example: 10d
                        n = x[:len(x) - 1]
                        s = x[-1]
                    N = nd[n] if n in nd.keys() else None
                    S = sd[s] if s in sd.keys() else None
            elif type(y) == str:
                if type(x) == str:  # example card('10','d')
                    N = nd[x]
                    S = sd[y] if y != '*' else '*'
                elif type(x) == int:  # example card(8,'d')
                    N = x
                    S = sd[y] if y != '*' else '*'
            else:
                S = N = None
            if S == None or N == None:
                x = rd.randrange(52)
                self.s = suit(x // 13)
                self.n = number(x % 13)
            else:
                self.s = suit(S)
                self.n = number(N)

    def deck_number(self):
        return self.n.i + self.s.i * 13

    def __repr__(self):
        return self.show(short=True)

    def __str__(self):
        return self.show(short=True)

    def __add__(self, something):
        if type(something) == int:
            return Card(self.n + something, suit('*'))

    def __sub__(self, something):
        if type(something) == int:
            return Card(self.n - something, suit('*'))

    def __getitem__(self, i):
        return self

    def show(self, short=False):
        sdt = ['s', 'h', 'c', 'd', '*']
        sdl = ['spades', 'hearts', 'clubs', 'diamonds']
        ndt = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        s = '%s%s%s' % (self.n, '' if short else ' of ', self.s.__repr__(short))
        return s

    def __eq__(self, card2):
        return self.n == card2.n and self.s == card2.s

    def __gt__(self, card2):
        return self.n.i > card2.n.i

    def __lt__(self, card2):
        return self.n.i < card2.n.i

    def __ge__(self, card2):
        return self > card2 or self == card2

    def __le__(self, card2):
        return self < card2 or self == card2


class Deck:
    def __init__(self, cardlist, now_check=True):
        if type(cardlist) == str:
            cardlist = [Card(c) for c in cardlist.split(',')]
        elif type(cardlist) == list and all([isinstance(c, Card) for c in cardlist]):
            pass
        elif type(cardlist) == list and all([type(c) == str for c in cardlist]):
            cardlist = [Card(c) for c in cardlist]
        else:
            print 'Warning!'

        cardlist.sort()
        self.fl = False
        self._len = len(cardlist)
        self.cards = []
        self.suits = [0, 0, 0, 0]
        self.numbers = []
        self.nn = []

        for card in cardlist:
            self.cards.append(card)
            tc = Card(card.n, suit('*'))

            if not tc in self.numbers:
                self.numbers.append(tc)
                self.nn.append(1)
            else:
                self.nn[self.numbers.index(tc)] += 1

            if card.s.i >= 0:
                self.suits[card.s.i] += 1
            else:
                for i in self.suits:
                    i += 1

        self.ncards = []
        for card in self.cards:
            self.ncards.append(self.nn[self.numbers.index(card)])
        self.lenu = len(self.numbers)
        self.maxu = max(self.nn)
        if max(self.suits) >= 5:
            self.fl = True
            self.fs = suit(self.suits.index(max(self.suits)))
            self.fd = [c for c in self.cards if c.s == self.fs]
        if now_check:
            self.check(verbose=False)
        else:
            pass

    def __getitem__(self, i):
        return self.cards[i]

    def __len__(self):
        return len(self.cards)

    def info(self):
        return self.fl, self.lenu, self.nn, self.suits

    def __repr__(self):
        return self.cards.__repr__()

    def __str__(self):
        return self.cards.__repr__()

    def itercards(self):
        return zip(range(self._len), self.cards)

    def check(self, verbose='points'):
        def oh(cards):
            k = min(5, len(cards))
            wc = cards[:]
            wc.sort()
            wc = wc[-k:]
            p = sum([(wc[-j].n.i) * (13 ** -j) for j in range(1, k + 1)])
            return wc, p

        def street(cards):
            for i in range(1, len(cards) + 1):
                hc = cards[-i]
                cc = cards[-i]
                ok = True
                strl = [hc]
                sti = 0
                while ok:
                    if cc - 1 in cards:
                        strl.append(cc - 1)
                        sti += 1
                        cc = cc - 1
                        # rint strl
                        if sti == 4:
                            if hc.n.i >= 3:
                                return strl, hc.n.i
                    else:
                        ok = False
            return [], -1

        def countin(card, deck):
            count = 0
            for c in deck.cards:
                if card == c:
                    count += 1
            return count

        if self._len >= 5:
            wcards = [0] * 9
            wwcards = [0] * 9
            points = [0] * 9
            if not self.fl:
                if self.maxu == 1:
                    wcards[0], points[0] = oh(self.cards)
                    wwcards[0] = wcards[0][-1:][:]
                elif self.maxu == 2:
                    if self.lenu == self._len - 1:
                        wcards[1] = [self.cards[-i] for i in
                                     range(1, len(self.cards) + 1) if self.ncards[-i] == 2]
                        wwcards[1] = wcards[1][:]
                        i = self._len - 1
                        ac = []
                        while len(ac) < 3:
                            if not self.cards[i] in wcards[1]:
                                ac.append(self.cards[i])
                            i -= 1
                        points[1] = 1 + float(wcards[1][-1].n.i) / 13 + oh(wcards[1] + ac)[1] / 169
                        wcards[1] += ac
                        wcards[1].sort()

                    elif self.lenu < self._len - 1:  # check 3 pairs
                        wcards[2] = [self.cards[-i] for i in range(1, len(self.cards) + 1)
                                     if self.ncards[-i] == 2]
                        wcards[2] = wcards[2][:4]
                        wwcards[2] = wcards[2][:]
                        i = self._len - 1
                        ac = []
                        while len(ac) < 1:
                            if not self.cards[i] in wcards[2]:
                                ac.append(self.cards[i])
                            i -= 1
                        points[2] = 2 + float(wcards[2][-3].n.i) / 13 + float(wcards[2][-1].n.i) / 169 + \
                                    oh(wcards[2] + ac)[1] / 2197
                        wcards[2] += ac
                        wcards[2].sort()
                elif self.maxu == 3:
                    if self.lenu == self._len - 2:
                        wcards[3] = [self.cards[-i] for i in range(1, len(self.cards) + 1) if self.ncards[-i] == 3]
                        wwcards[3] = wcards[3][:]
                        i = self._len - 1
                        ac = []
                        while len(ac) < 2:
                            if not self.cards[i] in wcards[3]:
                                ac.append(self.cards[i])
                            i -= 1
                        points[3] = 3 + float(wcards[3][-1].n.i) / 13 + oh(wcards[3] + ac)[1] / 169
                        wcards[3] += ac
                        wcards[3].sort()
                    if self.lenu < self._len - 2:
                        part3 = [self.cards[-i] for i in range(1, len(self.cards) + 1) if self.ncards[-i] == 3]
                        part3.sort()
                        part2 = [self.cards[-i] for i in range(1, len(self.cards) + 1) if self.ncards[-i] == 2]
                        part2.sort()

                        wcards[6] = (part2 + part3)[-5:]
                        wwcards[6] = wcards[6][:]
                        ####kostul####
                        rk3 = wcards[6][-1].n.i
                        rk2 = wcards[6][-0].n.i
                        """if self.lenu < self._len - 3: ### 2 sets
                            if rk3 < rk2:
                                rk3, rk2 = rk2, rk3
                        rk3 = max([i for i in range(len(self.ncards)) if self.ncards[i] == 3])
                        low1 = min([i for i in range(len(self.ncards)) if self.ncards[i] >= 2])"""
                        points[6] = 6 + float(rk3) / 13 + float(rk2) / 169
                        wcards[6].sort()

                elif self.maxu == 4:
                    wcards[7] = [self.cards[-i] for i in range(1, len(self.cards) + 1) if self.ncards[-i] == 4]
                    wwcards[7] = wcards[7][:]
                    i = self._len - 1
                    ac = []
                    while len(ac) < 1:
                        if not self.cards[i] in wcards[7]:
                            ac.append(self.cards[i])
                        i -= 1
                    points[7] = 7 + float(wcards[7][-1].n.i) / 13 + oh(wcards[7] + ac)[1] / 169
                    wcards[7] += ac
                    wcards[7].sort()

                if self.lenu >= 5:
                    strl, hc = street(self.cards)
                    if hc >= 0:
                        wcards[4] = [self.cards[-i] for i in range(1, len(self.cards) + 1) if self.cards[-i] in strl]
                        wcards[4].sort()
                        wwcards[4] = wcards[4][:]
                        points[4] = 4 + float(hc) / 13

            elif self.fl:
                wcards[5], points[5] = oh(self.fd)
                wwcards[5] = wcards[5][:]
                points[5] += 5
                strl, hc = street(self.fd)
                # print self.fd,strl,hc
                if hc >= 0:
                    wcards[8] = [self.fd[-i] for i in range(1, len(self.fd) + 1) if self.fd[-i] in strl]
                    wcards[8].sort()
                    wwcards[8] = wcards[8][:]
                    points[8] = 8 + float(hc) / 13

            self.points = max(points)
            self.wcards = wcards[points.index(self.points)]

            self.points = max(points)
            self.wcards = wcards[points.index(self.points)]

        elif self._len == 2:
            self.points = 0
            self.wcards = self.cards

        if verbose != False:
            if verbose == 'points':
                return self.points
            elif verbose == 'wcards':
                return self.points, wwcards
            else:
                return self.points, self.wcards

    def __add__(self, deck):
        if deck != None:
            return Deck(self.cards + deck.cards, now_check=False)
        else:
            return self

    def __sub__(self, deck):
        if deck != None:
            from copy import deepcopy
            temp = deepcopy(self.cards)
            for c in deck.cards:
                temp.remove(c)
            return Deck(temp, now_check=False)
        else:
            return self


_2 = Card('2', '*')
_3 = Card('3', '*')
_4 = Card('4', '*')
_5 = Card('5', '*')
_6 = Card('6', '*')
_7 = Card('7', '*')
_8 = Card('8', '*')
_9 = Card('9', '*')
_T = Card('T', '*')
_J = Card('J', '*')
_Q = Card('Q', '*')
_K = Card('K', '*')
_A = Card('A', '*')

check_file = True


class PokerError(Exception):
    def __init__(self, text='', value=-1):
        self.text = text
        self.value = value

    def __str__(self):
        return "{0} Err no. {1}".format(self.text, self.value)


class fulldeck:
    """
    creates full deck without excep_cards
    """

    def __init__(self, except_cards=[], shuffle=True):
        import numpy as np
        self.cards = []
        for nn in range(52):
            card = Card(nn)
            if not card in except_cards:
                self.cards.append(card)
        if shuffle:
            np.random.shuffle(self.cards)
        else:
            pass

    def __getitem__(self, i):
        return self.cards[i]

    def __sub__(self, cardlist, shuffle=True):
        import numpy as np
        if type(cardlist) == list or isinstance(cardlist, Deck):
            for card in cardlist:
                self.cards.remove(card)
        elif isinstance(cardlist, Card):
            self.cards.removed(cardlist)
        else:
            raise PokerError('Cant substract {} from deck'.format(str(type(cardlist))))
        if shuffle:
            np.random.shuffle(self.cards)
        return self

    def __add__(self, cardlist, shuffle=True):
        import numpy as np
        if type(cardlist) == list or isinstance(cardlist, Deck):
            for card in cardlist:
                if not card in self.cards:
                    self.cards.append(card)
        elif isinstance(cardlist, Card):
            if not card in self.cards:
                self.cards.append(cardlist)
        else:
            raise PokerError('Cant add {} to deck'.format(str(type(cardlist))))
        if shuffle:
            np.random.shuffle(self.cards)
        return self

    def get_cards(self, shape2=2, shape1=1, no_remove=True):
        result = []
        cards = self.cards[:shape1 * shape2]
        i = 0
        for k in range(shape1):
            deck = []
            for j in range(shape2):
                deck.append(cards[i])
                i += 1
            result.append(Deck(deck, now_check=False))
        if not no_remove:
            self = self - cards
        else:
            pass
        return result if shape1 > 1 else result[0]

    def shuffle(self):
        import numpy as np
        np.random.shuffle(self.cards)


def monte_carlo_c(p1_hand, desk, n_players=2, N=1000):
    if desk == None:
        full_deck = fulldeck(p1_hand.cards)
    else:
        full_deck = fulldeck(p1_hand.cards + desk.cards)

    result = []
    if desk == None:
        for i in range(N):
            p_points = []
            temp = full_deck.get_cards(5, no_remove=False)
            temp_desk = temp
            p1_points = (p1_hand + temp_desk).check()
            p_hands = full_deck.get_cards(2, n_players - 1)
            for player in p_hands:
                points = (player + temp_desk).check()
                p_points.append(points)
            result.append(int(p1_points >= max(p_points)))
            full_deck = full_deck + temp.cards
            full_deck.shuffle()
    elif len(desk) == 5:
        p1_points = (p1_hand + desk).check()
        for i in range(N):
            p_points = []
            p_hands = full_deck.get_cards(2, n_players - 1)
            if n_players == 2:
                p_hands = [p_hands]
            for player in p_hands:
                points = (player + desk).check()
                p_points.append(points)
                # print p_points
            # print p1_points, max(p_points)
            result.append(int(p1_points >= max(p_points)))
            full_deck.shuffle()
    elif len(desk) < 5:
        for i in range(N):
            p_points = []
            temp = full_deck.get_cards(len(desk) - 5, no_remove=False)
            temp_desk = desk + temp
            p1_points = (p1_hand + temp_desk).check()
            p_hands = full_deck.get_cards(2, n_players - 1)
            for player in p_hands:
                points = (player + temp_desk).check()
                p_points.append(points)
            result.append(int(p1_points >= max(p_points)))
            full_deck = full_deck + temp
            full_deck.shuffle()

    return float(sum(result)) / len(result)


def paral(args):
    deck, players_cnt, desk, hand = args

    rd.shuffle(deck)
    desk_other = [deck[i] for i in range(5 - len(desk))]
    hand_other = [deck[5 + i] for i in range((players_cnt - 1) * 2)]
    if Deck(desk + desk_other + hand).check() >= max(
            [Deck(desk + desk_other + hand_other[i * 2:i * 2 + 2]).check() for i in range(players_cnt - 1)]):
        return 1
    else:
        return 0


def monte_carlo(hand, desk, players_cnt, n, engines):
    if players_cnt > 1:
        hand = [Card(i) for i in hand.split(',')]
        if len(desk) > 0:
            desk = [Card(i) for i in desk.split(',')]
        else:
            desk = []

        deck = [Card(i) for i in range(52)]
        [deck.remove(i) for i in hand]
        [deck.remove(i) for i in desk]
        # win_ratio = 0.
        # test = []
        pool = Pool(engines)
        win_ratio = sum(
            pool.map(paral, [(deck[:], players_cnt, desk, hand) for m in range(n)])
        )

        pool.close()
        pool.join()
        return float(win_ratio) / n
    else:
        return 1
