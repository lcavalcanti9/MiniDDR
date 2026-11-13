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
smallFont = pygame.font.SysFont("helveticaneue", 12)  #copilot3
menuFont = pygame.font.SysFont("helveticaneue", 42)  #copilot3
scoreFont = pygame.font.SysFont("helveticaneue", 28)  #copilot3
canvas = pygame.Surface((screenWidth, screenHeight))  #copilot3
# Define the nine pad keys in the same three-row layout as the keyboard. #copilot1
padKeys = [("R", pygame.K_r), ("T", pygame.K_t), ("Y", pygame.K_y), ("F", pygame.K_f), ("G", pygame.K_g), ("H", pygame.K_h), ("V", pygame.K_v), ("B", pygame.K_b), ("N", pygame.K_n)]  #copilot1
keySize = 42  #copilot1 #copilot3
keyGap = 6  #copilot1 #copilot3
keyLeft = 24  #copilot1
keyTop = screenHeight - 24 - (3 * keySize + 3 * keyGap + 34)  #copilot1 #copilot3
laneKeys = [pygame.K_f, pygame.K_b, pygame.K_t, pygame.K_h]  #copilot2
laneTopX = [350, 383, 417, 450]  #copilot2
laneBottomX = [220, 340, 460, 580]  #copilot2
stringTopY = 75  #copilot2
stringBottomY = 490  #copilot2
targetRadius = 24  #copilot2
noteTravelBeats = 5.0  #copilot2
activePadKeys = {pygame.K_t, pygame.K_f, pygame.K_h, pygame.K_b}  #copilot2
laneLabels = ("F", "B", "T", "H")  #copilot3
laneArrows = ("left", "down", "up", "right")  #copilot3
isGameRunning = True  #copilot3
selectedSong = 0  #copilot3
songNames = audio.get_song_names()  #copilot3
scene = "selection"  #copilot3
fadeAlpha = 0  #copilot3
score = 0  #copilot3
scoredNotes = set()  #copilot3
shakePower = 0.0  #copilot3
waitingForNotes = True  #copilot3

