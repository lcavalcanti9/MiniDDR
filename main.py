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

font = pygame.font.SysFont("helveticaneue", 30)

# Define the nine pad keys in the same three-row layout as the keyboard. #copilot1
padKeys = [("R", pygame.K_r), ("T", pygame.K_t), ("Y", pygame.K_y), ("F", pygame.K_f), ("G", pygame.K_g), ("H", pygame.K_h), ("V", pygame.K_v), ("B", pygame.K_b), ("N", pygame.K_n)]  #copilot1
keySize = 52  #copilot1
keyGap = 8  #copilot1
keyLeft = 24  #copilot1
keyTop = screenHeight - (3 * keySize + 2 * keyGap) - 74  #copilot1

isGameRunning = True

while isGameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False

    pressedKeys = pygame.key.get_pressed()  #copilot1
    
    #background color Lapis Blue
    screen.fill((22, 43, 118))
    
    # Draw the nine input pads in the keyboard's R T Y / F G H / V B N orientation. #copilot1
    for index, (label, keyCode) in enumerate(padKeys):  #copilot1
        row = index // 3  #copilot1
        column = index % 3  #copilot1
        keyRect = pygame.Rect(keyLeft + column * (keySize + keyGap), keyTop + row * (keySize + keyGap), keySize, keySize)  #copilot1
        keyColor = (70, 210, 120) if pressedKeys[keyCode] else (55, 65, 95)  #copilot1
        pygame.draw.rect(screen, keyColor, keyRect, border_radius=6)  #copilot1
        pygame.draw.rect(screen, (230, 230, 240), keyRect, 2, border_radius=6)  #copilot1
        keyText = font.render(label, True, (255, 255, 255))  #copilot1
        screen.blit(keyText, keyText.get_rect(center=keyRect.center))  #copilot1
    # Draw the thumb's space-bar input below the pad grid; it lights while held. #copilot1
    spaceRect = pygame.Rect(keyLeft, keyTop + 3 * (keySize + keyGap), 3 * keySize + 2 * keyGap, 42)  #copilot1
    spaceColor = (70, 210, 120) if pressedKeys[pygame.K_SPACE] else (55, 65, 95)  #copilot1
    pygame.draw.rect(screen, spaceColor, spaceRect, border_radius=6)  #copilot1
    pygame.draw.rect(screen, (230, 230, 240), spaceRect, 2, border_radius=6)  #copilot1
    spaceText = font.render("SPACE (THUMB)", True, (255, 255, 255))  #copilot1
    screen.blit(spaceText, spaceText.get_rect(center=spaceRect.center))  #copilot1
    
    #flip to display
    pygame.display.flip()

    #60 fps
    clock.tick(60)

#exiter
pygame.quit()
sys.exit()
