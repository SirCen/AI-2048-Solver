import numpy as np
import gameFunctions as func

isPaused = False
# Code adapted from https://github.com/kiteco/python-youtube-code/tree/master/AI-plays-2048 
# Author of original code MikhailLenko on github
SEARCH_SCALE = 20
SEARCH_LEN = 8
SEARCH_PARAM = 200

def getSearchParams(moveNumber):
    searchesPerMove = SEARCH_SCALE * (1+(moveNumber // SEARCH_PARAM))
    searchLength = SEARCH_LEN * (1+(moveNumber // SEARCH_PARAM))
    return searchesPerMove, searchLength

def aiMove(board, searchesPerMove, searchLength, score):
    possibleFirstMove = [func.moveUp, func.moveLeft, func.moveDown, func.moveRight]
    firstMoveScores = np.zeros(len(possibleFirstMove)) #array of scores from each possible move
    for i in range(len(possibleFirstMove)):
        firstMoveFunc = possibleFirstMove[i] 
        boardWithMove, firstMoveMade, firstMoveScore = firstMoveFunc(board, score)
        if firstMoveMade:
            boardWithMove = func.addNewBlock(boardWithMove)
            firstMoveScores[i] += firstMoveScore #adds score to array of scores
        else:
            continue 
        for laterMoves in range(searchesPerMove): #searches later moves in the tree
            moveNumber = 1
            searchBoard = np.copy(boardWithMove) #copies board to a new board to be searched
            gameValid = True
            while gameValid and moveNumber < searchLength and not isPaused: #searches each move to find max score after searchLength amount of moves
                searchBoard, gameValid, score = func.randomMove(searchBoard, score) #performs a random move on the board 
                if gameValid:
                    searchBoard = func.addNewBlock(searchBoard)
                    firstMoveScores[i] += score #adds score to original score
                    moveNumber += 1 
    bestMoveIndex = np.argmax(firstMoveScores) #finds best move pos based on highest score
    bestMove = possibleFirstMove[bestMoveIndex] 
    score = firstMoveScores[bestMoveIndex] #finds score based on best move
    searchBoard, gameValid, score = bestMove(board, score)
    return searchBoard, gameValid #returns board after move and if the game is still valid

#Prints to command line
def aiPlay(board, score):
    moveNumber = 0
    validGame = True
    while validGame and not isPaused:
        moveNumber += 1
        numberOfSims, searchLen = getSearchParams(moveNumber) #retrieves the params of the search
        board, validGame = aiMove(board, numberOfSims, searchLen, score) #performs the search and returns the board after the move is made
        if validGame: 
            board = func.addNewBlock(board)
        if func.checkGameOver(board):
            validGame = False
        print(board)
        print(moveNumber)
    print(board)
    return np.amax(board) #returns the maximum score from the board
