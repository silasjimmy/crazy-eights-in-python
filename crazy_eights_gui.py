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
from CrazyEights import SUITS, DrawPile, DiscardPile, Hand, Computer

CARDS_FOLDER = os.path.join(os.getcwd(), "cards")
CARD_WIDTH = 82
CARD_HEIGHT = 113
CARD_PAD_X = 22
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_PADDING = 50

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crazy Eights")
        self.resizable(False, False)
        
        # Center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) / 2
        y = (screen_height - WINDOW_HEIGHT) / 2
        self.geometry("%dx%d+%d+%d" % (WINDOW_WIDTH, WINDOW_HEIGHT, x, y))
        
        self.player_points = 0
        self.computer_points = 0
        self.player_points_str = tk.StringVar()
        self.computer_points_str = tk.StringVar()
        self.suit_choice = tk.StringVar()
        self.suit_in_play = None
        
        self.player_points_str.set("Player points: " +  str(self.player_points))
        self.computer_points_str.set("Computer points: " +  str(self.computer_points))
        
        # Creating the game screen
        self.create_game_screen()
        
        # Creating the intro screen
        self.intro_screen = tk.Frame(self, width=800, height=600, bg="white")
        self.intro_screen.pack_propagate(0)
        self.intro_msg = tk.Label(self.intro_screen, text="Welcome to the game Crazy Eights!", font="Arial 20 bold", bg="white")
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
    
    def create_game_screen(self):
        '''
        Creates the game screen.
        '''
        self.game_screen = tk.Frame(self, width=800, height=600, bg="green")
        self.game_screen.pack_propagate(0)
        
        self.player_points_label = tk.Label(self.game_screen, textvar=self.player_points_str, font="Arial 15 bold", fg="white", bg="green")
        self.comp_points_label = tk.Label(self.game_screen, textvar=self.computer_points_str, font="Arial 15 bold", fg="white", bg="green")
        
        self.player_points_label.pack(side=tk.RIGHT, anchor=tk.S, padx=(0, 20), pady=(0, 15))
        self.comp_points_label.pack(side=tk.LEFT, anchor=tk.N, padx=(20, 0), pady=(15, 0))
        
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
        '''
        Initializes a new game.
        '''
        self.draw_pile = DrawPile()
        self.draw_pile.shuffle()
        
        player_cards = self.draw_pile.deal_player_cards()
        computer_cards = self.draw_pile.deal_player_cards()
        
        self.player = Hand(player_cards)
        self.computer = Computer(computer_cards)
        
        self.discard_pile = DiscardPile()
        self.top_card = self.draw_pile.draw_card()
        self.discard_pile.add_card(self.top_card)
        
        self.display_computer_hand(f_time=True)
        self.display_draw_pile()
        self.display_discard_pile(f_time=True)
        self.display_player_hand(f_time=True)
        
        self.game_screen.pack(side=tk.LEFT, anchor=tk.N)
        self.computer_turn = False
        
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
        f_time (bool): Flag to indicate whether it is the first time to display cards or not.
        '''
        # Destroy the images if they already exist
        if not f_time:
            for label in self.player_card_labels:
                label.destroy()
                
        player_cards = self.player.get_cards()
        self.player_card_names = [self.card_name(card) for card in player_cards]
        self.player_card_images = [ImageTk.PhotoImage(Image.open(CARDS_FOLDER + "/" + card_name)) for card_name in self.player_card_names]
        self.player_card_labels = [tk.Label(self.game_screen, image=card_image) for card_image in self.player_card_images]
        
        # Centering the cards horizontally
        cards_length = ((len(player_cards) - 1) * CARD_PAD_X) + CARD_WIDTH
        rem_space = WINDOW_WIDTH - cards_length
        x = rem_space // 2
        y = WINDOW_HEIGHT - (CARD_HEIGHT + WINDOW_PADDING)
        
        for i, card_label in enumerate(self.player_card_labels):
            x_pad = i * CARD_PAD_X
            card_label.place(x=x+x_pad, y=y)
            self.make_dragable(card_label)   
            
    def display_computer_hand(self, f_time=False, reveal=False):
        '''
        Displays the computer's hand.
        f_time (bool): Flag to indicate whether it is the first time to display cards or not.
        reveal (bool): Flag to indicate whether to reveal the hand or not
        '''
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
        f_time (bool): Flag to indicate whether it is the first time to display the card or not.
        '''
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
        '''
        Draws a card, adds it to the player's hand and lets the computer play.
        '''        
        draw = self.draw_pile.draw_card()
        self.player.add_card(draw)
        self.display_player_hand()
        
        self.computer_play()
        if self.computer.hand_empty():
            print("Hand over!!")
            self.hand_over("computer")
        
    def moved_card(self, card_widget):
        '''
        Gets the index of the dragged card to be dropped.
        '''
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
        card (Card object): The card to check if it is an 8.
        Returns True if it is, False otherwise.
        '''
        if card.value.isdigit() and int(card.value) == 8:
            return True
        return False
    
    def add_more_card(self, hand):
        '''
        Adds a card to the hand if the last card played was an 8.
        hand (Hand object): Player/Computer hand.
        '''
        draw = self.draw_pile.draw_card()
        hand.add_card(draw)
        
    def center_pop_up(self, window_width, window_height):
        '''
        Finds the coordinates to center the pop up window to the screen.
        window_width (int): The window width.
        window_height (int): The window height.
        Returns (int, int) the x and y points to place the pop up.
        '''
        window_geometry_info = self.winfo_geometry().split("+")
        
        win_x = int(window_geometry_info[1])
        win_y = int(window_geometry_info[2])
        
        rem_space_x = (WINDOW_WIDTH - window_width) / 2
        rem_space_y = (WINDOW_HEIGHT - window_height) / 2
        
        x_center = win_x + rem_space_x
        y_center = win_y + rem_space_y
        
        return x_center, y_center
        
    def prompt_suit(self):
        '''
        Prompts the player to chose a suit after playing an 8.
        '''
        suit_win_width, suit_win_height = 250, 200
        self.suit_window = tk.Toplevel(bg="white")
        title = tk.Label(self.suit_window, text="Choose a suit:", bg="white", font="Arial 15 bold")
        title.pack(anchor=tk.CENTER, pady=(15, 5))
        
        x, y = self.center_pop_up(suit_win_width, suit_win_height)
        self.suit_window.geometry("%dx%d+%d+%d" % (suit_win_width, suit_win_height, x, y))
        self.suit_window.overrideredirect(1)
        
        for suit in SUITS:
            s = tk.Radiobutton(self.suit_window, text=suit, font="Arial 12 bold", variable=self.suit_choice, value=suit, bg="white", command=self.set_chosen_suit)
            s.pack(anchor=tk.CENTER, pady=(10, 5))
        
    def set_chosen_suit(self):
        '''
        Sets the chosen suit and destroys the window.
        '''
        self.suit_in_play = self.suit_choice.get()
        self.suit_window.after(500, self.suit_window.destroy)
        msg.showinfo("Chosen suit", "You chose the suit " + self.suit_in_play)
    
    def drop_card(self, card_pos):
        '''
        Drops the player's card.
        card_pos (int): Position of the card dropped.
        '''
        drop = self.player.drop_card(card_pos)
        self.discard_pile.add_card(drop)
        self.display_discard_pile()
        self.display_player_hand()
        
    def on_drag_start(self, event):
        '''
        Detects when the card is clicked.
        '''
        widget = event.widget
        widget._drag_start_x = event.x
        widget._drag_start_y = event.y
        
        # Card's original coords
        self.original_x = widget.winfo_x()
        self.original_y = widget.winfo_y()
        
    def on_drag_motion(self, event):
        '''
        Detects when the card is dragged across the window.
        '''
        widget = event.widget
        x = widget.winfo_x() - widget._drag_start_x + event.x
        y = widget.winfo_y() - widget._drag_start_y + event.y
        
        # Define the window boundary of the drag and drop
        x_boundary = 800 - widget.winfo_width()
        y_boundary = 600 - widget.winfo_height()
        if (x > 0 and x < x_boundary) and (y > 0 and y < y_boundary):
            widget.place(x=x, y=y)
            
    def on_drag_release(self, event):
        '''
        Detects when the card is dropped.
        '''
        widget = event.widget
        x = widget.winfo_x()
        y = widget.winfo_y()
        
        if (x > 546 and x < 690) and (y > 147 and y < 353):
            position = self.moved_card(widget)
            dropped = self.player.get_card(position)
            if self.is_eight(dropped) or self.suit_in_play == dropped.suit or (self.match_top_card(dropped) and self.suit_in_play == None):
                # Check if it is an 8
                if self.is_eight(dropped):
                    self.drop_card(position)
                    self.prompt_suit()
                    self.game_screen.wait_window(self.suit_window)
                    
                    if self.player.hand_empty():
                        self.add_more_card(self.player)
                        
                # If not, check if suit in play
                elif self.suit_in_play and dropped.suit == self.suit_in_play:
                    self.drop_card(position)
                    self.suit_in_play = None
                    
                # If not, check if matches top card
                elif self.match_top_card(dropped):
                    self.drop_card(position)
                        
                self.display_player_hand()
                self.computer_turn = True
                    
                if self.player.hand_empty():
                    print("Hand over!!")
                    self.hand_over("player")
                    
                ### Computer's turn to play ###
                if self.computer_turn:
                    self.computer_play()
            
                    if self.computer.hand_empty():
                        print("Hand over!!")
                        self.hand_over("computer")
                print("Discard pile size:", len(self.discard_pile.get_cards()))
                print("Draw pile size:", len(self.draw_pile.get_cards()))
            else:
                widget.place(x=self.original_x, y=self.original_y)
        else:
            widget.place(x=self.original_x, y=self.original_y)
            
    def computer_play(self):
        '''
        Plays the computer's turn.
        '''
        self.top_card = self.discard_pile.get_top_card()        
        comp_suit, comp_dropped = self.computer.play(self.top_card, self.suit_in_play)
        print("Comp suit:", comp_suit, "Comp dropped:", comp_dropped)
        
        if comp_suit:
            self.discard_pile.add_card(comp_dropped)
            self.display_discard_pile()
            self.display_computer_hand()
            self.suit_in_play = comp_suit
            msg.showinfo("Suit choice", "The computer chose the suit " + self.suit_in_play)
            
            if self.computer.hand_empty():
                draw = self.draw_pile.draw_card()
                self.computer.add_card(draw)
                
        if comp_suit == None and comp_dropped:
            self.discard_pile.add_card(comp_dropped)
            self.display_discard_pile()
            self.suit_in_play = None
            self.display_computer_hand()
            
        if comp_suit == None and comp_dropped == None:
            draw = self.draw_pile.draw_card()
            self.computer.add_card(draw)
            self.display_computer_hand()
        
        self.display_player_hand()
        
    def hand_over(self, winner):
        if winner == "player":
            self.display_computer_hand(reveal=True)
            player_points = self.computer.get_hand_value()
            self.player_points += player_points
            msg.showinfo("Hand over", "Congratulations! You win the hand with " + str(player_points) + " points!")
        else:
            computer_points = self.player.get_hand_value()
            self.computer_points += computer_points
            msg.showinfo("Hand over", "The computer won the hand with " + str(computer_points) + " points!")
        
        self.player_points_str.set("Player points: " +  str(self.player_points))
        self.computer_points_str.set("Computer points: " +  str(self.computer_points))
        
        if self.player_points >=100:
            self.game_over("player")
        elif self.computer_points >= 100:
            self.game_over("computer")
        else:
            self.game_screen.destroy()
            self.create_game_screen()
            self.play_game()
        
    def game_over(self, winner):
        '''
        Ends the game or initializes a new game if the player decides so.
        winner (str): The winner of the game.
        '''
        if winner == "player":
            self.display_computer_hand(reveal=True)
            new_game = msg.askquestion("Game over!", "Congratulations!!! You won the game with " + str(self.player_points) + "!\nPlay another game?")
        else:
            new_game = msg.askquestion("Game over!", "Aww, sorry buddy. The computer won the game with " + str(self.computer_points) + "!\nPlay another game?")
        
        if new_game == "yes":
            self.player_points = 0
            self.computer_points = 0
            self.player_points_str.set("Player points: " +  str(self.player_points))
            self.computer_points_str.set("Computer points: " +  str(self.computer_points))
            self.game_screen.destroy()
            self.create_game_screen()
            self.play_game()
        else:
            msg.showinfo("Crazy Eights", "Bye and thanks for playing the game!")
            self.after(300, self.destroy)
        
    def make_dragable(self, widget):
        '''
        Makes the card widget draggable.
        '''
        widget.bind("<Button-1>", self.on_drag_start)
        widget.bind("<B1-Motion>", self.on_drag_motion)
        widget.bind("<ButtonRelease-1>", self.on_drag_release)
        
if __name__ == "__main__":
    game = Game()
    game.mainloop()