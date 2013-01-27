class Player:

    def __init__(self):
        self.x = 200
        self.y = 200
        self.speed_x = 0
        self.speed_y = 0

    def advance(self, time):
        self.x += self.speed_x
        self.y += self.speed_y

    def move(self, dx, dy):
        self.speed_x = dx
        self.speed_y = dy



