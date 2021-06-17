import unittest
import sys
sys.path.insert(1,'src/2048Game')
import gameFunctions as gameF
import gameGUI as game
import numpy as np

class myTest(unittest.TestCase):
    
    def testGameInitialise(self):
        self.assertTrue(len(gameF.initGame()))
    
    def testMoveBoardRight(self):
        self.board = ([0,2,0,0],[0,2,0,0],[0,0,0,0],[0,0,0,0])
        self.movedRight, _ = gameF.moveBlocksRight(self.board)
        self.assertGreater(self.board[0][1], self.movedRight[0][1])
    
    def testCombineBlocks(self):
        self.board = ([0,0,0,0],[0,2,2,0],[0,0,0,0],[0,0,0,0])
        self.Movedboard, _ = gameF.moveBlocksRight(self.board)
        self.boardCombine, _, _ = gameF.combineBlocks(self.Movedboard, 0)
        self.assertGreater(self.board[1][1], self.boardCombine[1][1])

    def testWin(self):
        self.board = gameF.initGame()
        self.board[1][1] = 512
        self.assertTrue(game.checkGameOver(self.board))
    
    def testNoHorizonatlMovePos(self):
        self.board = ([2,4,8,16], 
                        [2,4,8,16],
                        [2,4,8,16],
                        [2,4,8,16])
        self.assertFalse(gameF.horizontalMovePossible(self.board))
    
    def testHorizonatlMovePos(self):
        self.board = ([2,4,8,16], 
                        [2,0,8,16],
                        [2,2,4,16],
                        [2,4,8,16])
        self.assertTrue(gameF.horizontalMovePossible(self.board))
    
    def testNoVerticalMovePos(self):
        self.board = ([2,4,32,4], 
                        [4,2,64,16],
                        [16,4,32,8],
                        [8,2,8,16])
        self.assertFalse(gameF.verticalMovePossible(self.board))
    
    def testVerticalMovePos(self):
        self.board = ([2,4,32,4], 
                        [2,4,64,16],
                        [16,4,32,8],
                        [8,2,8,16])
        self.assertTrue(gameF.verticalMovePossible(self.board))

    def testAddNewBlock(self):
        self.board = gameF.initGame()
        addedBoard = gameF.addNewBlock(self.board)
        self.assertFalse(addedBoard is not self.board)


if __name__ == '__main__':
    unittest.main()
