# coding: utf-8
from poker2.poker_approx import mc_approx
import pandas as pd

test_df = pd.DataFrame(
    [
        ['', '2h,3c,4d,5s,As', 5]
    ],
    columns=['hand', 'desk', 'players_cnt']
)
result = mc_approx(test_df)
print 'Input', test_df
print 'Output', result
