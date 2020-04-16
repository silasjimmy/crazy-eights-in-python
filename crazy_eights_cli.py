#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 08:38:11 2020

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
    
class Deck:
    '''
    Defines the deck of cards.
    '''
    def __init__(self):
        self.cards = [Card(s, v) for s in ["Spades", "Clubs", "Hearts", "Diamonds"] 
                                for v in ["A", "2", "3", "4", "5", "6", "7", "8", 
                                "9", "10", "J", "Q", "K"]]
        
    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)
            
    def deal_cards(self):
        player_cards = []
        for i in range(7):
            player_cards.append(self.cards.pop(i))
        return player_cards
        
class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.value = 0
        
    def get_num_of_cards(self):
        return len(self.cards)
        
    def add_card(self, card):
        self.cards.append(card)
        
    def drop_card(self, num):
        dropped_card = self.cards.pop(num)
        return dropped_card
        
    def calculate_value(self):
        pass
            
    def get_value(self):
#        self.calculate_value()
#        return self.value
        pass
    
    def display(self):
        print("Remaining cards: {}".format(len(self.cards)))
        for i, card in enumerate(self.cards):
            print("{}. -> {}".format(i, card))

### Requirements:
# Deck of cards
# Discard pile
# PLayer hand
# Computer hand

class Game:
    def __init__(self):
        # Deck of cards
        self.deck = Deck()
        self.deck.shuffle()
        
        self.play_game()
        
    def play_game(self):
        # Discard pile
        self.discard_pile = []
        
        # Player hand
        self.player_hand = Hand(self.deck.deal_cards())
        
        card_num = input("Enter the card number to discard or any other input to draw: ")
        num_of_cards = self.player_hand.get_num_of_cards()
        valid_card_nums = [str(num) for num in list(range(num_of_cards))]
        if card_num in valid_card_nums:
            card_num = int(card_num)
            dropped_card = self.player_hand.drop_card(card_num)
            self.discard_pile.append(dropped_card)
            self.player_hand.display()
            print(self.discard_pile)
        else:
            print("Draw a card")
            

if __name__ == "__main__":
    game = Game()







