import tkinter as tk
from tkinter import messagebox


def create_board():
    return [[' ' for _ in range(3)] for _ in range(3)]

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]

    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    return None

def is_board_full(board):
    for row in board:
        if ' ' in row:
            return False
    return True

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    elif is_board_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, depth + 1, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, depth + 1, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def find_best_move(board):
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'X'
                score = minimax(board, 0, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = create_board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'O'
        self.create_widgets()

    def create_widgets(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self.root, text=' ', font='normal 20 bold', height=3, width=6, command=lambda i=i, j=j: self.on_button_click(i, j))
                self.buttons[i][j].grid(row=i, column=j)

    def on_button_click(self, i, j):
        if self.board[i][j] == ' ' and self.current_player == 'O':
            self.board[i][j] = 'O'
            self.buttons[i][j].config(text='O')
            self.current_player = 'X'
            if self.check_game_over():
                return
            self.ai_move()

    def ai_move(self):
        move = find_best_move(self.board)
        if move:
            self.board[move[0]][move[1]] = 'X'
            self.buttons[move[0]][move[1]].config(text='X')
            self.current_player = 'O'
        self.check_game_over()

    def check_game_over(self):
        winner = check_winner(self.board)
        if winner:
            messagebox.showinfo("Tic-Tac-Toe", f"Winner: {winner}")
            self.root.quit()
            return True
        elif is_board_full(self.board):
            messagebox.showinfo("Tic-Tac-Toe", "Draw!")
            self.root.quit()
            return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()
