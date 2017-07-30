# coding: utf-8

import os
import inspect
import pickle
import numpy as np
import pandas as pd
import operator
from collections import Counter
from operator import itemgetter
from old_poker import Card, Deck
import gzip


card_mapper = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
                   'J': 11, 'Q': 12, 'K': 13, 'A': 14}

sorting = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'combination',
           'hand_combination', 'hand_wcards', 'higher_hand_wcard',
           'max_straigh', 'max_straigh_one_sided', 'max_straight_in_hand',
           'max_suit_cnt', 'max_suit_hand', 's0', 's1', 's2', 's3', 's4', 's5',
           's6', 'share_straight_in_hand', 'players_cnt', 'round',
           'combination_0', 'combination_1', 'combination_2',
           'combination_3', 'combination_4', 'combination_5',
           'combination_6', 'combination_7', 'combination_8', 'round_0',
           'round_8', 'round_11', 'round_14']

fet_names = ['c0', 'c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'combination',
             'hand_combination', 'hand_wcards', 'higher_hand_wcard',
             'max_straigh', 'max_straigh_one_sided', 'max_straight_in_hand',
             'max_suit_cnt', 'max_suit_hand', 's0', 's1', 's2', 's3', 's4', 's5',
             's6', 'share_straight_in_hand', 'players_cnt', 'round',
             'combination_0.0', 'combination_1.0', 'combination_2.0',
             'combination_3.0', 'combination_4.0', 'combination_5.0',
             'combination_6.0', 'combination_7.0', 'combination_8.0', 'round_0',
             'round_8', 'round_11', 'round_14']

def load_model():
    """Loads a compressed object from disk"""
    lib_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = lib_path + '/poker_approx_model.gz'
    file = gzip.GzipFile(filename, 'rb')
    buffer = ""
    while 1:
        data = file.read()
        if data == "":
            break
        buffer += data
    object = pickle.loads(buffer)
    file.close()
    return object


def get_features(hand, desk, players_cnt):
    # simple_features

    if hand == '' or hand*0 != '':
        return [-1.]*len(fet_names)

    if desk * 0 != '':
        desk = ''

    features = dict()
    if len(desk) > 0:
        deck = (hand + ',' + desk).split(',')
    else:
        deck = hand.split(',')

    v = [card_mapper[card[0]] for card in deck]

    v += [0] * (7 - len(v))

    suits = [card[1] for card in deck]
    suit_mapper = Counter(suits)

    s = [suit_mapper[i] for i in suits]
    s += [0] * (7 - len(s))
    # sorting
    k = [v, s]
    tuples = [(k[0][i], k[1][i]) for i in range(0, 7)]
    tuples = sorted(tuples[0:2], key=itemgetter(0), reverse=True) + sorted(tuples[2:], key=itemgetter(0), reverse=True)

    i = 0
    for c, s in tuples:
        features['c' + str(i)] = c
        features['s' + str(i)] = s
        i += 1
    # max_suit_cnt
    features['max_suit_cnt'] = max([(hand + desk).count('h'), (hand + desk).count('c'),
                                    (hand + desk).count('s'), (hand + desk).count('d')])
    # hand_combination + hand_wcards + higher_hand_wcard
    if len(desk) > 0:
        hand_ = [Card(i) for i in hand.split(',')]
        desk_ = [Card(i) for i in desk.split(',')]
        wc = Deck(desk_ + hand_).wcards
        features['hand_combination'] = len([1 for i in hand_ if i in wc])

        p, w = Deck(desk_ + hand_).check(verbose='wcards')
        wc = w[int(p)]
        features['hand_wcards'] = len([1 for i in hand_ if i in wc])
        if len([1 for i in hand_ if i in wc]) > 0:
            features['higher_hand_wcard'] = card_mapper[str(max([i for i in hand_ if i in wc]).n)]
        else:
            features['higher_hand_wcard'] = 0
        features['combination'] = int(Deck(desk_ + hand_).check())

        c = Counter([i[1] for i in (hand + ',' + desk).split(',')])
        m = max(c.iteritems(), key=operator.itemgetter(1))[1]
        hand_suit = [i[1] for i in hand.split(',')]
        features['max_suit_hand'] = max([Counter(hand_suit).get(i) for i in [i for i in c if c[i] == m]] + [0])

    else:
        features['hand_combination'] = 2
        features['hand_wcards'] = 2
        features['higher_hand_wcard'] = card_mapper[str(max([Card(i) for i in hand.split(',')]).n)]
        features['combination'] = 0

        hand_suit = [i[1] for i in hand.split(',')]
        if hand_suit[0] == hand_suit[1]:
            features['max_suit_hand'] = 2
        else:
            features['max_suit_hand'] = 1

    # straighs

    if len(desk) > 0:
        deck = [i for i in (hand + ',' + desk).split(',')]
    else:
        deck = [i for i in hand.split(',')]
    v = [card_mapper[i[0]] for i in deck]
    if 14 in v: v.append(1)
    s = sorted(list(set(v)))

    seqs = []
    curseq = [s[0]]
    for i in range(len(s) - 1):

        if s[i] == s[i + 1] - 1:
            curseq.append(s[i + 1])
        else:
            seqs.append(curseq)
            curseq = [s[i + 1]]
    seqs.append(curseq)
    features['max_straigh'] = max([len(i) for i in seqs])

    ml = max(enumerate(seqs), key=lambda tup: len(tup[1]))[1]
    if 1 in ml or 14 in ml:
        features['max_straigh_one_sided'] = 1
    else:
        features['max_straigh_one_sided'] = 0

    features['share_straight_in_hand'] = sum([1 for i in v[0:2] if i in ml]) / float(len(ml))
    features['max_straight_in_hand'] = max([i for i in v[0:2] if i in ml and i not in v[2:]] + [0])

    r = len(desk)
    features['round'] = r
    for i in [0, 8, 11, 14]:
        if r == i:
            features['round_' + str(i)] = 1
        else:
            features['round_' + str(i)] = 0

    c = features['combination']
    for i in range(9):
        if c == i:
            features['combination_' + str(i)] = 1
        else:
            features['combination_' + str(i)] = 0

    features['players_cnt'] = players_cnt

    return [features[i] for i in sorting]


def mc_approx(*args):  # hand,desk,players_cnt):

    if type(args[0]) == pd.DataFrame:
        # return model.predict(pd.DataFrame(args[0].apply(
        #            lambda x: features(x.hand,x.desk,x.players_cnt), axis=1), index=fet_names))
        df = args[0][['hand', 'desk', 'players_cnt']].apply(
            lambda x: pd.Series(get_features(x.hand, x.desk, x.players_cnt)), axis=1)
        df.columns = fet_names
        raw_result = model.predict(df)
        result = np.where(args[0].hand.isnull() | (args[0].hand == ''), np.nan, raw_result)
        return result

    else:
        return model.predict(pd.DataFrame(features(args[0], args[1], args[2]), index=fet_names).T)[0]

model = load_model()
