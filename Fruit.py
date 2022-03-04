# IMPORTS
import pygame


class Fruit:

    # CLASS VARS
    size = 70
    speed = 5
    isCut = False

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.fruitRect = pygame.Rect(_x, _y, self.size, self.size)

    def render(self, _color, _window):
        self.fruitRect = pygame.Rect(self.x, self.y, self.size, self.size)
        pygame.draw.rect(_window, _color, self.fruitRect)
        # pygame.draw.circle(_window, _color, (self.x, self.y), self.size)

    def move(self):
        self.y += self.speed #move fruit down one pixel every frame
        print(self.fruitRect)
