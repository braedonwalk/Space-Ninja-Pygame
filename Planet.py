# IMPORTS
import pygame


class Planet:

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
        self.planetRect = pygame.Rect(_x, _y, self.size, self.size)

    def update(self, _color, _window, _planet):
        self.planetRect = pygame.Rect(self.x, self.y, self.size, self.size)
        planetAsset = pygame.image.load(_planet).convert_alpha()
        planetAsset = pygame.transform.scale(planetAsset, (self.size, self.size))
        _window.blit(planetAsset, (self.x, self.y))
        pygame.draw.rect(_window, _color, self.planetRect)
        # pygame.draw.circle(_window, _color, (self.x, self.y), self.radius)

    def move(self):
        self.yAccel = self.mass    #set acceleration equal to mass
        self.yVel += self.yAccel    #increase velocity at rate of acceleration
        self.y += self.yVel      #move planet down at the rate of velocity
        self.x -= self.xVel      #move planet down at the rate of acceleration
        # print(self.planetRect)