'''Tic-Tac-Toe, Object Oriented Version

Created for COS30002 AI for Games, Lab,
by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publically share or post this code without
permission.

Notes/Tips:
* Exactly the same behaviour as the function based version (tictactoe_cli.py).
* Very simple single class conversion of functions and global variables
* Game loop still controlled by the three input/update/render methods
* Internal class helper functions are marked by a leading "_"

General Python Notes:
* All class methods have "self" as their first parameter
* All class variables/methods need to be accessed by a leading "self."

'''

from random import randrange


class TicTacToe(object):
    # class variables - belong to the *class* - NOT object instance.
    WIN_SET = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
        (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)
    )

    HR = '-' * 40

    moves = ""

    def __init__(self):
        # class instance variables for game data (were global variables)
        self.board = [' '] * 9
        self.players = {'x': 'Human', 'o': 'Super AI' }
        self.winner = None
        self.move = None
        # by default the human player starts. This could be random or a choice.
        self.current_player = 'x'
        # Welcome ...
        print('Welcome to the amazing+awesome tic-tac-toe!')
        # Show help (number) details
        self.show_human_help()
        # show the initial board and the current player's move
        self.render_board()

    def _check_move(self):
        '''This function will return True if ``move`` is valid (in the board range
        and free cell), or print an error message and return False if not valid.
        ``move`` is an int board position [0..8].
        '''
        try:
            self.move = int(self.move)
            if self.board[self.move] == ' ':
                return True
            else:
                print('>> Sorry - that position is already taken!')
                return False
        except:  # bare except bad practice but works
            print('>> %s is not a valid position! Must be int between 0 and 8.' % self.move)
            return False

    def _check_for_result(self):
        '''Checks the current board to see if there is a winner, tie or not.
        Returns a 'x' or 'o' to indicate a winner, 'tie' for a stale-mate game, or
        simply False if the game is still going.
        '''
        board = self.board
        for row in self.WIN_SET:
            if board[row[0]] == board[row[1]] == board[row[2]] != ' ':
                return board[row[0]] # return an 'x' or 'o' to indicate winner

        if ' ' not in board:
            return 'tie'

        return None

    #===========================================================================
    # agent (human or AI) functions
    def get_human_move(self):
        '''Get Mihai's AI's next move '''
        corners =  [0, 2, 6, 8]

        symbols = ["o", "x"]

        for j in symbols:
            space = 0
            for i in self.board:
                if(space % 3 == 0) & (self.board[space] == j):
                    if(self.board[space+2] == j) & (self.board[space+1] == ' '):
                        return space+1
                elif((space == 1) | (space ==  4) | (space == 7)) & (self.board[space] == j):
                    if(self.board[space+1] == j) & (self.board[space-1] == ' '):
                        return space-1
                    elif(self.board[space-1] == j) & (self.board[space+1] == ' '):
                        return space+1
                if(space < 3) & (self.board[space] == j):
                    if(self.board[space+6] == j) & (self.board[space+3] == ' '):
                        return space+3
                elif((space == 3) | (space ==  4) | (space == 5)) & (self.board[space] == j):
                    if(self.board[space+3] == j) & (self.board[space-3] == ' '):
                        return space-3
                    elif(self.board[space-3] == j) & (self.board[space+3] == ' '):
                        return space+3
                if(space in corners) & (self.board[space] == j) & (self.board[4] == j):
                    if(space == 0) & (self.board[8] == " "):
                        return 8
                    if(space == 2) & (self.board[6] == " "):
                        return 6
                    if(space == 6) & (self.board[2] == " "):
                        return 2
                    if(space == 8) & (self.board[0] == " "):
                        return 0
                space += 1

        if(self.move == 0):
            if(self.board[8] == " "):
                return 8
        if(self.move == 2):
            if(self.board[6] == " "):
                return 6
        if(self.move == 6):
            if(self.board[2] == " "):
                return 2
        if(self.move == 8):
            if(self.board[0] == " "):
                return 0

        if (self.board[4] == ' '):
            return 4

        if(self.move == 1) | (self.move == 7):
            if(randrange(2) == 0):
                if(self.board[self.move - 1] == " "):
                    return (self.move - 1)
            else:
                if(self.board[self.move + 1] == " "):
                    return (self.move + 1)
        elif(self.move == 3) | (self.move == 5):
            if(randrange(2) == 0):
                if(self.board[self.move - 3] == " "):
                    return (self.move - 3)
            else:
                if(self.board[self.move + 3] == " "):
                    return (self.move + 3)

        if(self.board[0] != " ") & (self.board[2] != " ") & (self.board[6] != " ") & (self.board[8] != " "):
            space = randrange(9)
            while(self.board[space] != " "):
                space = randrange(9)
            return space
        else:
            corner = 0
            while(self.board[corner] != " "):
                x = randrange(len(corners))
                corner = corners[x]
            return corner

    def get_ai_move(self):
        '''Get the AI's next move '''
        avoidMoves = []
        potMoves = []
        with open('data.txt') as f:
            datamoves = f.readlines()
       
        for i in datamoves:
            if (self.moves in i):
                if ('o' in i): #take a win
                    if (len(self.moves) < len(i)):
                        if (i[len(self.moves) + 1] == 'o'):
                            return i[len(self.moves)]
                        if (self.moves in i):
                            if (i[len(self.moves)] not in potMoves):
                                potMoves.insert(-1,int(i[len(self.moves)]))
                if ('x' in i): #avoid a loss
                    if (len(self.moves) < len(i) + 1):
                        if (i[len(self.moves) + 2] == 'x'):
                            if (i[len(self.moves)] not in avoidMoves):
                                avoidMoves.insert(-1,int(i[len(self.moves)]))

        if (len(avoidMoves) > 0):
            for x in avoidMoves:
                if (x in potMoves):
                    potMoves.remove(x)
        if (len(potMoves) > 0):
            return potMoves[randrange(len(potMoves))]
        else:
            return randrange(9)
        
    #===========================================================================
    # Standard trinity of game loop methods (functions)
    
    def process_input(self):
        '''Get the current players next move.'''
        if self.current_player == 'x':
            self.move = self.get_human_move()
        else:
            self.move = self.get_ai_move()
        

    def update_model(self):
        '''If the current players input is a valid move, update the board and check
        the game model for a winning player. If the game is still going, change the
        current player and continue. If the input was not valid, let the player
        have another go.
        '''
        if self._check_move():
            # do the new move (which is stored in the instance 'move' variable)
            self.board[self.move] = self.current_player
            # check board for winner (now that it's been updated)
            self.winner = self._check_for_result()
            # change the current player (regardless of the outcome)
            if self.current_player == 'x':
                self.moves += str(self.move)
                self.current_player = 'o'
            else:
                self.moves += str(self.move)
                self.current_player = 'x'
                
        else:
            print('Try again')

    def render_board(self):
        '''Display the current game board to screen.'''
        board = self.board
        print('    %s | %s | %s' % tuple(board[:3]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(board[3:6]))
        print('   -----------')
        print('    %s | %s | %s' % tuple(board[6:]))

        # pretty print the current player name
        if self.winner is None:
            print('The current player is: %s' % self.players[self.current_player])

    def show_human_help(self):
        '''Show the player help/instructions. '''
        tmp = '''\
    To make a move enter a number between 0 - 8 and press enter.
    The number corresponds to a board position as illustrated:

        0 | 1 | 2
        ---------
        3 | 4 | 5
        ---------
        6 | 7 | 8
        '''
        print(tmp)
        print(self.HR)

    def show_gameresult(self):
        '''Show the game result winner/tie details'''
        print(self.HR)
        if self.winner == 'tie':
            print('TIE!')
        else:
            print('%s is the WINNER!!!' % self.players[self.winner])
        print(self.HR)
        print('Game over. Goodbye')

        with open('1000GamesResult.txt', "a") as f:
            f.write(self.moves + self.winner + "\n")
        f.close()
        
#==============================================================================
# Separate the running of the game using a __name__ test. Allows the use of this
# file as an imported module
#==============================================================================
if __name__ == '__main__':
    # create instance (~ "new") object of type TicTacToe class
    game = TicTacToe()
    loop = True
    gameCount = 0
    # Standard game loop structure
    while (loop == True):
        # Standard game loop structure
        while game.winner is None:
            game.process_input()
            game.update_model()
            game.render_board()

        # Some pretty messages for the result
        game.show_gameresult()

        if(gameCount < 200):
            game = TicTacToe()
            gameCount += 1
        else:
            loop = False
    
    
    
