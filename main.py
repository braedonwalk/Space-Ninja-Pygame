#############
# imports
#############

import cv2, pygame, random, math

from HandDetector import HandDetector
from Fruit import Fruit, CircleFruit

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

#initialize all fonts
pygame.font.init()

#fruit list
fruitList = []
fruitList.append(CircleFruit(WIDTH, random.randrange(0,HEIGHT/2)))     #INITIAL FRUIT AT START *FOR TESING*
cutFruitList = []   #for fruit that has been cut

#health
health = 3
healthColor = (255,0,0) #red
healthFont = pygame.font.SysFont("Helvetica", 40)
healthObject = healthFont.render(str(health), True, healthColor)


################
# Function defs
################

# flips the screen to make more sense
def mapToNewRange(val, inputMin, inputMax, outputMin, outputMax):
    return outputMin + ((outputMax - outputMin) / (inputMax - inputMin)) * (val - inputMin)

#test function to collide with cirle hitbox
def collide_circle(circle1, circle2):
    radius1, radius2 = circle1.width/2, circle2.width/2
    dist = math.hypot(circle1.centerx-circle2.centerx, circle1.centery-circle2.centery)
    return dist < radius1+radius2

#########
# main function
#########

def main():
    #use variables called from beginning of sketch
    global fruitList
    global cutFruitList
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
    cursorWidth = 25
    cursorHeight = 25

    #fruit vars
    fruitColor = (255,0,255)    #pink
    cutFruitColor = (0,0,255)   #blue

    #test fruit object
    # aFruit = Fruit(WIDTH/2, 0)  #draw fruit rectangle at top of screen center 

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
        # fill the background with black
        WINDOW.fill(0)
        #display health
        WINDOW.blit(healthObject, (0, 0))

        # #FOR ALL CUT FRUIT
        # for aCutFruit in cutFruitList:
        #     aCutFruit.render(cutFruitColor, WINDOW) #SHOW CUT FRUIT ON SCREEN
        #     aCutFruit.move()                        #MOVE CUT FRUIT

        # #FOR ALL UNCUT FRUIT
        # for aFruit in fruitList:
        #     aFruit.render(fruitColor, WINDOW)       #SHOW UNCUT FRUIT ON SCREEN 
        #     aFruit.move()                           #MOVE UNCUT FRUIT
        #     if aFruit.isCut == True:                #if the fruit has been cut
        #         cutFruitList.append(aFruit)         #add fruit to the cutFruit list
        #         fruitList.remove(aFruit)            #remove the cut fruit from the uncut fruit list
        #         healthObject = healthFont.render(str(health), True, healthColor)    #display new health
        #         fruitList.append(Fruit(WIDTH, random.randrange(0,HEIGHT/2)))    #this is a test
        #         # print(cutFruitList)
        #     if aFruit.y > HEIGHT:                   #if uncut fruit falls below the screen
        #         fruitList.remove(aFruit)            #remove from list
        #         health -= 1                         #remove one life
        #         healthObject = healthFont.render(str(health), True, healthColor)    #display new health
        #         fruitList.append(Fruit(WIDTH, random.randrange(0,HEIGHT/2)))    #this is a test
        
        #CIRCLE FRUITTTTTTTTTTTTT
        #FOR ALL CUT FRUIT
        for aCutFruit in cutFruitList:
            aCutFruit.render(cutFruitColor, WINDOW) #SHOW CUT FRUIT ON SCREEN
            aCutFruit.move()                        #MOVE CUT FRUIT

        #FOR ALL UNCUT FRUIT
        for aFruit in fruitList:
            aFruit.render(fruitColor, WINDOW)       #SHOW UNCUT FRUIT ON SCREEN 
            aFruit.move()                           #MOVE UNCUT FRUIT
            if aFruit.isCut == True:                #if the fruit has been cut
                cutFruitList.append(aFruit)         #add fruit to the cutFruit list
                fruitList.remove(aFruit)            #remove the cut fruit from the uncut fruit list
                healthObject = healthFont.render(str(health), True, healthColor)    #display new health
                fruitList.append(CircleFruit(WIDTH, random.randrange(0,HEIGHT/2)))    #spawn new fruit on random spot on right sude of screen #this is a test
                # print(cutFruitList)
            if aFruit.y > HEIGHT:                   #if uncut fruit falls below the screen
                fruitList.remove(aFruit)            #remove from list
                health -= 1                         #remove one life
                healthObject = healthFont.render(str(health), True, healthColor)    #display new health
                fruitList.append(CircleFruit(WIDTH, random.randrange(0,HEIGHT/2)))  #spawn new fruit on random spot on right sude of screen 

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
            # draw rectangle at hand point 
            cursorRect = pygame.Rect(cursorX, cursorY, cursorWidth, cursorHeight)
            pygame.draw.rect(WINDOW, cursorColor, cursorRect)
            
            #check collison between rectangle and hand point
            # if aFruit.fruitRect.collidepoint(cursorX, cursorY):
            #     aFruit.isCut = True
            # else:
            #     fruitColor = (255,0,255)

            #check collision between circles


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
