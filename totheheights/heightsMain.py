import pygame, random, sys
from pygame.locals import *
import time
##
## A simple platform jumping game
## Basic code borrowed from Paul Makl
## Physics code derived from http://www.rodedev.com/tutorials/gamephysics/
## Author: Kyle Dybdal
## Version: Fall 2013
##
WINDOWWIDTH = 420
WINDOWHEIGHT = 600
TEXTCOLOR = (40, 40, 40)
BACKGROUNDCOLOR = (230, 230, 230)
FPS = 50
GRAVITY = 1
TILESIZE = 30
# quit the game
def terminate():
    pygame.quit()
    sys.exit()

    
def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

#draws text
def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

#draw the bottom row  
def drawRow():
    i = 7
    j = 7
    while i >= 0:
        windowSurface.blit(tileImage1, bottomRow[i])
        windowSurface.blit(tileImage1, bottomRow[j])
        if landed:      # if the player just landed, play the animation
            pygame.time.delay(25)
            pygame.display.update()
        j += 1
        i -= 1

def drawPlat():
    for p in platforms:
        if p[1]:
            p[0].move_ip(tileSpeed, 0)
            windowSurface.blit(platSize(), p[0])
        if p[0].right + tileSpeed >= WINDOWWIDTH:
            p[1] = False
        if not p[1]:
            p[0].move_ip(-tileSpeed, 0)
            windowSurface.blit(platSize(), p[0])
        if p[0].left + tileSpeed <= 0:
            p[1] = True
                
def isInBounds():
    if playerRect.left > platforms[0][0].left + TILESIZE:
        if playerRect.right < platforms[1][0].right + TILESIZE:
            return True
    return False

def nextPlat():
        return [pygame.Rect((random.randint(0,WINDOWWIDTH-size*TILESIZE),-50,size*TILESIZE,TILESIZE)), True]

def platSize():
    if size == 5:
        return tileImage5
    elif size == 4:
        return tileImage4
    elif size == 3:
        return tileImage3
    elif size == 2:
        return tileImage2
    else:
        return tileImage1
    
    
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
windowSurface.fill(BACKGROUNDCOLOR)
pygame.display.set_caption('To the Heights!')
#pygame.mouse.set_visible(False)

#load fonts
scoreFont = pygame.font.SysFont('helvetica', 28)
titleFont = pygame.font.SysFont('helvetica', 48)

#load images
playerImage = pygame.image.load('grizz.png')
playerImage = pygame.transform.scale(playerImage, (20, 40))
playerRect = playerImage.get_rect()
playerRect[1] -= 2

tileImage1 = pygame.image.load('tile1.jpg')
tileRect1 = tileImage1.get_rect()
tileImage2 = pygame.image.load('tile2.jpg')
tileRect2 = tileImage2.get_rect()
tileImage3 = pygame.image.load('tile3.jpg')
tileRect3 = tileImage3.get_rect()
tileImage4 = pygame.image.load('tile4.jpg')
tileRect4 = tileImage4.get_rect()
tileImage5 = pygame.image.load('tile5.jpg')
tileRect5 = tileImage5.get_rect()

backgroundImage = pygame.image.load('background.jpg')
backgroundRect = backgroundImage.get_rect()

#draw start menu
drawText('To the Heights!', titleFont, windowSurface, (WINDOWWIDTH/5), (WINDOWHEIGHT/3))
drawText('Press a key to start.', titleFont, windowSurface, (WINDOWWIDTH/5) - 30, (WINDOWHEIGHT/3) + 50)
pygame.display.update()
waitForPlayerToPressKey()

# fill an array wil all the tiles of the bottom row    
bottomRow = []
for x in range(0,15):
    bottomRow.append(pygame.Rect(x*TILESIZE,WINDOWHEIGHT-TILESIZE, TILESIZE, TILESIZE))

platforms = [None, None, None]
   
