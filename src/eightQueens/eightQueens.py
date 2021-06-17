import tkinter as tk
import numpy as np

CELLCOUNT = 8

class eightQueens(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title('Eight Queens Problem Solver')
        self.grid()
        self.boardCells = []
        self.makeBoard()
        self.initBoard(CELLCOUNT)

    def makeBoard(self):
        background = tk.Frame(self, bg='#858282', width=600, height=600)
        background.grid(padx=(150,150),pady=(150,150))

        for row in range(CELLCOUNT):
            gridRow = [] 
            for col in range(CELLCOUNT):
                cell = tk.Label(background, text='', bg='#ffffff', justify=tk.CENTER, width=10, height=4)
                cell.grid(row=row, column=col, padx=1, pady=1)
                gridRow.append(cell)
            self.boardCells.append(gridRow)
    
    def initBoard(self, n):
        self.board = np.zeros((n**2), dtype='int').reshape((n,n))
    
    def placeQueen(self,n):
        board = self.board
        for row in range(n):
            for col in range(n):
                value = board[row][col]
                if value != 0:
                    self.boardCells[row][col].configure(bg='red')
        self.update_idletasks()
    

gameBoard = eightQueens()