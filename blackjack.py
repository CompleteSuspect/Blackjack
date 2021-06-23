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
        self.cards = []
        self.bid = 0
        self.score = 0

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, idx):
        return self.cards[idx]

    def card_52(self, reps = 1, face_card = 10): #Maybe set the face card max value in the get_score() method.
        suites = ['Clubs','Diamonds','Hearts','Spades']
        ranks = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']

        rep = 0
        while rep < reps:
            for suite in suites:
                score = 1
                for rank in ranks:
                    if score < face_card:
                        self.cards.append(Card(score, rank, suite))
                    else:
                        self.cards.append(Card(face_card, rank, suite))
                    score += 1
            rep +=1

    def shuffle(self):

        if len(self.cards) != 0:
            random.shuffle(self.cards)
        else:
            print('shuffle error: deck_lst is empty')

    def draw_card(self, idx = 0):

        try:
            return self.cards.pop(idx)
        except IndexError as e:
            print('draw_card error:', e)

    def add_card(self, card):

        if type(card) == Card:
            self.cards.append(card)
        else:
            print('add_card error: appended object is not of type: Card')

    def get_score(self, ace = '11'): # I may convert this into a stand alone function rather than a method.
                                    # Also, doeasnt quite work the way i want.
        card_values = [card.__dict__ for card in self.cards]
        score = 0

        if self.score > 21:
            for card in card_values:
                if card.get('score') == 1:
                    card['score'] = ace
        self.score = sum([card.get('score') for card in card_values])

        return self.score


class Player():

    def __init__(self, name):
        self.hands = [Deck()]
        self.name = name
        self.money = 1000

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

class Dealer(Player):

    def __init__(self):
        super().__init__('Dealer')

def set_players(player_max = 5):
    player_lst = []

    while len(player_lst) < player_max:
        good_name = True
        player_name = input(f'Player {len(player_lst) + 1} of {player_max}, please input player name or press enter to continue: ')


        if len(player_name) != 0:
            for ch in player_name.lower():                                          #checking for valid name.
                if ch not in 'abcdefghijklmnopqrstuvwqxyz':
                    print('Name can only contain characters from a-z! \n')
                    good_name = False
                    break

            for player in player_lst:                                          #checking to see if name is already in use
                if player_name == player.name:
                    print('Name is already in use!\n')
                    good_name = False
                    break

            if good_name == True:
                player_lst.append(Player(player_name))

        else:
            return player_lst

    return player_lst

def blackjack():
    print('-------------------------Blackjack-------------------------\n')
    print('-------------------------Adding Players-------------------------\n')

    players = set_players()

    if len(players) == 0:
        print('Goodbye!')
        return None

    print(f'\nStarting game with {len(players)} players!\n')
    players.append(Dealer())
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

            if bid >= 1 and bid <= player.money:
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
            #time.sleep(1)
            card = shoe.draw_card()
            if type(player) == Dealer and rep == 1: # conditional to hide dealers 2nd card
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
                print(hand.get_score())

blackjack()
