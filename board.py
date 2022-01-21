# Board is a 8x8 grid 
from typing import NamedTuple
from enum import Enum


class Square(NamedTuple):
    x: int 
    y: int


class Direction(Enum):
    UP = 1
    DOWN = -1

class Board:

    def __init__(self, board_size=8):
        self.board_size = board_size
        if board_size < 5 or board_size > 12:  # max is pretty arbitrary 
            raise Exception('That is not a valid size.')

        self.board = [ ( ['0'] * board_size ) for x in range(board_size) ]

        # set up computer pieces on first two rows
        for square in range(board_size):
            self.board[0][square] = f'C{str(square+1).zfill(2)}'
            self.board[1][square] = f'C{str(square+1+board_size).zfill(2)}'

        # set up human pieces on last two rows 
        # label H1 through H16
        for square in range(board_size):
            self.board[board_size - 2][square] = f'H{str(square+1).zfill(2)}'
            self.board[board_size - 1][square] = f'H{str(square+1+board_size).zfill(2)}'


    def move(self, startxy, endxy):
        print(xy_to_coords(startxy))
        print(xy_to_coords(endxy))

    # 
    # direction is UP or DOWN the board 
    # player is H or C for human or computer
    # start is a Square
    # destination is a Square
    #
    # Valid moves are 
    #    - forward one square but not off the edge of the board and not into another piece
    #    - diagonally forward in appropriate direction, one square, but not off the edge of the board and not into one of the player's pieces 
    #    - diagonally forward into an opponents piece 

    # Return tuple includes the following, as appropriate 
    # ( move is valid, reason why not, piece taken )
    def is_valid_move(direction, player, start, destination):
        pass

    def __str__(self):

        current_row = self.board_size - 1
        output = '\n'
        
        for row in self.board:
            output += f'{current_row:<4}'
            current_row -= 1 

            r = ' '.join([ r.center(3) for r in row ])
            output += r
            output += '\n'

        # add letters to the end 
        letters = [ chr(index + 65).center(3) for index in range(self.board_size) ]
        letter_string = ' '.join(letters)
        output += '\n'
        output += f'    {letter_string}'
        output += '\n'


        return output            


    def game_over(self):
        """ Return name of winner if game is over and someone has won, 
        return None otherwise """
        if [ piece for piece in self.board[7] if 'C' in piece ]:
            return 'Computer'
        elif [ piece for piece in self.board[0] if 'H' in piece ]:
            return 'Human'
        else:
            return None   # no winner 