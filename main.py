#############
# imports
#############

import cv2
import pygame
import random

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
pygame.display.set_caption("Space Ninja")
# frame rate
FPS = 60
# INIT CURSOR VARS
CURSORWIDTH = 125
CURSORHEIGHT = 25
# all backgrounds
mainBackground = pygame.image.load("Assets/Space/starField.png").convert()
knifeBackground = pygame.image.load("Assets/Space/greenNebula.png").convert()
gameBackground = pygame.image.load("Assets/Space/blueNebula.png").convert()
endBackground = pygame.image.load("Assets/Space/purpleNebula.png").convert()
# scale to the size of the screen
mainBackground = pygame.transform.scale(mainBackground, (WIDTH, HEIGHT))
knifeBackground = pygame.transform.scale(knifeBackground, (WIDTH, HEIGHT))
gameBackground = pygame.transform.scale(gameBackground, (WIDTH, HEIGHT))
endBackground = pygame.transform.scale(endBackground, (WIDTH, HEIGHT))

# init assets
# KINVES
knifeList = {"Knife1": 7, "Knife2": 1, "Knife3": 2, "Knife4": 4, "Knife5": 8, "Knife6": 15, "Knife7": 19, "Knife8": 20}
chosenKnife = knifeList["Knife1"]
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
cutPlanetList = []  # for Planet that has been cut

# health
health = 3
healthColor = (255, 0, 0)  # red
healthFont = pygame.font.Font("SPACE.ttf", 50)
healthObject = healthFont.render(str(health), True, healthColor)

# score
score = 0
# WE ARE NOT KEEPING MOST OF THIS FONT STUFF
scoreColor = (255, 100, 0)  # orange
scoreFont = pygame.font.Font("SPACE.ttf", 50)
scoreObject = scoreFont.render(str(score), True, scoreColor)

screenCase = 0  # "switch case" for displaying the screen    #default is 0

# HOMESCREEN VARIABLES
startButtonColor = (0, 120, 50)  # DARK GREEN
startButton = Button(startButtonColor, WIDTH/3, HEIGHT - 200, 75)  # COLOR, X, Y, RADIUS
knifeButtonColor = (255,255,255)  # WHITE
knifeButton = Button(knifeButtonColor, WIDTH-WIDTH/3, HEIGHT - 200, 75)  # COLOR, X, Y, RADIUS

updateTime = True
updateKnifeTime = True

#KNIFE SCREEN
knifeButtonColor = (255,255,255)
knifeButtonR = 75
topRowHeight = HEIGHT/2 - 50
bottomRowHeight = HEIGHT-HEIGHT/4-50
knifeButton1 = Button(knifeButtonColor, WIDTH/5, topRowHeight, knifeButtonR)
knifeButton2 = Button(knifeButtonColor, WIDTH/5*2, topRowHeight, knifeButtonR)
knifeButton3 = Button(knifeButtonColor, WIDTH-WIDTH/5*2, topRowHeight, knifeButtonR)
knifeButton4 = Button(knifeButtonColor, WIDTH-WIDTH/5, topRowHeight, knifeButtonR)
knifeButton5 = Button(knifeButtonColor, WIDTH/5, bottomRowHeight, knifeButtonR)
knifeButton6 = Button(knifeButtonColor, WIDTH/5*2, bottomRowHeight, knifeButtonR)
knifeButton7 = Button(knifeButtonColor, WIDTH-WIDTH/5*2, bottomRowHeight, knifeButtonR)
knifeButton8 = Button(knifeButtonColor, WIDTH-WIDTH/5, bottomRowHeight, knifeButtonR)
backButton = Button(knifeButtonColor, WIDTH/2, HEIGHT-100, 50)

