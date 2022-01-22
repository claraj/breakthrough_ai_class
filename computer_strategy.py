
# The computer needs its own representation of the board, separate to the one that stores the game's state. 
# use same class? 

import random
from board import Direction, Move

class Computer():

    def decide_move(self, board):
        # TODO make and walk tree according to strategy 
        # TODO evaluate state function for nodes 
        # TODO return best move 
        self.where_can_i_go(board)


    def where_can_i_go(self, board):
        # make list of valid moves for computer 
        moves = board.list_of_valid_moves('C', 'H', Direction.DOWN)

        print('the moves')
        print(moves)

        if len(moves) == 0:
            # oh dear 
            # is this possible?
            raise Exception("Meep. There's nowhere I can move.")

        # parallel "array"
        evaluations = [ self.static_evaluation_function(move, board) for move in moves]
        
        # best is the smallest evaluation number 
        best_evaluation = min(evaluations)
        # what moves are associated with this evaluation?

        best_moves = []
        for move, evaluation in zip(moves, evaluations):
            if evaluation == best_evaluation:
                moves.append(move)

        # If only one best, return that. Otherwise pick one at random.  
        if len(best_moves) == 1:
            return move[0] 

        return random.choice(best_moves)




    def static_evaluation_function(self, move, board):
        # first go - how close is the nearest piece to the other side? 
        # return the distance the closest piece is to the other side
        # and the number of opponent pieces - want to minimize that too 
        
        # assuming the computer is heading towards the bottom of the board and the board is 8x8  TODO make more general 
        
        board_with_move_made = board.make_new_board_with_move_made(move)

        distances = [] 

        pieces = board_with_move_made.list_of_pieces('C')

        opponent_pieces = board_with_move_made.list_of_pieces('H')

        for piece in pieces:   # a piece might be in row 0 so it's at the end, or at row 2 so it's 2 from the end 
            distances.append(piece.row)

        return min(distances) * len(opponent_pieces)    # * ?????? 


    def make_tree():
        pass 


class Tree:
    def __init__(self):
        self.root = Node()


class Node:
    def __init__(self):
        self.children = []
        self.board_state = None   # big todo! 