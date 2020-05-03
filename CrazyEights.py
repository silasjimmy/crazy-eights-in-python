#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:05:30 2020

@author: silasjimmy
"""

import random

class Card:
    '''
    Defines a card.
    '''
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __str__(self):
        return " of ".join((self.value, self.suit))
    
class DiscardPile:
    '''
    Defines a discard pile.
    '''
    def __init__(self, other_cards=None):
        if other_cards:
            self.cards = other_cards
        else:
            self.cards = []
        
    def get_cards(self):
        '''
        Gets the pile's cards
        Returns (list of Card objects) the pile's cards.
        '''
        return self.cards
    
    def get_top_card(self):
        '''
        Returns (Card object) the top card in the pile.
        '''
        return self.cards[-1]
        
    def add_card(self, card):
        '''
        Adds a card to the pile.
        card (Card object): The card to add to the pile.
        '''
        self.cards.append(card)
        
    def draw_card(self):
        '''
        Removes a card from the pile.
        Returns (Card object) a card.
        '''
        if len(self.cards) > 1:
            return self.cards.pop(-1)
        
    def shuffle(self):
        '''
        Shuffles the pile.
        '''
        if len(self.cards) > 1:
            random.shuffle(self.cards)
            
    def is_empty(self):
        '''
        Checks if the pile has less than 2 cards to declare empty.
        Returns True if it is, False otherwise.
        '''
        if len(self.cards) < 2:
            return True
        return False
            
class DrawPile(DiscardPile):
    '''
    Defines a draw pile
    '''
    def __init__(self, other_cards=None):
        super().__init__()
        if other_cards:
            self.cards = other_cards
        else:
            self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"] 
                                    for v in ["A", "2", "3", "4", "5", "6", "7", "8", 
                                    "9", "10", "J", "Q", "K"]]
            
    def deal_player_cards(self):
        '''
        Deals the players with 7 cards.
        Returns (list of Cards) cards dealt.
        '''
        return [self.cards.pop(i) for i in range(7)]
        
class Hand:
    '''
    Defines a hand
    '''
    def __init__(self, cards):
        self.cards = cards
        self.value = 0
        
    def get_num_of_cards(self):
        '''
        Returns (int) the number of cards in the hand.
        '''
        return len(self.cards)
    
    def get_card(self, position):
        '''
        Returns (Card object) the card at the specified position.
        '''
        return self.cards[position]
    
    def add_card(self, card):
        '''
        Adds a card to the hand.
        card (Card object): The card to add.
        '''
        self.cards.append(card)
        
    def drop_card(self, num):
        '''
        Removes a card at the position specified with num.
        num (int): The position of the card to remove.
        Returns (Card object) the card removed.
        '''
        dropped_card = self.cards.pop(num)
        return dropped_card
    
    def get_hand_value(self):
        '''
        Returns (int) the value of the hand.
        '''
        self.calculate_hand_value()
        return self.value
        
    def calculate_hand_value(self):
        '''
        Calculates the value of the hand.
        '''
        self.value = 0
        for card in self.cards:
            if card.value.isnumeric():
                if int(card.value) == 8:
                    self.value += 50
                else:
                    self.value += int(card.value)
            else:
                self.value += 10
    
    def display_hand(self):
        '''
        Displays the hand.
        '''
        for i, card in enumerate(self.cards):
            print("({}) -> {}".format(i, card))
            
    def hand_over(self):
        '''
        Checks if the hand is over or not.
        Returns True if it is, False otherwise.
        '''
        if self.cards:
            return False
        return True
    
class Computer(Hand):
    '''
    Defines the computer's hand
    '''
    def __init__(self, cards):
        super().__init__(cards)
        
    def get_playable_card(self, top_card):
        '''
        Checks for a card matching the suit or rank of the top card in the discard pile.
        top_card (Card object): The card on the top of the discard pile.
        Returns (int, Card object) the index of the card found and the card, None if not.
        '''
        for index, card in enumerate(self.cards):
            if card.suit == top_card.suit or card.value == top_card.value:
                return index, card
        return None, None
    
    def check_for_eight(self):
        '''
        Checks the hand for an 8.
        Returns (int, Card object) index of the card found and the card, None if not.
        '''
        for index, card in enumerate(self.cards):
            if card.value.isdigit() and int(card.value) == 8:
                return index, card
        return None, None
            
    def get_card_with_suit(self, specific_suit):
        '''
        Gets the card with the specified suit.
        specific_suit (str): The suit to find.
        Returns (int, Card object) index of the card found and the card, None if not.
        '''
        for index, card in enumerate(self.cards):
            if card.suit == specific_suit:
                return index, card
        return None, None
    
    def play(self, top_card=None, specific_suit=None):
        '''
        Defines how the computer plays.
        top_card (Card object): The top card in the discard pile.
        specific_suit (str): The suit chosen by the player.
        Returns (str, Card object) the suit chosen in case an 8 was played and the card played.
        '''
        suit = None
        
        # Play if it is a specific suit
        if specific_suit:
            # PLay card if found a card with specific suit
            index, card = self.get_card_with_suit(specific_suit)
            if card:
                if card.value.isdigit() and int(card.value) == 8:
                    suits = list(set([c.suit for c in self.cards if c.suit != card.suit]))
                    suit = random.choice(suits)
                card = self.drop_card(index)
                return suit, card
            
            # Play card if found no card and there is an 8
            index, card = self.check_for_eight()
            if card:
                if self.get_num_of_cards() == 1:
                    suits = ["Diamonds", "Clubs", "Spades", "Hearts"]
                else:
                    suits = list(set([c.suit for c in self.cards if c.suit != card.suit]))
                suit = random.choice(suits)
                card = self.drop_card(index)
                return suit, card
        
        if top_card:
            # Play if it is has a card matching the top card in discard pile
            index, card = self.get_playable_card(top_card)
            if card:
                card = self.drop_card(index)
                return None, card
            
            # Play if has an 8
            index, card = self.check_for_eight()
            if card:
                suits = list(set([c.suit for c in self.cards if c.suit != card.suit]))
                suit = random.choice(suits)
                card = self.drop_card(index)
                return suit, card
        
        # Return if no card is found
        return None, None