knife1 = pygame.image.load("Assets/Knives/"+str(knifeList["Knife1"])+".png").convert_alpha()
knife1 = pygame.transform.rotate(knife1, 90)
knife1 = pygame.transform.scale(knife1, (CURSORWIDTH, CURSORHEIGHT))
knife1_center = knife1.get_rect(center=(knifeButton1.x, knifeButton1.y))
knife2 = pygame.image.load("Assets/Knives/"+str(knifeList["Knife2"])+".png").convert_alpha()
knife2 = pygame.transform.rotate(knife2, 90)
knife2 = pygame.transform.scale(knife2, (CURSORWIDTH, CURSORHEIGHT))
knife2_center = knife2.get_rect(center=(knifeButton2.x, knifeButton2.y))
knife3 = pygame.image.load("Assets/Knives/"+str(knifeList["Knife3"])+".png").convert_alpha()
knife3 = pygame.transform.rotate(knife3, 90)
knife3 = pygame.transform.scale(knife3, (CURSORWIDTH, CURSORHEIGHT))
knife3_center = knife3.get_rect(center=(knifeButton3.x, knifeButton3.y))
knife4 = pygame.image.load("Assets/Knives/"+str(knifeList["Knife4"])+".png").convert_alpha()
knife4 = pygame.transform.rotate(knife4, 90)
knife4 = pygame.transform.scale(knife4, (CURSORWIDTH, CURSORHEIGHT))
knife4_center = knife4.get_rect(center=(knifeButton4.x, knifeButton4.y))
knife5 = pygame.image.load("Assets/Knives/"+str(knifeList["Knife5"])+".png").convert_alpha()
knife5 = pygame.transform.rotate(knife5, 90)
knife5 = pygame.transform.scale(knife5, (CURSORWIDTH, CURSORHEIGHT))
knife5_center = knife5.get_rect(center=(knifeButton5.x, knifeButton5.y))
knife6 = pygame.image.load("Assets/Knives/"+str(knifeList["Knife6"])+".png").convert_alpha()
knife6 = pygame.transform.rotate(knife6, 90)
knife6 = pygame.transform.scale(knife6, (CURSORWIDTH, CURSORHEIGHT))
knife6_center = knife6.get_rect(center=(knifeButton6.x, knifeButton6.y))
knife7 = pygame.image.load("Assets/Knives/"+str(knifeList["Knife7"])+".png").convert_alpha()
knife7 = pygame.transform.rotate(knife7, 90)
knife7 = pygame.transform.scale(knife7, (CURSORWIDTH, CURSORHEIGHT))
knife7_center = knife7.get_rect(center=(knifeButton7.x, knifeButton7.y))
knife8 = pygame.image.load("Assets/Knives/"+str(knifeList["Knife8"])+".png").convert_alpha()
knife8 = pygame.transform.rotate(knife8, 90)
knife8 = pygame.transform.scale(knife8, (CURSORWIDTH, CURSORHEIGHT))
knife8_center = knife8.get_rect(center=(knifeButton8.x, knifeButton8.y))

updateKnife1 = True
updateKnife2 = True
updateKnife3 = True
updateKnife4 = True
updateKnife5 = True
updateKnife6 = True
updateKnife7 = True
updateKnife8 = True
updateBack = True

#END SCREEN
textHeight = HEIGHT - 250
mainButtonColor = (0,0,255) #BLUE
mainButtDimensions = (WIDTH-WIDTH/3, textHeight)
mainButton = Button(mainButtonColor, WIDTH-WIDTH/3, textHeight, 75)
playButtonColor = (0,120,50)    #DARK GREEN
playButtDimensions = (WIDTH/3, textHeight)
playButton = Button(playButtonColor, WIDTH/3, textHeight, 75)

updateMain = True
updatePlay = True

################
# Function defs
################

# flips the screen to make more sense


def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)

def knifeScreen():
    knifeColor = (255,255,255)
    knifeFont = pygame.font.Font("SPACE.ttf", 50)
    backFont = pygame.font.Font("SPACE.ttf", 25)

    knifeText = knifeFont.render("Choose Your Weapon", True, knifeColor)
    knifeText_center = knifeText.get_rect(center=(WIDTH/2, HEIGHT/4 - 50))
    backText = backFont.render("Back", True, knifeColor)
    backText_center = backText.get_rect(center=(backButton.x, backButton.y))

    WINDOW.blit(knifeBackground, (0,0))
    WINDOW.blit(knifeText, knifeText_center)
    knifeButton1.update(WINDOW, 5)
    knifeButton2.update(WINDOW, 5)
    knifeButton3.update(WINDOW, 5)
    knifeButton4.update(WINDOW, 5)
    knifeButton5.update(WINDOW, 5)
    knifeButton6.update(WINDOW, 5)
    knifeButton7.update(WINDOW, 5)
    knifeButton8.update(WINDOW, 5)
    
    WINDOW.blit(knife1, knife1_center)
    WINDOW.blit(knife2, knife2_center)
    WINDOW.blit(knife3, knife3_center)
    WINDOW.blit(knife4, knife4_center)
    WINDOW.blit(knife5, knife5_center)
    WINDOW.blit(knife6, knife6_center)
    WINDOW.blit(knife7, knife7_center)
    WINDOW.blit(knife8, knife8_center)

    backButton.update(WINDOW, 5)
    WINDOW.blit(backText, backText_center)

