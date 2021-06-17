import numpy as np 

CELLCOUNT = 4


def initGame():
    board = np.zeros((16), dtype="int")
    initBlocks = np.random.default_rng().choice(16, 2, replace=False)
    board[initBlocks] = 2
    board = board.reshape((4,4))
    return (board)

def loadGame(board, score):
    loadBoard = np.fromstring(board, dtype=int, sep=' ')
    loadBoard = loadBoard.reshape((4,4))
    loadScore = int(score)
    return loadBoard, loadScore


def moveBlocksRight(board):
    newBoard = np.zeros((CELLCOUNT,CELLCOUNT), dtype='int')
    done = False
    for row in range(CELLCOUNT):
        count = CELLCOUNT - 1
        for col in range(CELLCOUNT-1, -1, -1):
            if board[row][col] != 0:
                newBoard[row][count] = board[row][col]
                if col != count:
                    done = True
                count -= 1
    return (newBoard, done)

def combineBlocks(board, score):
    done = False
    for row in range(CELLCOUNT):
        for col in range(CELLCOUNT-1, 0, -1):
            if board[row][col] == board[row][col-1] and board[row][col] != 0:
                board[row][col] *= 2
                score += board[row][col]
                board[row][col-1] = 0
                done = True
    return board, done, score

def addNewBlock(board):
    number = np.random.choice([2,4], p=[0.9,0.1])
    rowAvailable, colAvailable = np.nonzero(np.logical_not(board))
    if len(rowAvailable) > 0:
        newBlockLocation = np.random.randint(0, len(rowAvailable))
        board[rowAvailable[newBlockLocation],colAvailable[newBlockLocation]] = number
    return board

def moveLeft(board, score):
    board = np.rot90(board, 2)
    board, hasMoved = moveBlocksRight(board)
    board, hasCombined, newscore = combineBlocks(board, score)
    board, _ = moveBlocksRight(board)
    board = np.rot90(board, -2)
    moveMade = hasMoved or hasCombined
    return board, moveMade, newscore


def moveRight(board, score):
    board, hasMoved = moveBlocksRight(board)
    board, hasCombined, newscore = combineBlocks(board, score)
    board, _ = moveBlocksRight(board)
    moveMade = hasMoved or hasCombined
    return board, moveMade, newscore

def moveUp(board,score):
    rotBoard = np.rot90(board, -1)
    movedBoard, hasMoved = moveBlocksRight(rotBoard)
    secondMovedBoard, hasCombined, newscore = combineBlocks(movedBoard,score)
    rotBackBoard = np.rot90(secondMovedBoard, 1)
    moveMade = hasMoved or hasCombined
    return rotBackBoard, moveMade, newscore

def moveDown(board,score):
    board = np.rot90(board, 1)
    board, hasMoved = moveBlocksRight(board)
    board, hasCombined, newscore = combineBlocks(board,score)
    board = np.rot90(board, -1)
    moveMade = hasMoved or hasCombined
    return board, moveMade, newscore

def randomMove(board, score):
    moveMade = False
    moveOrder = [moveRight, moveUp, moveDown, moveLeft]
    while not moveMade and len(moveOrder) > 0:
        moveIndex = np.random.randint(0, len(moveOrder))
        move = moveOrder[moveIndex]
        board, moveMade, score = move(board, score)
        if moveMade:
            return board, True, score
        moveOrder.pop(moveIndex)
    return board, False, score

def checkGameOver(board):
    return 2048 in board

