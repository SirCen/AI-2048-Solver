
from tkinter import Frame, Label, CENTER, Button, Tk, messagebox, simpledialog, commondialog
import assets as assets
from gameFunctions import initGame, moveDown, moveLeft, moveRight, moveUp, addNewBlock, loadGame
import gameAIMCTS as mcts
import xml.etree.ElementTree as xml
import gameAI as ai
import numpy as np
import time
from datetime import datetime
from pathlib import Path, PureWindowsPath

UP = "'w'"
DOWN = "'s'"
LEFT = "'a'"
RIGHT = "'d'"
AIPLAY = "'p'"
AIMOVE = "'q'"
PAUSE = "'t'"
MCTS = "'m'"

CELLCOUNT = 4



class Launch(Tk):
    def __init__(self): 
        # Initialise the class and create Tk object
        Tk.__init__(self)
        # Set attributes of the Tk object
        self.title('2048') 
        self.geometry("740x750+0+0")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.frame = None
        # Initialise and call method
        self.switchFrame(StartScreen)
    
    def switchFrame(self, frameClass):
        newFrame = frameClass(self) # copies frame to new frame
        if self.frame is not None: # checks if frame is already made
            self.frame.destroy() # destroys old frame
        self.frame = newFrame # sets frame to the new frame
        self.frame.grid(row=0,column=0,sticky='N') # Sets frame attributes
        self.frame.grid_rowconfigure(2, weight=2)
        self.frame.grid_columnconfigure(0, weight=1)

