# Board is a 8x8 grid 
from typing import NamedTuple
from enum import Enum


class Square(NamedTuple):
    row: int 
    col: int

class Move(NamedTuple):
    start: Square
    destination: Square


class Direction(Enum):
    UP = 1
    DOWN = -1


class Board:

    EMPTY = '0'

    def __init__(self, board_size=8):
        self.board_size = board_size
        if board_size < 5 or board_size > 12:  # max is pretty arbitrary 
            raise Exception('That is not a valid size.')

        self.board = [ ( [self.EMPTY] * board_size ) for x in range(board_size) ]

        # set up computer pieces on first two rows
        for square in range(board_size):
            self.board[0][square] = f'C{str(square+1).zfill(2)}'
            self.board[1][square] = f'C{str(square+1+board_size).zfill(2)}'

        # set up human pieces on last two rows 
        # label H1 through H16
        for square in range(board_size):
            self.board[board_size - 2][square] = f'H{str(square+1).zfill(2)}'
            self.board[board_size - 1][square] = f'H{str(square+1+board_size).zfill(2)}'


    def move(self, start, end):
        print("BEFORE")
        print(self)
        piece = self.board[start.row][start.col]
        self.board[start.row][start.col] = self.EMPTY
        self.board[end.row][end.col] = piece
        print("AFTER")
        print(self)



    def is_valid_move(self, direction, player, opponent, start, destination):
        # 
        # Assume the board is in a valid state. 
        # Assumes destination is not outside the board. 
        # 
        # direction is UP or DOWN the board 
        # player is H or C for human or computer
        # start is a Square
        # destination is a Square
        #
        # Valid moves 
        #    - start from a piece owned by this player
        # 
        # Valid moves are 
        #    - forward one square but not off the edge of the board and not into another piece
        #    - diagonally forward in appropriate direction, one square, but not off the edge of the board and not into one of the player's pieces 
        #    - diagonally forward into an opponents piece 

        # Return tuple includes the following, as appropriate 
        # ( move is valid, reason why not, piece taken )

        # is the start piece one of this player's? 

        piece = self.board[start.row][start.col]
        destination_contents = self.board[destination.row][destination.col]
        print(piece, destination_contents, direction.value)

        if piece == Board.EMPTY:
            return (False, 'That starting position is an empty square.', None)


        if player not in piece:
            return (False, 'That is not one of your pieces.', None)


        print("DIAG", destination.row - start.row,  abs(destination.col - destination.col))

# class Direction(Enum):
#     UP = 1
#     DOWN = -1
        # Are we going straight, or diagonal? 
        if (start.col == destination.col) and (destination.row - start.row == direction.value):
            # moving straight forward 
            move_type = "STRAIGHT"
        elif (destination.row - start.row == direction.value) and abs(start.col - destination.col) == 1:
            # diagonally forward left or right 
            move_type = "DIAGONAL"
        else:
            # nope       
            return (False, 'You may only move ahead or diagonally ahead one square.', None)


        if move_type == "STRAIGHT":
            # can only move into another piece 
            if destination_contents == Board.EMPTY:
                # ok 
                return (True, 'Moving forward one into an empty space is cool', None)
            else:
                return (False, 'You cannot move straight ahead into another piece', None)
    

        if move_type == 'DIAGONAL':
            if destination_contents == Board.EMPTY:
                return (True, 'Moving diagonally forward one square into an empty space is cool.', None)
            elif player in destination_contents:
                # that's your piece, nope
                return (False, 'You cannot move diagonally into your own piece.', None)
            elif opponent in destination_contents:  
                return (True, 'Moving diagonally forward one square to take your opponents piece is valid.', destination_contents)
            else:
                # not empty, not yours, not the opponent
                raise Exception('something else got onto the board. a frog? A dug? a bug? Probably a bug.')



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