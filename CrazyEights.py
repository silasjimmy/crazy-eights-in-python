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
    Defines a discard pile
    '''
    def __init__(self):
        self.cards = []
    
    def get_top_card(self):
        '''
        Returns the top card in the pile.
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
            return self.cards.pop(0)
        
    def shuffle(self):
        '''
        Shuffles the pile.
        '''
        if len(self.cards) > 1:
            random.shuffle(self.cards)
            
class DrawPile(DiscardPile):
    '''
    Defines a draw pile
    '''
    def __init__(self):
        super().__init__()
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"] 
                                for v in ["A", "2", "3", "4", "5", "6", "7", "8", 
                                "9", "10", "J", "Q", "K"]]
            
    def deal_player_cards(self):
        '''
        Deals the players with 7 cards.
        Returns (list of Cards) cards dealt.
        '''
        return [self.cards.pop(i) for i in range(7)]
    
    def is_empty(self):
        '''
        Checks if the pile is empty.
        Returns True if it is, False otherwise.
        '''
        if self.cards:
            return False
        return True
        
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
        self.calculate_hand_value()
        return self.value
        
    def calculate_hand_value(self):
        self.value = 0
        for card in self.cards:
            if card.value.isnumeric():
                self.value += int(card.value)
            else:
                self.value += 10
    
    def display_hand(self):
        '''
        Displays the hand.
        '''
        for i, card in enumerate(self.cards):
            print("{}. -> {}".format(i, card))
            
    def hand_over(self):
        '''
        Checks if the hand is over or not.
        Returns True if it is, False otherwise.
        '''
        if self.cards:
            return False
        return True