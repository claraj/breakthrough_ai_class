
# The computer needs its own representation of the board, separate to the one that stores the game's state. 
# use same class? 
import random
from board import Direction, Move


# # best move? 
#         evaluations = [ node.evaluation for node in leaf_nodes ]

#         # best is the smallest evaluation number 
#         best_evaluation = min(evaluations)
#         # what moves are associated with this evaluation?

#         best_moves = []
#         for move, evaluation in zip(moves, evaluations):
#             if evaluation == best_evaluation:
#                 best_moves.append(move)

#         # If only one best, return that. Otherwise pick one at random.  
#         if len(best_moves) == 1:
#             return move[0] 

#         return random.choice(best_moves)


directions_for_players = {
    'H': Direction.UP,
    'C': Direction.DOWN
}

class Computer():

    PLAYS_AHEAD = 5   # tweak probably 
    
    def __init__(self):
        self.player = 'C'
        self.opponent = 'H'
        self.current_level = 0
    

    def toggle_player(self):
        if self.player == 'C':
            self.player = 'H'
            self.opponent = 'C'
        else:
            self.player = 'C'
            self.opponent = 'H'


    def decide_move(self, board):
        # TODO make and walk tree according to strategy 
        # TODO evaluate state function for nodes 
        # TODO return best move 
        # TODO identify similar states obtained by different moves and responses? 


        # self.leaf_nodes = []
        self.current_level = 0
        # self.moves_to_best_evaluation = []  
        self.best_evaluation_so_far = 0
        self.best_evaluation_node = None

        self.current_search_path = []   # A STACK A STACK A STACKSFSFOKDPRDOKRTSEPKRTGSPERQ@#$SDFSZF 
        # never mind we can store a node's parent and go backwards to root

        # self.where_can_i_go(board)

        player = 'C'
        opponent = 'H'
        
        first_ply_move_nodes = self.where_can_i_go(board, player, opponent, directions_for_players.get(player))
        tree = Tree(board, first_ply_move_nodes)

        for child_node in tree.children:
            self.generate_next_moves(tree, 1, player, opponent)
        
        moves_to_best_evaluation = self.get_moves_to_node(self.best_evaluation_node)

        return moves_to_best_evaluation[0]

    # def pick_best_move(tree):
    #     # walk level 5, choose state with best evaluation function.  Walk back and identify first move in the sequence 
    # TODO what if game is over in less than 5 moves 
    #     # return move and if this move takes opponent 
    #     for child in tree.children 


    def get_moves_to_node(self, node):
        moves = [] 
        while node.parent is not None: 
            moves.append(node.move)
            node = node.parent
        return moves 


    def generate_next_moves(self, node, level, player, opponent):

        MAX_DEPTH = 5

        next_ply_move_nodes = self.where_can_i_go(node.board, player, opponent, directions_for_players.get(player))
        node.children = next_ply_move_nodes

        if not next_ply_move_nodes:  # found an end-game state, someone won - or stalemate if possible? 
            # better than any other state? 
            evaluation = self.static_evaluation_function(node.board)
            if evaluation > self.best_evaluation_so_far:
                self.best_evaluation_so_far = evaluation
                self.best_evaluation_node = node

        self.current_level += 1
        if self.current_level > MAX_DEPTH:
            # lowest level of dealing with this. add states to leaf_nodes 
            # self.leaf_nodes += next_ply_move_nodes
            return 

        player, opponent = opponent, player

        for child in node.children:
            self.generate_next_moves(child, level, player, opponent)
        


    def where_can_i_go(self, board, player, opponent, direction):
        
        # returns a list of nodes, each with board state and move. not children 
        
        # 
        # make list of valid moves for computer 
        moves = board.list_of_valid_moves(player, opponent, direction)

        # print('the moves')
        print(moves)

        if len(moves) == 0:
            # oh dear 
            # is this possible?
            raise Exception("Meep. There's nowhere I can move.")

        # parallel "array"
        # evaluations = [ self.static_evaluation_function(board) for move in moves]
        
        # STOP HERE and return the evaluations... as a list of NODES (oo!)

        nodes = [] 

        for move in moves:
            board_state_on_move = board.make_new_board_with_move_made(move)
            evaluation = self.static_evaluation_function(board_state_on_move)
            #     def __init__(self, board, evaluation, player, parent, move):
            node = Node(board_state_on_move, evaluation, player, None, move)
            nodes.append(node)

        return nodes 

    """
    # this is going to come in at some point in the future

            # best is the smallest evaluation number 
            best_evaluation = min(evaluations)
            # what moves are associated with this evaluation?

            best_moves = []
            for move, evaluation in zip(moves, evaluations):
                if evaluation == best_evaluation:
                    best_moves.append(move)

            # If only one best, return that. Otherwise pick one at random.  
            if len(best_moves) == 1:
                return move[0] 

            return random.choice(best_moves)

    """


    def static_evaluation_function(self, board):
        # first go - how close is the nearest piece to the other side? 
        # return the distance the closest piece is to the other side
        # and the number of opponent pieces - want to minimize that too 
        
        # assuming the computer is heading towards the bottom of the board and the board is 8x8  TODO make more general 
        # is it better to be in the middle of the board? What about blocking opponent? Strategies for pinning or taking opponent?
        # board_with_move_made = board.make_new_board_with_move_made(move)

        distances = [] 

        pieces = board.list_of_pieces('C')

        opponent_pieces = board.list_of_pieces('H')

        for piece in pieces:   # a piece might be in row 0 so it's at the end, or at row 2 so it's 2 from the end 
            distances.append(piece.row)

        return min(distances) * len(opponent_pieces)    # * ?????? 


"""

node 
   - board state
   - evaluation 
   - list of next states 

"""

class Tree:
    def __init__(self, board, children):
        self.children = children  # list of nodes 
        self.board = board 


class Node:
    def __init__(self, board, evaluation, player, parent, move):
        self.board = board  # the current board state  
        self.evaluation = evaluation
        self.player = player
        self.children = []  # more nodes - where this state can move to 
        self.parent = parent 
        self.move_to_this_node = move