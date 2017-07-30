from pokerlib.poker2 import *

TEST_SET7 = [
    '2h,3s,4d,8c,9c,As,Kd',
    '2h,3h,5d,5s,8c,Qs,Kd',
    '9h,9s,Js,Qd,Kc,As,Ac',
    '2s,3d,4s,4c,4d,Qs,Kc',
    '2s,3s,4s,5s,6d,Ad,Ac',
    'As,2s,3d,4s,5s,7d,Kc',
    '9h,9s,9d,Qd,Kc,As,Ac',
    '9h,9s,9d,Qd,Ad,As,Ac',
    'Ts,Tc,Td,Th,Ks,Ad,Ac',
    'Ts,Tc,Td,Th,As,Ad,Ac',
    'Td,Jd,Qd,Kd,Ad,2d,3s',
    'Ac,2c,3c,4c,5c,6s,9d'
    ]
TEST_SET6 = [
    '2h,3s,4d,8c,9c,Kd',
    '2h,3h,5d,5s,8c,Qs',
    '9h,9s,Js,Qd,As,Ac',
    '2s,3d,4s,4c,4d,Qs',
    '2s,3s,4s,5s,6d,Ad',
    'As,2s,3d,4s,5s,7d',
    '9h,9s,9d,Qd,As,Ac',
    '9h,9s,9d,Ad,As,Ac',
    'Ts,Tc,Td,Th,Ad,Ac',
    'Ts,Tc,Td,Th,Ad,Ac',
    'Td,Jd,Qd,Kd,Ad,2d',
    'Ac,2c,3c,4c,5c,6s'
    ]
TEST_SET5 = [
    '2h,3s,4d,8c,9c',
    '2h,3h,5d,5s,8c',
    '9h,9s,Js,As,Ac',
    '2s,3d,4s,4c,4d',
    '2s,3s,4s,5s,Ad',
    'As,2s,3d,4s,5s',
    '9h,9s,9d,As,Ac',
    '9h,9s,9d,As,Ac',
    'Ts,Tc,Td,Th,Ac',
    'As,Tc,Ad,Ah,Ac',
    'Td,Jd,Qd,Kd,Ad',
    'Ac,2c,3c,4c,5c'
]

"""TEST_SET2 = [
    'Ts,Jd',
    'Qs,Qd'
]"""

inner_ranks = []

for TEST_SET in (TEST_SET7, TEST_SET6, TEST_SET5):
    for test in TEST_SET:

        for test in TEST_SET:
            incards = Deck(test)
            info = incards.info
            print """
Cards: {cardlist}
Top five: {top_five}
Best combination: {best_combination}
Kickers: {kickers}
Combinations: {combinations}
Points: {result_points}

""".format(**info)
