from board import Board, Square, Direction, Move
from computer_strategy import Computer

board = Board()

board.start_positions()

computer = Computer()

def main():

    print(board)
    while not game_over():
        computer_move()
        human_move()


def human_move():
    # get human's move 
    # decide if valid 
    # if so, update board
    # report on pieces taken?  
    while True:
        start = get_square_coord('Enter coordinates of piece to move: ')
        destination = get_square_coord('Enter coordinates of destination to move to e.g. A2: ')
        valid, why, piece_taken = valid_move(Direction.DOWN, player='H', opponent='C', start=start, destination=destination)
        if not valid:
            print(f'You can\'t make that move because {why}')
        else:
            break
    
    board.move(Move(start, destination))
    print(board)


def get_square_coord(message):

    # don't forget to flip the Y row value (making more problems for future clara)
    while True: 
        square = input(message)
        if len(square) != 2:
            print('Wrong length input ')
            continue
        letter_number = list(square)
        print(letter_number)
        try:
            print(letter_number[1])
            row = int(letter_number[1])

            # row = 7 - row 

            if row < 0 or row > 7:
                raise Exception('Out of range')
        except: 
            print('The row must be a number between 0 and 7')
            continue

        col_letter = letter_number[0].upper()
        col = ord(col_letter) - 65

        if col < 0 or col > 7:
            print(f'Letter must be one of ABCDEFGH {square} {col_letter}' )
            continue

        # it must be valid 
        break # ick
        

    square_tuple = Square(row, col)
    print(f'{square} converted to {square_tuple}')
    return square_tuple


def computer_move():
    # build decision tree, evaluate state function  
    # decide on most advantageous move 
    # make move and update board 
    # report on piece taken, if any   
    computer.decide_move(board)



def valid_move(direction, player, opponent, start, destination):
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
    return board.is_valid_move(direction, player, opponent, start, destination)

    


def game_over():
    winner = board.game_over()
    if winner:
        print(f'{winner} has won')

if __name__ == '__main__':
    main()