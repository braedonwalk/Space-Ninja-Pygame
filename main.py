#############
# imports
#############

import cv2, pygame, random, math

from HandDetector import HandDetector
from Planet import Planet
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
#frame rate
FPS = 60
#INIT CURSOR VARS
CURSORWIDTH = 125
CURSORHEIGHT = 25
#background
background = pygame.image.load("Assets/Space1/Blue Nebula/Blue Nebula 1 - 1024x1024.png").convert()
#scale to the size of the screen
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

#init assets
knife = pygame.image.load("Assets/Knives/7.png").convert_alpha()
knife = pygame.transform.rotate(knife, 90)
knife = pygame.transform.scale(knife, (CURSORWIDTH, CURSORHEIGHT))

#booleans for state machine
mainMenu = True
gameScreen = False
gameOver = False
gameWin = False

#initialize all fonts
pygame.font.init()

#Planet list
planetList = []
#INITIAL Planet AT START *FOR TESING*
planetList.append(Planet(WIDTH, random.randrange(int(HEIGHT/3),int(HEIGHT-(HEIGHT/3)))))  #spawn Planet in random spot in the middle thrid of the right side of the screen
cutPlanetList = []   #for Planet that has been cut

#health
health = 3
#WE ARE NOT KEEPING MOST OF THIS FONT STUFF
healthColor = (255,0,0) #red
healthFont = pygame.font.SysFont("Helvetica", 40)   
healthObject = healthFont.render(str(health), True, healthColor)


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
    #use variables called from beginning of sketch
    global planetList
    global cutPlanetList
    global health
    global healthObject

    # make a hand detector
    handDetector = HandDetector()

    #chosen hand point
    handPoint = 8  #THE TIP OF POINTER FINGER
    # handPoint = 19  #THE FIRST JOINT OF PINKIE

    # cursor vars
    cursorX = 0
    cursorY = 0
    cursorZ = 0
    cursorColor = (255, 120, 0) #orange

    #Planet vars
    # fruitGroup = pygame.sprite.Group()
    #THIS WILL NOT STAY
    planetColor = (255,0,255)    #pink
    cutPlanetColor = (0,0,255)   #blue

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

        ###################
        #GAME SCREEN STUFF
        ###################
        # display game screen background
        WINDOW.blit(background, (0,0))
        #display health
        WINDOW.blit(healthObject, (0, 0))

        #FOR ALL CUT PLANETS
        for aCutPlanet in cutPlanetList:
            aCutPlanet.update(cutPlanetColor, WINDOW, knife) #SHOW CUT PLANET ON SCREEN
            aCutPlanet.move()                        #MOVE CUT PLANET

        #FOR ALL UNCUT PLANETS
        for aPlanet in planetList:
            aPlanet.update(planetColor, WINDOW, "Assets/Knives/7.png")       #SHOW UNCUT PLANET ON SCREEN 
            aPlanet.move()                           #MOVE UNCUT PLANET
            if aPlanet.isCut == True:                #if the PLANET has been cut
                cutPlanetList.append(aPlanet)         #add PLANET to the cutPLANET list
                planetList.remove(aPlanet)            #remove the cut PLANET from the uncut PLANET list
                healthObject = healthFont.render(str(health), True, healthColor)    #display new health
                planetList.append(Planet(WIDTH, random.randrange(int(HEIGHT/3),int(HEIGHT-(HEIGHT/3)))))  #spawn Planet in random spot in the middle thrid of the right side of the screen
                # print(cutFruitList)
            if aPlanet.y > HEIGHT:                   #if uncut Planet falls below the screen
                planetList.remove(aPlanet)            #remove from list
                health -= 1                         #remove one life
                healthObject = healthFont.render(str(health), True, healthColor)    #display new health
                planetList.append(Planet(WIDTH, random.randrange(int(HEIGHT/3),int(HEIGHT-(HEIGHT/3)))))  #spawn Planet in random spot in the middle thrid of the right side of the screen
        
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
            # draw rectangle at hand point 
            cursorRect = pygame.Rect(cursorX, cursorY, CURSORWIDTH, CURSORHEIGHT)
            pygame.draw.rect(WINDOW, cursorColor, cursorRect)   #DRAW RECTANGLE
            WINDOW.blit(knife, (cursorX, cursorY))

            
            # check collison between rectangle and hand point
            #collide rectangle with rectangle
            if aPlanet.planetRect.colliderect(cursorRect):
                aPlanet.isCut = True
            else:
                planetColor = (255,0,255)
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
