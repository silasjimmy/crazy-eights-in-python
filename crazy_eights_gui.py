#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 07:20:05 2020

@author: silasjimmy
"""

import os
import tkinter as tk
import tkinter.messagebox as msg
from PIL import ImageTk, Image
from CrazyEights import DrawPile, DiscardPile, Hand, Computer

CARDS_FOLDER = os.path.join(os.getcwd(), "cards")
CARD_WIDTH = 82
CARD_HEIGHT = 113
CARD_PAD_X = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_PADDING = 50

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crazy Eights")
        self.resizable(False, False)
        
        # Center the window
#        screen_width = self.winfo_screenwidth()
#        screen_height = self.winfo_screenheight()
#        x = (screen_width / 2) - (WINDOW_WIDTH / 2)
#        y = (screen_height / 2) - (WINDOW_HEIGHT / 2)
        x, y = self.center_window(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.geometry("%dx%d+%d+%d" % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))
        
        # Game variables
        self.player_points = 0
        self.computer_points = 0
        
        # GUI variables
        self.player_points_str = tk.StringVar()
        self.computer_points_str = tk.StringVar()
        self.suit_choice = tk.StringVar()
        self.suit_in_play = None
        
        # Set the point strings
        self.player_points_str.set("Player points: " +  str(self.player_points))
        self.computer_points_str.set("Computer points: " +  str(self.computer_points))
        
        #### Creating the game screen ####
        # Creating the game screen
        self.game_screen = tk.Frame(self, width=800, height=600, bg="green")
        self.game_screen.pack_propagate(0)
        
        # Points labels
        self.player_points_label = tk.Label(self.game_screen, textvar=self.player_points_str, font="Arial 15 bold", fg="white", bg="green")
        self.comp_points_label = tk.Label(self.game_screen, textvar=self.computer_points_str, font="Arial 15 bold", fg="white", bg="green")
        
        # Pack the points labels
        self.player_points_label.pack(side=tk.RIGHT, anchor=tk.S, padx=(0, 20), pady=(0, 15))
        self.comp_points_label.pack(side=tk.LEFT, anchor=tk.N, padx=(20, 0), pady=(15, 0))
        
        #### Creating the intro screen ####
        # Creating the intro screen
        self.intro_screen = tk.Frame(self, width=800, height=600, bg="white")
        self.intro_screen.pack_propagate(0)
        
        # Creating the intro message
        self.intro_msg = tk.Label(self.intro_screen, text="Welcome to the game Crazy Eights!", font="Arial 20 bold", bg="white")
        
        # Creating the play and quit buttons
        self.play_btn = tk.Button(self.intro_screen, text="Start", font=5, width=25, command=self.start_game)
        self.quit_btn = tk.Button(self.intro_screen, text="Quit", font=5, width=25, command=self.quit_game)
        
        # Coords to place intro widgets
        msg_x = (WINDOW_WIDTH - self.intro_msg.winfo_reqwidth()) // 2
        btn_x = (WINDOW_WIDTH - (WINDOW_PADDING + self.play_btn.winfo_reqwidth()))
        btn_y = WINDOW_HEIGHT - ((WINDOW_PADDING * 2) + self.play_btn.winfo_reqheight())
       
        # Placing widgets to the intro screen
        self.intro_msg.place(x=msg_x, y=250)
        self.play_btn.place(x=WINDOW_PADDING, y=btn_y)
        self.quit_btn.place(x=btn_x, y=btn_y)
        self.make_dragable(self.play_btn)
        self.intro_screen.pack_propagate(0)
        self.intro_screen.pack(side=tk.LEFT, anchor=tk.N)
        
    def center_window(self, window_width, window_height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_center = (screen_width - window_width) / 2
        y_center = (screen_height - window_height) / 2
        return x_center, y_center
        
    def start_game(self):
        '''
        Starts the game by clearing the intro screen and displaying the game screen.
        '''
        self.intro_screen.pack_forget()
        self.play_game()
#        msg.showinfo("Crazy Eights", "The goal is to reach 100 points. The first player to get the points is the winner. \nStart the game!")
        
    def quit_game(self):
        '''
        Destroys the game window.
        '''
        self.after(300, self.destroy)
        
    def play_game(self):
        # Create the draw pile and shuffle it
        self.draw_pile = DrawPile()
        self.draw_pile.shuffle()
        
        # Deal the players their cards
        player_cards = self.draw_pile.deal_player_cards()
        computer_cards = self.draw_pile.deal_player_cards()
        
        # Create the players' hands
        self.player = Hand(player_cards)
        self.computer = Computer(computer_cards)
        
        # Create the discard pile
        self.discard_pile = DiscardPile()
        self.top_card = self.draw_pile.draw_card()
        self.discard_pile.add_card(self.top_card)
        
        # Display the computer's hand
        self.display_computer_hand(f_time=True, reveal=True)
        
        # Display the draw and discard pile
        self.display_draw_pile()
        self.display_discard_pile(f_time=True)
        
        # Display the player's hand
        self.display_player_hand(f_time=True)
        
        self.game_screen.pack(side=tk.LEFT, anchor=tk.N)
        
    def card_name(self, card):
        '''
        Retrieves the card name.
        card (Card object): A card.
        Returns (str) the name (suit+rank) of the card.
        '''
        suit = card.suit
        rank = card.value
        card_name = suit + rank + ".png"
        return card_name
        
    def display_player_hand(self, f_time=False):
        '''
        Displays the player's hand.
        '''
        # Destroy the images if they already exist
        if not f_time:
            for label in self.player_card_labels:
                label.destroy()
        # Creating the card images
        player_cards = self.player.get_cards()
        self.player_card_names = [self.card_name(card) for card in player_cards]
        self.player_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + card_name)) for card_name in self.player_card_names]
        self.player_card_labels = [tk.Label(self.game_screen, image=card_image) for card_image in self.player_card_images]
        
        # Centering the cards horizontally
        cards_length = ((len(player_cards) - 1) * CARD_PAD_X) + CARD_WIDTH
        rem_space = WINDOW_WIDTH - cards_length
        x = rem_space // 2
        y = WINDOW_HEIGHT - (CARD_HEIGHT + WINDOW_PADDING)
        
        # Placing the cards to the game screen
        for i, card_label in enumerate(self.player_card_labels):
            x_pad = i * CARD_PAD_X
            card_label.place(x=x+x_pad, y=y)
            self.make_dragable(card_label)   
            
    def display_computer_hand(self, f_time=False, reveal=False):
        '''
        Displays the computer's hand.
        '''
        # Destroy the images if they already exist
        if not f_time:
            for label in self.comp_card_labels:
                label.destroy()
        computer_cards = self.computer.get_cards()
        if reveal:
            self.comp_card_names = [self.card_name(card) for card in computer_cards]
            self.comp_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + card_name)) for card_name in self.comp_card_names]
        else:
            self.comp_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/back.png")) for i in range(len(computer_cards))]
        self.comp_card_labels = [tk.Label(self.game_screen, image=card_image) for card_image in self.comp_card_images]
        
        cards_length = ((len(computer_cards) - 1) * CARD_PAD_X) + CARD_WIDTH
        rem_space = WINDOW_WIDTH - cards_length
        x = rem_space // 2
        y = WINDOW_PADDING
        
        for i, card_label in enumerate(self.comp_card_labels):
            x_pad = i * CARD_PAD_X
            card_label.place(x=x+x_pad, y=y)
            
    def display_draw_pile(self):
        '''
        Displays the draw pile.
        '''
        self.card_back = ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/back.png"))
        self.draw_pile_image = tk.Label(self.game_screen, image=self.card_back)
        
        occupied_space = (CARD_HEIGHT * 2) + (WINDOW_PADDING * 2)
        rem_space = WINDOW_HEIGHT - occupied_space
        x = WINDOW_PADDING * 2
        y = CARD_HEIGHT + (rem_space // 2)
        
        self.draw_pile_image.place(x=x, y=y)
        self.draw_pile_image.bind("<Button-1>", self.draw_card)
        
    def display_discard_pile(self, f_time=False):
        '''
        Displays the discard pile.
        '''
        # Destroy the image it already exist
        if not f_time:
            self.top_card_label.destroy()
        self.top_card = self.discard_pile.get_top_card()
        top_card_name = self.card_name(self.top_card)
        self.top_card_img = ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + top_card_name))
        self.top_card_label = tk.Label(self.game_screen, image=self.top_card_img)
        
        occupied_space = (CARD_HEIGHT * 2) + (WINDOW_PADDING * 2)
        rem_space = WINDOW_HEIGHT - occupied_space
        x = WINDOW_WIDTH - (CARD_WIDTH + (WINDOW_PADDING * 2))
        y = CARD_HEIGHT + (rem_space // 2)
        
        self.top_card_label.place(x=x, y=y)
        
    def draw_card(self, event):
        # Draw a card from the draw pile
        draw = self.draw_pile.draw_card()
        # Add the card to the player's hand
        self.player.add_card(draw)
#        # Display the player's hand
#        self.display_player_hand()
        
        ### Let the computer play ###
        self.computer_play()
        # Check if computer hand is over
        if self.computer.hand_over():
            msg.showinfo("Hand over", "The computer won the hand!")
        
    def moved_card(self, card_widget):
        for index, card_label in enumerate(self.player_card_labels):
            if card_widget == card_label:
                return index
            
    def match_top_card(self, card):
        '''
        Checks if the card matches the top card's suit or rank.
        Returns True if it matches, False otherwise.
        '''
        self.top_card = self.discard_pile.get_top_card()
        if card.suit == self.top_card.suit or card.value == self.top_card.value:
            return True
        return False
    
    def is_eight(self, card):
        '''
        Checks if the card is an 8.
        Returns True if it is, False otherwise.
        '''
        if card.value.isdigit() and int(card.value) == 8:
            return True
        return False
    
    def add_more_card(self, hand):
        draw = self.draw_pile.draw_card()
        hand.add_card(draw)
        print("The hand was added a card because played 8 as the last card.")
        
    def prompt_suit(self):
        # Creating the suit window
        suit_window = tk.Toplevel(bg="white")
        suit_window.title("Choose a suit")
        # Width and Height of the suit window
        suit_win_width, suit_win_height = 250, 200
        # Centering the suit window
        x, y = self.center_window(suit_win_width, suit_win_height)
        suit_window.geometry("%dx%d+%d+%d" % (suit_win_width, suit_win_height, x, y))
        SUITS = [("Diamonds", "Diamonds"), 
                 ("Hearts", "Hearts"),
                 ("Spades", "Spades"), 
                 ("Clubs", "Clubs")]
        for suit, suit_choice in SUITS:
            s = tk.Radiobutton(suit_window, text=suit, font="Arial 12 bold", variable=self.suit_choice, value=suit_choice)
            s.pack(anchor=tk.CENTER, pady=(10, 5))
    
    def drop_card(self, card_pos):
        # Drop the card
        drop = self.player.drop_card(card_pos)
        # Add it to the discard pile
        self.discard_pile.add_card(drop)
        # Diplay the discard pile
        self.display_discard_pile()
        # Display the player hand
        self.display_player_hand()
        
    def on_drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        # Card's original coords
        self.original_x = widget.winfo_x()
        self.original_y = widget.winfo_y()
        # Track the card if dropped
        self.card_dropped = False
        
    def on_drag_motion(self, event):
        widget = event.widget
        # Get the position to place the widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        # Define the window boundary of the drag and drop
        x_boundary = 800 - widget.winfo_width()
        y_boundary = 600 - widget.winfo_height()
        
        if (x > 0 and x < x_boundary) and (y > 0 and y < y_boundary):
            widget.place(x=x, y=y)
            
    def on_drag_release(self, event):
        widget = event.widget
        x = widget.winfo_x()
        y = widget.winfo_y()
        if (x > 546 and x < 690) and (y > 147 and y < 353):
            # Get the card that has been dropped
            position = self.moved_card(widget)
            dropped = self.player.get_card(position)
            if (self.suit_in_play == dropped.suit and not self.match_top_card(dropped)) or (self.match_top_card(dropped) and self.suit_in_play == None) or self.is_eight(dropped):
                # Check if the play is based on a suit
                if self.suit_in_play:
                    if dropped.suit == self.suit_in_play:
                        # Drop the card
                        self.drop_card(position)
                        # Set the suit to None
                        self.suit_in_play = None
                        print("Player dropped a card matching", self.suit_in_play)
                    elif self.is_eight(dropped):
                        # Drop the card
                        self.drop_card(position)
                        # Prompt for a suit
                        self.prompt_suit()
                        self.suit_in_play = "Diamonds"
                        print("Player prompted the suit", self.suit_in_play)
                        # Check if last play was an 8
                        if self.player.hand_over():
                            self.add_more_card(self.player)
                else:
                    # Check if the play is a normal one
                    if self.match_top_card(dropped):
                        # Drop the card
                        self.drop_card(position)
                    elif self.is_eight(dropped):
                        # Drop the card
                        self.drop_card(position)
                        # Prompt for a suit
                        self.prompt_suit()
                        self.suit_in_play = "Hearts"
                        print("Player prompted the suit", self.suit_in_play)
                        # Check if last play was an 8
                        if self.player.hand_over():
                            self.add_more_card(self.player)
                            
                # Display the player hand
                self.display_player_hand()
                    
                # Check if the player's hand is over
                if self.player.hand_over():
                    msg.showinfo("Hand over", "Congratulations! You win the hand!")
                    
                ### Let the computer play ###
                self.computer_play()
                
                # Check if computer hand is over
                if self.computer.hand_over():
                    msg.showinfo("Hand over", "The computer won the hand!")
            else:
                widget.place(x=self.original_x, y=self.original_y)
        else:
            widget.place(x=self.original_x, y=self.original_y)
            
    def computer_play(self):
        self.top_card = self.discard_pile.get_top_card()
        print("\nSuit in play:", self.suit_in_play)
        
        comp_suit, comp_dropped = self.computer.play1(self.top_card, self.suit_in_play)
        print("Comp suit:", comp_suit, "Comp dropped:", comp_dropped)
        if comp_suit:
            # Add the card to the discard pile
            self.discard_pile.add_card(comp_dropped)
            # Display the discard pile
            self.display_discard_pile()
            # Set the suit in play to the chosen suit by comp
            self.suit_in_play = comp_suit
            # Notify the player of the suit chosen by computer
            msg.showinfo("Suit choice", "The computer chose the suit " + self.suit_in_play)
#            # Check if its the only card remainining
#            if self.computer.hand_over():
#                # Draw a card and add it to the computer's hand
#                draw = self.draw_pile.draw_card()
#                self.computer.add_card(draw)
        if comp_suit == None and comp_dropped:
            # Add the card in the discard pile
            self.discard_pile.add_card(comp_dropped)
            # Display the discard pile
            self.display_discard_pile()
            # Set the suit in play to none
            self.suit_in_play = None
        if comp_suit == None and comp_dropped == None:
            # Draw a card and add it to the computer's hand
            draw = self.draw_pile.draw_card()
            self.computer.add_card(draw)
            print("Computer had no card and drew", draw)
        
        # Display the computer's hand
        self.display_computer_hand(reveal=True)
        # Display the player's hand
        self.display_player_hand()
        
    def make_dragable(self, widget):
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)
        widget.bind("<ButtonRelease-1>", self.on_drag_release)
        
game = Game()
game.mainloop()