#!/usr/bin/python

import pygame

black = [0, 0, 0]
white = [255, 255, 255]


def init():
    global lander
    global offsetX, offsetY
    global scaleX, scaleY
    global previousVelocity
    global landerHeight

    offsetX = 0
    offsetY = -worldHeight / 2
    scaleX = screenWidth / float(worldWidth)
    scaleY = screenHeight / float(worldHeight)

    landerHeight = worldHeight

    previousVelocity = float(0)
    lander = pygame.Rect(-5, landerHeight, 10, 10)


screenWidth = 800
screenHeight = 800

worldWidth = float(200)
worldHeight = float(200)

gravity = -9.81  # gravity in msec

init()
pygame.init()
pygame.font.init()
pygame.display.set_caption("Lander")
font = pygame.font.Font("freesansbold.ttf", 20)
screen = pygame.display.set_mode((screenWidth, screenHeight))

previousTime = pygame.time.get_ticks() / 1000


################################################################################
#
# translate world coordinates to screen coordinates
#
################################################################################
def translateRect(rect):

    topleft = translate(rect.left, rect.top)
    newRect = pygame.Rect(topleft, (rect.width * scaleX, rect.height * scaleY))
    return newRect


def translate(x, y):

    # translate
    x = x + offsetX
    y = y + offsetY

    # scale
    x = x * scaleX
    y = y * scaleY

    # transform to screen coordinates
    x = screenWidth / 2 + x
    y = screenHeight / 2 - y

    return int(x), int(y)


################################################################################
#
# render screen
#
################################################################################
def render():
    global previousTime
    global previousVelocity
    global landerHeight

    currentTime = pygame.time.get_ticks() / 1000
    deltaTime = currentTime - previousTime
    #print("current",currentTime,"diff",deltaTime)
    previousTime = currentTime

    velocity = previousVelocity + gravity * deltaTime
    distance = previousVelocity * deltaTime + gravity * deltaTime * deltaTime / 2
    landerHeight = landerHeight + distance

    #print("v0",previousVelocity,"v",velocity,"s",distance,"h",landerHeight)

    previousVelocity = velocity

    lander.y = landerHeight

    screen.fill(black)
    pygame.draw.rect(screen, white, translateRect(lander))
    pygame.display.update()


################################################################################
#
# main loop
#
################################################################################
init()
running = True
pygame.key.set_repeat(75, 50)
while running:
    for event in pygame.event.get():
        # print('event',event)
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_s:
                lander.move_ip(0, -1)
            if event.key == pygame.K_w:
                lander.move_ip(0, 1)
            if event.key == pygame.K_a:
                lander.move_ip(-1, 0)
            if event.key == pygame.K_d:
                lander.move_ip(1, 0)
            if event.key == pygame.K_r:
                init()

    render()

    if lander.y - lander.height < 0:
        running = False

pygame.quit()
