#coding: utf-8
from __future__ import print_function
from poker2 import Deck
hands = [
    '8c,2d,Ah,9s,3d,Ks,Qc',
    '8c,2d,Ah,9s,3d,Kh,Ad',
    '8c,2d,Ah,9s,3d,9s,Kh',
    '8c,2d,Ah,9s,3d,5c,Qh',
    '8c,2d,Ah,9s,3d,Jc,3s',
    '8c,2d,Ah,9s,3d,8c,Ad',
    '8c,2d,Ah,9s,3d,5c,9h',
    '8c,2d,Ah,9s,3d,As,3s',
    '2c,3s,4c,5h,7d,8c,9d'
]

def letter_to_number(letter):
    letter = letter.lower()
    letter_digits = {
        let: k for k, let in zip('0123456789abcdefghijklmnopqrstuvwxyz', range(100))
    }
    return letter_digits[letter]


def number_to_base(number, base_to, base_from=10, return_precesser=None):


    # Convert to to x10
    number = number if isinstance(number, basestring) else str(number)
    x10 = int(number, base_from)
    k = 0
    done = False
    digits = []
    while not done:
        x10, r = x10 // base_to, x10 % base_to
        done = x10 == 0
        digits.append(r)
    return digits[::-1]

pp = Deck('2c,3s,4c,5h,7d,8c,9d').check()['result_points']
ll = lambda x: [0]*(7-len(x)) + x

for hand in hands:
    print(hand, Deck(hand).check()['result_points'], ll(number_to_base(Deck(hand).check()['result_points'], 13)), Deck(hand).check()['best_combination'])