class StartScreen(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        Label(self, text="2048", font=assets.LABEL_FONT, pady=50).grid() #Title Label
        # Buttons for play, controls and exit
        Button(self, text="Play 2048!", fg='white', bg=assets.GAME_COLOUR, borderwidth=5, width=50, command=lambda: master.switchFrame(Display)).grid(row=1,sticky='NESW',padx=10,pady=10)
        Button(self, text="Controls",fg='white', bg=assets.GAME_COLOUR, borderwidth=5, width=50, command=lambda: self.showMessageBox()).grid(padx=10,pady=10)
        Button(self, text="Exit",fg='white', bg='red', borderwidth=5, width=50, command=lambda: self.closeWindow(master)).grid(padx=10,pady=10)
    
    def showMessageBox(self): # Shows control message box
        messagebox.Message(self, title="Controls", message='Controls: \nUP: w \nDOWN: s \nLEFT: a \nRIGHT: d \nAI Solve: p \nAI Single Move: q \nMonte Carlo Tree Search: m').show()

    def closeWindow(self,master): # Closes program
        master.destroy()
   

class Display(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        # Sets and declares self attributes
        self.master.title('2048')
        self.grid()
        self.master.bind("<Key>", self.keyPress)
        # Controls for game
        self.controls = {LEFT: moveLeft,
                        RIGHT: moveRight,
                        UP: moveUp,
                        DOWN: moveDown,
                        PAUSE: self.showPauseMenu}
        self.gridCells = []
        self.score = 0
        self.scoreLabel = Label(self)
        self.startTime = None
        self.timePaused = None
        self.isPaused = False
        # Initialises and calls methods
        self.makeGrid()
        self.initBoard()
        self.drawBlocks()
        self.loadButton()
        self.scoreBoard()
        self.timerStart()
        self.timer()
        self.updateGUI()
        self.movePossible()
        self.checkGameEnd()
    
    # Makes Game Grid
    def makeGrid(self): 
        # Background for game grid
        background = Frame(self,bg = assets.GAME_COLOUR, width = 600, height = 600)
        background.grid(pady=(150,0))
        # iterates through, creates new grid row with cells
        for row in range(CELLCOUNT):
            gridRow = []
            for col in range(CELLCOUNT):
                # cell for game block
                cell = Frame(background, bg=assets.EMPTY_COLOUR, width = 600/CELLCOUNT, height = 600/CELLCOUNT)
                cell.grid(row=row, column=col, padx=10, pady=10)
                # label for block value
                cellText = Label(master=cell, text="", bg=assets.EMPTY_COLOUR, justify=CENTER, font=assets.LABEL_FONT, fg='white', width=5, height=2)
                cellText.grid()
                gridRow.append(cellText)
            self.gridCells.append(gridRow) # adds row to grid cells
    
    # Initiates game board
    def initBoard(self):
        self.board = initGame()

    # Updates labels and cells to new values
    def drawBlocks(self):
        for row in range(CELLCOUNT):
            for col in range(CELLCOUNT):
                blockValue = self.board[row][col]
                if blockValue != 0: #Configures block to correct colour and text
                    self.gridCells[row][col].configure(text=str(blockValue), bg=assets.BLOCK_COLOURS[blockValue], fg='white')
                else:
                    self.gridCells[row][col].configure(text="", bg=assets.EMPTY_COLOUR)
        self.update_idletasks()

    # Load game button
    def loadButton(self):
        Button(self, text="Load Previous Game", bg=assets.GAME_COLOUR, fg='white', command=self.readGame).place(relx=0.1,rely=0.18, anchor='center')

    # Score board for game
    def scoreBoard(self):
        scoreFrame = Frame(self)
        scoreFrame.place(relx=0.5, y=55, anchor="center")
        self.scoreLabel = Label(scoreFrame, text="Score: " + str(self.score), font=assets.LABEL_FONT)
        self.scoreLabel.grid(row=0)
    
    # Game Timer 
    # Start Timer
    def timerStart(self):
        self.startTime = datetime.now()

    # Pause Timer
    def timerPaused(self):
        self.timePaused = datetime.now()

    # Resume Timer
    def timerResume(self):
        pausedTime = datetime.now() - self.timePaused
        self.startTime += pausedTime

    # Get time for timer
    # returns time delta for whether timer is paused or not
    def getTime(self):
        if self.isPaused:
            return self.timePaused - self.startTime 
        else:
            return datetime.now() - self.startTime    
    
    # Timer UI
    def timer(self):
        time = self.getTime()
        now = 'Time Played: '
        now += str(time).split('.')[0] # Splits timer value to not include miliseconds
        Label(self, text=now, font=assets.TIMER_FONT).place(relx=0.79, rely=0.17, anchor="center")
        self.master.after(1000, self.timer)   # After 1 secoond, call method to update timer

    # Handles key presses 
    # Input: event; any user input        
    def keyPress(self, event):
        validGame = True
        key = repr(event.char) # gets char value of input
        if key == AIPLAY and not self.isPaused: #AI Play Game
            validMove = True
            while not self.checkGameEnd(): # loops until game ended
                self.board, validMove, self.score = ai.expectimax(self.board, ai.CURRENT_DEPTH, ai.MAX_DEPTH, self.score)
                if validMove:
                    self.board = addNewBlock(self.board) # adds new block to grid
                    self.drawBlocks() # updates game aspects
                    self.scoreBoard()
                    self.timer()
                    self.updateGUI()
                if self.checkGameEnd():
                    break 
        if key == AIMOVE and not self.isPaused: # AI Single Move
            self.board, moveMade, self.score = ai.expectimax(self.board, ai.CURRENT_DEPTH, ai.MAX_DEPTH, self.score)
            if moveMade:
                self.board = addNewBlock(self.board) #adds new block to grid
                self.drawBlocks() # updates game aspects
                self.scoreBoard()
                self.updateGUI()
                moveMade = False
                self.checkGameEnd()
        if key == MCTS and not mcts.isPaused: # Monte-Carlo Tree Search
            moveCount = 0
            validGame = True
            while not self.checkGameEnd():
                self.board, validGame = mcts.aiMove(self.board,30,40, self.score)
                if validGame:
                    self.board = addNewBlock(self.board) # adds new block to grid
                    self.drawBlocks() # updates game aspects
                    self.scoreBoard()
                    self.updateGUI()
                moveCount += 1
                if self.isPaused:
                    break
        if key == PAUSE:
            self.isPaused = True
            self.timerPaused()
            self.showPauseMenu()
        elif key in self.controls and not self.isPaused: # User Play
            self.board, moveMade, self.score = self.controls[key](self.board, self.score)
            if moveMade:
                self.board = addNewBlock(self.board) #adds new block to grid
                self.drawBlocks() # updates game aspects
                self.scoreBoard()
                self.updateGUI()
                moveMade = False
            self.checkGameEnd()
    
    # Updates graphical user interface 
    def updateGUI(self):
        for i in range(CELLCOUNT):
            for j in range(CELLCOUNT):
                blockValue = self.board[i][j]
                if blockValue == 0:
                    self.gridCells[i][j].configure(bg=assets.EMPTY_COLOUR, text="")
                else:
                    self.gridCells[i][j].configure(bg=assets.BLOCK_COLOURS[blockValue], text=str(blockValue),  fg='white')
                    
        self.update_idletasks()

    # Checks if game has ended either win or lose
    # If game has ended returns true, else returns false    
    def checkGameEnd(self):
        if (2048 in self.board): # Win
            self.gameEndFrame("Win")
            self.timerPaused()
            return True
        elif self.movePossible(): # Lose
            self.gameEndFrame("Lose")
            self.timerPaused()
            return True
        else:
            return False
    
    # Checks if any move is possible
    # returns true if no moves possible, false if moves possible
    def movePossible(self):
        newBoard = np.copy(self.board) # copies current board
        moves = [moveDown, moveLeft, moveRight, moveUp]
        moveMadesArr = [] # boolean array of if move was made
        #iterates through moves
        for move in moves: 
            newBoard, moveMade, _ = move(newBoard, self.score) # simulates move
            moveMadesArr.append(moveMade) # appends bool to array
        return not any(moveMadesArr) 
                
    # Frame shown if game won/lose
    # Input: outcome; string
    def gameEndFrame(self, outcome):
        gameOverFrame = Frame(self, borderwidth = 5)
        gameOverFrame.place(relx=0.5, rely=0.5, anchor='center')
        state = outcome + '!'
        Label(gameOverFrame, text=state, bg='grey', fg='yellow', font=assets.LABEL_FONT).pack()
    
    # Menu when game paused
    def showPauseMenu(self):
        pauseMenu = Frame(self, borderwidth=5, bg='grey')
        pauseMenu.place(relx=0.5, rely=0.5, anchor='center')
        Label(pauseMenu, text='Paused', bg='grey', fg='white', font=assets.LABEL_FONT).pack()
        # Buttons on pause menu, return to game, save game, load game, exit game
        Button(pauseMenu, text='Return to Game', command=lambda:[pauseMenu.destroy(), self.unpause()]).pack()
        Button(pauseMenu, text='Save Game', command=self.saveGame).pack()
        Button(pauseMenu, text='Load Previous Game', command=lambda:[self.readGame(), self.unpause(), pauseMenu.destroy()]).pack()
        Button(pauseMenu, text='Exit Game', command=self.exitGame, bg='red', fg='white').pack()

    # Unpauses game, resumes timer
    def unpause(self):
        self.isPaused = False
        self.timerResume()

    # Exits program
    def exitGame(self):
        self.master.destroy()

    # Loads game from save file if file exists
    def readGame(self):
        data = xml.parse('saves.xml')
        print('Game Loaded')
        root = data.getroot()
        self.board, self.score = loadGame(root[0].text.replace("]", '').replace("[",''), root[1].text)
        self.drawBlocks()
        self.updateGUI()
        self.scoreBoard()

    # Saves game to file, if file doesnt exist create file.
    def saveGame(self):
        data = xml.Element('Game')
        matrix = xml.SubElement(data, 'Matrix')
        score = xml.SubElement(data, 'Score')
        print(self.board)
        matrix.text = str(self.board)
        score.text = str(self.score)
        b_xml = xml.tostring(data)
        with open("saves.xml", "wb") as f:
            f.write(b_xml)
            print("Game saved")

if __name__ == "__main__":
    app = Launch()
    app.mainloop()
    