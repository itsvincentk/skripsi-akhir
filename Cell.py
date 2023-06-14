class Cell:
    WHITE = 6
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    ANY = 5
    LAMP = 7
    LIT = 8
    COLLISION = 9
    FORBIDDEN = 10
    AVAILABLE = 'AVAILABLE'
    NOT_AVAILABLE = 'NOT_AVAILABLE'
    BULB_PLACED = 'BULB_PLACED'

    def __init__(self, number) -> None:
        self.type = number
        self.available = [None, None, None, None]
        self.countAvailable = self.type
        
    def setAvailable (self, available):
        self.available = available
        self.checkAvailable()
    
    def setType (self, newType):
        self.type = newType

    def checkAvailable (self):
        self.countAvailable = self.type
        for i in range (4):
            if self.available[i] == Cell.BULB_PLACED:
                self.countAvailable -= 1
        if self.countAvailable == 0: return False
        else: return True