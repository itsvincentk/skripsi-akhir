from Cell import Cell
import numpy as np
import copy

class Board:
    def __init__(self, firstBoard) -> None:
        self.makeBoard(firstBoard)
        self.movement = [[0, 1, 0, -1], [1, 0, -1, 0]]
        
    def makeBoard (self, firstBoard):
        board = []
        self.rowSize = len(firstBoard)
        self.colSize = len(firstBoard[0])
        for row in firstBoard:
            col = []
            for element in row:
                col.append(Cell(element))
            board.append(col)
        self.board = np.array(board)

    def printBoard (self):
        for row in self.board:
            for element in row:
                p = ''
                e = element.type
                if e == Cell.ZERO: p = '0'
                elif e == Cell.ONE: p = '1'
                elif e == Cell.TWO: p = '2'
                elif e == Cell.THREE: p = '3'
                elif e == Cell.FOUR: p = '4'
                elif e == Cell.ANY: p = 'A'
                elif e == Cell.WHITE: p = 'W'
                elif e == Cell.LAMP: p = 'B'
                elif e == Cell.LIT: p = 'L'
                elif e == Cell.COLLISION: p = 'C'
                elif e == Cell.FORBIDDEN: p = 'F'
                print (p, end=' ')
            print()
        print()
    
    def printAvailable (self):
        for row in self.board:
            for element in row:
                if element.type <= Cell.ANY:
                    print (element.type, element.available, element.checkAvailable(), element.countAvailable)

    def setForbidden (self):
        for i, row in enumerate (self.board):
                for j, element in enumerate (row):
                    if element.type == Cell.ZERO:
                        for k in range (4):
                            nextRow = i + self.movement[0][k]
                            nextCol = j + self.movement[1][k]
                            if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                                if self.board[nextRow][nextCol].type == Cell.WHITE: 
                                    self.board[nextRow][nextCol].setType(Cell.FORBIDDEN)
                    elif element.type <= Cell.FOUR and not element.checkAvailable():
                        for k in range (4):
                            nextRow = i + self.movement[0][k]
                            nextCol = j + self.movement[1][k]
                            if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                                if element.available[k] == Cell.AVAILABLE and self.board[nextRow][nextCol].type != Cell.LIT:
                                    self.board[nextRow][nextCol].setType(Cell.FORBIDDEN)

    def setAvailability (self):
        for i, row in enumerate (self.board):
                for j, element in enumerate (row):
                    if (element.type < Cell.ANY and element.type >= Cell.ZERO):
                        available = []
                        for k in range (4):
                            nextRow = i + self.movement[0][k]
                            nextCol = j + self.movement[1][k]
                            if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                                if self.board[nextRow][nextCol].type == Cell.WHITE: available.append(Cell.AVAILABLE)
                                elif self.board[nextRow][nextCol].type == Cell.LAMP: available.append(Cell.BULB_PLACED)
                                else: available.append(Cell.NOT_AVAILABLE)
                            else: available.append(Cell.NOT_AVAILABLE)
                        element.setAvailable(available)
    def preproc (self):
        while True:
            check = False
            for i, row in enumerate (self.board):
                for j, element in enumerate (row):
                    if (element.type <= Cell.FOUR and element.type > Cell.ZERO and element.checkAvailable() == True):
                        countWhite = 0
                        whitePosition = []
                        for k in range (4):
                            nextRow = i + self.movement[0][k]
                            nextCol = j + self.movement[1][k]
                            if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                                if self.board[nextRow][nextCol].type == Cell.WHITE:
                                    countWhite += 1
                                    whitePosition.append([nextRow, nextCol])
                        if countWhite == element.countAvailable:
                            check = True
                            for white in whitePosition: 
                                self.putSingleLamp(white[0], white[1])
                                self.setForbidden()
                                self.setAvailability()
                    elif (element.type == Cell.WHITE):
                        checkWhiteCenter = True
                        for k in range (4):
                            nextRow = i + self.movement[0][k]
                            nextCol = j + self.movement[1][k]
                            if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                                if self.board[nextRow][nextCol].type > Cell.ANY:
                                    checkWhiteCenter = False
                                    break
                        if checkWhiteCenter: 
                            self.putSingleLamp(i, j)
                            self.setForbidden()
                            self.setAvailability()
                            check = True
            if not check: break

    def preprocSecond(self):
        while True:
            check = False
            for i, row in enumerate (self.board):
                for j, cell in enumerate (row):
                    if (cell.type <= Cell.FOUR and cell.type > Cell.ZERO and cell.checkAvailable() == True):
                        countWhite = 0
                        whitePosition = []
                        for k in range (4):
                            nextRow = i + self.movement[0][k]
                            nextCol = j + self.movement[1][k]
                            if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                                if self.board[nextRow][nextCol].type == Cell.WHITE:
                                    countWhite += 1
                                    whitePosition.append([nextRow, nextCol])
                        if countWhite == cell.countAvailable:
                            check = True
                            for white in whitePosition: 
                                self.putSingleLamp(white[0], white[1])
                                self.setForbidden()
                                self.setAvailability()
                    elif (cell.type == Cell.FORBIDDEN or cell.type == Cell.WHITE):
                        rowPos = i
                        colPos = j
                        countWhite = 0
                        resRow = None
                        resCol = None
                        # check rightside
                        for k in range (colPos+1, self.colSize):
                            if (k < 0 or k >= self.colSize or self.board[rowPos][k].type <= Cell.ANY): break
                            if (self.board[rowPos][k].type == Cell.WHITE):
                                resRow = rowPos
                                resCol = k
                                countWhite += 1
                        # check leftside
                        for k in range (colPos-1, -1, -1):
                            if (k < 0 or k >= self.colSize or self.board[rowPos][k].type <= Cell.ANY): break
                            if (self.board[rowPos][k].type == Cell.WHITE):
                                resRow = rowPos
                                resCol = k
                                countWhite += 1
                        # check downside
                        for k in range (rowPos+1, self.rowSize):
                            if (k < 0 or k >= self.rowSize or self.board[k][colPos].type <= Cell.ANY): break
                            if (self.board[k][colPos].type == Cell.WHITE):
                                resRow = k
                                resCol = colPos
                                countWhite += 1
                        # check upside
                        for k in range (rowPos-1, -1, -1):
                            if (k < 0 or k >= self.rowSize or self.board[k][colPos].type <= Cell.ANY): break
                            if (self.board[k][colPos].type == Cell.WHITE):
                                resRow = k
                                resCol = colPos
                                countWhite += 1
                        if (countWhite == 1 and cell.type == Cell.FORBIDDEN):
                            check = True
                            self.putSingleLamp(resRow, resCol)
                            self.setForbidden()
                            self.setAvailability()
                        if (countWhite == 0 and cell.type == Cell.WHITE):
                            check = True
                            self.putSingleLamp(rowPos, colPos)
                            self.setForbidden()
                            self.setAvailability()
            if not check: break

    def lastPreproc (self):
        for i, row in enumerate (self.board):
            for j, cell in enumerate (row):
                if cell.type == Cell.WHITE:
                    rowPos = i
                    colPos = j
                    check = False
                    # check rightside
                    for k in range (colPos+1, self.colSize):
                        if (k < 0 or k >= self.colSize or self.board[rowPos][k].type <= Cell.ANY): break
                        if (self.board[rowPos][k].type == Cell.WHITE):
                            check = True
                            break
                    # check leftside
                    for k in range (colPos-1, -1, -1):
                        if (k < 0 or k >= self.colSize or self.board[rowPos][k].type <= Cell.ANY): break
                        if (self.board[rowPos][k].type == Cell.WHITE):
                            check = True
                            break
                    # check downside
                    for k in range (rowPos+1, self.rowSize):
                        if (k < 0 or k >= self.rowSize or self.board[k][colPos].type <= Cell.ANY): break
                        if (self.board[k][colPos].type == Cell.WHITE):
                            check = True
                            break
                    # check upside
                    for k in range (rowPos-1, -1, -1):
                        if (k < 0 or k >= self.rowSize or self.board[k][colPos].type <= Cell.ANY): break
                        if (self.board[k][colPos].type == Cell.WHITE):
                            check = True
                            break
                    if not check: 
                        self.putSingleLamp(rowPos, colPos)
                        self.setAvailability()
    
    def putSingleLamp (self, rowPos, colPos):
        if (rowPos < 0 or rowPos >= self.rowSize or colPos < 0 or colPos >= self.colSize): return
        if self.board[rowPos][colPos].type == Cell.LIT: self.board[rowPos][colPos].setType(Cell.COLLISION)
        elif self.board[rowPos][colPos].type == Cell.WHITE: self.board[rowPos][colPos].setType(Cell.LAMP)
        # lit rightside
        for i in range (colPos+1, self.colSize):
            if (i < 0 or i >= self.colSize): break
            if (self.board[rowPos][i].type <= Cell.ANY): break
            elif (self.board[rowPos][i].type == Cell.WHITE or self.board[rowPos][i].type == Cell.FORBIDDEN): self.board[rowPos][i].setType(Cell.LIT)
            elif self.board[rowPos][i].type == Cell.LAMP: self.board[rowPos][i].setType(Cell.COLLISION)
        # lit leftside
        for i in range (colPos-1, -1, -1):
            if (i < 0 or i >= self.colSize): break
            if (self.board[rowPos][i].type <= Cell.ANY): break
            elif (self.board[rowPos][i].type == Cell.WHITE or self.board[rowPos][i].type == Cell.FORBIDDEN): self.board[rowPos][i].setType(Cell.LIT)
            elif self.board[rowPos][i].type == Cell.LAMP: self.board[rowPos][i].setType(Cell.COLLISION)
        # lit downside
        for i in range (rowPos+1, self.rowSize):
            if (i < 0 or i >= self.rowSize): break
            if (self.board[i][colPos].type <= Cell.ANY): break
            elif (self.board[i][colPos].type == Cell.WHITE or self.board[i][colPos].type == Cell.FORBIDDEN): self.board[i][colPos].setType(Cell.LIT)
            elif self.board[i][colPos].type == Cell.LAMP: self.board[i][colPos].setType(Cell.COLLISION)
        # lit upside
        for i in range (rowPos-1, -1, -1):
            if (i < 0 or i >= self.rowSize): break
            if (self.board[i][colPos].type <= Cell.ANY): break
            elif (self.board[i][colPos].type == Cell.WHITE or self.board[i][colPos].type == Cell.FORBIDDEN): self.board[i][colPos].setType(Cell.LIT)
            elif self.board[i][colPos].type == Cell.LAMP: self.board[i][colPos].setType(Cell.COLLISION)
        

    def findBlackPosition (self):
        blackPosition = []
        for i, row in enumerate (self.board):
            for j, element in enumerate (row):
                if element.countAvailable < Cell.ANY and element.countAvailable > Cell.ZERO and element.checkAvailable() == True:
                    blackPosition.append([i, j])
        self.blackPosition = np.array(blackPosition)

    def findWhitePosition (self):
        whitePosition = []
        for i, row in enumerate (self.board):
            for j, element in enumerate (row):
                if element.type == Cell.WHITE:
                    check = True
                    for k in range (4):
                        nextRow = i + self.movement[0][k]
                        nextCol = j + self.movement[1][k]
                        if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                            if self.board[nextRow][nextCol].type <= Cell.FOUR: check = False
                    if check: whitePosition.append([i, j])
        self.whitePosition = np.array(whitePosition)

    def getRandomBlack (self):
        randomBlack = []
        for black in self.blackPosition:
            random = []
            rowPos = black[0]
            colPos = black[1]
            avail = self.board[rowPos][colPos].available
            if self.board[rowPos][colPos].countAvailable == Cell.ONE:
                for i in range (4): 
                    if avail[i] == Cell.AVAILABLE: random.append(i)
            elif self.board[rowPos][colPos].countAvailable == Cell.TWO:
                if avail[0] == Cell.AVAILABLE and avail[1] == Cell.AVAILABLE: random.append(0)
                if avail[1] == Cell.AVAILABLE and avail[2] == Cell.AVAILABLE: random.append(1)
                if avail[2] == Cell.AVAILABLE and avail[3] == Cell.AVAILABLE: random.append(2)
                if avail[0] == Cell.AVAILABLE and avail[3] == Cell.AVAILABLE: random.append(3)
                if avail[0] == Cell.AVAILABLE and avail[2] == Cell.AVAILABLE: random.append(4)
                if avail[1] == Cell.AVAILABLE and avail[3] == Cell.AVAILABLE: random.append(5)
            elif self.board[rowPos][colPos].countAvailable == Cell.THREE:
                if avail[0] == Cell.AVAILABLE and avail[1] == Cell.AVAILABLE and avail[2] == Cell.AVAILABLE: random.append(0)
                if avail[1] == Cell.AVAILABLE and avail[2] == Cell.AVAILABLE and avail[3] == Cell.AVAILABLE: random.append(0)
                if avail[0] == Cell.AVAILABLE and avail[2] == Cell.AVAILABLE and avail[3] == Cell.AVAILABLE: random.append(0)
                if avail[0] == Cell.AVAILABLE and avail[1] == Cell.AVAILABLE and avail[3] == Cell.AVAILABLE: random.append(0)
            elif self.board[rowPos][colPos].countAvailable == Cell.FOUR: random.append(0)
            randomBlack.append(random)
        return randomBlack
  
    def putBlackLamps (self, position):
        self.board = copy.deepcopy(self.original) # copy the original board back to board
        for i, black in enumerate (self.blackPosition): # for every black squares in blackPosition
            rowPos = black[0] # row position (int)
            colPos = black[1] # col position (int)
            element = self.board[rowPos][colPos].countAvailable # calculate the number of possible bulb placement around black
            if element == Cell.ONE:
                if position[i] == 0: self.putSingleLamp(rowPos, colPos+1)
                elif position[i] == 1: self.putSingleLamp(rowPos+1, colPos)
                elif position[i] == 2: self.putSingleLamp(rowPos, colPos-1)
                elif position[i] == 3: self.putSingleLamp(rowPos-1, colPos)
            elif element == Cell.TWO:
                if position[i] == 0:
                    self.putSingleLamp(rowPos, colPos+1)
                    self.putSingleLamp(rowPos+1, colPos)
                elif position[i] == 1:
                    self.putSingleLamp(rowPos+1, colPos)
                    self.putSingleLamp(rowPos, colPos-1)
                elif position[i] == 2:
                    self.putSingleLamp(rowPos, colPos-1)
                    self.putSingleLamp(rowPos-1, colPos)
                elif position[i] == 3:
                    self.putSingleLamp(rowPos-1, colPos)
                    self.putSingleLamp(rowPos, colPos+1)
                elif position[i] == 4:
                    self.putSingleLamp(rowPos, colPos+1)
                    self.putSingleLamp(rowPos, colPos-1)
                elif position[i] == 5:
                    self.putSingleLamp(rowPos+1, colPos)
                    self.putSingleLamp(rowPos-1, colPos)
            elif element == Cell.THREE:
                if position[i] == 0:
                    self.putSingleLamp(rowPos, colPos+1)
                    self.putSingleLamp(rowPos+1, colPos)
                    self.putSingleLamp(rowPos, colPos-1)
                elif position[i] == 1:
                    self.putSingleLamp(rowPos+1, colPos)
                    self.putSingleLamp(rowPos, colPos-1)
                    self.putSingleLamp(rowPos-1, colPos)
                elif position[i] == 2:
                    self.putSingleLamp(rowPos, colPos-1)
                    self.putSingleLamp(rowPos-1, colPos)
                    self.putSingleLamp(rowPos, colPos+1)
                elif position[i] == 3:
                    self.putSingleLamp(rowPos-1, colPos)
                    self.putSingleLamp(rowPos, colPos+1)
                    self.putSingleLamp(rowPos+1, colPos)
            elif element == Cell.FOUR:
                self.putSingleLamp(rowPos, colPos+1)
                self.putSingleLamp(rowPos+1, colPos)
                self.putSingleLamp(rowPos, colPos-1)
                self.putSingleLamp(rowPos-1, colPos)

    def putWhiteLamps (self, position):
        for i, white in enumerate (self.whitePosition):
            rowPos = white[0]
            colPos = white[1]
            if (position[i] == 1):
                self.putSingleLamp(rowPos, colPos)

    def saveBoard (self):
        self.original = copy.deepcopy(self.board)

    def updateFitness (self, punishment):
        collision = 0
        whiteTiles = 0
        blackLamp = 0
        centerWhite = 0
        endBlack = 0
        fitness = 0
        trapped = 0
        for i, row in enumerate (self.board):
            for j, element in enumerate (row):
                if element.type == Cell.WHITE or element.type == Cell.FORBIDDEN:
                    whiteTiles+=1
                    # find center white
                    check = True
                    for k in range (4):
                        nextRow = i + self.movement[0][k]
                        nextCol = j + self.movement[1][k]
                        if (nextRow >= 0 and nextCol >= 0 and nextRow < self.rowSize and nextCol < self.colSize):
                            if (self.board[nextRow][nextCol].type > Cell.ANY and self.board[nextRow][nextCol].type <= Cell.FORBIDDEN):
                                check = False
                                break
                    if check: centerWhite+=1
                    if element.type == Cell.FORBIDDEN:
                        rowPos = i
                        colPos = j
                        check = False
                        # check rightside
                        for k in range (colPos+1, self.colSize):
                            if (k < 0 or k >= self.colSize or self.board[rowPos][k].type <= Cell.ANY): break
                            if (self.board[rowPos][k].type == Cell.WHITE):
                                check = True
                                break
                        # check leftside
                        for k in range (colPos-1, -1, -1):
                            if (k < 0 or k >= self.colSize or self.board[rowPos][k].type <= Cell.ANY): break
                            if (self.board[rowPos][k].type == Cell.WHITE):
                                check = True
                                break
                        # check downside
                        for k in range (rowPos+1, self.rowSize):
                            if (k < 0 or k >= self.rowSize or self.board[k][colPos].type <= Cell.ANY): break
                            if (self.board[k][colPos].type == Cell.WHITE):
                                check = True
                                break
                        # check upside
                        for k in range (rowPos-1, -1, -1):
                            if (k < 0 or k >= self.rowSize or self.board[k][colPos].type <= Cell.ANY): break
                            if (self.board[k][colPos].type == Cell.WHITE):
                                check = True
                                break
                        if not check: trapped+=1
                elif element.type == Cell.COLLISION: collision+=1
                elif element.type <= Cell.FOUR:
                    if element.checkAvailable(): 
                        blackLamp+=1
                        # cek ujung
                        if ((i == 0 and (j == self.colSize-1 or j == 0)) or (i == self.rowSize-1 and (j == self.colSize-1 or j == 0))):
                            if element.type == Cell.TWO: endBlack+=1
                        # cek tepi
                        if (((i == 0 or i == self.rowSize-1) and (j < self.colSize-1 and j > 0)) or ((j == 0 or j == self.colSize-1) and (i < self.rowSize-1 and i > 0))):
                            if element.type == Cell.THREE: endBlack+=1
                
        fitness += (collision * punishment[0] + blackLamp * punishment[1] + whiteTiles * punishment[2] + endBlack * punishment[3] + centerWhite * punishment[4] + trapped * punishment[5])
        violation = [collision, blackLamp, whiteTiles, centerWhite, endBlack, trapped]
        return fitness, violation