#############
# imports
#############

import cv2
import pygame

from HandDetector import HandDetector

################
# GLOBAL THINGS
################

# Define the size of the game window
WIDTH = 1200
HEIGHT = 800
# make the game window object
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
# name the game window
pygame.display.set_caption("Best game")

################
# Funciton defs
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

    # cursor vars
    cursorX = 0
    cursorY = 0
    cursorZ = 0
    cursorColor = (255, 120, 0)

    # keeps track of whether hand is open or closed
    handIsOpen = True

    # rectangle object
    aRect = pygame.Rect(300, 300, 400, 200)
    rectColor = (255,0,255)

    # while the opencv window is running and pygame screen is up
    while not handDetector.shouldClose and pygameIsRunning:
        # update the webcam feed and hand tracker calculations
        handDetector.update()

        # fill the background
        WINDOW.fill(0)

        

        #display rectangle on screen
        pygame.draw.rect(WINDOW, rectColor, aRect)

        # if there is at least one hand seen, then
        # do all this code
        if len(handDetector.landmarkDictionary) > 0:
            # print(handDetector.landmarkDictionary[0])
            # [first hand][hand point][x coordinate]
            cursorX = (handDetector.landmarkDictionary[0][9][0])
            # [first hand][hand point][y coordinate]
            cursorY = (handDetector.landmarkDictionary[0][9][1])
            # [first hand][hand point][z coordinate]
            cursorZ = (handDetector.landmarkDictionary[0][9][2])

            # mirror cursorX so it is not confusing
            cursorX = WIDTH - mapToNewRange(cursorX, 0, 640, 0, WIDTH)
            # map cursorY to pygame window size
            cursorY = mapToNewRange(cursorY, 0, 480, 0, HEIGHT)

            ######################
            # Track whether the hand is open or closed
            ######################
            if handDetector.landmarkDictionary[0][12][1] < handDetector.landmarkDictionary[0][9][1]:
                handIsOpen = True
                cursorColor = (0, 255, 255)
            else:
                handIsOpen = False
                cursorColor = (255, 120, 0)

            #check collison between rectangle and hand point
            if aRect.collidepoint(cursorX, cursorY):
                rectColor = (255,0,0)
            else:
                rectColor = (255,0,255)

            # draw circle at point 9
            pygame.draw.circle(WINDOW, cursorColor, (cursorX, cursorY), 50)

            print(handIsOpen)

        # for all the game events
        for event in pygame.event.get():
            # if the game is exited out of, then stop running the game
            if event.type == pygame.QUIT:
                pygameIsRunning = False

        # put code here that should be run every frame
        # of your game
        pygame.display.update()

    # Closes all the frames
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
