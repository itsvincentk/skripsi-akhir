import numpy as np
import random as rand
from Wolf import Wolf
from Board import Board
from Cell import Cell
import copy

class Game:
    def __init__(self, seed, population, punishment, epoch, rank, preproc) -> None:
        rand.seed(seed)
        np.random.seed(seed)
        self.population = population
        self.punishment = punishment
        self.epoch = epoch
        self.rank = rank
        self.preproc = preproc
        self.tempBoard2 = None


    def play (self, playBoard, tiles, actions):
        self.board = Board(playBoard)
        self.board.setForbidden()
        self.board.setAvailability()
        self.tempBoard = copy.deepcopy(self.board).board
        fitness = 0
        if self.preproc: 
            self.board.preproc()
            self.board.setForbidden()
            self.board.setAvailability()
            self.board.preprocSecond()
            self.board.setForbidden()
            self.board.setAvailability()
            fitness = self.board.updateFitness(self.punishment)[0]
            self.clickBoard(tiles, actions, self.board.board, fitness)
        if fitness == 0: return
        firstResult = self.firstGWO()
        firstResult.sort(key = lambda wolf : wolf.fitness)
        max = 2**31 - 1
        ans = None
        for wolf in firstResult:
            if self.preproc:
                wolf.board.preprocSecond()
                wolf.board.setForbidden()
                wolf.board.setAvailability()
                fitness = wolf.board.updateFitness(self.punishment)[0]
                self.clickBoard(tiles, actions, wolf.board.board, fitness)
                if fitness == 0: return
            res = self.secondGWO(wolf)
            if self.preproc:
                res.board.lastPreproc()
                res.updateFitness(self.punishment)
            fitness = res.fitness
            self.clickBoard(tiles, actions, res.board.board, fitness)
            if fitness == 0: return
            if res.fitness < max:
                max = res.fitness
                ans = res
            if max == 0: 
                break
        self.clickBoard(tiles, actions, ans.board.board, fitness)

    def experiment (self, firstBoard):
        self.board = Board(firstBoard)
        self.board.setForbidden()
        self.board.setAvailability()
        ans = None
        if self.preproc: 
            self.board.preproc()
            self.board.setForbidden()
            self.board.setAvailability()
            self.board.preprocSecond()
            self.board.setForbidden()
            self.board.setAvailability()
            ans = Wolf(self.board)
            if ans.updateFitness(self.punishment) == 0: return ans
        firstResult = self.firstGWO()
        firstResult.sort(key = lambda wolf : wolf.fitness)
        max = 2**31 - 1
        for wolf in firstResult:
            if self.preproc:
                wolf.board.preprocSecond()
                wolf.board.setForbidden()
                wolf.board.setAvailability()
                if wolf.updateFitness(self.punishment) == 0: return wolf
            if not self.checkSame(wolf.board.board): continue
            wolf.updateFitness(self.punishment)
            print(wolf.fitness, wolf.violation)
            res = self.secondGWO(wolf)
            if self.preproc:
                res.board.lastPreproc()
                res.updateFitness(self.punishment)
            if res.fitness == 0: return res
            if res.fitness < max:
                max = res.fitness
                ans = copy.deepcopy(res)
        return ans

    def firstGWO (self):
        population = []
        self.board.findBlackPosition()
        randomBlack = self.board.getRandomBlack()
        if len(randomBlack) == 0: 
            wolf = Wolf(self.board)
            wolf.updateFitness(self.punishment)
            return [wolf]
        max = 2**31 - 1
        best = ''
        for _ in range (self.population): population.append(Wolf(copy.deepcopy(self.board)))
        for wolf in population:
            initPosition = []
            for r in randomBlack:
                initPosition.append(rand.choice(r))
            initPosition = np.array(initPosition)
            wolf.board.saveBoard()
            wolf.updateBlackPosition(initPosition)
            wolf.updateFitness(self.punishment)
            if wolf.fitness < max:
                max = wolf.fitness
                best = copy.deepcopy(wolf)
        population.sort(key = lambda wolf : wolf.fitness)
        alpha = population[0]
        beta = population[1]
        delta = population[2]
        a = 2
        for i in range (self.epoch):
            for wolf in population:
                a = 2 - (i/self.epoch)*2
                thisPosition = wolf.blackPosition
                dimension = len(randomBlack)
                A1 = 2 * a * np.random.sample(size=dimension) - a
                A2 = 2 * a * np.random.sample(size=dimension) - a
                A3 = 2 * a * np.random.sample(size=dimension) - a
                C1 = 2 * np.random.sample(size=dimension) 
                C2 = 2 * np.random.sample(size=dimension) 
                C3 = 2 * np.random.sample(size=dimension) 
                X1 = alpha.blackPosition - A1 * abs(C1 * alpha.blackPosition - thisPosition)
                X2 = beta.blackPosition - A2 * abs(C2 * beta.blackPosition - thisPosition)
                X3 = delta.blackPosition - A3 * abs(C3 * delta.blackPosition - thisPosition)
                newPosition = (X1 + X2 + X3) / 3.0
                newPosition = np.where(newPosition < 0, -newPosition, newPosition)
                randomBlackSizes = []
                for r in randomBlack: randomBlackSizes.append(len(r))
                newPosition = np.round(newPosition).astype(int)
                newPosition %= randomBlackSizes
                for i, r in enumerate (randomBlack):
                    newPosition[i] = r[newPosition[i]]
                wolf.updateBlackPosition(newPosition)
                wolf.updateFitness(self.punishment)
                if wolf.fitness < max:
                    max = wolf.fitness
                    best = copy.deepcopy(wolf)
            population.sort(key = lambda wolf : wolf.fitness)
            alpha = population[0]
            beta = population[1]
            delta = population[2]
        result = self.roulette(population)
        result.insert(0, best)
        return result
    
    def secondGWO (self, wolf):
        firstWolf = copy.deepcopy(wolf)
        population = []
        max = 2**31 - 1
        best = ''
        firstWolf.board.findWhitePosition()
        for _ in range (self.population): population.append(copy.deepcopy(firstWolf))
        for wolf in population:
            initPosition = np.random.randint(2, size=len(firstWolf.board.whitePosition))
            wolf.board.saveBoard()
            wolf.updateWhitePosition(initPosition)
            wolf.updateFitness(self.punishment)
            if wolf.fitness < max:
                if wolf.fitness == 0: return wolf
                max = wolf.fitness
                best = copy.deepcopy(wolf)
        population.sort(key = lambda wolf : wolf.fitness)
        alpha = population[0]
        beta = population[1]
        delta = population[2]
        a = 2
        for i in range (self.epoch):
            for wolf in population:
                a = 2 - (i/self.epoch)*2
                thisPosition = wolf.whitePosition
                dimension = len(thisPosition)
                A1 = 2 * a * np.random.sample(size=dimension) - a
                A2 = 2 * a * np.random.sample(size=dimension) - a
                A3 = 2 * a * np.random.sample(size=dimension) - a
                C1 = 2 * np.random.sample(size=dimension) 
                C2 = 2 * np.random.sample(size=dimension) 
                C3 = 2 * np.random.sample(size=dimension) 
                X1 = alpha.whitePosition - A1 * abs(C1 * alpha.whitePosition - thisPosition)
                X2 = beta.whitePosition - A2 * abs(C2 * beta.whitePosition - thisPosition)
                X3 = delta.whitePosition - A3 * abs(C3 * delta.whitePosition - thisPosition)
                newPosition = (X1 + X2 + X3) / 3.0
                newPosition = np.where(newPosition < 0, -newPosition, newPosition)
                newPosition = np.round(newPosition).astype(int)
                newPosition %= 2
                wolf.updateWhitePosition(newPosition)
                wolf.updateFitness(self.punishment)
                if wolf.fitness < max:
                    if wolf.fitness == 0: return wolf
                    max = wolf.fitness
                    best = copy.deepcopy(wolf)
            population.sort(key = lambda wolf : wolf.fitness)
            alpha = population[0]
            beta = population[1]
            delta = population[2]
        return best
    
    def roulette (self, population): # Involves roulette wheel with rank selection
        result = []
        size = int (self.population*self.rank)
        for _ in range (size):
            probabilities = []
            totalFitness = sum(wolf.fitness for wolf in population)
            for wolf in population:
                probabilities.append(wolf.fitness/totalFitness)
            spin = rand.uniform(0,1)
            accumulatedProb = 0
            for i, prob in enumerate(probabilities):
                accumulatedProb += prob
                if accumulatedProb >= spin:
                    if population[i].violation[0] == 0 and population[i].violation[1] == 0 and population[i].violation[3] == 0 and population[i].violation[4] == 0 and population[i].violation[5] == 0:
                        result.append(population[i])
                    population.pop(i)
                    break
        return result

    def clickBoard (self, tiles, actions, board, fitness):
        i = 1
        for rowTemp, rowBoard in zip(self.tempBoard, board):
            for cellTemp, cellBoard in zip(rowTemp, rowBoard):
                if (cellTemp.type == Cell.LAMP and cellBoard.type != Cell.LAMP) or (cellTemp.type != Cell.LAMP and cellBoard.type == Cell.LAMP):
                    tiles[i].click()
                if (fitness > 0):
                    if (cellTemp.type == Cell.FORBIDDEN and cellBoard.type != Cell.FORBIDDEN) or (cellTemp.type != Cell.FORBIDDEN and cellBoard.type == Cell.FORBIDDEN):
                        actions.context_click(tiles[i]).perform()
                i+=1
        self.tempBoard = copy.deepcopy(board)

    def checkSame (self, board):
        if self.tempBoard2 is None:
            self.tempBoard2 = copy.deepcopy(board)
            return True
        for rowTemp, rowBoard in zip(self.tempBoard2, board):
            for cellTemp, cellBoard in zip(rowTemp, rowBoard):
                if cellTemp.type != cellBoard.type:
                    self.tempBoard2 = copy.deepcopy(board)
                    return True
        self.tempBoard2 = copy.deepcopy(board)
        return False
    