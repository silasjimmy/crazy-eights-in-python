# Crazy Eights in Python

Crazy Eights is a popular card game played by two or more players. A standard deck of 52 cards is used to play. However, if the players are many two decks can be used.

## How to play

1. Each player is dealt with 5 cards (7 cards if players are two).
2. The remaining cards are placed face down in a pile and used as the draw pile.
3. A card is drawn from the top of the draw pile and placed face up as the top card (and also the discard pile) which signals the start of the game.
4. The first player starts by either dropping a card to the discard pile or drawing a card from the draw pile.
5. To discard a card:
	- The card must match the rank or suit of the top card.
	- The card can be an 8 of any suit which can be played at any point of the game. However if a player drops an 8 he/she should choose the suit of the next card to be played.
6. If the player cannot meet the above conditions or he/she decides willingly not to drop a card, the player must repeatedly draw a card from the draw pile until he/she draws a card he's able and willing to play/discard.
7. If the draw pile runs out, the discard pile except for the top card is reshuffled and used as the draw pile.

The player who clears his hand the first wins the hand. The opponent's hand value is calculated as follows:

	- 8 values 50 each
	- court cards values 10 each
	- the rest value their face values

and the points assigned to the winner. Since this game is a two player game (you and the computer) the target point is 100.

## The CLI version

The commandline version of the game lets you play the game in your python console. To play make sure you have python 3 installed in your computer by running

`python3`

in the command prompt/terminal. Exit the python shell by running

`exit()`

Then:

1. Run

`python3 crazy_eights_cli.py`

or,

2. Open the *crazy_eights_cli.py* file using your favorite Python IDE and run the script.

`NB: There might be some issues with the CLI game because i may have modified some bits during the making of the GUI version. Hopefully those errors will be resolved soon.`

## The GUI version

If you have played the CLI version we can both agree it isn't much interesting as playing a GUI version of it. On that note i have good and bad news (well not that bad actually). The good news is that the GUI version is now complete. But since its my first public release there may be some bugs which am currently working on. Run the *crazy_eights_gui.py* script and enjoy!

## About the game's AI

The game's AI is fair but not simple. Think hard of your moves, which will need a bit of arithmetic. Play smart and maybe you will have a chance of winning a hand, or even a game! Anyway, i hope you enjoy the game and don't forget to improve the AI, if interested also improve the whole program.

