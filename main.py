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
laneKeys = [pygame.K_f, pygame.K_b, pygame.K_t, pygame.K_h]  #copilot2
laneTopX = [350, 383, 417, 450]  #copilot2
laneBottomX = [220, 340, 460, 580]  #copilot2
stringTopY = 75  #copilot2
stringBottomY = 490  #copilot2
targetRadius = 24  #copilot2
noteTravelBeats = 5.0  #copilot2
activePadKeys = {pygame.K_t, pygame.K_f, pygame.K_h, pygame.K_b}  #copilot2

isGameRunning = True

audio.start_playback()  #copilot2

while isGameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isGameRunning = False

    pressedKeys = pygame.key.get_pressed()  #copilot1
    
    #background color Lapis Blue
    screen.fill((22, 43, 118))
    
    # Draw four perspective guitar strings, targets, and notes. #copilot2
    beatNow = audio.current_beat()  #copilot2
    pygame.draw.polygon(screen, (37, 58, 135), [(350, stringTopY), (450, stringTopY), (650, stringBottomY), (150, stringBottomY)])  #copilot2
    for laneIndex in range(4):  #copilot2
        pygame.draw.line(screen, (245, 245, 255), (laneTopX[laneIndex], stringTopY), (laneBottomX[laneIndex], stringBottomY), 3)  #copilot2
        targetCenter = (laneBottomX[laneIndex], stringBottomY)  #copilot2
        pygame.draw.circle(screen, (245, 245, 255), targetCenter, targetRadius, 3)  #copilot2
        targetText = font.render(("F", "B", "T", "H")[laneIndex], True, (255, 255, 255))  #copilot2
        screen.blit(targetText, targetText.get_rect(center=targetCenter))  #copilot2
    for note in audio.get_visible_notes(noteTravelBeats):  #copilot2
        laneIndex = note["lane"] - 1  #copilot2
        progress = 1 - (note["beat"] - beatNow) / noteTravelBeats  #copilot2
        progress = max(0.0, min(1.0, progress))  #copilot2
        noteX = laneTopX[laneIndex] + (laneBottomX[laneIndex] - laneTopX[laneIndex]) * progress  #copilot2
        noteY = stringTopY + (stringBottomY - stringTopY) * progress  #copilot2
        noteRadius = int(9 + progress * 15)  #copilot2
        pygame.draw.circle(screen, (255, 205, 70), (int(noteX), int(noteY)), noteRadius)  #copilot2
        pygame.draw.circle(screen, (255, 255, 255), (int(noteX), int(noteY)), noteRadius, 2)  #copilot2
    
    # Draw active controls brightly and unused keys dimmed in the bottom-left HUD. #copilot2
    for index, (label, keyCode) in enumerate(padKeys):  #copilot2
        row = index // 3  #copilot2
        column = index % 3  #copilot2
        keyRect = pygame.Rect(keyLeft + column * (keySize + keyGap), keyTop + row * (keySize + keyGap), keySize, keySize)  #copilot2
        isActive = keyCode in activePadKeys  #copilot2
        keyColor = (70, 210, 120) if pressedKeys[keyCode] and isActive else ((55, 65, 95) if isActive else (32, 38, 57))  #copilot2
        pygame.draw.rect(screen, keyColor, keyRect, border_radius=6)  #copilot2
        pygame.draw.rect(screen, (230, 230, 240) if isActive else (80, 84, 98), keyRect, 2, border_radius=6)  #copilot2
        keyText = font.render(label, True, (255, 255, 255) if isActive else (105, 108, 120))  #copilot2
        screen.blit(keyText, keyText.get_rect(center=keyRect.center))  #copilot2
    spaceRect = pygame.Rect(keyLeft, keyTop + 3 * (keySize + keyGap), 3 * keySize + 2 * keyGap, 42)  #copilot2
    spaceColor = (70, 210, 120) if pressedKeys[pygame.K_SPACE] else (55, 65, 95)  #copilot2
    pygame.draw.rect(screen, spaceColor, spaceRect, border_radius=6)  #copilot2
    pygame.draw.rect(screen, (230, 230, 240), spaceRect, 2, border_radius=6)  #copilot2
    spaceText = font.render("SPACE (THUMB)", True, (255, 255, 255))  #copilot2
    screen.blit(spaceText, spaceText.get_rect(center=spaceRect.center))  #copilot2
    
    #flip to display
    pygame.display.flip()

    #60 fps
    clock.tick(60)

#exiter
pygame.quit()
sys.exit()
