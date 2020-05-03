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

and the points assigned to the winner. Since this game is a two player game (you and the computer) the target points are 100.

## The CLI version

Currently only the commandline version is available.

## The GUI version

It is under development. Run the `crazy_eights_gui.py` file to see the progress.

## About the game's AI

The game's AI is fair but not simple. Play smart and win!
