import math
import random


class Minimax:
    #Anlik olan oyun tahtasini alan obje
    gameBoard = None
    signs = ["x", "o"]
    human = signs[0]
    ai = signs[1]
    row = 6
    col = 7

    def __init__(self, gameBoard):

        self.gameBoard = gameBoard.copy()

    def best_move(self, state, depth, alpha, beta, maximizing_player):
        #En iyi hareketi sutun numarasi olarak donduren fonksiyon
        #Butun uygun hareketleri tutar
        valid_moves = []
        for col in range(self.col):
            if self.is_valid_move(col, state):
                valid_moves.append(col)

        if depth == 0 or self.is_game_over(state):
            return None, self.value(state, self.ai)
        if len(valid_moves) == 0:
            return None, 0

        if maximizing_player: #maksimum icin degerleri dondurur
            value = -math.inf
            column = random.choice(valid_moves)
            for col in valid_moves:
                temp = self.make_move(state, col, self.ai)
                _, new_score = self.best_move(temp, depth - 1, alpha, beta, False)
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else: #minimum icin degerleri dondurur
            value = math.inf
            column = random.choice(valid_moves)
            for col in valid_moves:
                temp = self.make_move(state, col, self.human)
                _, new_score = self.best_move(temp, depth - 1, alpha, beta, True)
                if new_score < value:
                    value = new_score
                    column = col
                alpha = min(alpha, value)
                if alpha >= beta:
                    break
            return column, value

    def is_valid_move(self, column, state):
        #Yapilacak hareketin uygun olup olmadigini kontrol eder
        for i in range(self.row):
            if state[i][column] == ' ':
                return True
        #Eger bos sutun yoksa False dondurur
        return False

    def is_game_over(self, state):
        #Oyunun bitip bitmedigini kontrol eder
        return self.count_streak(state, self.human, 4) >= 1 \
               or self.count_streak(state, self.ai, 4) >= 1

    def make_move(self, state, column, color):
        #Oyuncuyu kopyalayarak eklenmis hareketle yeni bir dizi dondurur
        temp = [x[:] for x in state]
        for i in range(self.row):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def value(self, state, color):
       
        if color == self.human:
            o_color = self.ai
        else:
            o_color = self.human

        center_array = [row[self.col // 2] for row in state]
        center_count = center_array.count(color)

        my_fours = self.count_streak(state, color, 4)
        my_threes = self.count_streak(state, color, 3)
        my_twos = self.count_streak(state, color, 2)
        opp_fours = self.count_streak(state, o_color, 4)
        opp_threes = self.count_streak(state, o_color, 3)

        if opp_fours > 0:
            return -100000
        else:
            return center_count * 3 + my_fours * 100 + my_threes * 5 + my_twos * 2 - opp_threes * 4

    def count_streak(self, state, color, streak):
        count = 0
        #tahtadaki her bir parca icin
        for i in range(self.row):
            for j in range(self.col):
                if state[i][j].lower() == color.lower():
                    #dikey kontrol
                    count += self.vertical_streak(i, j, state, streak)

                    #yatay kontrol
                    count += self.horizontal_streak(i, j, state, streak)

                    #carpraz kontrol
                    count += self.diagonal_streak(i, j, state, streak)

        return count

    #Dikey dort oldu mu
    def vertical_streak(self, row, col, state, streak):
        consecutive_count = 0
        color = state[row][col].lower()
        for i in range(row, self.row):
            if state[i][col].lower() == color:
                consecutive_count += 1
            else:
                break

        return 1 if consecutive_count >= streak else 0

    #Yatay dort oldu mu
    def horizontal_streak(self, row, col, state, streak):
        consecutive_count = 0
        color = state[row][col].lower()

        for j in range(col, self.col):
            if state[row][j].lower() == color:
                consecutive_count += 1
            else:
                break

        return 1 if consecutive_count >= streak else 0

    #Carpraz dort oldu mu
    def diagonal_streak(self, row, col, state, streak):
        color = state[row][col].lower()
        total = 0

        consecutive_count = 0
        j = col
        for i in range(row, self.row):
            if j > self.col - 1:
                break
            elif state[i][j].lower() == color:
                consecutive_count += 1
            else:
                break
            j += 1 

        if consecutive_count >= streak:
            total += 1

        consecutive_count = 0
        j = col
        for i in range(row, -1, -1):
            if j > self.col - 1:
                break
            elif state[i][j].lower() == color:
                consecutive_count += 1
            else:
                break
            j += 1 

        if consecutive_count >= streak:
            total += 1

        return total