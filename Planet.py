# IMPORTS
import random
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

    def __init__(self, _x, _y, _planetAsset):
        self.x = _x
        self.y = _y
        self.mass = random.uniform(0.4,0.7) #random mass between 0.4 and 0.7
        self.planetAsset = pygame.image.load(_planetAsset).convert_alpha()                    #load in image of planet
        self.planetAsset = pygame.transform.scale(self.planetAsset, (self.size, self.size))   #scale image to size of planet
        self.planetRect = pygame.Rect(_x, _y, self.size, self.size)

    def update(self, _window):
        self.planetRect = pygame.Rect(self.x, self.y, self.size, self.size) #update bounds of planet
        # self.planetAsset = pygame.image.load(_planet).convert_alpha()            #load in image of planet
        # self.planetAsset = pygame.transform.scale(self.planetAsset, (self.size, self.size))   #scale image to size of planet
        _window.blit(self.planetAsset, (self.x, self.y))                         #draw planet on screen
        # pygame.draw.rect(_window, _color, self.planetRect)                  #draw hit box
        # pygame.draw.circle(_window, _color, (self.x, self.y), self.radius)

    def move(self, _coinFlip):
        self.yAccel = self.mass    #set acceleration equal to mass
        self.yVel += self.yAccel    #increase velocity at rate of acceleration
        self.y += self.yVel      #move planet down at the rate of velocity
        if _coinFlip:
            self.x -= self.xVel      #move planet left at the rate of acceleration
        else:
            self.x += self.xVel      #move planet left at the rate of acceleration
        # print(self.planetRect)