while isGameRunning:  #copilot3
    justPressed = set()  #copilot3
    for event in pygame.event.get():  #copilot3
        if event.type == pygame.QUIT:  #copilot3
            isGameRunning = False  #copilot3
        elif event.type == pygame.KEYDOWN:  #copilot3
            justPressed.add(event.key)  #copilot3
            if event.key in activePadKeys:  #copilot3
                shakePower = min(1.35, shakePower + 0.14)  #copilot3
            if scene == "selection" and event.key == pygame.K_t:  #copilot3
                selectedSong = (selectedSong - 1) % len(songNames)  #copilot3
                audio.select_song(selectedSong)  #copilot3
            elif scene == "selection" and event.key == pygame.K_b:  #copilot3
                selectedSong = (selectedSong + 1) % len(songNames)  #copilot3
                audio.select_song(selectedSong)  #copilot3
            elif scene == "selection" and event.key == pygame.K_h and pygame.key.get_pressed()[pygame.K_SPACE]:  #copilot3
                audio.select_song(selectedSong)  #copilot3
                audio.start_playback()  #copilot3
                scene = "fade"  #copilot3
                fadeAlpha = 255  #copilot3
            elif scene == "playing" and event.key in laneKeys:  #copilot3
                beatNow = audio.current_beat()  #copilot3
                matching = [(abs(note["beat"] - beatNow), index, note) for index, note in enumerate(audio.get_visible_notes(noteTravelBeats)) if note["lane"] == laneKeys.index(event.key) + 1 and (index, note["beat"], note["lane"]) not in scoredNotes]  #copilot3
                if matching:  #copilot3
                    timingError, noteIndex, hitNote = min(matching, key=lambda item: item[0])  #copilot3
                    if timingError <= 0.5:  #copilot3
                        award = max(1, int(200 * (1 - timingError / 0.5)))  #copilot3
                        score += award  #copilot3
                        scoredNotes.add((noteIndex, hitNote["beat"], hitNote["lane"]))  #copilot3
    pressedKeys = pygame.key.get_pressed()  #copilot1
    if scene == "fade":  #copilot3
        fadeAlpha = max(0, fadeAlpha - 9)  #copilot3
        if fadeAlpha == 0:  #copilot3
            scene = "playing"  #copilot3
    if scene == "playing" and waitingForNotes and pressedKeys[pygame.K_f] and pressedKeys[pygame.K_h]:  #copilot3
        waitingForNotes = False  #copilot3
    shakePower = max(0.0, shakePower - 0.035)  #copilot3
    shakeX = int((pygame.time.get_ticks() // 17 % 3 - 1) * shakePower)  #copilot3
    shakeY = int((pygame.time.get_ticks() // 23 % 3 - 1) * shakePower)  #copilot3
    canvas.fill((22, 43, 118))  #copilot3
    if scene == "selection":  #copilot3
        title = menuFont.render("SONG SELECTION", True, (255, 255, 255))  #copilot3
        canvas.blit(title, title.get_rect(center=(screenWidth // 2, 145)))  #copilot3
        instruction = font.render("T / B to choose    H + SPACE to play", True, (210, 220, 245))  #copilot3
        canvas.blit(instruction, instruction.get_rect(center=(screenWidth // 2, 215)))  #copilot3
        for songIndex, songName in enumerate(songNames):  #copilot3
            songColor = (255, 220, 90) if songIndex == selectedSong else (180, 195, 225)  #copilot3
            songText = font.render((">  " if songIndex == selectedSong else "    ") + songName, True, songColor)  #copilot3
            canvas.blit(songText, songText.get_rect(center=(screenWidth // 2, 300 + songIndex * 52)))  #copilot3
    else:  #copilot3
        beatNow = audio.current_beat()  #copilot3
        pygame.draw.polygon(canvas, (37, 58, 135), [(350, stringTopY), (450, stringTopY), (650, stringBottomY), (150, stringBottomY)])  #copilot3
        for laneIndex in range(4):  #copilot3
            laneActive = pressedKeys[laneKeys[laneIndex]]  #copilot3
            targetCenter = (laneBottomX[laneIndex], stringBottomY)  #copilot3
            pygame.draw.line(canvas, (245, 245, 255), (laneTopX[laneIndex], stringTopY), targetCenter, 3)  #copilot3
            pygame.draw.circle(canvas, (75, 225, 135) if laneActive else (65, 80, 145), targetCenter, targetRadius)  #copilot3
            pygame.draw.circle(canvas, (245, 245, 255), targetCenter, targetRadius, 2)  #copilot3
            arrowColor = (255, 255, 255) if laneActive else (215, 225, 250)  #copilot3
            cx, cy = targetCenter  #copilot3
            if laneArrows[laneIndex] == "left":  #copilot3
                arrowPoints = [(cx - 15, cy), (cx + 11, cy - 14), (cx + 11, cy + 14)]  #copilot3
            elif laneArrows[laneIndex] == "right":  #copilot3
                arrowPoints = [(cx + 15, cy), (cx - 11, cy - 14), (cx - 11, cy + 14)]  #copilot3
            elif laneArrows[laneIndex] == "up":  #copilot3
                arrowPoints = [(cx, cy - 15), (cx - 14, cy + 11), (cx + 14, cy + 11)]  #copilot3
            else:  #copilot3
                arrowPoints = [(cx, cy + 15), (cx - 14, cy - 11), (cx + 14, cy - 11)]  #copilot3
            pygame.draw.polygon(canvas, arrowColor, arrowPoints)  #copilot3
            buttonLetter = smallFont.render(laneLabels[laneIndex], True, (255, 255, 255))  #copilot3
            canvas.blit(buttonLetter, buttonLetter.get_rect(center=(cx, cy + 17)))  #copilot3
        if not waitingForNotes:  #copilot3
            for noteIndex, note in enumerate(audio.get_visible_notes(noteTravelBeats)):  #copilot3
                noteId = (noteIndex, note["beat"], note["lane"])  #copilot3
                if noteId in scoredNotes:  #copilot3
                    continue  #copilot3
                laneIndex = note["lane"] - 1  #copilot3
                progress = 1 - (note["beat"] - beatNow) / noteTravelBeats  #copilot3
                progress = max(0.0, min(1.0, progress))  #copilot3
                noteX = laneTopX[laneIndex] + (laneBottomX[laneIndex] - laneTopX[laneIndex]) * progress  #copilot3
                noteY = stringTopY + (stringBottomY - stringTopY) * progress  #copilot3
                noteRadius = int(9 + progress * 15)  #copilot3
                pygame.draw.circle(canvas, (255, 205, 70), (int(noteX), int(noteY)), noteRadius)  #copilot3
                pygame.draw.circle(canvas, (255, 255, 255), (int(noteX), int(noteY)), noteRadius, 2)  #copilot3
        scoreText = scoreFont.render(f"{score:06d}", True, (255, 255, 255))  #copilot3
        canvas.blit(scoreText, scoreText.get_rect(topright=(screenWidth - 24, 20)))  #copilot3
        for index, (label, keyCode) in enumerate(padKeys):  #copilot3
            row = index // 3  #copilot3
            column = index % 3  #copilot3
            keyRect = pygame.Rect(keyLeft + column * (keySize + keyGap), keyTop + row * (keySize + keyGap), keySize, keySize)  #copilot3
            isActive = keyCode in activePadKeys  #copilot3
            keyColor = (70, 210, 120) if pressedKeys[keyCode] and isActive else ((55, 65, 95) if isActive else (32, 38, 57))  #copilot3
            pygame.draw.rect(canvas, keyColor, keyRect, border_radius=6)  #copilot3
            pygame.draw.rect(canvas, (230, 230, 240) if isActive else (80, 84, 98), keyRect, 2, border_radius=6)  #copilot3
            keyText = smallFont.render(label, True, (255, 255, 255) if isActive else (105, 108, 120))  #copilot3
            canvas.blit(keyText, keyText.get_rect(center=keyRect.center))  #copilot3
        spaceRect = pygame.Rect(keyLeft, keyTop + 3 * (keySize + keyGap), 3 * keySize + 2 * keyGap, 34)  #copilot3
        spaceColor = (70, 210, 120) if pressedKeys[pygame.K_SPACE] else (55, 65, 95)  #copilot3
        pygame.draw.rect(canvas, spaceColor, spaceRect, border_radius=6)  #copilot3
        pygame.draw.rect(canvas, (230, 230, 240), spaceRect, 2, border_radius=6)  #copilot3
        spaceText = smallFont.render("SPACE (THUMB)", True, (255, 255, 255))  #copilot3
        canvas.blit(spaceText, spaceText.get_rect(center=spaceRect.center))  #copilot3
    screen.fill((0, 0, 0))  #copilot3
    screen.blit(canvas, (shakeX, shakeY))  #copilot3
    if scene == "fade" and fadeAlpha > 0:  #copilot3
        fadeSurface = pygame.Surface((screenWidth, screenHeight))  #copilot3
        fadeSurface.fill((0, 0, 0))  #copilot3
        fadeSurface.set_alpha(fadeAlpha)  #copilot3
        screen.blit(fadeSurface, (0, 0))  #copilot3
    pygame.display.flip()  #copilot3
    clock.tick(60)  #copilot3
pygame.quit()  #copilot3
sys.exit()  #copilot3
