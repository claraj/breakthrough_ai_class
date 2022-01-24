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
    UP = -1  # number to add to the row to move a piece forward if the player is up down the board, as in up looking at the board on a screen
    DOWN = 1  # number to add to the row to move a piece forward if the player is moving down the board


class Board: 

    """ Represents the board, as the game is playing. 
    The computer strategy class(es) use board objects for their own
    internal representation of the board state for future move planning 
    """

    EMPTY = '0'

    def __init__(self, board_size=8):
        self.board_size = board_size
        # if board_size < 5 or board_size > 12:  # max is pretty arbitrary 
        #     raise Exception('That is not a valid size.')

        self.board = [ ( [self.EMPTY] * board_size ) for x in range(board_size) ]
        self.most_recent_move = None 


    def start_positions(self):
        # set up computer pieces on first two rows
        for square in range(self.board_size):
            self.board[0][square] = f'C{str(square + 1).zfill(2)}'
            # self.board[1][square] = f'C{str(square + 1 + self.board_size).zfill(2)}'

        # set up human pieces on last two rows 
        # label H1 through H16
        for square in range(self.board_size):
            # self.board[self.board_size - 2][square] = f'H{str(square+1).zfill(2)}'
            self.board[self.board_size - 1][square] = f'H{str(square+1+self.board_size).zfill(2)}'


    def make_new_board_with_move_made(self, move):
        new_board = Board()
        new_board_board = [] 
        new_board.board_size = self.board_size

        # slicey slice 
        for row in self.board:
            new_row = row[:]
            new_board_board.append(new_row)
        
        new_board.board = new_board_board  # NAAAAAAAAAAAAMES  If you are one of my students send me an email for extra credit next time I tell you that you need to use better variable names in one of your projects
        new_board.make_move(move)
        return new_board


    def make_new_board(self):
        new_board = Board()
        new_board_board = [] 
        new_board.board_size = self.board_size

        # slicey slice 
        for row in self.board:
            new_row = row[:]
            new_board_board.append(new_row)
        
        new_board.board = new_board_board  # NAAAAAAAAAAAAMES  If you are one of my students send me an email for extra credit next time I tell you that you need to use better variable names in one of your projects
        return new_board


    def make_move(self, move):
        piece = self.board[move.start.row][move.start.col]
        self.board[move.start.row][move.start.col] = self.EMPTY
        self.board[move.destination.row][move.destination.col] = piece
        self.most_recent_move = move 


    def list_of_pieces(self, player):
        pieces = []
        for row_index, row in enumerate(self.board):
            for col_index, col in enumerate(row):
                if player in self.board[row_index][col_index]:
                    pieces.append(Square(row_index, col_index))

        return pieces


    def list_of_valid_moves(self, player, opponent, direction):
        # Where can one go? player = "C" or "H"
        # Find locations of this player's pieces 
        # make list of possible Move objects for each piece 
        # the computer needs to decide how player could respond to computer moves so this needs to work in both directions
        # or have two computers play each other 

        # if win state, return empty list 
        winner = self.game_over()
        if winner:
            return winner, []


        # otherwise find moves 

        possible_moves = []

        pieces = []
        for row_index, row in enumerate(self.board):
            for col_index, square_contents in enumerate(row):
                square = Square(row_index, col_index)
                # if player in self.contents_for_square(square):
                if player in square_contents:
                    pieces.append(square)

        for piece in pieces:
            # print(piece)
            if direction == Direction.DOWN and piece.row + 1 > (self.board_size - 1):
                raise Exception('Checking for moves off the bottom is not valid. Shoul\'nt be here since the player moving down has won.')
            elif direction == Direction.UP and piece.row - 1 < 0:
                raise Exception('Checking for moves off the top is not valid. Shoul\'nt be here since the player moving up has won.')

            # where to? 
            # choices are forward if empty, diagonal if empty, diagonal if opponent 


            # can go forward? 

            one_square_forward = Square(piece.row + direction.value, piece.col)
            contents = self.contents_for_square(one_square_forward) 
            if contents == Board.EMPTY:
                possible_moves.append(Move(piece, one_square_forward))
    
            # diagonal one way, 
            one_square_diagonal_minus = Square(piece.row + direction.value, piece.col - 1) 
            contents = self.contents_for_square(one_square_diagonal_minus) 
            if contents is None:  # off the side 
                pass 
            elif contents == Board.EMPTY:
                possible_moves.append(Move(piece, one_square_diagonal_minus))
            elif opponent in contents:
                possible_moves.append(Move(piece, one_square_diagonal_minus))
            else:
                # current player in square? not valid
                pass

            # diagonal other way
            one_square_diagonal_plus = Square(piece.row + direction.value, piece.col + 1) 
            contents = self.contents_for_square(one_square_diagonal_plus) 
            if contents is None:  # off the side 
                pass 
            elif contents == Board.EMPTY:
                possible_moves.append(Move(piece, one_square_diagonal_plus))
            elif opponent in contents:
                possible_moves.append(Move(piece, one_square_diagonal_plus))
            else:
                # current player in square? not valid
                pass


        if not possible_moves:
            print(self)
            raise Exception('No possible moves found and this does not seem to be a win state')

        return None, possible_moves


    def contents_for_square(self, square):
        if square.row < 0 or square.col < 0:
            return None
        if square.row >= self.board_size or square.col >= self.board_size:
            return None
        try:
            return self.board[square.row][square.col]
        except:
            return None


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
        # print(piece, destination_contents, direction.value)

        if piece == Board.EMPTY:
            return (False, 'That starting position is an empty square.', None)


        if player not in piece:
            return (False, 'That is not one of your pieces.', None)


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
            # some other destination       
            return (False, 'You may only move ahead or diagonally ahead one square.', None)


        if move_type == "STRAIGHT":
            # can only move into an empty space 
            if destination_contents == Board.EMPTY:
                return (True, 'Moving forward one into an empty space is valid', None)
            else:
                return (False, 'You cannot move straight ahead into another piece', None)
    

        if move_type == 'DIAGONAL':
            if destination_contents == Board.EMPTY:
                return (True, 'Moving diagonally forward one square into an empty space is valid.', None)
            elif player in destination_contents:
                # that's your piece, nope
                return (False, 'You cannot move diagonally into your own piece.', None)
            elif opponent in destination_contents:  
                return (True, 'Moving diagonally forward one square to take your opponents piece is valid.', destination_contents)
            else:
                # not empty, not yours, not the opponent
                raise Exception('Something else got onto the board. a frog? A dug? a bug? Probably a bug.')


    def __str__(self):

        YELLOW = '\u001B[1;33m'
        GREEN = '\u001B[1;32m'
        RESET = '\u001B[0m'

        RED = '\u001B[1;31m'
        BLUE = '\u001B[1;36m'  # well, cyan
        
   
        if self.most_recent_move:
            destination_row = self.most_recent_move.destination.row 
            destination_col = self.most_recent_move.destination.col 
        else: 
            destination_col = None 
            destination_row = None

        current_row = 0
        output = '\n'
        
        for row_index, row in enumerate(self.board):

            output += f'{current_row:<4}'
            current_row += 1

            to_color = row[:]  # copy 

            # # print(destination_row, row, destination_col )
            # if destination_row == row_index: 
            #     piece = row[destination_col]
            #     row[destination_col] = GREEN + piece + RESET
            #     # print(row)

            # r = ' '.join([ r.center(3) for r in row ])
            # output += r
            
            # if destination_row == row_index: 
            #     row[destination_col] = piece

            # print(destination_row, row, destination_col )

            for i, c in enumerate(to_color):
                if destination_row == row_index and destination_col == i:
                    if 'H' in c:
                        to_color[i] = YELLOW + c + RESET
                    if 'C' in c:
                        to_color[i] = GREEN + c + RESET


                elif 'C' in c:
                    to_color[i] = BLUE + c + RESET
                elif 'H' in c:
                    to_color[i] = RED + c + RESET

                # print(row)

            r = ' '.join([ r.center(3) for r in to_color ])
            output += r
            
            # if destination_row == row_index: 
            #     row[destination_col] = piece
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
        if [ piece for piece in self.board[ self.board_size -1 ] if 'C' in piece ]:
            return 'Computer'
        elif [ piece for piece in self.board[0] if 'H' in piece ]:
            return 'Human'
        else:
            return None   # no winner 




    


