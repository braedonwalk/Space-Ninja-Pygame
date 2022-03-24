#############
# imports
#############

from glob import glob
import cv2
import pygame
import random
import math

from sympy import sec

from HandDetector import HandDetector
from Planet import Planet
from Button import Button

################
# GLOBAL THINGS
################

# Define the size of the game window
WIDTH = 1200
HEIGHT = 800
# make the game window object
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# name the game window
pygame.display.set_caption("Produce Slicer")
# frame rate
FPS = 60
# INIT CURSOR VARS
CURSORWIDTH = 125
CURSORHEIGHT = 25
# all backgrounds
gameBackground = pygame.image.load(
    "Assets/Space1/Blue Nebula/Blue Nebula 1 - 1024x1024.png").convert()
mainBackground = pygame.image.load(
    "Assets/Space1/Starfields/Starfield 1 - 1024x1024.png").convert()
# scale to the size of the screen
gameBackground = pygame.transform.scale(gameBackground, (WIDTH, HEIGHT))
mainBackground = pygame.transform.scale(mainBackground, (WIDTH, HEIGHT))


# init assets
# KINVES
knifeList = {"Knife1": 1, "Knife2": 2, "Knife3": 4, "Knife4": 7, "Knife5": 8, "Knife6": 15, "Knife7": 20}
chosenKnife = knifeList["Knife4"]
knife = pygame.image.load("Assets/Knives/"+str(chosenKnife)+".png").convert_alpha()
knife = pygame.transform.rotate(knife, 90)
knife = pygame.transform.scale(knife, (CURSORWIDTH, CURSORHEIGHT))

# PLANETS
planetAssets = ["Assets/Planets/barren1.png", "Assets/Planets/barren2.png", "Assets/Planets/barren3.png", "Assets/Planets/barren4.png", "Assets/Planets/desert1.png", "Assets/Planets/desert2.png", "Assets/Planets/forest1.png", "Assets/Planets/forest2.png", "Assets/Planets/gas1.png", "Assets/Planets/gas2.png", "Assets/Planets/gas3.png", "Assets/Planets/gas4.png", "Assets/Planets/ice1.png", "Assets/Planets/lava1.png", "Assets/Planets/lava2.png", "Assets/Planets/lava3.png", "Assets/Planets/ocean1.png",
                "Assets/Planets/ocean2.png", "Assets/Planets/rocky1.png", "Assets/Planets/rocky2.png", "Assets/Planets/rocky3.png", "Assets/Planets/sun1.png", "Assets/Planets/sun2.png", "Assets/Planets/sun3.png", "Assets/Planets/sun4.png", "Assets/Planets/sun5.png", "Assets/Planets/sun6.png", "Assets/Planets/sun7.png", "Assets/Planets/tech1.png", "Assets/Planets/tech2.png", "Assets/Planets/tech3.png", "Assets/Planets/terran1.png", "Assets/Planets/terran2.png", "Assets/Planets/tundra1.png"]

# booleans for state machine
mainMenu = True
gameScreen = False
gameOver = False
gameWin = False

# initialize all fonts
pygame.font.init()

# Planet list
planetList = []
# INITIAL Planet AT START *FOR TESING*
# spawn Planet in random spot in the middle thrid of the right side of the screen
# planetList.append(Planet(WIDTH, random.randrange(
#     int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))
cutPlanetList = []  # for Planet that has been cut

# health
health = 3
# WE ARE NOT KEEPING MOST OF THIS FONT STUFF
healthColor = (255, 0, 0)  # red
healthFont = pygame.font.SysFont("Helvetica", 40)
healthObject = healthFont.render(str(health), True, healthColor)

screenCase = 0  # "switch case" for displaying the screen    #default is 0

# HOMESCREEN VARIABLES
# startButton = Button(WIDTH/2, HEIGHT - 50, 200, 50)
startButtonColor = (0, 120, 50)  # DARK GREEN
startButton = Button(startButtonColor, WIDTH/2, HEIGHT - 100, 50)  # COLOR, X, Y, RADIUS
# startButtonCenter = startButton.buttonRect.center = (startButton.r/2, startButton.r/2)

updateTime = True

################
# Function defs
################

# flips the screen to make more sense


def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)


