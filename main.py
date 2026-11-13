import settings  #copilot1
import hardware  #copilot1
import audio  #copilot1
import leaderboard  #copilot1
import pygame  #copilot1
import sys  #copilot1
#copilot1
pygame.init()  #copilot1
#copilot1
screenHeight = 600  #copilot1
screenWidth = 800  #copilot1
screen = pygame.display.set_mode((screenWidth, screenHeight))  #copilot1
pygame.display.set_caption("Mini Dance Dance Revolution")  #copilot1
clock = pygame.time.Clock()  #copilot1
font = pygame.font.Font(None, 30)  #copilot1
#copilot1
# Define the nine pad keys in the same three-row layout as the keyboard. #copilot1
padKeys = [("R", pygame.K_r), ("T", pygame.K_t), ("Y", pygame.K_y), ("F", pygame.K_f), ("G", pygame.K_g), ("H", pygame.K_h), ("V", pygame.K_v), ("B", pygame.K_b), ("N", pygame.K_n)]  #copilot1
keySize = 52  #copilot1
keyGap = 8  #copilot1
keyLeft = 24  #copilot1
keyTop = screenHeight - (3 * keySize + 2 * keyGap) - 74  #copilot1
#copilot1
isGameRunning = True  #copilot1
while isGameRunning:  #copilot1
    for event in pygame.event.get():  #copilot1
        if event.type == pygame.QUIT:  #copilot1
            isGameRunning = False  #copilot1
    #copilot1
    pressedKeys = pygame.key.get_pressed()  #copilot1
    screen.fill((22, 43, 118))  #copilot1
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
    pygame.display.flip()  #copilot1
    clock.tick(60)  #copilot1
pygame.quit()  #copilot1
sys.exit()  #copilot1
