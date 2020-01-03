#!/usr/bin/python

import pygame
import math

black = [0, 0, 0]
red = [255, 0, 0]
gray = [127, 127, 127]
white = [255, 255, 255]
lightGray = [180, 180, 180]

screenWidth = 800
screenHeight = 800

worldWidth = float(100)
worldHeight = float(100)

offsetX = offsetY = 0
scaleX = screenWidth / float(worldWidth)
scaleY = screenHeight / float(worldHeight)

rect = pygame.Rect(-5, 5, 10, 10)

pygame.init()
pygame.font.init()
pygame.display.set_caption("Rectangle")
font = pygame.font.Font("freesansbold.ttf", 20)
screen = pygame.display.set_mode((screenWidth, screenHeight))


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
    x = x - offsetX
    y = y - offsetY

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

    screen.fill(white)
    pygame.draw.rect(screen, red, translateRect(rect))
    pygame.draw.circle(screen, black, translate(0, 0), 5)
    pygame.display.update()


################################################################################
#
# main loop
#
################################################################################
running = True
pygame.key.set_repeat(75, 50)
while running:
    event = pygame.event.wait()
    # print('event',event)
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            running = False
        if event.key == pygame.K_s:
            rect.move_ip(0, -1)
        if event.key == pygame.K_w:
            rect.move_ip(0, 1)
        if event.key == pygame.K_a:
            rect.move_ip(-1, 0)
        if event.key == pygame.K_d:
            rect.move_ip(1, 0)
        if event.key == pygame.K_UP:
            offsetY = offsetY + 1
        if event.key == pygame.K_DOWN:
            offsetY = offsetY - 1
        if event.key == pygame.K_LEFT:
            offsetX = offsetX + 1
        if event.key == pygame.K_RIGHT:
            offsetX = offsetX - 1
        if event.key == pygame.K_r:
            offsetX = offsetY = 0
            rect = pygame.Rect(-5, 5, 10, 10)

    render()

pygame.quit()