def homeScreen():
    titleColor = (0, 0, 255)  # color of font
    titleFont = pygame.font.Font("SPACE.ttf", 75)  # initialize font
    startFont = pygame.font.Font("SPACE.ttf", 20)
    instructionFont = pygame.font.Font("SPACE.ttf", 20)

    titleObject = titleFont.render("Space Ninja", True, titleColor)  # set text to font
    titleObject_center = titleObject.get_rect(center=(WIDTH/2, HEIGHT/3))  # set the center point of the text
    startObject = startFont.render("Start", True, titleColor)
    startObject_center = startObject.get_rect(center=(WIDTH/2, startButton.y))  # set the center point of the text
    instructionText = "To begin, hover your pointer finger over the Start button."
    instructionObject = instructionFont.render(instructionText, True, titleColor)
    instructionObject_center = instructionObject.get_rect(center=(WIDTH/2, HEIGHT/2))

    WINDOW.blit(mainBackground, (0, 0))
    # pygame.draw.rect(WINDOW, startButtonColor, startButton.buttonRect, 3)
    startButton.update(WINDOW, 5)
    WINDOW.blit(titleObject, titleObject_center)  # blit text on screen
    WINDOW.blit(startObject, startObject_center)  # blit text on screen
    WINDOW.blit(instructionObject, instructionObject_center)
    # pygame.draw.rect()


def flipCoin():
    return random.choice([True, False])

def showKnife(_handDetector, _handPoint):
    # print(handDetector.landmarkDictionary[0])
    # [first hand][hand point][x coordinate]
    cursorX = (_handDetector.landmarkDictionary[0][_handPoint][0])
    # [first hand][hand point][y coordinate]
    cursorY = (_handDetector.landmarkDictionary[0][_handPoint][1])

    # mirror cursorX so it is not confusing
    cursorX = WIDTH - mapToNewRange(cursorX, 0, _handDetector.width, 0, WIDTH)
    # map cursorY to pygame window size
    cursorY = mapToNewRange(cursorY, 0, _handDetector.height, 0, HEIGHT)

    # define hitbox at hand point
    cursorRect = pygame.Rect(cursorX, cursorY, CURSORWIDTH, CURSORHEIGHT)
    # pygame.draw.rect(WINDOW, cursorColor, cursorRect)   #DRAW RECTANGLE
    WINDOW.blit(knife, (cursorX, cursorY))


#########
# main function
#########

