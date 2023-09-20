#Needed for game to run, in theory we could make character be a child of object

class Object:
    def __init__(self, x, y, width, height, health):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health

