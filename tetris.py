from tkinter import *
import random

class Shape:
    def __init__(self, coordsList, color, squareList, game, center):
        """
        Initializing a new Shape by setting variables and showing itself
        
        Parameters:
        - List of coordinates (a 2 number list) in the shape
        - The color of the shape
        - Dictionary of all squares in Tetris game
        - Tetris object
        - "Center" of the shape (set to certain block, since each piece is 4 blocks), list of length 2 of integers
        """
        self.coords = coordsList
        self.color = color
        self.squareList = squareList
        self.game = game
        self.center = center
        self.show()

    def fall(self):
        """
        Erases itself and redraws itself 1 block down
        """
        self.erase()
        for i in self.coords:
            i[0] += 1
        self.center[0] += 1
        self.show()

    def get_coords(self):
        """
        Getter for coordinates
        """
        return(self.coords)

    def set(self):
        """
        Sets each square in the shape to occupied
        """
        for i in self.coords:
            self.squareList[tuple(i)].occupy()
            

    def show(self):
        """
        Draws each shape in the set coolor
        """
        for i in self.coords:
            self.squareList[tuple(i)].draw(self.color)
            

    def erase(self):
        """
        Erases all squares on the main board
        """
        for i in self.coords:
            self.squareList[tuple(i)].erase()

    def left(self):
        """
        If possible, moves the shape to the left
        """
        possible = True

        # Checking to see if there are any blocks/walls to the left
        for i in self.coords:
            if i[1] == 1:
                possible = False
            elif self.squareList[(i[0], i[1] - 1)].is_occupied():
                possible = False

        # Moves the piece to the left
        if possible:
            self.erase()
            for i in self.coords:
                i[1] -= 1
            self.center[1] -= 1
            self.show()
            
    def right(self):
        """
        If possible, moves the shape to the left
        """
        possible = True
        
        # Checking to see if there are any blocks/walls to the right
        for i in self.coords:
            if i[1] == 10:
                possible = False
            elif self.squareList[(i[0], i[1] + 1)].is_occupied():
                possible = False
        
        # Moves the piece to the right
        if possible:
            self.erase()
            for i in self.coords:
                i[1] += 1
            self.center[1] += 1
            self.show()

    def rotate(self):
        """
        Rotates the piece
        """
        # Creates an empty copy of the piece coordinates
        copy2 = []
        
        for coordinate in self.coords:
            # Find the distance between a square and the center in both the x and y coordinates
            differencex = coordinate[0] - self.center[0]
            differencey = coordinate[1] - self.center[1]

            # Rotates the piece about the center            
            if differencex < 0:
                copy2.append([self.center[0] + differencey, self.center[1]-differencex - 1])
            else:
                copy2.append([self.center[0] + differencey, self.center[1]-differencex - 1])

        # Finding the lowest and highest square the piece contains                  
        maxheight = copy2[0][0]
        minheight = copy2[0][0]
        for coordinate in copy2:
            if coordinate[0] > maxheight:
                maxheight = coordinate[0]
            if coordinate[0] < minheight:
                minheight = coordinate[0]        

        # Checking to make sure the rotated piece doesn't go through walls/other pieces
        possible = True
        if minheight < 0 or maxheight > 21:
            possible = False
        else:
            for coords in copy2:
                if self.squareList[tuple(coords)].is_occupied():
                    possible = False
        
        # Erases the piece and redraws it
        if possible:
            self.erase()
            self.coords = copy2.copy()
            self.show()
        
        

    def slam(self):
        pass

class TetrisSquare(Canvas):
    def __init__(self, coords, master, game):
        """
        Initializing a new square in the Tetris grid by setting fill colors and intializing attributes

        Parameters:
        - Coordinates of the sqaure
        - Tkinter root
        - Tetris object
        """
        Canvas.__init__(self, master, height = 30, width = 30)
        self['bg'] = 'Gray'
        self['highlightthickness'] = 1
        self['highlightbackground'] = 'black'
        self.master = master
        self.game = game
        self.occupied = False
        self.coords = coords
        self.color = None

        self.grid(row = coords[0], column = coords[1])

    def draw(self, color):
        """
        Draws a square with the given color
        """
        if not color is None:
            self.color = color
            self['bg'] = color

    def occupy(self):
        """
        Sets the status of the square as occupied
        """
        self.occupied = True

    def is_occupied(self):
        """
        Check if the square is occupied
        """
        return self.occupied

    def erase(self):
        """
        Erases the square and resets the square to its original color
        """
        self['bg'] = 'Gray'
        self.occupied = False
        self.color = None
        

    def fall(self):
        """
        Moves the current square to the one below
        """
        if self.occupied:
            if not self.squareDict[self.coords[0] + 1, self.coords[1]].is_occupied():
                self.squareDict[self.coords[0] + 1, self.coords[1]].draw(self.color)
                self.squareDict[self.coords[0] + 1, self.coords[1]].occupy()
                self.erase()

    def assign_dict(self, squareDict):
        """
        Assigns a dictionary of squares
        """
        self.squareDict = squareDict
        

