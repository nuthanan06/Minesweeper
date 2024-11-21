import random 
import re

class Board: 
    def __init__(self, dim_size, num_bombs): 
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self.make_new_board()
        self.assign_values_to_board()
        self.dug = set() 
    
    def make_new_board(self): 
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0; 
        while bombs_planted < self.num_bombs: 
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size; 
            col = loc % self.dim_size; 

            if board[row][col] == '*': 
                continue
            board[row][col] = '*'
            bombs_planted += 1 
        
        return board
    
    def get_num_neighboring_bombs(self, row, col):
            positions = [
                [row-1, col-1], [row-1, col], [row-1, col+1],
                [row, col-1], [row, col+1],
                [row+1, col-1], [row+1, col], [row+1, col+1]
            ]
            counter = 0
            for x, y in positions:
                if 0 <= x < self.dim_size and 0 <= y < self.dim_size:  # Ensure within bounds
                    if self.board[x][y] == "*":
                        counter += 1
            return counter

    def assign_values_to_board(self): 
        for x in range(self.dim_size): 
            for y in range(self.dim_size):
                if self.board[x][y] == '*':
                    continue 
                self.board[x][y] = self.get_num_neighboring_bombs(x,y)


    def dig(self, row, col):
        # Prevent out-of-bounds digging or redundant digging
        if (row < 0 or row >= self.dim_size or col < 0 or col >= self.dim_size or 
                (row, col) in self.dug):
            return True

        self.dug.add((row, col))  # Mark this spot as dug

        # Hit a bomb
        if self.board[row][col] == '*':
            return False

        # If cell is not empty (number of neighboring bombs > 0), stop recursion
        if self.board[row][col] > 0:
            return True

        # If cell is empty (0 neighboring bombs), recursively dig neighbors
        neighbors = [
            (row-1, col-1), (row-1, col), (row-1, col+1),
            (row, col-1), (row, col+1),
            (row+1, col-1), (row+1, col), (row+1, col+1)
        ]
        for r, c in neighbors:
            self.dig(r, c)  # Recursive call for each neighbor

        return True


    def __str__(self): 
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for x in range(self.dim_size): 
            for y in range(self.dim_size): 
                if (x, y) in self.dug: 
                    visible_board[x][y] = str(self.board[x][y])  
                else: 
                    visible_board[x][y] = ' '  
        
        string_rep = ''
        for row in visible_board: 
            string_rep += ' | '.join(row) 
            string_rep += '\n' + '-' * (self.dim_size * 4 - 1) + '\n'  
        
        return string_rep

        

def play(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)

    safe = True

    while len(board.dug) < board.dim_size**2 - num_bombs: 
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like to dig? Input as row,col: "))  # '0, 3'
        row, col = int(user_input[0]), int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Invalid location. Try again.")
            continue

        # if it's valid, we dig
        safe = board.dig(row, col)
        if not safe:
            break
    
    if safe: 
        print("Congratulations! You won!")
    else:
        print("Oh no! You dug a bomb, game over.")
        board.dug = [(r, c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)

if __name__ == '__main__': 
    play() 