def homeScreen():
    titleColor = (50, 0, 255)  # color of font
    titleFont = pygame.font.Font("SPACE.ttf", 75)  # initialize font
    buttonFont = pygame.font.Font("SPACE.ttf", 25)
    instructionFont = pygame.font.Font("SPACE.ttf", 20)

    titleText = titleFont.render("Space Ninja", True, titleColor)  # set text to font
    titleText_center = titleText.get_rect(center=(WIDTH/2, HEIGHT/3))  # set the center point of the text
    instructionText = "To begin, hover your pointer finger over the Start button."
    instructionText = instructionFont.render(instructionText, True, titleColor)
    instructionText_center = instructionText.get_rect(center=(WIDTH/2, HEIGHT/2))
    startText = buttonFont.render("Start", True, titleColor)
    startText_center = startText.get_rect(center=(startButton.x, startButton.y))  # set the center point of the text
    knifeText = buttonFont.render("Weapon Select", True, (120,120,120))
    knifeText_center = knifeText.get_rect(center=(knifeButton.x, knifeButton.y))

    WINDOW.blit(mainBackground, (0, 0))
    # pygame.draw.rect(WINDOW, startButtonColor, startButton.buttonRect, 3)
    startButton.update(WINDOW, 5)
    knifeButton.update(WINDOW, 5)
    WINDOW.blit(titleText, titleText_center)  # blit text on screen
    WINDOW.blit(instructionText, instructionText_center)
    WINDOW.blit(startText, startText_center)  # blit text on screen
    WINDOW.blit(knifeText, knifeText_center)  # blit text on screen

def endScreen():
    endColor = (255,0,0)
    endFont = pygame.font.Font("SPACE.ttf", 40)
    mainFont = pygame.font.Font("SPACE.ttf", 20)
    playFont = pygame.font.Font("SPACE.ttf", 20)

    endText = endFont.render("You've Ninja-ed your last...", True, endColor)
    endText_center = endText.get_rect(center=(WIDTH/2, HEIGHT/3))
    mainText = mainFont.render("Main Menu", True, mainButtonColor)
    mainText_center = mainText.get_rect(center=(mainButtDimensions))
    playText = playFont.render("Play Again", True, playButtonColor)
    playText_center = playText.get_rect(center=(playButtDimensions))

    WINDOW.blit(endBackground, (0,0))   #display end background
    WINDOW.blit(endText, endText_center)
    #BUTTONS
    mainButton.update(WINDOW, 5)
    playButton.update(WINDOW, 5)
    WINDOW.blit(mainText, mainText_center)
    WINDOW.blit(playText, playText_center)

def flipCoin():
    return random.choice([True, False])

#########
# main function
#########