class Tetris(Frame):
    def __init__(self, master):
        """"
        Initializes a game of Tetris
    
        Parameters:
        - Tkinter root

        Inherited from:
        - Tkinter frame
        """

        # Initializes its frame and sets up a grid
        Frame.__init__(self, master)
        self.grid()

        self.gameover = False

        # Setting up the score feature
        self.score = IntVar()
        self.score.set(0)
        self.scoreLabel = Label(master, font = ['Helvitica', 30], textvariable = str(self.score))
        self.scoreLabel.grid(row = 0, column = 0, columnspan = 22, sticky = W)

        # Creating the board made up of TetrisSquare objects
        self.squareDict = {}
        for row in range(1, 21):
            for column in range(1, 11):
                self.squareDict[(row, column)] = TetrisSquare((row, column), master, self)

        # Assign the dictionary of squares to each of the squares on the board
        for square in list(self.squareDict.values()):
            square.assign_dict(self.squareDict)

        # Setting the first piece
        self.piece = None
        self.pieceList = ['Z', 'S', 'O', 'I', 'J', 'L', 'T']
        random.shuffle(self.pieceList)
        self.piece = self.getpiece(self.pieceList.pop())
        
        #Forcing the window to be at front and binding keys
        self.focus_set()
        self.bind('<Left>', self.left)
        self.bind('<Right>', self.right)
        self.bind('<Down>', self.slam)
        self.gameStart()

    def left(self, event):
        """
        Binds the left arrow key to the left function of the piece
        """
        self.piece.left()

    def right(self, event):
        """
        Binds the right arrow key to the right function of the piece
        """
        self.piece.right()

    def rotate(self, event):
        """
        Binds the up arrow key to the rotate function of the piece
        """
        self.piece.rotate()

    def getpiece(self, letter):
        """
        Creates a tetris shape object and returns it
        """
        if letter == 'Z':
            piece = Shape([[1,6], [2,6], [2,5], [3,5]], 'red', self.squareDict, self, [2,6])
        elif letter == 'S':
            piece = Shape([[1,5], [2,6], [2,5], [3,6]], 'lime', self.squareDict, self, [2,6])
        elif letter == 'O':
            piece = Shape([[1,6], [1,5], [2,6], [2,5]], 'yellow', self.squareDict, self, [2,6])
        elif letter == 'I':
            piece = Shape([[1,6], [2,6], [3,6], [4,6]], 'sky blue', self.squareDict, self, [3,6])
        elif letter == 'J':
            piece = Shape([[1,6], [2,6], [3,6], [3, 5]], 'blue', self.squareDict, self, [2,6])
        elif letter == 'L':
            piece = Shape([[1,5], [2,5], [3,5], [3,6]], 'orange', self.squareDict, self, [2,6])
        else:
            piece = Shape([[1,6], [2,6], [3,6], [2,5]], 'purple', self.squareDict, self, [2,5])

        return piece
        
    def gameStart(self):
        """
        Plays a game of tetris
        """
        self.piece.fall()
        
        # If the piece should stop, stop the piece.
        if self.check_fall():
            self.piece.set()
            del self.piece

            # Create a new piece
            if len(self.pieceList) == 0:
                self.pieceList = ['Z', 'S', 'O', 'I', 'J', 'L', 'T']
                random.shuffle(self.pieceList)
                self.piece = self.pieceList.pop()
            else:
                self.piece = self.pieceList.pop()
            self.piece = self.getpiece(self.piece)

            # If there are pieces of other tetris blocks where it starts, end the game
            for i in self.piece.get_coords():
                if self.squareDict[tuple(i)].is_occupied():
                    self.gameover = True

            # Check to find out which squares should be cleared, and clear them
            clearedList = self.check_clear()
            for i in clearedList:
                self.clearLine(i)

        # If the game isn't over, keep going
        if not self.gameover:    
            self.master.after(200, self.gameStart)

    def check_fall(self):
        """
        Returns a boolean based on if the piece should fall
        """
        for i in self.piece.get_coords():
            if i[0] == 20:
                return True
            
            elif self.squareDict[(i[0] + 1, i[1])].is_occupied():
                return True

        return False

    def check_clear(self):
        """
        Returns a list based on what lines should be cleared
        """
        clearedList = []
        for i in range(1,21):
            cleared = True
            for j in range(1, 11):
                
                if not self.squareDict[(i,j)].is_occupied():
                    cleared = False

            if cleared == True:
                clearedList.append(i)

        return clearedList

    def clearLine(self, row):
        """
        Clears a line and adds 100 to the score
        """
        for i in range(1,11):
            self.squareDict[(row, i)].erase()
            self.score.set(self.score.get() + 100)
        for i in range(row-1, 1, -1):
            for j in range(1,11):
                self.squareDict[(i, j)].fall()

        
            

root = Tk()
root.title('Tetris')
Tetris = Tetris(root)
Tetris.mainloop()
