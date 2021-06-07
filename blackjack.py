import random

class Card():

    def __init__(self, value, rank, suite , hidden = False):
        self.value = value
        self.suite = suite
        self.rank = rank
        self.hidden = hidden

    def flip(self):
        if self.hidden == False:
            self.hidden = True
        else:
            self.hidden = False

    def __str__(self):
        return f'{self.value} {self.rank} {self.suite} {self.hidden}'

class Deck():

    def __init__(self):
        self.deck_lst = []


    def card_52(self, reps = 1):
        card_attb =  {'rank':
                        {1:'Ace', 2:'2', 3:'3', 4:'4', 5:'5',
                         6:'6', 7:'7', 8:'8', 9:'9', 10:'10',
                         11:'Jack', 12:'Queen', 13:'King'},
                      'suite':
                         {0:'Clubs',1:'Diamonds',2:'Hearts', 3:'Spades'},
                      'colour':
                         {0:'Black', 1:'Red' ,2:'Red',3:'Black'}
                      }

        rep = 0
        while rep < reps:
            for suite in range(4):
                for rank in range(1, 14):
                    self.deck_lst.append(Card(rank, card_attb['rank'][rank], card_attb['suite'][suite]))
            rep += 1

    def shuffle(self):
        random.shuffle(self.deck_lst)

    def add_card(self, card):
        self.deck_lst.append(card)

    def draw_card(self, index = 0):
        return self.deck_lst.pop(index)

class Player():

    def __init__(self, name):
        self.hand = Deck()
        self.name = name
        self.money = 1000

#everything below here is code to test the classes, game logic has not yet been implemented

shoe = Deck()

shoe.card_52()

player_lst = []

while True:
    name = input('Please enter your name, enter blank name to continue: ')
    if len(name) > 0:
        player_lst.append(Player(name))
    else:
        break

player_lst[0].hand.add_card(shoe.draw_card())
player_lst[0].hand.add_card(shoe.draw_card())


for card in player_lst[0].hand:
    print(card)
