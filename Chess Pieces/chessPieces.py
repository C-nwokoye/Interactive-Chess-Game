

class Piece(object):
    def __init__(self, y, x, type, color):
        self.x = x
        self.y = y
        self.color = color
        self.type = type
        self.firstMove = True
    
    def move(self, newY, newX):
        # aka set position
        self.firstMove = False 
        self.x = newX
        self.y = newY
    
    def __str__(self):
        # color should either be 'b' for black or 'w' for white
        # type should be 'P' for pawn, 'R' for rook, 'Q' for queen, 'K' for king, 'N' for knight, or 'B' for bishop
        return str(self.color + self.type)
    
    def getColor(self):
        return self.color
    
    def getFirstMove(self):
        return self.firstMove
    
    def getType(self):
        return self.type
    
    def setType(self, newType):
        self.type = newType
    
    def getPosition(self):
        return (self.y, self.x)

