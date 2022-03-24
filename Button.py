import pygame

class Button:

    def __init__(self, _color, _x, _y, _r):
        self.color = _color
        self.x = _x
        self.y = _y
        self.r = _r

        # self.buttonCenter = (_x - _r, _y - _y)
        self.buttonRect = pygame.Rect(_x - _r, _y - _r, _r*2, _r*2)               #hitbox
        # self.buttonCenter = self.buttonRect.center(_x-_r, _y-_r)
        # pygame.draw.circle(_window, _color, (_x-_r, _y-_r), _r)   #draw the circle for button

    def update(self, _window):
        pygame.draw.circle(_window, self.color, (self.x , self.y ), self.r, 3)   #draw the circle for button
