#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 10:05:30 2020

@author: silasjimmy
"""

import random

SUITS = ["Diamonds", "Clubs", "Hearts", "Spades"]

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
        
    def get_cards(self):
        return self.cards
        
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
            
    def hand_empty(self):
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
        
    def play(self, top_card, suit_in_play):
        '''
        Makes the computer play.
        top_card (Card object): The top card in the discard pile.
        suit_in_play (str): The chosen suit in case the player dropped an 8.
        Returns (Card, str) the card to drop and the suit chosen if it played an 8.
        '''
        drop_match_options = []
        drop_suit_options = []
        chosen_suit, card_to_drop = None, None
        
        for index, card in enumerate(self.cards):
            if card.value == "8":
                # Drop the card
                card_to_drop = self.drop_card(index)
                # Find the suit with many cards
                suit_totals = {}
                # Calculate the totals
                for suit in SUITS:
                    suit_totals[suit] = 0
                    for card in self.cards:
                        if card.suit == suit:
                            suit_totals[suit] += 1
                            
                # Find the suit with many cards
                s, l = None, 0
                for suit_name, total in list(suit_totals.items()):
                    if total > l:
                        s = suit_name
                        l = total
                chosen_suit = s
                return chosen_suit, card_to_drop
            elif suit_in_play and card.suit == suit_in_play:
                drop_suit_options.append(card)
            else:
                if card.value == top_card.value or card.suit == top_card.suit:
                    drop_match_options.append(card)
                    
        # Check the cards to compare
        if suit_in_play:
            to_compare = drop_suit_options[:]
        else:
            to_compare = drop_match_options[:]
            
        # Find the card with highest value
        high_value, best_play = 0, None
        for card in to_compare:
            if card.value.isnumeric():
                card_value = int(card.value)
                if card_value > high_value:
                    high_value = card_value
                    best_play = card
            else:
                high_value = 10
                best_play = card
                
        # Drop the card
        if best_play:
            card_index = self.cards.index(best_play)
            card_to_drop = self.drop_card(card_index)
            
        return chosen_suit, card_to_drop