from random import sample
from itertools import chain

NUM_OF_DECKS = 7  # the number of card decks affects the frequencies of cards that can come up given you know what has already been played 

card_values = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
               "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10, "K": 10}

card_deck = {"A": 4 * NUM_OF_DECKS, "2": 4 * NUM_OF_DECKS, "3": 4 * NUM_OF_DECKS, "4": 4 * NUM_OF_DECKS,
             "5": 4 * NUM_OF_DECKS, "6": 4 * NUM_OF_DECKS, "7": 4 * NUM_OF_DECKS,
             "8": 4 * NUM_OF_DECKS, "9": 4 * NUM_OF_DECKS, "10": 4 * NUM_OF_DECKS,
             "J": 4 * NUM_OF_DECKS, "Q": 4 * NUM_OF_DECKS, "K": 4 * NUM_OF_DECKS
             }  # we have 4 * NUM_OF_DECKS as the value for each card since in each deck there are 4 suits of cards

total = 0  # player and dealer running score
dealer = 0

bet_total = 1000  # initial amount to bet
bet = 0  # how much player bets at start of each game

player_bust = False  # boolean to check if player or dealer busts, important in winning situations
dealer_bust = False


def sort_deck(deck: dict):
    card = []
    for key in deck:
        card.append([key] * 4)
    flatten = list(chain.from_iterable(card))
    shuffled = sample(flatten, len(flatten))  # shuffles the entire deck 
    return shuffled


cards = sort_deck(card_deck)


def check_shuffle(deck):  # checks if we're out of cards, in which case it reshuffles the deck
    global card_deck
    if not deck:
        deck = sort_deck(card_deck)
        return deck
    else:
        return deck


def play_again():  # asks player if they want to play another game, in which case scores are reset
    global total, dealer
    ans = input("do you want to play again [yes/no]: ")
    if ans == "yes":
        total = 0
        dealer = 0
        play_blackjack()
    else:
        quit()


def check_total():  # all the different winning situations, changes bet total accordingly
    global total, dealer, bet_total
    if total > 21:
        print("bust")
        bet_total -= bet
        play_again()
    elif total == 21:
        print("blackjack")
        bet_total += 1.5 * bet  # blackjack returns 3:2 of initial bet 
        play_again()
    elif dealer > 21 and player_bust:
        print("you lose, bet lost")
        bet_total -= bet
        play_again()
    elif dealer > 21 and not player_bust:
        print("you win")
        bet_total += bet
        play_again()
    elif 17 <= dealer <= 21:
        if dealer > total:
            print("you lose, bet lost ")
            bet_total -= bet
            play_again()
        elif dealer == total:
            print("no winner")
            play_again()
        elif dealer < total:
            print("you win")
            bet_total += bet
            play_again()


def draw_card(deck):  # picks the top card from the deck
    global total, dealer, card_deck
    ans = input("hit or stay: ")
    if ans == "hit":
        draw = check_shuffle(deck)[0]
        print("card:", draw)
        total += int(card_values[draw])
        del check_shuffle(deck)[0]  # top card is removed from the deck
        print("total: ", total)
        check_total()  # scores are analyzed after card is drawn
        draw_card(deck)
    elif ans == "stay" and dealer < 17:  
        while dealer < 17:  # if the player stays then the dealer draws until they have a score greater than or equal to 17. 
            dealer += card_values[check_shuffle(deck)[0]]
            print("card:", check_shuffle(deck)[0])
            print("dealer total: ", dealer)
            del check_shuffle(deck)[0]
            check_total()


def play_blackjack():  # allows player to bet and play game
    global bet
    print("money: ", bet_total)
    if bet_total == 0:
        print("game over, no more money")
        quit()
    else:
        bet = int(input("enter a bet: "))
        draw_card(cards)


play_blackjack()
