#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 07:20:05 2020

@author: silasjimmy
"""

import tkinter as tk
#import tkinter.messagebox as msg

class Game(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Crazy Eights")
        self.geometry("800x600")
        self.resizable(False, False)
        
        # The intro screen
        self.intro_frame = tk.Frame(self, width=800, height=600, bg="white")
        self.intro_msg = tk.Label(self.intro_frame, text="Welcome to the game Crazy Eights!", font="Arial 20 bold", bg="white")
        self.play_btn = tk.Button(self.intro_frame, text="Start", font=5, width=25, command=self.start_game)
        self.quit_btn = tk.Button(self.intro_frame, text="Quit", font=5, width=25, command=self.quit_game)
        
        # The game screen
        self.game_screen = tk.Canvas(self, width=800, height=600, bg="green")
        self.game_screen.bind("<Button-1>", self.get_coords)
        
        # Pack the intro screen
        self.intro_msg.place(x=170, y=200)
        self.play_btn.pack(side=tk.LEFT, anchor=tk.S, padx=(80, 30), pady=(0, 100))
        self.quit_btn.pack(side=tk.LEFT, anchor=tk.S, padx=(30, 80), pady=(0, 100))
        self.intro_frame.pack_propagate(0)
        self.intro_frame.pack(side=tk.LEFT, anchor=tk.N)
        
    def start_game(self):
        self.intro_frame.pack_forget()
        self.game_screen.pack(side=tk.LEFT, anchor=tk.N)
        
    def quit_game(self):
        self.after(300, self.destroy)
        
    def get_coords(self, event):
        if event.y > 0 and event.y < 151:
            print("Computer cards area")
        elif event.y > 150 and event.y < 451:
            print("Draw and discard pile area")
        elif event.y > 450 and event.y < 600:
            print("Player cards area")
        
game = Game()
game.mainloop()