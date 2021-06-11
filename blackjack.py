import random

class Card():

    def __init__(self, score, rank, suite , hidden = False):
        self.score = score
        self.rank = rank
        self.suite = suite
        self.hidden = hidden

    def __str__(self):
        return f'{self.score} {self.rank} {self.suite} {self.hidden}'

    def flip(self):
        if self.hidden == False:
            self.hidden = True
        else:
            self.hidden = False

class Deck():

    def __init__(self):
        self.deck_lst = []

    def __iter__(self):
        return iter(self.deck_lst)

    def __getitem__(self, idx):
        return self.deck_lst[idx]

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
                    self.deck_lst.append(Card(rank, card_attb['rank'][rank], card_attb['suite'][suite])) #Card(score, rank, suite)
            rep += 1

    def shuffle(self):
        random.shuffle(self.deck_lst)

    def add_card(self, card):
        if type(card) == Card:
            self.deck_lst.append(card)

    def draw_card(self, idx = 0):
        try:
            return self.deck_lst.pop(idx)
        except IndexError as e:
            print(e)

    def get_score(self):
        total = 0
        for card in self.deck_lst:
            total += card.score
        return total

    def get_qty(self):
        return len(self.deck_lst)

class Player():

    def __init__(self, name):
        self.hand = Deck()
        self.name = name
        self.money = 1000
        self.bid = 0
        self.split_bid = 0

    def split_pair(self):
        if self.bid != 0:
            if self.bid <= self.money:
                self.split_hand = Deck()
                self.split_hand.add_card(self.hand[1])
                self.split_bid = self.bid
                self.money -= self.bid
            else:
                print(f'{self.name} does not have enough money to split a pair.')
        else:
            print(f'{self.name} has not yet set a bid.')

    def set_bid(self, bid):
        if bid <= self.money:
            self.bid = bid
            self.money -= bid
        else:
            print(f'{self.name} does not have enough money (${self.money}).')

    def double_down(self):
        if self.bid != 0:
            if self.bid <= self.money:
                self.money -= self.bid
                self.bid += self.bid
            else:
                print(f'{self.name} does not have enough money ({self.money}) to double the bid of {self.bid}.')
        else:
            print(f'{self.name} has not yet set a bid.')
#------------------------------------------------------------------------------------------

zoe = Player('zoe')

zoe.hand.add_card(Card(4, '4', 'Clubs'))
zoe.hand.add_card(Card(5, '5', 'Hearts', hidden = True))
zoe.set_bid(500)

zoe.split_pair()
print(zoe.hand[0])
print(zoe.split_hand[0])
print(zoe.split_bid)
