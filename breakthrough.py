from board import Board, Square, Direction

board = Board()

def main():

    print(board)
    while not game_over():
        human_move()
        computer_move()


def human_move():
    # get human's move 
    # decide if valid 
    # if so, update board
    # report on pieces taken?  
    while True:
        start = get_square_coord('Enter coordinates of piece to move: ')
        destination = get_square_coord('Enter coordinates of destination to move to e.g. A2: ')
        if valid_move(Direction.DOWN, 'H', start, destination):
            break
    
    board.move(start_xy, destination_xy)


def get_square_coord(message):
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
            if row < 0 or row > 7:
                raise Exception('Out of range')
        except: 
            print('The row must be a number between 0 and 7')
            continue

        col_letter = letter_number[0].upper()
        col = ord(col_letter) - 65

        print(f'{col:}')
        if col < 0 or col > 7:
            print(f'Letter must be one of ABCDEFGH {square} {col_letter}' )

        return Square(col, row)


def computer_move():
    # build decision tree, evaluate state function  
    # make move 
    # update board 
    # report on pieces taken?  
    pass


def valid_move(direction, player, start, destination):
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
    return board.is_valid_move(direction, player, start, destination)

    


def game_over():
    winner = board.game_over()
    if winner:
        print(f'{Winner} has won')

if __name__ == '__main__':
    main()