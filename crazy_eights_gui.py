#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 07:20:05 2020

@author: silasjimmy
"""

import os
import tkinter as tk
#import tkinter.messagebox as msg
from PIL import ImageTk, Image
from CrazyEights import DrawPile, DiscardPile

CARDS_FOLDER = os.path.join(os.getcwd(), "cards")
CARD_WIDTH = 82
CARD_HEIGHT = 113
CARD_PAD_X = 20
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_PADDING = 50
INTRO_MSG_WIDTH = 466
BTN_WIDTH = 278
BTN_HEIGHT = 30

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crazy Eights")
        self.resizable(False, False)
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 800
        window_height = 600
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))
        
        # Game variables
        self.player_points = 0
        self.computer_points = 0
        self.player_points_str = tk.StringVar()
        self.computer_points_str = tk.StringVar()
        # Set the point strings
        self.player_points_str.set("Player points: " +  str(self.player_points))
        self.computer_points_str.set("Computer points: " +  str(self.computer_points))
        
        #### Creating the game screen ####
        # Creating the game screen
        self.game_screen = tk.Frame(self, width=800, height=600, bg="green")
        self.game_screen.pack_propagate(0)
        # Create the draw pile and shuffle it
        self.draw_pile = DrawPile()
        self.draw_pile.shuffle()
        # Deal the players their cards
        self.player_cards = self.draw_pile.deal_player_cards()
        self.computer_cards = self.draw_pile.deal_player_cards()
        # Create the discard pile
        self.discard_pile = DiscardPile()
        self.top_card = self.draw_pile.draw_card()
        self.discard_pile.add_card(self.top_card)
        # Points labels
        self.player_points_label = tk.Label(self.game_screen, textvar=self.player_points_str, font="Arial 15 bold", fg="white", bg="green")
        self.comp_points_label = tk.Label(self.game_screen, textvar=self.computer_points_str, font="Arial 15 bold", fg="white", bg="green")
        # Display the computer's hand
        self.display_computer_hand(self.computer_cards)
        # Display the draw and discard pile
        self.display_draw_pile()
        self.display_discard_pile()
        # Pack the points labels
        self.player_points_label.pack(side=tk.RIGHT, anchor=tk.S, padx=(0, 20), pady=(0, 15))
        self.comp_points_label.pack(side=tk.LEFT, anchor=tk.N, padx=(20, 0), pady=(15, 0))
        # Display the player's hand
        self.display_player_hand(self.player_cards)
        
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
        msg_x = (WINDOW_WIDTH - INTRO_MSG_WIDTH) // 2
        btn_x = (WINDOW_WIDTH - (WINDOW_PADDING + BTN_WIDTH))
        btn_y = WINDOW_HEIGHT - ((WINDOW_PADDING * 2) + BTN_HEIGHT)
        # Placing widgets to the intro screen
        self.intro_msg.place(x=msg_x, y=250)
        self.play_btn.place(x=WINDOW_PADDING, y=btn_y)
        self.quit_btn.place(x=btn_x, y=btn_y)
        self.make_dragable(self.play_btn)
        self.intro_screen.pack_propagate(0)
        self.intro_screen.pack(side=tk.LEFT, anchor=tk.N)
        
    def start_game(self):
        '''
        Starts the game by clearing the intro screen and displaying the game screen.
        '''
        self.intro_screen.pack_forget()
        self.game_screen.pack(side=tk.LEFT, anchor=tk.N)
#        msg.showinfo("Crazy Eights", "The goal is to reach 100 points. The first player to get the points is the winner. \nStart the game!")
        
    def quit_game(self):
        '''
        Destroys the game window.
        '''
        self.after(300, self.destroy)
        
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
        
    def display_player_hand(self, cards):
        '''
        Displays the player's hand.
        '''
        # Creating the card images
        self.player_card_names = [self.card_name(card) for card in cards]
        self.player_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + card_name)) for card_name in self.player_card_names]
        self.player_card_labels = [tk.Label(self.game_screen, image=card_image) for card_image in self.player_card_images]
        
        # Centering the cards horizontally
        cards_length = ((len(cards) - 1) * CARD_PAD_X) + CARD_WIDTH
        rem_space = WINDOW_WIDTH - cards_length
        x = rem_space // 2
        y = WINDOW_HEIGHT - (CARD_HEIGHT + WINDOW_PADDING)
        
        # Placing the cards to the game screen
        for i, card_label in enumerate(self.player_card_labels):
            x_pad = i * CARD_PAD_X
            card_label.place(x=x+x_pad, y=y)
            self.make_dragable(card_label)   
            
    def display_computer_hand(self, cards, reveal=False):
        '''
        Displays the computer's hand.
        '''
        if reveal:
            self.comp_card_names = [self.card_name(card) for card in cards]
            self.comp_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + card_name)) for card_name in self.comp_card_names]
        else:
            self.comp_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/back.png")) for i in range(len(cards))]
        self.comp_card_labels = [tk.Label(self.game_screen, image=card_image) for card_image in self.comp_card_images]
        
        cards_length = ((len(cards) - 1) * CARD_PAD_X) + CARD_WIDTH
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
        
    def display_discard_pile(self):
        '''
        Displays the discard pile.
        '''
        self.top_card_name = self.card_name(self.top_card)
        self.top_card_img = ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + self.top_card_name))
        self.top_card_label = tk.Label(self.game_screen, image=self.top_card_img)
        
        occupied_space = (CARD_HEIGHT * 2) + (WINDOW_PADDING * 2)
        rem_space = WINDOW_HEIGHT - occupied_space
        x = WINDOW_WIDTH - (CARD_WIDTH + (WINDOW_PADDING * 2))
        y = CARD_HEIGHT + (rem_space // 2)
        
        self.top_card_label.place(x=x, y=y)
        
    def draw_card(self, event):
        print("Draw a card!")
        
    def on_drag_start(self, event):
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        # Card's original coords
        self.original_x = widget.winfo_x()
        self.original_y = widget.winfo_y()
        
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
            print("Discard")
        else:
            print("Return to base!")
            widget.place(x=self.original_x, y=self.original_y)
        
    def make_dragable(self, widget):
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)
        widget.bind("<ButtonRelease-1>", self.on_drag_release)
        
game = Game()
game.mainloop()