def main():
    # use variables called from beginning of sketch
    global planetList
    global cutPlanetList
    global health
    global healthObject
    global screenCase

    # make a hand detector
    handDetector = HandDetector()

    # chosen hand point
    handPoint = 8  # THE TIP OF POINTER FINGER
    # handPoint = 19  #THE FIRST JOINT OF PINKIE

    # cursor vars
    cursorX = 0
    cursorY = 0
    cursorZ = 0
    cursorColor = (255, 120, 0)  # orange

    # make a clock object that will be used
    # to make the game run at a consistent framerate
    clock = pygame.time.Clock()
    # keeps track if pygame should keep running
    pygameIsRunning = True

    # while the opencv window is running and pygame screen is up
    while not handDetector.shouldClose and pygameIsRunning:
        # update the webcam feed and hand tracker calculations
        handDetector.update()

        # this makes it so this function can run at most FPS times/sec
        clock.tick(FPS)

        if screenCase == 0:
            homeScreen()  # display eveything on the main screen
            if len(handDetector.landmarkDictionary) > 0:
                showKnife(handDetector, handPoint)
            #     # print(handDetector.landmarkDictionary[0])
            #     # [first hand][hand point][x coordinate]
            #     cursorX = (handDetector.landmarkDictionary[0][handPoint][0])
            #     # [first hand][hand point][y coordinate]
            #     cursorY = (handDetector.landmarkDictionary[0][handPoint][1])

            #     # mirror cursorX so it is not confusing
            #     cursorX = WIDTH - mapToNewRange(cursorX, 0, handDetector.width, 0, WIDTH)
            #     # map cursorY to pygame window size
            #     cursorY = mapToNewRange(
            #         cursorY, 0, handDetector.height, 0, HEIGHT)

            #     # define hitbox at hand point
            #     cursorRect = pygame.Rect(cursorX, cursorY, CURSORWIDTH, CURSORHEIGHT)
            #     # pygame.draw.rect(WINDOW, cursorColor, cursorRect)   #DRAW RECTANGLE
            #     WINDOW.blit(knife, (cursorX, cursorY))

                # if hand icon
                if startButton.buttonRect.colliderect(cursorRect):
                    inButton = True
                    # print("ur dumb")
                else:
                    inButton = False

                global updateTime
                if inButton:
                    if(updateTime):
                        sec_in_startButton = pygame.time.get_ticks()
                        updateTime = False
                else:
                    sec_in_startButton = pygame.time.get_ticks()
                    updateTime = True

                currentTime = pygame.time.get_ticks()

                if currentTime - sec_in_startButton > 2000:
                    screenCase = 1
                    coinFlip = flipCoin()
                    if coinFlip == True:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(WIDTH, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))
                    else:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(0, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))

        if screenCase == 1:
            ###################
            # GAME SCREEN STUFF
            ###################
            # display game screen background
            WINDOW.blit(gameBackground, (0, 0))
            # display health
            WINDOW.blit(healthObject, (0, 0))

            # if there is at least one hand seen, then
            # do all this code
            if len(handDetector.landmarkDictionary) > 0:
                # print(handDetector.landmarkDictionary[0])
                # [first hand][hand point][x coordinate]
                cursorX = (handDetector.landmarkDictionary[0][handPoint][0])
                # [first hand][hand point][y coordinate]
                cursorY = (handDetector.landmarkDictionary[0][handPoint][1])
                # [first hand][hand point][z coordinate]
                cursorZ = (handDetector.landmarkDictionary[0][handPoint][2])

                # mirror cursorX so it is not confusing
                cursorX = WIDTH - mapToNewRange(cursorX, 0, handDetector.width, 0, WIDTH)
                # map cursorY to pygame window size
                cursorY = mapToNewRange(cursorY, 0, handDetector.height, 0, HEIGHT)

                ######################
                # Track collision between hand point and PLANETS
                ######################
                # define hitbox at hand point
                cursorRect = pygame.Rect(
                    cursorX, cursorY, CURSORWIDTH, CURSORHEIGHT)
                # pygame.draw.rect(WINDOW, cursorColor, cursorRect)   #DRAW RECTANGLE
                WINDOW.blit(knife, (cursorX, cursorY))

            # FOR ALL CUT PLANETS
            for aCutPlanet in cutPlanetList:
                # aCutPlanet.update(cutPlanetColor, WINDOW) #SHOW CUT PLANET ON SCREEN
                # aCutPlanet.move()                        #MOVE CUT PLANET
                pass

            # FOR ALL UNCUT PLANETS
            for aPlanet in planetList:
                # SHOW UNCUT PLANET ON SCREEN
                aPlanet.update(WINDOW)
                aPlanet.move(coinFlip)  # MOVE UNCUT PLANET
                if aPlanet.isCut == True:  # if the PLANET has been cut
                    # add PLANET to the cutPLANET list - remove planet from screen
                    cutPlanetList.append(aPlanet)
                    # remove the cut PLANET from the uncut PLANET list
                    planetList.remove(aPlanet)
                    healthObject = healthFont.render(
                        str(health), True, healthColor)  # display new health
                    
                    coinFlip = flipCoin()
                    if coinFlip == True:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(WIDTH, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))
                    else:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(0, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))
                    
                    # print(cutFruitList)
                if aPlanet.y > HEIGHT:  # if uncut Planet falls below the screen
                    planetList.remove(aPlanet)  # remove from list
                    health -= 1  # remove one life
                    healthObject = healthFont.render(
                        str(health), True, healthColor)  # display new health

                    coinFlip = flipCoin()
                    if coinFlip == True:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(WIDTH, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))
                    else:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(0, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))

                # check collison between rectangle and hand point
                # collide rectangle with rectangle
                if aPlanet.planetRect.colliderect(cursorRect):
                    aPlanet.isCut = True
                else:
                    planetColor = (255, 0, 255)
                # #collide rectangle with circle
                # if cursorRect.collidepoint(aPlanet.x, aPlanet.y):
                #     aPlanet.isCut = True
                # else:
                #     planetColor = (255,0,255)

        # for all the game events
        for event in pygame.event.get():

            # if the game is exited out of, then stop running the game
            if event.type == pygame.QUIT:
                pygameIsRunning = False

        # put code here that should be run every frame
        # of your game
        pygame.display.update()

    # Closes all the frames if pygameIsRunning is false
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
