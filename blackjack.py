import random
import time

class Card():

    def __init__(self, score, rank, suite , hidden = False):
        self.score = score
        self.rank = rank
        self.suite = suite
        self.hidden = hidden

    def __str__(self):
        if self.hidden == False:
            return f'{self.rank} of {self.suite}'
        else:
            return '<Hidden>'

    def flip(self):
        if self.hidden == False:
            self.hidden = True
        else:
            self.hidden = False

class Deck():

    def __init__(self):
        self.deck_lst = []
        self.bid = 0

    def __iter__(self):
        return iter(self.deck_lst)

    def __getitem__(self, idx):
        return self.deck_lst[idx]

    def card_52(self, reps = 1, rules = 'blackjack'):
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
                    score = rank
                    if rules == 'blackjack' and rank > 10:
                        score = 10
                    self.deck_lst.append(Card(score, card_attb['rank'][rank], card_attb['suite'][suite])) #Card(score, rank, suite)
            rep += 1

    def shuffle(self):
        if len(self.deck_lst) != 0:
            random.shuffle(self.deck_lst)
        else:
            print('shuffle error: deck_lst is empty')

    def draw_card(self, idx = 0):
        try:
            return self.deck_lst.pop(idx)
        except IndexError as e:
            print('draw_card error:', e)

    def add_card(self, card):
        if type(card) == Card:
            self.deck_lst.append(card)
        else:
            print('add_card error: appended object is not of type: Card')

    def get_score(self):
        total = 0
        if len(self.deck_lst) != 0:
            for card in self.deck_lst:
                total += card.score
            return total
        else:
            print('get_score error: deck_lst is empty')

class Player():

    def __init__(self, name):
        self.hands = [Deck()]
        self.name = name
        self.money = 1000
        self.blackjack = False

    def __str__(self):
        return self.name

    def set_bid(self, bid, idx = 0):
        if bid != 0:
            try:
                self.hands[idx].bid = bid
                self.money -= bid
            except IndexError as e:
                self.hands[0].bid = bid
                self.money -= bid
                print('set_bid error:', e, 'defaulting to hands[0]')
        else:
            print('set_bid error: bid value is 0')

    def reset(self):
        self.__init__(name = self.name)


def blackjack():
    print('-------------------------Blackjack-------------------------\n')
    players = []
    player_count = 0
    player_max = 5

    print('-------------------------Adding Players-------------------------\n')
    while player_count < player_max : #player init loop
        name_fail = False
        player_name = input(f'Player {player_count + 1} of {player_max}, please input player name or press enter to continue: ')

        if len(player_name) != 0 and player_count <= player_max:
            for ch in player_name:                                          #checking for valid name.
                if ch.lower() not in 'abcdefghijklmnopqrstuvwqxyz':
                    print('Name can only contain characters from a-z! \n')
                    name_fail = True
                    break

            for player in players:                                          #checking to see if name is already in use
                if player_name == player.name:
                    print('Name is already in use!\n')
                    name_fail = True
                    break

            if name_fail == False:
                players.append(Player(player_name))
                player_count += 1

        else:
            if len(players) == 0:
                print('Thanks for playing!')
                return None

            else:
                break

    print(f'\nStarting game with {player_count} players!\n')
    players.append(Player('Dealer'))
    shoe = Deck()               # here the shoe is set up with 4 packs of cards and then shuffled.
    shoe.card_52(4)             # You can add more or less packs in the argument.
    shoe.shuffle()

    print('-------------------------Adding Bids-----------------------------\n')
    for player in players[:-1]: #bid loop
        print(f'\n{player}, you have £{player.money}.')
        while True:
            try:
                bid = int(input(f'Please enter a bid between 2 and {player.money}: '))
            except:
                print('Invalid bid')
                continue

            if bid >= 2 and bid <= player.money:
                print(f'{player} has entered bid of {bid}!')
                player.set_bid(bid)
                break

            else:
                print('Invalid bid!')
                continue

    print('-------------------------Building Hands-------------------------\n')
    rep = 0
    while rep < 2: #player hand builder loop
        for player in players:
            time.sleep(1)
            card = shoe.draw_card()
            if player.name == 'Dealer' and rep == 1: # conditional to hide dealers 2nd card
                card.flip()
                player.hands[0].add_card(card)
                print(f"Dealer added {card} to {player.name}'s hand")
            else:
                player.hands[0].add_card(card)
                print(f"Dealer added {card} to {player.name}'s hand")

        print('')
        rep += 1

    for player in players:
        for hand in player.hands:
            for card in hand:
                print(player, 'Ace' in card.__dict__.values())

blackjack()
