import settings
import hardware
import audio
import leaderboard

import pygame
import sys

#initialize pygame
pygame.init()

#screen variables
screenHeight = 600
screenWidth = 800
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Mini Dance Dance Revolution")

#framerate setter
clock = pygame.time.Clock()

# 4. Main Game Loop
isGameRunning = True

while isGameRunning:
    #event handler (keyboard inputs and exiting the game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False

    #game logic tbd

    #rendering tbf

    #background color Lapis Blue
    screen.fill((22, 43, 118))

    #flip to display
    pygame.display.flip()

    #60 fps
    clock.tick(60)

#exiter
pygame.quit()
sys.exit()
