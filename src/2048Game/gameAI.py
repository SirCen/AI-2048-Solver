import tkinter as tk
import numpy as np
from gameFunctions import initGame, moveDown, moveUp, moveRight, moveLeft, addNewBlock, randomMove

CURRENT_DEPTH = 0
MAX_DEPTH = 2
MOVES = [moveUp, moveLeft, moveDown, moveRight]


def expectimax(board, currentDepth, maxDepth, score):
    if currentDepth == maxDepth:
        return board, False, score
    else:
        searchBoard = np.copy(board)
        bestMove = nextMove(searchBoard, score)
        newBoard, moveMade, score = bestMove(searchBoard, score)
    return newBoard, moveMade, score
    

#Determine Next Move
#input: board, score
#output: bestMove
#variables: bestMove, bestScore
def nextMove(board, score):
    bestMove = moveUp
    bestScore = 0
    for move in MOVES:
        score = calculateScore(board, move, score)
        if score > bestScore:
            bestScore = score
            bestMove = move
    return bestMove

#Calculate Score
#input: board, move, score
#output: generateScore
#varibales: newBoard
def calculateScore(board, move, score):
    newBoard, moveMade, score = move(board, score)
    if not moveMade:
        return 0
    return generateScore(newBoard, CURRENT_DEPTH, MAX_DEPTH)



#Generate Score
#input: board, current depth, max depth
#output: finalScore
#variables: finalScore, newBoard2, newBoard4, moveScore2, moveScore4
def generateScore(board, currentDepth, maxDepth):
    if currentDepth == maxDepth:
        return calculateFinalScore(board)
    finalScore = 0
    rows = board.shape[0]
    cols = board.shape[1]
    for i in range(0, rows):
        for j in range(0, cols):
            if not board[i][j]:
                newBoard2 = np.copy(board)#board if 2 is added
                newBoard2[i][j] = 2
                moveScore2 = calculateMoveScore(newBoard2, currentDepth, maxDepth)
                finalScore = finalScore + (0.9*moveScore2)
                newBoard4 = np.copy(board) #board if 4 is addded
                newBoard4[i][j] = 4
                moveScore4 = calculateMoveScore(newBoard4, currentDepth, maxDepth)
                finalScore = finalScore + (0.1*moveScore4)
    return finalScore


#Calculate Move Score
#input: board, current depth, max depth
#output: bestScore
#variables: bestScore, newBoard, genScore, score, moveMade
def calculateMoveScore(board, currentDepth, maxDepth):
    bestScore = 0
    for move in MOVES:
        newBoard, moveMade, score = move(board, bestScore)
        if moveMade:
            genScore = generateScore(newBoard, currentDepth+1, maxDepth)
            bestScore = max(genScore, bestScore)
    return bestScore

#Calculate Final Score
#input: board
#output: finalScore
#variables: finalScore, mergeScore
def calculateFinalScore(board):
    finalScore = 0
    mergeScore = 0
    rows = board.shape[0]
    cols = board.shape[1]
    for i in range(0, rows):
        for j in range(0, cols):
            if board[i][j] == board[i][j-1]:
                mergeScore += board[i][j] * 2
            if board[i][j] == board[i-1][j]:
                mergeScore += board[i][j] * 2
    finalScore += mergeScore
    return finalScore


        