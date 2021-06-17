from eightQueens import gameBoard, CELLCOUNT
QUEEN = 1
N = 8
def placeSolution(board):
        print(board)  
        gameBoard.placeQueen(N)
        
def canPlace(board, row, col): 
    # Check this row on left side 
    for i in range(col): 
        if board[row][i] == QUEEN: 
            return False
    # Check lower diagonal on left side
    lowerRowColList = zip(range(row, N, 1), range(col, -1, -1)) 
    for i, j in lowerRowColList: 
        if board[i][j] == QUEEN: 
            return False
    # Check upper diagonal on left side 
    upperRowColList = zip(range(row,-1,-1),range(col,-1,-1))
    for i,j in upperRowColList:
        if board[i][j] == QUEEN: 
            return False   
    return True
  
def solveNQueens(board, col): 
    if col >= N: 
        return True

    for i in range(N): 
        if canPlace(board, i, col):  
            board[i][col] = QUEEN 
            if solveNQueens(board, col + 1) == True: 
                return True
            board[i][col] = 0
    return False 

def solve():
    board = gameBoard.board
    if (solveNQueens(board, 0) == False):
        print("No Solution")
        return False  
    placeSolution(board)
    return True  

solve()
gameBoard.mainloop()