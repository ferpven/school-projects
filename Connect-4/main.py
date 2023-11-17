import random
import math
from minimaxalgo import Minimax

class Game:
    #Baslangic degerlerinin olusturulmasi
    gameBoard = []
    round = None
    finish = None
    winner = None
    turn = None
    players = [None, None]
    signs = ['x', 'o']
    row = 6
    col = 7

    def __init__(self):
        #Oyunun baslamasi icin gerekli degerlerin atanmasi
        self.round = 1
        self.finish = 0
        self.winner = 0

        print('Welcome to the Connect-4')
        print('Player is \'x\' and AI is \'o\' ')

        #Oyuncularin players'a atilmasi. Oyuncu her zaman 'x' olacaktir
        self.players[0] = self.signs[0]
        self.players[1] = self.signs[1]

        #Rastgele baslangic oyuncu secimi ve bos oyun tahtasi olusumu
        self.turn = self.players[random.randint(0,1)]
        self.gameBoard = self.createEmptyGameBoard()

    def createEmptyGameBoard(self):
        board = []
        for i in range(self.row):
            board.append([])
            for j in range(self.col):
                board[i].append(' ')
        return board
    
    #Round basinda durumu gosteren ve oyunun bitip bitmedigine dikkat eden fonksiyon
    def show_state(self):
        print(f"Round: {self.round}")
        for i in range(self.row -1, -1, -1):
            print("\t", end="")
            for j in range(self.col):
                print(f"| {str(self.gameBoard[i][j])}", end=" ")
            print("|")
        print("\t  _   _   _   _   _   _   _ ")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finish:
            print('Game Finished!')
            if self.winner == self.players[0]:
                print('Player has won!')
            elif self.winner == self.players[1]:
                print('AI is the winner!')
            else:
                print('Draw')

    def switch_turn(self):
        if self.turn == self.players[0]:
            self.turn = self.players[1]
        else:
            self.turn = self.players[0]

        self.round += 1
    
    #Oyun tahtasinda dikey, yatay veya carpraz 4'lu olup olmadigini kontrol eden fonksiyon
    def check_for_fours(self):
        for i in range (self.row):
            for j in range (self.col):
                if self.gameBoard[i][j] != ' ':

                    if self.ver_check(i, j):
                        self.finish = True

                    if self.hor_check(i, j):
                        self.finish = True
                    
                    diag_fours, slope = self.dig_check(i, j)
                    if diag_fours:
                        self.finish = True

    #Dikey kontrol
    def ver_check(self, row, col):
        four = False
        count = 0
        color = self.gameBoard[row][col].lower()
        for i in range(row, self.row):
            if self.gameBoard[i][col].lower() == color:
                count += 1
            else:
                break
        
        if count >= 4:
            four = True
            if color == self.signs[0]:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
        
        return four

    #Yatay kontrol
    def hor_check(self, row, col):
        four = False
        count = 0
        color = self.gameBoard[row][col].lower()
        for i in range(col, self.col):
            if self.gameBoard[row][i].lower() == color:
                count += 1
            else:
                break
        
        if count >= 4:
            four = True
            if color == self.signs[0]:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]
        
        return four

    #Carpraz kontrol
    def dig_check(self, row, col):
        four = False
        color = self.gameBoard[row][col].lower()
        positive_slope = False
        negative_slope = False
        slope = None

        count = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.gameBoard[i][j].lower() == color:
                count += 1
            else:
                break
            j += 1  

        if count >= 4:
            positive_slope = True
            slope = 'positive'
            if color == self.signs[0]:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        count = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.gameBoard[i][j].lower() == color:
                count += 1
            else:
                break
            j += 1  

        if count >= 4:
            negative_slope = True
            slope = 'negative'
            if color == self.signs[0]:
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        four = positive_slope or negative_slope
        if positive_slope and negative_slope:
            slope = 'both'
        return four, slope

    #Sonraki hareketi oyuncuya gore gerceklestiren fonksiyon
    def next_move(self):
        player = self.turn

        #Oyun tahtasinda maksimum 6*7 tane tas konabilir, bu deger gecilirse oyun biter
        if self.round > self.row * self.col:
            self.finish = True

        chosen_col = None
        #Sira oyuncuda mi AI'da mi kontrolu
        if player == self.signs[0]:
           while chosen_col is None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                print("Invalid choice, try again")
                continue
            if 0 <= choice <= 6:
                chosen_col = choice
            else:
                print("Column must be between 1 and 7, try again") 
    
        else:
            m = Minimax(self.gameBoard)
            best_move, value = m.best_move(state=self.gameBoard, depth=4, alpha=-math.inf, beta=math.inf,
                                       maximizing_player=True)
            chosen_col = best_move

        for i in range(self.row):
            if self.gameBoard[i][chosen_col] == ' ':
                self.gameBoard[i][chosen_col] = player
                self.switch_turn()
                self.check_for_fours()
                self.show_state()
                return

        print("Invalid move (column is full)")


game = Game()
game.show_state()
player = game.players[0]
AI = game.players[1]
#Oyun bitene kadar devam eder
while not game.finish:
    game.next_move()

game.show_state()
        
