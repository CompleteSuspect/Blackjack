import random
import time
import math #used for ceil() on the 1.5x win

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
        self.hidden = not self.hidden

class Deck():

    def __init__(self):
        self.cards = []
        self.bid = 0
        self.score = 0

    def __iter__(self):
        return iter(self.cards)

    def __getitem__(self, idx):
        return self.cards[idx]

    def __len__(self):
        return len(self.cards)

    def card_52(self, reps = 1, face_max = 10): #Generate a standard pack of 52 cards.
        suites = ['Clubs','Diamonds','Hearts','Spades']
        ranks = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']

        rep = 0
        while rep < reps:
            for suite in suites:
                score = 1
                for rank in ranks:
                    if score < face_max:
                        self.cards.append(Card(score, rank, suite))

                    else:
                        self.cards.append(Card(face_max, rank, suite))

                    score += 1

            rep +=1

    def shuffle(self):
        if len(self.cards):
            random.shuffle(self.cards)

        else:
            print('shuffle error: deck is empty')

    def draw_card(self, idx = 0):
        try:
            return self.cards.pop(idx)

        except IndexError as e:
            if not len(self.cards): # if shoe is empty, add more packs and shuffle
                print('\n\nShoe is empty, adding more cards!\n\n')
                self.card_52(4)
                self.shuffle()
                return self.cards.pop(idx)

            else:
                print('draw_card error:', e)

    def add_card(self, card):
        if type(card) == Card:
            self.cards.append(card)

        else:
            print('add_card error: appended object is not of type: Card')

class Player():

    def __init__(self, name):
        self.name = name
        self.money = 5000
        self.hands = [] #A player can have multiple hands

    def __str__(self):
        return self.name

class Dealer():

    def __init__(self):
        self.hand = Deck()
        self.score = 0

def set_players(player_lst, player_max = 5):

    players_copy = player_lst[:]

    for player in players_copy:
        while True:
            choice = input(f'{player.name}, play again? (yes/no): ').lower()

            if choice == 'no':
                player_lst.remove(player)
                break

            elif choice == 'yes':
                break

            else:
                print('Invalid choice')
                continue

    print('\n-------------------------Adding Players-------------------------\n')


    while len(player_lst) < player_max:
        good_name = True
        player_name = input(f'Player {len(player_lst) + 1} of {player_max}, please input player name or press enter to continue: ')

        if len(player_name) == 0:
            break

        if len(player_name):
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

    return player_lst

def get_score(hand):
    hand = sorted(hand, key = lambda card: card.score, reverse = True)
    score = 0

    for card in hand:
        if card.rank == 'Ace':
            if score + 11 > 21: #ace is 'soft' if the hand value is more than 21
                score += 1
            else:
                score += 11

        else:
            score += card.score

    return score

