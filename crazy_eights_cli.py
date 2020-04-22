#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 08:38:11 2020

@author: silasjimmy
"""

import random

from CrazyEights import Card, DiscardPile, DrawPile, Hand
            
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
        Returns (Card object) the card found, None if not.
        '''
        for index, card in enumerate(self.cards):
            if card.suit == top_card.suit or card.value == top_card.value:
                drop = self.drop_card(index)
                return drop
    
    def check_for_eight(self):
        '''
        Checks the hand for an 8.
        Returns (Card object) the card found, None if not.
        '''
        for index, card in enumerate(self.cards):
            if card.value.isdigit() and int(card.value) == 8:
                drop = self.drop_card(index)
                return drop
            
    def get_card_with_suit(self, specific_suit):
        '''
        Gets the card with the specified suit.
        specific_suit (str): The suit to find.
        Returns (Card object) the card found, None if not.
        '''
        for index, card in enumerate(self.cards):
            if card.suit == specific_suit:
                drop = self.drop_card(index)
                return drop
    
    def play(self, top_card=None, specific_suit=None):
        '''
        Defines how the computer plays.
        top_card (Card object): The top card in the discard pile.
        specific_suit (str): The suit chosen by the player.
        Returns (str, Card object) the suit chosen in case an * was played and the card played.
        '''
        suit = None
        
        # Play if it is a specific suit
        if specific_suit:
            # PLay card if found a card with specific suit
            card = self.get_card_with_suit(specific_suit)
            if card and card.value.isdigit() and int(card.value) == 8:
                suit = random.choice(list(set([card.suit for card in self.cards])))
                return suit, card
            # Play card if found no card and there is an 8
            eight = self.check_for_eight()
            if eight:
                suit = random.choice(list(set([card.suit for card in self.cards])))
                return suit, eight
        
        if top_card:
            # Play if it is has a card matching the top card in discard pile
            playable_card = self.get_playable_card(top_card)
            if playable_card:
                return suit, playable_card
            
            # Play if has an 8
            eight = self.check_for_eight()
            if eight:
                suit = random.choice(list(set([card.suit for card in self.cards])))
                return suit, eight
        return suit, None

class Game:
    def __init__(self):
        print("######################")
        print("##### Crazy Eights####")
        print("######################")
        print("\nWelcome to the card game Crazy Eights!")
        self.play_game()
    
    def play_game(self):
        '''
        Initiates and controls the game.
        '''
        # Create the draw pil
        draw_pile = DrawPile()
        # Shuffle the draw pile
        draw_pile.shuffle()
        
        # Create the discard pile
        discard_pile = DiscardPile()
        
        # Deal each player 7 cards
        player_cards = draw_pile.deal_player_cards()
        comp_cards = draw_pile.deal_player_cards()
        
        # Create the player hands
        cardz = [Card("Spades", "3"), Card("Clubs", "8"), Card("Diamonds", "Q")]
        carnz = [Card("Hearts", "4"), Card("Spades", "8"), Card("Clubs", "9")]
        player = Hand(cardz)
        computer = Computer(carnz)
        
        # Draw the starting card
        self.top_card = Card("Clubs", "4")# draw_pile.draw_card()
        
        # Set the suit and rank of the top card
        self.top_card_suit = self.top_card.suit
        self.top_card_rank = self.top_card.value
        
        # Add the start card to the discard pile
        discard_pile.add_card(self.top_card)
        
        # Track the winner
        self.winner = None
        # Track if 8 played
        self.any_card = False
        
        # Start the game loop
        while not player.hand_over() and not computer.hand_over():
            # Print the player's hand
            print("\nYour cards are:")
            player.display_hand()
            
            # Print computer's hand
            print("\nComps cards are:")
            computer.display_hand()
            
            # Print the top card
            if not self.any_card:
                print("\nThe top card is", self.top_card)
            else:
                print("\nThe suit in play is:", self.top_card_suit)
            
            # Ask for the user input
            num = self.prompt_card_num()
            
            # Check if the player played a number or letter
            if num.isdigit():
                # Convert num to int
                num = int(num)
                # Check if the number is valid
                if self.card_in_hand(num, player):
                    # Played card
                    played_card = player.get_card(num)
                    # Check if the prev card is was an 8
                    if self.any_card:
                        # Check if the suit of card dropped matches selected one
                        if played_card.suit == self.top_card_suit:
                            # Player drops a card
                            dropped = player.drop_card(num)
                            # Add the card to the discard pile
                            discard_pile.add_card(dropped)
                            # Print Dropped card
                            print("\nYou  dropped", dropped)
                            # Set the suit and rank of the top card
                            self.top_card_suit = dropped.suit
                            self.top_card_rank = dropped.value
                            # Turn the game to the set rank and suit
                            self.any_card = False
                            # Set top card to dropped
                            self.top_card = dropped
                            # Set suit to None
                            self.top_card_suit = None
                        # Check if card played is an 8
                        elif self.is_eight(played_card):
                            # Player drops a card
                            dropped = player.drop_card(num)
                            # Add the dropped card to the discard pile
                            discard_pile.add_card(dropped)
                            # Choose a suit
                            self.top_card_suit = self.prompt_suit()
                            # Print the chosen suit
                            print("\nYou dropped {} and chose the suit {}".format(dropped, self.top_card_suit))
                            # Turn the game to the chosen suit
                            self.any_card = True
                            # Set top card to None
                            self.top_card = None
                        else:
                            print("Please drop a card with suit {} or drop an 8 or draw a card.".format(self.top_card_suit))
                            continue
                    # Check if the dropped card is an 8
                    elif self.is_eight(played_card):
                        # Player drops a card
                        dropped = player.drop_card(num)
                        # Add the dropped card to the discard pile
                        discard_pile.add_card(dropped)
                        # Choose a suit
                        self.top_card_suit = self.prompt_suit()
                        # Print the chosen suit
                        print("\nYou dropped {} and chose the suit {}".format(dropped, self.top_card_suit))
                        # Turn the game to the chosen suit
                        self.any_card = True
                        # Set top card to None
                        self.top_card = None
                    # Check if it matches suit or rank of the top card
                    elif self.match_top_card(played_card):
                        # Player drops a card
                        dropped = player.drop_card(num)
                        # Add the card to the discard pile
                        discard_pile.add_card(dropped)
                        # Print Dropped card
                        print("\nYou  dropped", dropped)
                        # Set the suit and rank of the top card
                        self.top_card_suit = dropped.suit
                        self.top_card_rank = dropped.value
                    else:
                        # Player draws a card
                        draw = draw_pile.draw_card()
                        player.add_card(draw)
                        # Print denied card
                        print("\nThe card was denied. You were given {} as a penalty.".format(draw))
                else:
                    # Print a message of not a valid card number in hand
                    print("\nThe number you entered is not a valid card number.")
                    continue
            else:
                # Draw a card from the draw pile
                draw = draw_pile.draw_card()
                player.add_card(draw)
                print("\nYou drew {}".format(draw))
            
            if player.hand_over():
                self.winner = "player"
                break
            
            print("\nPlayed 8 after player:", self.any_card)
            
            ### Let the computer to play ###
            self.comp_suit, self.comp_dropped = computer.play(top_card=self.top_card, specific_suit=self.top_card_suit)
                
            print("\nComputer's choice is: suit -> {}, card -> {}".format(self.comp_suit, self.comp_dropped))
        
            if self.comp_suit and self.comp_dropped:
                # Add the card in the discard pile
                discard_pile.add_card(self.comp_dropped)
                # Set the suit in play
                self.top_card_suit = self.comp_suit
                # Print the chosen suit
                print("\nThe computer dropped ", self.comp_dropped, "and chose the suit", self.top_card_suit)
                # Set the rank to the chosen one
                self.top_card_suit = self.comp_suit
                # Turn the game to the chosen suit
                self.any_card = True
                # Set top card to None
                self.top_card = None
            if not self.comp_suit and self.comp_dropped:
                # Add the card in the discard pile
                discard_pile.add_card(self.comp_dropped)
                # Notify the player what card the computer dropped
                print("\nThe computer dropped ", self.comp_dropped)
                # Set the suit and rank of the top card
                self.top_card_suit = self.comp_dropped.suit
                self.top_card_rank = self.comp_dropped.value
                # Change the specific suit play
                self.any_card = False
                # Set top card to dropped
                self.top_card = self.comp_dropped
                # Set suit to None
                self.top_card_suit = None
            if not self.comp_suit and not self.comp_dropped:
                # Draw a card
                draw = draw_pile.draw_card()
                computer.add_card(draw)
#                # Print the desicion to the screen
#                print("\nThe computer drew a card!")
                
            if computer.hand_over():
                self.winner = "computer"
                break
#            
            print("\nPlayed 8 after computer:", self.any_card)
#            # Print the game state
#            print("\nDraw pile empty:", draw_pile.is_empty())
        
        print("\nGame over!")
        # Print comps hand
        print("\nComputer's cards:")
        computer.display_hand()
        # Print winner
        print("\nThe {} wins!".format(self.winner))
            
    def prompt_card_num(self):
        '''
        Prompts the player to enter a card number to drop or d/D to draw a card.
        Returns (int/str) the number/character entered.
        '''
        num = input("Enter the number of the card to drop or d/D to draw: ")
        while not num.isdigit() and num not in ['d', 'D']:
            num = input("Please enter a valid card number or characters d/D: ")
        if num.isalpha():
            return num.lower()
        return num
    
    def is_eight(self, card):
        if card.value.isdigit() and int(card.value) == 8:
            return True
        return False
            
    def card_in_hand(self, num, hand):
        '''
        Checks if the card is in the player's hand.
        num (int): The position of the card in the hand.
        hand (Hand object): The player's hand
        Returns True if the card is in the hand, False otherwise.
        '''
        num_of_cards = hand.get_num_of_cards()
        valid_nums = list(range(num_of_cards))
        return int(num) in valid_nums
    
    def prompt_suit(self):
        '''
        Prompts the player to enter his desired suit.
        Returns (str) the suit chosen.
        '''
        suit = input("Enter the desired suit to continue (S/D/C/H): ").lower()
        while suit not in ['s', 'd', 'c', 'h']:
            suit = input("The initials (S/D/C/H) represent the 4 suits. Please enter a valid input: ")
        if suit == 's':
            return "Spades"
        elif suit == 'd':
            return "Diamonds"
        elif suit == 'c':
            return "Clubs"
        elif suit == 'h':
            return "Hearts"
        
    def match_top_card(self, card):
        '''
        Checks if the card matches the top card's suit or rank.
        Returns True if it matches, False otherwise.
        '''
        if card.suit == self.top_card_suit or card.value == self.top_card_rank:
            return True
        return False


if __name__ == '__main__':
    game = Game()


    