def main():
    # use variables called from beginning of sketch
    global planetList
    global cutPlanetList
    global health
    global healthObject
    global score
    global scoreObject
    global screenCase
    global knife
    global chosenKnife

    # make a hand detector
    handDetector = HandDetector()

    # chosen hand point
    handPoint = 8  # THE TIP OF POINTER FINGER
    # handPoint = 19  #THE FIRST JOINT OF PINKIE

    # cursor vars
    cursorX = 0
    cursorY = 0

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

        currentTime = pygame.time.get_ticks()
        
        if screenCase == -1:
            knifeScreen()
            if len(handDetector.landmarkDictionary) > 0:
                # print(handDetector.landmarkDictionary[0])
                # [first hand][hand point][x coordinate]
                cursorX = (handDetector.landmarkDictionary[0][handPoint][0])
                # [first hand][hand point][y coordinate]
                cursorY = (handDetector.landmarkDictionary[0][handPoint][1])

                # mirror cursorX so it is not confusing
                cursorX = WIDTH - mapToNewRange(cursorX, 0, handDetector.width, 0, WIDTH)
                # map cursorY to pygame window size
                cursorY = mapToNewRange(cursorY, 0, handDetector.height, 0, HEIGHT)

                # define hitbox at hand point
                cursorRect = pygame.Rect(cursorX, cursorY, CURSORWIDTH, CURSORHEIGHT)
                # pygame.draw.rect(WINDOW, cursorColor, cursorRect)   #DRAW RECTANGLE
                WINDOW.blit(knife, (cursorX, cursorY))

                #PRESSING KNIFE BUTTONS
                #KNIFE 1
                if knifeButton1.buttonRect.colliderect(cursorRect):
                    inKnifeButton1 = True
                else:
                    inKnifeButton1 = False

                global updateKnife1
                if inKnifeButton1:
                    if(updateKnife1):
                        sec_in_knifeButton1 = pygame.time.get_ticks()
                        updateKnife1 = False
                else:
                    sec_in_knifeButton1 = pygame.time.get_ticks()
                    updateKnife1 = True

                if currentTime - sec_in_knifeButton1 > 2000:
                    chosenKnife = knifeList["Knife1"]
                #KNIFE 2
                if knifeButton2.buttonRect.colliderect(cursorRect):
                    inKnifeButton2 = True
                else:
                    inKnifeButton2 = False

                global updateKnife2
                if inKnifeButton2:
                    if(updateKnife2):
                        sec_in_knifeButton2 = pygame.time.get_ticks()
                        updateKnife2 = False
                else:
                    sec_in_knifeButton2 = pygame.time.get_ticks()
                    updateKnife2 = True

                if currentTime - sec_in_knifeButton2 > 2000:
                    chosenKnife = knifeList["Knife2"]
                #KNIFE 3
                if knifeButton3.buttonRect.colliderect(cursorRect):
                    inKnifeButton3 = True
                else:
                    inKnifeButton3 = False

                global updateKnife3
                if inKnifeButton3:
                    if(updateKnife3):
                        sec_in_knifeButton3 = pygame.time.get_ticks()
                        updateKnife3 = False
                else:
                    sec_in_knifeButton3 = pygame.time.get_ticks()
                    updateKnife3 = True

                if currentTime - sec_in_knifeButton3 > 2000:
                    chosenKnife = knifeList["Knife3"]
                #KNIFE 4
                if knifeButton4.buttonRect.colliderect(cursorRect):
                    inKnifeButton4 = True
                else:
                    inKnifeButton4 = False

                global updateKnife4
                if inKnifeButton4:
                    if(updateKnife4):
                        sec_in_knifeButton4 = pygame.time.get_ticks()
                        updateKnife4 = False
                else:
                    sec_in_knifeButton4 = pygame.time.get_ticks()
                    updateKnife4 = True

                if currentTime - sec_in_knifeButton4 > 2000:
                    chosenKnife = knifeList["Knife4"]
                #KNIFE 5
                if knifeButton5.buttonRect.colliderect(cursorRect):
                    inKnifeButton5 = True
                else:
                    inKnifeButton5 = False

                global updateKnife5
                if inKnifeButton5:
                    if(updateKnife5):
                        sec_in_knifeButton5 = pygame.time.get_ticks()
                        updateKnife5 = False
                else:
                    sec_in_knifeButton5 = pygame.time.get_ticks()
                    updateKnife5 = True

                if currentTime - sec_in_knifeButton5 > 2000:
                    chosenKnife = knifeList["Knife5"]
                #KNIFE 6
                if knifeButton6.buttonRect.colliderect(cursorRect):
                    inKnifeButton6 = True
                else:
                    inKnifeButton6 = False

                global updateKnife6
                if inKnifeButton6:
                    if(updateKnife6):
                        sec_in_knifeButton6 = pygame.time.get_ticks()
                        updateKnife6 = False
                else:
                    sec_in_knifeButton6 = pygame.time.get_ticks()
                    updateKnife6 = True

                if currentTime - sec_in_knifeButton6 > 2000:
                    chosenKnife = knifeList["Knife6"]
                #KNIFE 7
                if knifeButton7.buttonRect.colliderect(cursorRect):
                    inKnifeButton7 = True
                else:
                    inKnifeButton7 = False

                global updateKnife7
                if inKnifeButton7:
                    if(updateKnife7):
                        sec_in_knifeButton7 = pygame.time.get_ticks()
                        updateKnife7 = False
                else:
                    sec_in_knifeButton7 = pygame.time.get_ticks()
                    updateKnife7 = True

                if currentTime - sec_in_knifeButton7 > 2000:
                    chosenKnife = knifeList["Knife7"]
                #KNIFE 8
                if knifeButton8.buttonRect.colliderect(cursorRect):
                    inKnifeButton8 = True
                else:
                    inKnifeButton8 = False

                global updateKnife8
                if inKnifeButton8:
                    if(updateKnife8):
                        sec_in_knifeButton8 = pygame.time.get_ticks()
                        updateKnife8 = False
                else:
                    sec_in_knifeButton8 = pygame.time.get_ticks()
                    updateKnife8 = True

                if currentTime - sec_in_knifeButton8 > 2000:
                    chosenKnife = knifeList["Knife8"]
                #BACK BUTTON
                if backButton.buttonRect.colliderect(cursorRect):
                    inBackButton = True
                else:
                    inBackButton = False

                global updateBack
                if inBackButton:
                    if(updateBack):
                        sec_in_backButton = pygame.time.get_ticks()
                        updateBack = False
                else:
                    sec_in_backButton = pygame.time.get_ticks()
                    updateBack = True

                if currentTime - sec_in_backButton > 2000:
                    screenCase = 0

                knife = pygame.image.load("Assets/Knives/"+str(chosenKnife)+".png").convert_alpha()
                knife = pygame.transform.rotate(knife, 90)
                knife = pygame.transform.scale(knife, (CURSORWIDTH, CURSORHEIGHT))
            else:
                cursorRect = pygame.Rect(0,0,0,0)

        ##### HOME SCREEN ##########
        if screenCase == 0:
            homeScreen()  # display eveything on the main screen
            if len(handDetector.landmarkDictionary) > 0:
                # print(handDetector.landmarkDictionary[0])
                # [first hand][hand point][x coordinate]
                cursorX = (handDetector.landmarkDictionary[0][handPoint][0])
                # [first hand][hand point][y coordinate]
                cursorY = (handDetector.landmarkDictionary[0][handPoint][1])

                # mirror cursorX so it is not confusing
                cursorX = WIDTH - mapToNewRange(cursorX, 0, handDetector.width, 0, WIDTH)
                # map cursorY to pygame window size
                cursorY = mapToNewRange(cursorY, 0, handDetector.height, 0, HEIGHT)

                # define hitbox at hand point
                cursorRect = pygame.Rect(cursorX, cursorY, CURSORWIDTH, CURSORHEIGHT)
                # pygame.draw.rect(WINDOW, cursorColor, cursorRect)   #DRAW RECTANGLE
                WINDOW.blit(knife, (cursorX, cursorY))

                #BUTTON PRESSING
                #START BUTTON
                if startButton.buttonRect.colliderect(cursorRect):
                    inButton = True
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

                if currentTime - sec_in_startButton > 2000:
                    screenCase = 1
                    coinFlip = flipCoin()
                    if coinFlip == True:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(WIDTH, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))
                    else:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(0, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))
                #KNIFE BUTTON
                if knifeButton.buttonRect.colliderect(cursorRect):
                    inKnifeButton = True
                else:
                    inKnifeButton = False

                global updateKnifeTime
                if inKnifeButton:
                    if(updateKnifeTime):
                        sec_in_knifeButton = pygame.time.get_ticks()
                        updateKnifeTime = False
                else:
                    sec_in_knifeButton = pygame.time.get_ticks()
                    updateKnifeTime = True

                if currentTime - sec_in_knifeButton > 2000:
                    screenCase = -1
            else:
                cursorRect = pygame.Rect(0,0,0,0)

        ####### GAME SCREEN ###########
        if screenCase == 1:
            ###################
            # GAME SCREEN STUFF
            ###################
            # display game screen background
            WINDOW.blit(gameBackground, (0, 0))
            # display health
            healthObject = healthFont.render("Health: " + str(health), True, healthColor)  # display new health
            WINDOW.blit(healthObject, (0, 0))
            # display score
            scoreObject = scoreFont.render("Score: " + str(score), True, scoreColor)  # display new health
            scoreRect = scoreObject.get_rect()
            scoreRect.right = WIDTH
            WINDOW.blit(scoreObject, scoreRect)

            # if there is at least one hand seen, then
            # do all this code
            if len(handDetector.landmarkDictionary) > 0:
                # print(handDetector.landmarkDictionary[0])
                # [first hand][hand point][x coordinate]
                cursorX = (handDetector.landmarkDictionary[0][handPoint][0])
                # [first hand][hand point][y coordinate]
                cursorY = (handDetector.landmarkDictionary[0][handPoint][1])

                # mirror cursorX so it is not confusing
                cursorX = WIDTH - mapToNewRange(cursorX, 0, handDetector.width, 0, WIDTH)
                # map cursorY to pygame window size
                cursorY = mapToNewRange(cursorY, 0, handDetector.height, 0, HEIGHT)

                ######################
                # Track collision between hand point and PLANETS
                ######################
                # define hitbox at hand point
                cursorRect = pygame.Rect(cursorX, cursorY, CURSORWIDTH, CURSORHEIGHT)
                # pygame.draw.rect(WINDOW, cursorColor, cursorRect)   #DRAW RECTANGLE
                WINDOW.blit(knife, (cursorX, cursorY))
            else:
                cursorRect = pygame.Rect(0,0,0,0)

            # FOR ALL CUT PLANETS
            for aCutPlanet in cutPlanetList:
                #DISPLAY EXPLOSION?
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
                    score += 1
                    
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
                    healthObject = healthFont.render(str(health), True, healthColor)  # display new health

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

            if health == 0:
                screenCase = 2

        ###### END SCREEN #############
        if screenCase == 2:
            ############
            #END SCREEN
            ############
            for planet in planetList:
                planetList.remove(planet)

            endScreen()
            if len(handDetector.landmarkDictionary) > 0:
                # print(handDetector.landmarkDictionary[0])
                # [first hand][hand point][x coordinate]
                cursorX = (handDetector.landmarkDictionary[0][handPoint][0])
                # [first hand][hand point][y coordinate]
                cursorY = (handDetector.landmarkDictionary[0][handPoint][1])

                # mirror cursorX so it is not confusing
                cursorX = WIDTH - mapToNewRange(cursorX, 0, handDetector.width, 0, WIDTH)
                # map cursorY to pygame window size
                cursorY = mapToNewRange(cursorY, 0, handDetector.height, 0, HEIGHT)

                # define hitbox at hand point
                cursorRect = pygame.Rect(cursorX, cursorY, CURSORWIDTH, CURSORHEIGHT)
                # pygame.draw.rect(WINDOW, cursorColor, cursorRect)   #DRAW RECTANGLE
                WINDOW.blit(knife, (cursorX, cursorY))

                #PRESSING BUTTONS
                #MAIN MENU BUTTON
                if mainButton.buttonRect.colliderect(cursorRect):
                    inMainButton = True
                else:
                    inMainButton = False

                global updateMain
                if inMainButton:
                    if(updateMain):
                        sec_in_mainButton = pygame.time.get_ticks()
                        updateMain = False
                else:
                    sec_in_mainButton = pygame.time.get_ticks()
                    updateMain = True

                if currentTime - sec_in_mainButton > 2000:
                    score = 0
                    health = 3
                    screenCase = 0

                #PLAY AGAIN BUTTON
                if playButton.buttonRect.colliderect(cursorRect):
                    inPlayButton = True
                else:
                    inPlayButton = False

                global updatePlay
                if inPlayButton:
                    if(updatePlay):
                        sec_in_playButton = pygame.time.get_ticks()
                        updatePlay = False
                else:
                    sec_in_playButton = pygame.time.get_ticks()
                    updatePlay = True

                if currentTime - sec_in_playButton > 2000:
                    score = 0
                    health = 3
                    screenCase = 1
                    coinFlip = flipCoin()
                    if coinFlip == True:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(WIDTH, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))
                    else:
                        # spawn Planet in random spot in the middle thrid of the right side of the screen
                        planetList.append(Planet(0, random.randrange(int(HEIGHT/3), int(HEIGHT-(HEIGHT/3))), random.choice(planetAssets)))

            else:
                cursorRect = pygame.Rect(0,0,0,0)

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
