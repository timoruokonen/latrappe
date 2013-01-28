import random

class Animal:

    def __init__(self, x=100, y=100, owner=None):
        self.x = x
        self.y = y
        self.owner = owner
        self.target = (random.randint(self.x, self.x + 50), random.randint(self.y, self.y + 50))

    def advance(self, time):
        self.moveToTarget()

    def moveToTarget(self):
        if self.x < self.target[0]:
            self.x += 1
        elif self.x > self.target[0]:
            self.x -= 1

        if self.y < self.target[1]:
            self.y += 1
        elif self.y > self.target[1]:
            self.y -= 1

        if (self.x == self.target[0]) and (self.y == self.target[1]):
            self.target = (random.randint(200, 300), random.randint(200, 300))

