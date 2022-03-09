# IMPORTS
import pygame


class Fruit:

    # CLASS VARS
    size = 70
    mass = 0.5
    xVel = 12
    yVel = -15    #test moving upwards for a little bit
    xAccel = 0  #no acceleration on x axis for now
    yAccel = 0  
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
        self.yAccel = self.mass    #set acceleration equal to mass
        self.yVel += self.yAccel    #increase velocity at rate of acceleration
        self.y += self.yVel      #move fruit down at the rate of velocity
        self.x -= self.xVel      #move fruit down at the rate of acceleration
        # print(self.fruitRect)

class CircleFruit:

    # CLASS VARS
    radius = 25
    mass = 0.5
    xVel = 12
    yVel = -15    #test moving upwards for a little bit
    xAccel = 0  #no acceleration on x axis for now
    yAccel = 0  
    isCut = False

    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.fruitSprite = pygame.sprite.Sprite()
        self.fruitSprite.image = pygame.Surface((80,80))
        self.rect = self.fruitSprite.image.get_rect()
        self.rect.center = (self.x, self.y)

    def render(self, _color, _window):
        pygame.draw.circle(self.fruitSprite.image, _color, (self.x, self.y), self.radius)
        # pygame.draw.circle(_window, _color, (self.x, self.y), self.radius)

    def move(self):
        self.yAccel = self.mass    #set acceleration equal to mass
        self.yVel += self.yAccel    #increase velocity at rate of acceleration
        self.y += self.yVel      #move fruit down at the rate of velocity
        self.x -= self.xVel      #move fruit down at the rate of acceleration
        # print(self.fruitRect)