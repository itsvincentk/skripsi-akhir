class Wolf:
    def __init__(self, board) -> None:
        self.board = board
    
    def updateBlackPosition (self, newPosition):
        self.board.putBlackLamps(newPosition)
        self.blackPosition = newPosition
        self.board.setAvailability()

    def updateWhitePosition (self, newPosition):
        self.board.putWhiteLamps(newPosition)
        self.whitePosition = newPosition

    def updateFitness (self, punishment):
        self.fitness, self.violation = self.board.updateFitness(punishment)
        return self.fitness