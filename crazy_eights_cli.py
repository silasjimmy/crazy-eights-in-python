#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 08:38:11 2020

@author: silasjimmy
"""

from CrazyEights import DiscardPile, DrawPile, Hand, Computer

class Game:
    def __init__(self):
        self.player_points = 0
        self.computer_points = 0
        
        print("######################")
        print("#### Crazy Eights ####")
        print("######################")
        print("\nWelcome to the card game Crazy Eights!")
        print("\n*** The goal is to reach 100 points. The first player to get the points is the winner. ***")
        print("\nStart the game!")
        print("\n######################")
        
        while True:
            winner, points = self.play_game()
            self.update_player_points(winner, points)
            if self.player_points >= 100 or self.computer_points >= 100:
                break
            print("\n#### No player has reached the 100 points target. Start a new game ####")
            
        print("\n######################")
        print("#### Game over! ######")
        print("######################")
              
        if self.player_points > self.computer_points:
            print("\nCongratulations!! You win!")
            print("Your total points are:", self.player_points)
        else:
            print("\nAaw, sorry buddy. You lost to the computer.")
            print("The computer's total points are:", self.computer_points)
            
        print("\n########################################")
        print("#### Thanks for playing the game! ######")
        print("########################################")
    
    def play_game(self):
        '''
        Initiates and controls the game.
        Returns (str, int) the winner of the hand and the points acquired.
        '''
        # Create and shuffle the draw pile
        draw_pile = DrawPile()
        draw_pile.shuffle()
        
        # Create the discard pile
        discard_pile = DiscardPile()
        
        # Deal each player 7 cards and create their hands
        player_cards = draw_pile.deal_player_cards()
        comp_cards = draw_pile.deal_player_cards()
        player = Hand(player_cards)
        computer = Computer(comp_cards)
        
        # Draw the starting card
        self.top_card = draw_pile.draw_card()
        
        # Set the suit of the top card to None
        self.top_card_suit = None
        
        # Add the start card to the discard pile
        discard_pile.add_card(self.top_card)
        
        # Game variables
        self.winner = None
        self.suit_in_play = False
        self.winner_points = 0
        
        while not player.hand_over() and not computer.hand_over():
            # First check if the draw pile is empty
            if draw_pile.is_empty():
                # Get the remaining cards from the discard and draw piles and add them together
                discard_pile_cards = discard_pile.get_cards()
                draw_pile_cards = draw_pile.get_cards()
                all_cards = discard_pile_cards + draw_pile_cards
                
                # Create a new draw pile with the remaining cards from discard and draw pile
                draw_pile = DrawPile(other_cards=all_cards)
                draw_pile.shuffle()
                
                # Create a new discard pile
                discard_pile = DiscardPile()

            print("\n*** Computer's cards are hidden. ***")
#            print("Computer cards are:")
#            computer.display_hand()
            
            # Print the player's hand
            print("\n#### Your cards ####")
            player.display_hand()
            
            # Print the top card or suit in play
            if not self.suit_in_play:
                print("\n#### The top card is", self.top_card, "####")
            else:
                print("\n#### The suit in play is", self.top_card_suit, "####")
            
            # Ask for the user input
            num = self.prompt_card_num()
            
            if num.isdigit():
                num = int(num)
                if self.card_in_hand(num, player):
                    played_card = player.get_card(num)
                    # Check if the card in hand is an 8 only
                    if player.get_num_of_cards() == 1 and played_card.value =="8":
                        # Drop card and add it to the discard pile
                        dropped = player.drop_card(num)
                        discard_pile.add_card(dropped)
                        print("\n>>> You dropped", dropped)
                        
                        # Prompt for a suit
                        self.top_card_suit = self.prompt_suit()
                        print("\n>>> You chose the suit", self.top_card_suit)
                        
                        # Turn the game to the chosen suit
                        self.suit_in_play = True
                        self.top_card = None
                        
                        # Draw a card from the draw pile and add it to the player's hand
                        draw = draw_pile.draw_card()
                        player.add_card(draw)
                        print("\n*** You were added a card because you played an 8 as your last card ***")
                    # Check if the prev card is was an 8
                    elif self.suit_in_play:
                        if played_card.suit == self.top_card_suit:
                            dropped = player.drop_card(num)
                            discard_pile.add_card(dropped)
                            print("\n>>> You  dropped", dropped)
                            
                            self.suit_in_play = False
                            self.top_card = dropped
                            self.top_card_suit = None
                        # Check if card played is an 8
                        elif self.is_eight(played_card):
                            dropped = player.drop_card(num)
                            discard_pile.add_card(dropped)
                            print("\n>>> You dropped", dropped)
                            
                            self.top_card_suit = self.prompt_suit()
                            print("\n>>> You chose the suit", self.top_card_suit)
                            
                            self.suit_in_play = True
                            self.top_card = None
                        else:
                            # Print denied card
                            print("!!! Please drop a card with suit {} or drop an 8 or draw a card.".format(self.top_card_suit))
                            continue
                    # Check if the dropped card is an 8
                    elif self.is_eight(played_card):
                        dropped = player.drop_card(num)
                        discard_pile.add_card(dropped)
                        print("\n>>> You dropped", dropped)
                        
                        self.top_card_suit = self.prompt_suit()
                        print("\n>>> You chose the suit", self.top_card_suit)
                        
                        self.suit_in_play = True
                        self.top_card = None
                    # Check if it matches suit or rank of the top card
                    elif self.match_top_card(played_card):
                        dropped = player.drop_card(num)
                        discard_pile.add_card(dropped)
                        print("\n>>> You  dropped", dropped)
                        
                        self.top_card_suit = dropped.suit
                        self.top_card = dropped
                    else:
                        # Print denied card
                        print("\n!!! The card does not match the suit or rank of the top card. Please try again !!!")
                        continue
                else:
                    # Print a message of not a valid card number in hand
                    print("\n!!! The number you entered is not a valid card number !!!")
                    continue
            else:
                # Draw a card from the draw pile and add to the player's hand
                draw = draw_pile.draw_card()
                player.add_card(draw)
                print("\n>>> You drew", draw)
            
            if player.hand_over():
                self.winner = "player"
                break
            
            ### Let the computer to play ###
            self.comp_suit, self.comp_dropped = computer.play(top_card=self.top_card, self.top_card_suit)
        
            if self.comp_suit:
                discard_pile.add_card(self.comp_dropped)
                self.top_card_suit = self.comp_suit
                print("\n*** The computer dropped ", self.comp_dropped, "and chose the suit", self.top_card_suit, "***")

                self.top_card_suit = self.comp_suit
                self.suit_in_play = True
                self.top_card = None
                
                # Check if its the only card remainining
                if computer.hand_over():
                    # Draw a card and add it to the computer's hand
                    draw = draw_pile.draw_card()
                    computer.add_card(draw)
                    print("\n*** The computer drew a card because it played an 8 as the last card ***")
            
            if self.comp_suit == None and self.comp_dropped:
                # Add the card in the discard pile
                discard_pile.add_card(self.comp_dropped)
                # Notify the player what card the computer dropped
                print("\n*** The computer dropped ", self.comp_dropped, "***")
                self.top_card_suit = self.comp_dropped.suit
                self.suit_in_play = False
                self.top_card = self.comp_dropped
                self.top_card_suit = None
                
            if self.comp_suit == None and self.comp_dropped == None:
                # Draw a card and add it to the computer's hand
                draw = draw_pile.draw_card()
                computer.add_card(draw)
                print("\n*** The computer drew a card ***")
                
            if computer.hand_over():
                self.winner = "computer"
                break
    
        print("\n######################")
        print("#### Hand over! ######")
        print("######################")
              
        # Print opponent's hand
        print("\nOpponent's remaining cards:")
        if self.winner == "player":
            computer.display_hand()
            self.winner_points = computer.get_hand_value()
        else:
            player.display_hand()
            self.winner_points = player.get_hand_value()
        
        # Print winner
        print("\n######################")
        print("\n* The winner of the hand is the {} with {} points *".format(self.winner, self.winner_points))
        print("\n######################")
              
        return self.winner, self.winner_points
            
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
        '''
        Checks if the card is an 8.
        Returns True if it is, False otherwise.
        '''
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
        if card.suit == self.top_card.suit or card.value == self.top_card.value:
            return True
        return False
    
    def update_player_points(self, winner, points):
        '''
        Updates the player points after each hand.
        '''
        if winner == "player":
            self.player_points += points
        else:
            self.computer_points += points


if __name__ == '__main__':
    game = Game()