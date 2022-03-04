#############
# imports
#############

import cv2
import pygame

from HandDetector import HandDetector
from Fruit import Fruit

################
# GLOBAL THINGS
################

# Define the size of the game window
WIDTH = 1200
HEIGHT = 800
# make the game window object
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# name the game window
pygame.display.set_caption("Fruit Ninja")

#fruit List
fruitList = []
fruitList.append(Fruit(WIDTH/2, 0))

################
# Function defs
################

# flips the screen to make more sense
def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)

#########
# main function
#########

def main():
    # make a hand detector
    handDetector = HandDetector()

    # keeps track if pygame should keep running
    pygameIsRunning = True

    #chosen hand point
    handPoint = 19  #THE FIRST JOINT ON THE PINKIE

    # cursor vars
    cursorX = 0
    cursorY = 0
    cursorZ = 0
    cursorColor = (255, 120, 0)
    cursorRadius = 25

    #fruit vars
    fruitColor = (255,0,255)

    #test fruit object
    aFruit = Fruit(WIDTH/2, 0)  #draw fruit rectangle at top of screen center 
    # aFruitRect = pygame.Rect(300, 300, 400, 200)

    # while the opencv window is running and pygame screen is up
    while not handDetector.shouldClose and pygameIsRunning:
        # update the webcam feed and hand tracker calculations
        handDetector.update()
        
        # pygame.draw.rect(WINDOW, rectColor, aFruitRect)   #test rectangle
        
        # fill the background
        WINDOW.fill(0)
        #display test Fruit
        aFruit.render(fruitColor, WINDOW)
        # print("rendering")
        
        #move the fruit down the screen
        aFruit.move()

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
            # Track collision between hand point and fruit
            ######################

            #check collison between rectangle and hand point
            if aFruit.fruitRect.collidepoint(cursorX, cursorY):
                fruitColor = (255,0,0)
            else:
                fruitColor = (255,0,255)

            # draw circle at hand point 
            pygame.draw.circle(WINDOW, cursorColor, (cursorX, cursorY), cursorRadius)


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
