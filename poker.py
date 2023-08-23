#!/usr/bin/env python3
"""
A poker hand simulator

Future updates:
- Add a web version
- Add granularity to the simulation to allow for hands of same type to be ranked: 
i.e. 2 pair of 10s and 2 pair of 9s. Currently, the simulator will only rank the hgihest pair in each hand.

"""

import random
import click 

def deck_of_card():
    """
    Creates a deck of cards
    """
    suits = ["H", "D", "S", "C"]
    ranks = [str(i) for i in range(2,11)] + ["J", "Q", "K", "A"]
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append(rank + suit)
    
    return deck

def full_name_suit(suit):
    """
    Returns the full name of a suit
    """
    return {
        "H": "Hearts",
        "D": "Diamonds",
        "S": "Spades",
        "C": "Clubs"
    }[suit]

def deal_hand(deck, n=5):
    """
    Deals a hand of n cards from the deck
    """

    return random.sample(deck, n)

def display_poker_hand():
    """
    Return all possible poker hands with rank"""
    return {
        "Royal Flush": 10,
        "Straight Flush": 9,
        "Four of a Kind": 8,
        "Full House": 7,
        "Flush": 6,
        "Straight": 5,
        "Three of a Kind": 4,
        "Two Pair": 3,
        "One Pair": 2,
        "High Card": 1
    }

def build_poker_hand():
    """
    Build all example poker hands
    """
    return {
        "Royal Flush": ["10H", "JH", "QH", "KH", "AH"],
        "Straight Flush": ["9H", "10H", "JH", "QH", "KH"],
        "Four of Kind": ["10H", "10D", "10S", "10C", "AH"],
        "Full House": ["10H", "10D", "10C", "AH", "AD"],
        "Flush": ["10H", "JH", "QH", "KH", "2H"],
        "Straight": ["9H", "10D", "JC", "QH", "KH"],
        "Three of a Kind": ["10H", "10C", "10D", "KH", "AH"],
        "Two Pair": ["10H", "10D", "JC", "JH", "KH"],
        "One Pair": ["10H", "10D", "JC", "QH", "KH"],
        "High Card": ["10H", "JD", "JC", "QH", "KH"]
    }

def display_poker_hand_probability():
    """Display the probability of each hand of poker"""
    return {
        "Royal Flush": 0.000154,
        "Straight Flush": 0.00139,
        "Four of a Kind": 0.0240,
        "Full House": 0.14,
        "Flush": 0.196,
        "Straight": 0.39,
        "Three of a Kind": 2.11,
        "Two Pair": 4.75,
        "One Pair": 42.3,
        "High Card": 50.1,
    }

def evaluate_poker_hand(hand)
    """
    Evaluate a poker hand
    """
    # sort the hand
    hand = sorted(hand)
    # check for flush
    if len(set([card[-1]] for card in hand)) == 1:
        # check for straight
        if len(set([card[:-1] for card in hand])) == 5:
            # check for royal flush
            if hand[0][:-1] == "10" and hand[-1][:-1] == "A":
                return "Royal Flush"
            else:
                return "Straight Flush"
        else:
            return "Flush"
    elif len(set([card[:-1] for card in hand])) == 5:
        return "Straight"
    
    # check for four of a kind
    elif len(set([card[:-1] for card in hand])) == 2:
        if len(set([card[:-1] for card in hand if card[:-1] == hand[0][:-1]])) == 1:
            return "Four of a Kind"
        else:
            return "Full House"
    # check for three of a kind
    elif len(set([card[:-1] for card in hand])) == 3:
        if len(set([card[:-1] for card in hand if card[:-1] == hand[0][:-1]])) == 1:
            return "Three of a Kind"
        else:
            return "Two Pair"
    # check for a pair
    elif len(set([card[:-1] for card in hand])) == 4:
        return "One Pair"
    
    else: 
        return "High Card"
    

def simulate_hand(deck,hand):
    """Simulate multiple hands of cards"""
    return [deal_hand[deck] for _ in range(hand)]

def play_poker_hand(hand1, hand2):
    """
    Play two poker hands against each other
    """

    hand1_rank = evaluate_poker_hand(hand1)
    hand2_rank = evaluate_poker_hand(hand2)
    hand1_rank_value = display_poker_hand()[hand1_rank]
    hand2_rank_value = display_poker_hand()[hand2_rank]
    # print the hands as well as the rank and type of hand
    print("Hand 1: {} - {} - {}".format(hand1, hand1_rank, hand1_rank_value))
    print("Hand 2: {} - {} - {}".format(hand2, hand2_rank, hand2_rank_value))

    # determine the winner
    if hand1_rank_value > hand2_rank_value:
        return {"winner": "Hand 1", "hand": hand1}
    elif hand1_rank_value < hand2_rank_value:
        return {"winner": "Hand 2", "hand": hand2}
    else:
        return {"winner": "Tie", "hand": hand1}
    
@click.group()
def cli():
    """
    A hand poker simulator
    """

@cli.command("info")
@click.option(
    "--probability", is_flag=True, help="Display the probability of each hand of poker"
)
def info(probability):
    """Display information about poker"""
    poker_hand_rank = display_poker_hand_probability()
    poker_hand = build_poker_hand()
    if probability:
        poker_hand_probability = display_poker_hand_probability()
        for hand,_ in poker_hand_rank.items():
            # print probability of each hand with click colors and example and 1 in x chance
            click.secho(
                "{} - {} - 1 in {:,} - {:4f}".format(
                hand, 
                poker_hand[hand],
                1 / poker_hand_probability[hand],
                poker_hand_probability[hand],
                ),
                fg="yellow",
            )
    else:
        for hand in poker_hand_rank:
            click.secho(f"{hand}: ({poker_hand_rank[hand]})", fg="green")
            click.secho(f"{poker_hand[hand]}", fg="white")

@cli.command("deal")
@click.option(
    "--hands", default=1, help="Number of hands to simulate"
)
def deal(hands):
    """
    Deal a hand of cards
    """
    