def blackjack():
    print('\n-------------------------Blackjack-------------------------\n')
    players = []
    shoe = Deck() # Here the shoe is set up with 4 packs of cards and then shuffled.
    shoe.card_52(4)             # You can add more or less packs in the argument.
    shoe.shuffle()

    while True:
        players = set_players(players)
        dealer = Dealer()
        if not players:
            print('Thanks for playing')
            break

        print(f'\nStarting game with {len(players)} players!\n')


        print('\n-------------------------Adding Bids-----------------------------\n')

        for player in players: #bid loop
            player.hands = []
            player.hands.append(Deck()) #adding Deck object to player
            print(f'\n{player}, you have £{player.money}.')

            while True:
                try:
                    bid = int(input(f'Please enter a bid between 1 and {player.money}: '))
                except:
                    print('Invalid bid')
                    continue

                if bid > 0 and bid <= player.money:
                    print(f'{player} has entered bid of £{bid}!')
                    player.hands[0].bid = bid
                    player.money -= bid
                    break

                else:
                    print('Invalid bid!')
                    continue

        print('\n-------------------------Building Hands-------------------------\n')

        rep = 0
        while rep < 2: # player hand builder loop
            for player in players:
                time.sleep(1)

                card = shoe.draw_card()
                player.hands[0].add_card(card)
                print(f"Dealer added {card} to {player}'s hand")

            time.sleep(1)
            card = shoe.draw_card()
            if rep == 1:                    #conditional to hide the dealers 2nd card
                card.flip()
                dealer.hand.add_card(card)

            else:
                dealer.hand.add_card(card)

            print(f'Dealer added {card} to his own hand.\n')
            rep += 1

        for player in players:
            player.hands[0].score = get_score(player.hands[0])
            if player.hands[0].score == 21:
                print(f'{player.name} has a blackjack!')

        for player in [p for p in players if p.hands[0].score < 21]: # main player move loop
            time.sleep(1)
            print(f"\n-------------------------{player}'s turn.-------------------------\n")

            for hand in player.hands: # for each of the players hands
                if player.hands.index(hand): # player turn display
                    time.sleep(1)
                    print(f"\n-------------------------{player.name}'s split hand #{player.hands.index(hand)}-------------------------\n")

                hand.score = get_score(hand)

                while hand.score < 21: # while the hand is not bust or blackjack
                    time.sleep(1)
                    moves = ['hit', 'stand']

                    if player.money >= hand.bid: # allow player to double
                        moves.append('double')

                    if (len(hand) == 2 and hand[0].rank == hand[1].rank) and (player.money >= hand.bid):# allow player to split
                        moves.append('split')

                    print('You have:')
                    for card in hand:
                        print(card)

                    print('\nDealer has:')
                    for card in dealer.hand:
                        print(card)

                    player_move = input(f"\n{player}, please enter your move: ({', '.join(moves)}): ").lower()

                    if player_move not in moves:
                        print('Invalid move!')
                        continue

                    elif player_move == 'stand':
                        print(f'\n{player} stands with a score of {hand.score}')
                        break

                    elif player_move == 'hit':
                        card = shoe.draw_card()
                        hand.add_card(card)
                        print(f"\nDealer has added {card} to {player}'s hand\n")
                        hand.score = get_score(hand)
                        continue

                    elif player_move == 'double':
                        hand.bid += hand.bid
                        print(f'\n{player} has doubled down and has doubled their bid to {hand.bid}\n')
                        card = shoe.draw_card()
                        hand.add_card(card)
                        time.sleep(1)
                        print(f"\nDealer added {card} to {player}'s hand\n")
                        hand.score = get_score(hand)
                        time.sleep(1)
                        print(f'\n{player} stands with a score of {hand.score}')
                        break

                    elif player_move =='split':
                        print(f'\n{player.name} has split their hand.')
                        new_deck = Deck() # A new deck is created
                        new_deck.bid = hand.bid
                        new_deck.add_card(hand.draw_card(1))
                        player.hands.append(new_deck)
                        hand.score = get_score(hand)
                        continue

                if hand.score > 21:
                    print(f'\n{player} has bust with a score of {hand.score}!')
                    print(f'{player} has lost their bid of £{hand.bid}!\n')

                elif hand.score == 21:
                    print(f'\n{player} has a blackjack!\n')

        print("\n-------------------------Dealer's Turn-------------------------\n")

        dealer.hand[1].flip()
        print(f"Dealer reveals face down card: {dealer.hand[1]}")
        dealer.score = get_score(dealer.hand) # adds the dealer.score attribute
        print('\nDealer has:')

        for card in dealer.hand:
            print(card)

        time.sleep(1)
        print('')

        while dealer.score < 17: #the dealer must hit until the hand total is 17 or more.
            card = shoe.draw_card()
            print(f'Dealer adds {card} to his hand.')
            dealer.hand.add_card(card)
            dealer.score = get_score(dealer.hand)
            time.sleep(1)

        if dealer.score > 21:
            print(f'\nDealer has bust with a score of {dealer.score}!\n')

        elif dealer.score == 21:
            print(f'\nDealer has a blackjack!\n')

        else:
            print(f'\nDealer stands with a score of {dealer.score}\n')

        print("\n-------------------------Calculating winnings-------------------------\n")

        for player in players:
            loss_total = 0 #this is displayed when a player loses money
            win_total = 0

            for hand in player.hands:
                if hand.score > 21: # if player is bust
                    loss_total += hand.bid

                elif (hand.score == 21) and (len(hand) == 2) and (dealer.score < 21):#if player has a natural blackjack and dealer does not have 21
                    win_total += hand.bid + math.ceil(hand.bid * 1.5)

                elif dealer.score > 21: # if dealer busts
                    if hand.score < 22:
                        win_total += hand.bid * 2

                elif dealer.score < 22: # if dealer does not bust
                    if hand.score > dealer.score:
                        win_total += hand.bid * 2

                    elif hand.score == dealer.score:
                        win_total += hand.bid

                    else:
                        loss_total += hand.bid

            if win_total:
                player.money += win_total
                print(f'{player.name} has won £{win_total - hand.bid} and now has £{player.money}')

            else:
                print(f'{player.name} has lost £{loss_total} and now has £{player.money}')

        print('')

        players_copy = players[:]
        for player in players_copy:
                if player.money == 0:
                    print(f'{player.name} is broke and can no longer play!')
                    players.remove(player)

blackjack()
