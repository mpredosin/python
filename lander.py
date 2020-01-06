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


screenWidth = 1200
screenHeight = 720

worldWidth = float(screenWidth / 2)
worldHeight = float(screenHeight / 2)

gravity = -5  # moon gravity
thrust = -gravity * 3

currentThrust = 0.0

init()
pygame.init()
pygame.font.init()
pygame.display.set_caption("Lander")
font = pygame.font.Font("freesansbold.ttf", 20)
fontLineSize = font.get_linesize() / scaleY
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

    acceleration = gravity + currentThrust
    velocity = previousVelocity + acceleration * deltaTime
    distance = previousVelocity * deltaTime + acceleration * deltaTime * deltaTime / 2
    landerHeight = landerHeight + distance

    #print("v0",previousVelocity,"v",velocity,"s",distance,"h",landerHeight)

    previousVelocity = velocity

    lander.y = landerHeight

    screen.fill(black)

    leftMargin = 100
    altitudeStr = "Altitude: " + str(lander.y - lander.height)
    altitudeText = font.render(altitudeStr, True, white)
    screen.blit(altitudeText,
                translate(worldWidth / 2 - leftMargin, worldHeight))

    horizontalSpeedStr = "Horizontal Speed: " + str(int(round(0.0)))
    horizontalSpeedText = font.render(horizontalSpeedStr, True, white)
    screen.blit(
        horizontalSpeedText,
        translate(worldWidth / 2 - leftMargin, worldHeight - fontLineSize))

    verticalSpeedStr = "Vertical Speed: " + str(int(round(velocity)))
    verticalSpeedText = font.render(verticalSpeedStr, True, white)
    screen.blit(
        verticalSpeedText,
        translate(worldWidth / 2 - leftMargin, worldHeight - fontLineSize * 2))

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
                currentThrust = thrust
            if event.key == pygame.K_r:
                init()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                currentThrust = 0.0

    render()

    if lander.y - lander.height < 0:
        running = False

pygame.quit()
