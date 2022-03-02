#IMPORTS
import pygame

class Fruit:
    
    #CLASS VARS 
    size = 50;
    speed = 5;
    isCut = False;

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.fruitRect = pygame.Rect(_x,_y, self.size, self.size)

    def render(self, _window):
        pygame.draw.rect(_window, (255,0,255), self.fruitRect)


    def move(self):
        pass