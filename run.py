"""
Random
-This module implements pseudo-random
 number generators for various distributions.
Time
-This module provides various time-related functions.
pyfiglet
-pyfiglet takes ASCII text and renders it in ASCII art font.
pyinputplus
- PyInputPlus will keep asking the user for text until they enter valid input.
"""

import random
import time
import pyfiglet
import pyinputplus as pyip


values = {'Ace': 11, 'Two': 2, 'Three': 3, 'Four': 4,
          'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10}
suits = ('Diamonds', 'Hearts', 'Clubs', 'Spades')
ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
         'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')


# Classes


class Pot:
    """ creates instance of players pot """

    def __init__(self):
        self.pot = 1000
        self.bet = 0

    def win_bet(self):
        """ adds bet to pot if player wins """
        self.pot += self.bet
        return self.pot

    def lose_bet(self):
        """ takes bet if player loses """
        self.pot -= self.bet
        return self.pot

    def show_pot(self):
        """ Displays player pot """
        return self.pot


class Card:
    """ creates instance of cards in deck """

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:
    """ creates instances of a deck of 52 playing cards """

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank, suit))

    def shuffle(self):
        """ shuffles the deck of cards """
        random.shuffle(self.deck)

    def deal_card(self):
        """ deals a single card from the deck """
        single_card = self.deck.pop()
        return single_card


class Hand:
    """ creates instance of the hands the dealer and player has """

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0  # counts the aces in the hand

    def add_card(self, card):
        """ add a card to player or dealers hand """
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_aces(self):
        """ changes the value of an ace in
        the hand if the score exceeds 21 """
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


deck = Deck()
deck.shuffle()

player_pot = Pot()
pot = Pot().show_pot()

player_hand = Hand()
dealer_hand = Hand()
dealer_hand.add_card(deck.deal_card())
dealer_hand.add_card(deck.deal_card())
player_hand.add_card(deck.deal_card())
player_hand.add_card(deck.deal_card())


# Functions


def place_bet(pot):
    """ Prompts user to input their bet amounts """
    print('Place Your Bet')
    print('Minimum bets are $50')
    while True:
        player_pot.bet = pyip.inputNum(min=50, max=player_pot.pot)
        if accept_bet(player_pot.bet, player_pot.pot):
            remaining_pot = player_pot.pot - player_pot.bet
            print('\nBet placed!')
            print(f"Pot: ${remaining_pot}")
            start_round()
            break


def accept_bet(bet, pot):
    """ verifies if the bet amount is valid """
    try:
        if bet > pot or bet < 50:
            raise ValueError(
                f"\nYou tried to bet ${bet}\n"
                f"Your Pot is ${pot}\n"
                "Minimum bets are $50\n"
            )
    except ValueError as error:
        print(error)
        print('Please try again...')
        return False

    return True


def show_players_hand():
    """ reveals dealer hand and score to determine the winner """
    print('\nPlayer Hand:  ', *player_hand.cards, sep='\n')
    print('Player Score = ', player_hand.value, '\n')


def show_dealers_hand():
    """ reveals dealer hand and score to determine the winner """
    print('\nDealer Hand:  ', *dealer_hand.cards, sep='\n')
    print('Dealer Score = ', dealer_hand.value, '\n')


def start_round():
    """ shuffles the deck and starts the game """
    print('Dealer Shuffling Deck...\n')

    time.sleep(3)


def deal_first_hands(player, dealer):
    """ shows the first 4 cards dealt in the game """
    player.adjust_aces()
    dealer.adjust_aces()

    print('\nDealer Hand:')
    print('<Card Hidden>')
    print(dealer.cards[1])

    print('\nPlayer Hand:  ', *player.cards, sep='\n')
    print('Player Score = ', player.value)


def hit(hand, deck):
    """ deals card if to player or dealer if they
     hit and calls adjusts any aces of score > 21 """
    hand.add_card(deck.deal_card())
    hand.adjust_aces()


def dealer_plays():
    """ makes the dealers decision to hit or stay """

    while dealer_hand.value < player_hand.value and dealer_hand.value < 21:
        hit(dealer_hand, deck)
        show_dealers_hand()
        time.sleep(3)

    if dealer_hand.value > 21:
        dealer_busts()

    elif dealer_hand.value == 21:
        print('Blackjack')
        if dealer_hand.value == player_hand.value:
            round_draw(player_pot)
        else:
            dealer_wins(player_pot)

    elif dealer_hand.value > player_hand.value and dealer_hand.value <= 21:
        show_dealers_hand()
        dealer_wins(player_pot)
    elif dealer_hand.value == player_hand.value:
        show_dealers_hand()
        round_draw(player_pot)


def hit_or_stay(hand, deck):
    """ gives the player the option to hit or stay """

    global playing

    while True:
        option = input("\nDo you want to HIT or STAY ? Enter 'h' or 's': ")

        if option.lower() == 'h':
            hit(hand, deck)
            show_players_hand()
            if player_hand.value > 21:
                player_busts()
                break

        elif option.lower() == 's':
            print('Dealer is playing...')
            time.sleep(3)
            dealer_plays()
            break
        else:
            print("Enter 'h' to HIT or 's' to Stay: ")
            continue


def next_round(pot):
    """ offers the user the chance to play
     another round or cash in their bets """

    print("\nWould you like to play another round or cash in your bets?")
    play_again = input("Enter 'play' or 'cash': ")

    while True:

        if play_again.lower() == 'play':
            if player_pot.pot < 50:
                print("\nYou Went Broke, Better Luck Next Time!")
                break
            else:
                reset()
                game_play()
        elif play_again.lower() == 'cash':
            print(f" $$$ you won ${pot.show_pot()}. Thanks for playing! $$$ ")
            quit()
        else:
            print("Enter 'play' to Play another round "
                  "or 'cash' to Leave the Casino: ")
            next_round(player_pot)
            break


# game outcomes


def player_busts():
    """ keep bets, dealer wins, offer next round """

    print('Player Busts')
    dealer_wins(player_pot)


def dealer_busts():
    """ player wins, award winnings, offer next round """

    print('Dealer Busts')
    player_wins(player_pot)


def player_wins(pot):
    """ returns results if player wins """
    print('Player Wins!!!')
    player_pot.win_bet()
    print(f"Pot: ${pot.show_pot()}")


def dealer_wins(pot):
    """ returns results if player loses"""
    print('Dealer Wins!!!')
    pot.lose_bet()
    print(f"Pot: ${pot.show_pot()}")


def round_draw(pot):
    """ returns the results if a draw """
    print('Its a Draw!')
    print(f"Pot: ${pot.show_pot()}")


# game loop


def game_play():
    """ calls each game function in order to run the game loop """

    place_bet(player_pot)
    deal_first_hands(player_hand, dealer_hand)
    hit_or_stay(player_hand, deck)
    next_round(player_pot)


def reset():
    """ resets all the values for the nexr round """

    deck.__init__()
    deck.shuffle()
    player_hand.__init__()
    dealer_hand.__init__()

    dealer_hand.add_card(deck.deal_card())
    dealer_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())
    player_hand.add_card(deck.deal_card())


# game intro


print()
intro = pyfiglet.figlet_format('Welcome To BlackJack!!!')
print(intro)
print("Your Starting Pot is $1000")
input('Please Enter Your Name: ')
game_play()