topScore = 0
# main game loop
while True:
    score = 0
    jumped = False
    grounded = True
    landed = False   
    jumpSpeed = 0
    scrollSpeed = 10
    tileSpeed = 4
    size = 5
    maxy = 600
    x = 0
    y = -(backgroundRect.bottom - WINDOWHEIGHT) 
    print backgroundRect.bottom
    scrolling = False
    tileRect1.topleft = (0, WINDOWHEIGHT-30)
    playerRect.topleft = (WINDOWWIDTH / 2, tileRect1.topleft[1]-38)
    # playable game loop
    while True:
        if not scrolling:
            #windowSurface.fill(BACKGROUNDCOLOR)
            windowSurface.blit(backgroundImage, (x,y))
            for event in pygame.event.get(): 
                    if event.type == QUIT:
                        terminate()
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:    #space is jump
                            if grounded:
                                jumped = True
                                jumpSpeed = -20
                    if event.type == KEYUP:
                        if event.key == K_ESCAPE:
                                terminate()
            if not platforms[0]:
                platforms[0] = ([pygame.Rect((random.randint(0,WINDOWWIDTH-size*TILESIZE),370,size*TILESIZE,TILESIZE)), True])
                platforms[1] = ([pygame.Rect((random.randint(0,WINDOWWIDTH-size*TILESIZE),160,size*TILESIZE,TILESIZE)), True])
                platforms[2] = ([pygame.Rect((random.randint(0,WINDOWWIDTH-size*TILESIZE),-50,size*TILESIZE,TILESIZE)), True])
            if jumped:          # adjust vertical speed due to gravity
                if playerRect.bottom + jumpSpeed != (platforms[0][0].top +10):
                    grounded = False
                    playerRect.move_ip(0, jumpSpeed)
                    jumpSpeed += GRAVITY
                    #drawPlat()
                    #print playerRect.bottom - jumpSpeed - platforms[0][0].top
                if jumpSpeed > 0 and playerRect.bottom-jumpSpeed  < platforms[0][0].top and playerRect.colliderect(platforms[0][0]):
                    jumped = False
                    grounded = True
                    landed = True
                    scrolling = True
                    score += 1
            drawPlat()
            if grounded and not scrolling:
                drawRow()   
            if score > topScore:
                topScore = score
            drawText('Score: %s' % (score), scoreFont, windowSurface, 10, 10)
            drawText('Top Score: %s' % (topScore), scoreFont, windowSurface, 10, 40)
            windowSurface.blit(playerImage, playerRect)
            pygame.display.update()
            if playerRect.top > WINDOWHEIGHT:
                break
            mainClock.tick(FPS)
        else:
            #windowSurface.fill(BACKGROUNDCOLOR)
            windowSurface.blit(backgroundImage, (x,y))
            y += 1
            tileRect1.topleft = playerRect.bottomleft
            playerRect.move_ip(0, scrollSpeed)
            tileRect1.move_ip(0, scrollSpeed)
            platforms[1][0].move_ip(0, scrollSpeed)
            platforms[2][0].move_ip(0, scrollSpeed)
            windowSurface.blit(playerImage, playerRect)
            windowSurface.blit(tileImage1, tileRect1)
            windowSurface.blit(platSize(), platforms[1][0])
            windowSurface.blit(platSize(), platforms[2][0])
            drawText('Score: %s' % (score), scoreFont, windowSurface, 10, 10)
            drawText('Top Score: %s' % (topScore), scoreFont, windowSurface, 10, 40)
            pygame.display.update()
            mainClock.tick(FPS)
            if tileRect1.bottom >= WINDOWHEIGHT:
                platforms[0] = platforms[1]
                platforms[0][0].top = 370
                platforms[1] = platforms[2]
                platforms[1][0].top = 160
                platforms[2] = nextPlat()
                drawRow()
                landed = False
                scrolling = False
            
        
    drawText('GAME OVER', titleFont, windowSurface, (WINDOWWIDTH / 5), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', titleFont, windowSurface, (WINDOWWIDTH / 5) - 30, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()
