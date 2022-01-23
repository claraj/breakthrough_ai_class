import math 
from collections import deque
from typing import NamedTuple

from board import Board, Direction

"""

Minmax process

To evalutate a node, n, in a tree,

1. L = {n} the unexpanded nodes in the tree

1a. figure out n's children 

2. let x be the first node of n.  if x = n and has a value (computed by the state evaluation function) return n

3. if x HAS been assigned a value Vx then let p be the parent of x, and Vp the value assigned to p (the parent of x)
If p is a minimizing node, then Vp = min(Vp, Vx).   If  p is a maximizing node, return max(Vp, Vx)

4. if x HAS NOT been assigned a value   
      AND this is a terminal node or are done expanding at this level, 
      compute and set value Vx using state eval function

5. if x HAS NOT been assigned a value and we plan to expand further 
    if x is a maximizing node, set Vx to  -infinity
    if x is a minimizing node, set Vx to  +infinity
    Add children of X to the start of L 
    Goto step 2
"""

class MinMax(NamedTuple):
    MIN = 'minimizing'
    MAX = 'maximizing'


class Computer():

    def select_move(self, board):

        self.board = board.make_new_board()

        self.count_nodes = 0

        self.depth = 0
        self.max_depth = 3
    
        player = 'C'
        opponent = 'H'
        direction = Direction.DOWN
        
        #  1. L = {n} the unexpanded nodes in the tree

    #               board, evaluation, isMinMax, parent, move, isTerminal, player):
        base_node = Node(board, None, MinMax.MIN, None, None, False, opponent) 
        L = deque([base_node])

        node = self.minmax(L, base_node)

        if base_node.children:
            best_child = max(base_node.children, key=lambda x: x.evaluation)

            print(base_node.children)
            return best_child.move
        else:
            print('no moves')
            return None


    def minmax(self, L, first_node_called_n):

        depth = 0

        nodes_to_go_up_a_level = 0

        # 2. let x be the first node of n.  if x = n and has a value (computed by the state evaluation function) return n        

        while True:

            x = L[0]

            self.count_nodes +=1 
            # print('counted this many nodes', self.count_nodes, 'at depth', depth)

            if x == first_node_called_n and x.evaluation:
                depth -= 1
                return x   # effectively returning the root node 

            # 3. if x HAS been assigned a value Vx then let p be the parent of x, and Vp the value assigned to p (the parent of x)
            # If p is a minimizing node, then Vp = min(Vp, Vx).   If  p is a maximizing node, set Vp to  max(Vp, Vx)
            # remove x from L and return to step 2

            if x.evaluation is not None:
                parent = x.parent 

                if parent is None:
                    # root node 
                    # print('back to parent node', L)
                    return x 

                if parent.isMinMax == MinMax.MAX:
                    parent.evaluation = max(x.evaluation, parent.evaluation)
                else:
                    parent.evaluation = min(x.evaluation, parent.evaluation)
                # print('POP LEFT')
                L.popleft()   # remove from start, where x was 
                # print(f'l size {len(L)}')
                # depth =- 1  
                
                nodes_to_go_up_a_level -= 1
                if nodes_to_go_up_a_level == 0:
                    depth -= 1

                continue  # just in case..
               
            # 4. if x HAS NOT been assigned a value   
            #     AND this is a terminal node or are done expanding at this level, 
            #     compute and set value Vx using state eval function
            # goto step 2 
            
            else:

                children = self.generate_node_children(x)
                if not children:
                    x.isTerminal = True    
                
                if x.isTerminal or depth > self.max_depth:  # AND or we are done - see below 
                    # compute and set value 
                    x.evaluation = self.state_evaluation(x)
                    continue
                   
            # 5. if x HAS NOT been assigned a value and we plan to expand further 
            #     if x is a maximizing node, set Vx to  -infinity
            #     if x is a minimizing node, set Vx to  +infinity
            #     Add children of X to the start of L 
            #     Goto step 2        

                else: 
                    if x.isMinMax == MinMax.MAX:
                        x.evaluation = -math.inf  
                    else:
                        x.evaluation = math.inf

                    # children = self.generate_node_children(x)
                    x.children = children
                    if children:

                        depth += 1
                        nodes_to_go_up_a_level = len(children)
                        
                        for c in children:
                            L.appendleft(c)
                    # else:  # THIS IS A TERMINAL NODE 
                    #     x.isTerminal = True
                    #     # x.evaluation = self.state_evaluation(x)
                    #     # depth =- 1


    def generate_node_children(self, from_node):

        board = from_node.board
        
        if from_node.player == 'H':  
            player = 'C'
            opponent = 'H'
            direction = Direction.DOWN
            min_max = MinMax.MAX
        else:
            player = 'H'
            opponent = 'C'
            direction = Direction.UP
            min_max = MinMax.MIN

        # print(player, opponent, direction)
        winner, moves = board.list_of_valid_moves(player, opponent, direction)
        if moves == []:
            print('NO MORE MOVES', winner)

        if winner: # terminal node, someone won
            from_node.isTerminal = True 
            from_node.children = [] 
            return 

        nodes = [] 
        for move in moves:
            #     def __init__(self, board, evaluation, isMinMax, parent, move, isTerminal, player):
            node = Node(board.make_new_board_with_move_made(move), None, min_max, from_node, move, False, player)  # TODO is terminal part  
            nodes.append(node)

        from_node.children = nodes 
        return nodes 

    
    # def state_evaluation(board, player, opponent, direction):
    def state_evaluation(self, node):
        
        board = node.board
        board_max_index = board.board_size 

        if node.isMinMax == MinMax.MAX:
            player = 'C'
            opponent = 'H'
            direction = Direction.DOWN 
        else: 
            player = 'H'
            opponent = 'C'
            direction = Direction.UP

        players_pieces = board.list_of_pieces(player)  # piece is actually a Square 
        opponent_pieces = board.list_of_pieces(opponent)

        # distances for this player's pieces to the other side 
        player_distances = [] 
        opponent_distances = [] 

        if direction == Direction.DOWN: #traveling 0, 1, 2, 3... towards 7, higher numbers better  
            for piece in players_pieces:   
                if piece.row == board_max_index:
                    return 1    # this is a win state, piece is at the other end 
                player_distances.append((board_max_index - 1) - piece.row)  # Add 7 if piece in row 1, add 6 if in row 1 ... Number of moves to get to end 
            for piece in opponent_pieces:   
                if piece.row == 0:   # opponent, traveling up, is in the last row wrt this player so opponent win
                    return -1 
                opponent_distances.append(piece.row)  

        elif direction == Direction.UP:  # traveling 7, 6, 5 .. 0 so lower numbers are better 
            for piece in players_pieces:   
                if piece.row == 0:
                    return 1 
                player_distances.append(piece.row)
            for piece in opponent_pieces: 
                if piece.row == board_max_index:
                    return -1  
                opponent_distances.append((board_max_index - 1) - piece.row)

        opp_advantage = sum(opponent_distances) * len(players_pieces)  # want small distance, small number of opponent 
        player_advantage = sum(player_distances) * len(opponent_pieces)  

        evaluation = (opp_advantage - player_advantage) / (opp_advantage + player_advantage)  # TODO IDK
        return evaluation

        # TODO  be more enthusiastic about taking pieces 
        # TODO is it better to be in the middle of the board? What about blocking opponent? Strategies for pinning or taking opponent?


class Node:
    def __init__(self, board, evaluation, isMinMax, parent, move, isTerminal, player):
        self.board = board
        self.evaluation = evaluation
        self.isMinMax = isMinMax
        self.children = []  # more nodes - where this state can move to 
        self.parent = parent 
        self.move = move 
        self.isTerminal = isTerminal
        self.player = player

    def __repr__(self):
        if self.children:
            c = len(self.children)
        else:
            c = 0
        return f'eval={self.evaluation} {self.move=} {self.isMinMax} child count={c} Terminal? {self.isTerminal}\n'


# class Tree:
#     def __init__(self, children):
#         self.children = children  # list of nodes 
#         self.parent = None
