# Breakout game

## Not the one with the ball bouncing on bricks

## From the description


>	Breakthrough is a game of abstract strategy invented by Dan Troyka in 2000. It is played on a rectangular board, originally 7x7, with pieces of two colors. We > implement the 8x8 version, which won a game design prize in 2001. A number of web pages describe the game and its rules, which we summarize here.
> Initially, each player's 16 pieces occupy the two rows of the board nearest the player. In a player's turn, one piece is moved one position forward or diagonally > forward. An opponent's piece may be captured only by diagonal forward moves, and captures are not mandatory. The winner is the first to move a piece to the 
> opponent's back row.

Jan 21

A Python program

Board structure

* Draft of board structure 
* Can display board 
* Can get a human move, make that move
* Can decide if someone has won
* Can identify valid moves 


AI 

* Can generate a list of moves from a board state 
* Can run an evaluation function 

 minimax - best of mine, worst of opponents 
 alpha-beta - forward pruning - getting rid of poor outcome branches


TODO 

Colours in the terminal output
Some kind of AI evaluation function
alpha-beta decision tree
Clean up the data structures 
Web based version 
    - https://skulpt.org/
    - repl.it

Test it on humans


Notes 

The most number of moves there can possibly be is something like 6 * 8 = 48.  A tree with 48 levels would be rather large though. 


Jan 22 

Trash original computer and implement minmax from the book.

Max depth is not working correctly 