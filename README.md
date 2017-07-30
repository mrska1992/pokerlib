# pokerlib
	Ну это какбэ либа которая умеет очки в покер считать.
	Cпасибо пацанам из KamaGames и всем причастным
	Ты если хочешь че-нить посчитать то сделай такой типа:

```python
from __future__ import print_function
from poker2 import Deck

desk_cards = 'Ts,Js,Qs,2c,3d'
players_hand = 'Ks,As'

deck = Deck(','.join((desk_cards, players_hand)))
```
	А потом вот так
```python
print(deck.info)
```
	Ну или так
```python
print(deck['result_points']
```
	Чуть не забыл, еще вот так можно
```python
deck = Deck('Ks,Js,Qs,2c,3d,Ts,As,Ad,Ac'), engine='omaha'))
print(deck.info
```

# Развлекайся, кароче
