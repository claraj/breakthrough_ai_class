
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
    'H': Direction.UP,    # always human up and computer down
    'C': Direction.DOWN
}

class ComputerBase():

    PLAYS_AHEAD = 5   # tweak probably 
    
    def __init__(self):
        self.player = 'C'
        self.opponent = 'H'
        self.current_level = 0
    

    def decide_move(self, board):
        # TODO make and walk tree according to strategy 
        # TODO evaluate state function for nodes 
        # TODO return best move 
        # TODO identify similar states obtained by different moves and responses? 

        self.current_level = 0
        self.best_evaluation_so_far = 0
        self.best_evaluation_node = None  # nope

        player = 'C'
        opponent = 'H'
        direction = directions_for_players.get(player)
        
        first_ply_move_nodes = self.where_can_i_go(board, player, opponent, direction)
        tree = Tree(board, first_ply_move_nodes)

        for child_node in tree.children:
            self.generate_next_moves(tree, 1, player, opponent, direction)
        
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


    def generate_next_moves(self, node, level, player, opponent, direction):

        MAX_DEPTH = 5
        print(self.current_level)

        if self.current_level % 2 == 0:
            player = 'C'
            opponent = 'H'
            direction = Direction.DOWN
        else:
            player = 'H'
            opponent = 'C'
            direction = Direction.UP


        next_ply_move_nodes = self.where_can_i_go(node.board, player, opponent, direction)

        node.children = next_ply_move_nodes

        if not next_ply_move_nodes:  # found an end-game state, someone won - or stalemate if possible? 
            # better than any other state? 
            evaluation = self.static_evaluation_function(node.board)
            if evaluation > self.best_evaluation_so_far:
                print('found a better state', evaluation, node)
                self.best_evaluation_so_far = evaluation
                self.best_evaluation_node = node
            self.current_level -= 1
            return 

        
        if self.current_level > MAX_DEPTH:
            evaluation = self.static_evaluation_function(node.board, player, opponent)
            if evaluation > self.best_evaluation_so_far:
                self.best_evaluation_so_far = evaluation
                self.best_evaluation_node = node
            self.current_level -= 1
            return 

        player, opponent = opponent, player

        self.current_level += 1
        for child in node.children:    
            self.generate_next_moves(child, level, player, opponent, direction)
        
        self.current_level -= 1
            


    def where_can_i_go(self, board, player, opponent, direction):
        
        # returns a list of nodes, each with board state and move. not children 
        
        # 
        # make list of valid moves for computer 
        print(player, opponent, direction)
        winner, moves = board.list_of_valid_moves(player, opponent, direction)

        # print('the moves')
        # print(moves)
        # TODO evaluations in the range +1 to -1 where +1 is computer wins, -1 is human wins 

        
        # STOP HERE and return the evaluations... as a list of NODES (oo!)

        nodes = [] 

        for move in moves:
            board_state_on_move = board.make_new_board_with_move_made(move)
            evaluation = self.static_evaluation_function(board_state_on_move, player, opponent)
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


    def static_evaluation_function(self, board, player, opponent):

        # Low numbers are better, 0 is a win state  

        # first go - how close is the nearest piece to the other side? 
        # return the distance the closest piece is to the other side
        # and the number of opponent pieces - want to minimize that too 
        
        # assuming the computer is heading towards the bottom of the board and the board is 8x8  TODO make more general 
        # is it better to be in the middle of the board? What about blocking opponent? Strategies for pinning or taking opponent?
        # board_with_move_made = board.make_new_board_with_move_made(move)

        distances = [] 

        direction = directions_for_players[player]

        players_pieces = board.list_of_pieces(player)  # piece is actually a Square 
        opponent_pieces = board.list_of_pieces(opponent)

        if direction == Direction.DOWN: #traveling 0, 1, 2, 3... towards 7, higher numbers better  
            for piece in players_pieces:   # a piece might be in row 0 so it's at the end, or at row 2 so it's 2 from the end 
                distances.append(7 - piece.row)
        elif direction == Direction.UP:  # traveling 7, 6, 5 .. 0 so lower numbers are better 
            for piece in players_pieces:   
                distances.append(piece.row)

        return min(distances) * len(opponent_pieces)    # * ?????? The multiplication means that if a distance is 0 the whole thing is 0


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
        self.parent = None


class Node:
    def __init__(self, board, evaluation, player, parent, move):
        self.board = board  # the current board state  
        self.evaluation = evaluation
        self.player = player
        self.children = []  # more nodes - where this state can move to 
        self.parent = parent 
        self.move_to_this_node = move