from platformer import platformer
from cutscene import cutscene
from start_menu import start_menu
from end_credits import end_credits
from character import character
from boss import boss
import pygame

import os
os.environ['SDL_AUDIODRIVER'] = 'directsound'

pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.mixer.init()
pygame.init()


screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('SAVE 131')

pygame.mixer.music.load('img/music.wav')
pygame.mixer.music.play(-1, 0.0, 5000)

score = 0

if start_menu(screen) == -1: pygame.quit()
char = character(screen)
char.append("")
if char == -1: pygame.quit()


name = cutscene(screen, 0, screen.copy(), vars=char).capitalize()
if name == -1: pygame.quit()
char[2] = name

if cutscene(screen, 1, screen.copy(), vars=char) == -1: pygame.quit()

score_now = platformer(screen, 1, char, tutorial=True)
if score_now == -1: pygame.quit()
else: score+=score_now

if cutscene(screen, 2, screen.copy(), vars=char) == -1: pygame.quit()

if boss(screen, char, ["Bandit", 100, 0, [5, 7, 8, 4, 2, 4]], tutorial=True) == -1: pygame.quit()

if cutscene(screen, 3, screen.copy(), vars=char) == -1: pygame.quit()

score_now = platformer(screen, 2, char)
if score_now == -1: pygame.quit()
else: score+=score_now

while True:
    answer = cutscene(screen, 4, screen.copy(), vars=char) 
    if answer == -1: pygame.quit()
    elif "hole" in answer.lower():
        if cutscene(screen, "4_win", screen.copy(), vars=char) == -1: pygame.quit()
        break
    elif cutscene(screen, "4_lose", screen.copy(), vars=char) == -1: pygame.quit()

score_now = platformer(screen, 3, char)
if score_now == -1: pygame.quit()
else: score+=score_now

if cutscene(screen, 5, screen.copy(), vars=char) == -1: pygame.quit()

score_now = platformer(screen, 4, char)
if score_now == -1: pygame.quit()
else: score+=score_now
score_now = platformer(screen, 5, char)
if score_now == -1: pygame.quit()
else: score+=score_now

if cutscene(screen, 6, screen.copy(), vars=char) == -1: pygame.quit()

if boss(screen, char, ["Minotaur", 100, 5, [10, 12, 1, 4, 3, 5]]) == -1: pygame.quit()

if cutscene(screen, 7, screen.copy(), vars=char) == -1: pygame.quit()

score_now = platformer(screen, 6, char)
if score_now == -1: pygame.quit()
else: score+=score_now

if cutscene(screen, 8, screen.copy(), vars=char) == -1: pygame.quit()

if boss(screen, char, ["Medusa", 10, 0, [7, 13, 1, 10, 3, 3]], medusa_tutorial=True) == -1: pygame.quit()

if cutscene(screen, 9, screen.copy(), vars=char) == -1: pygame.quit()

score_now = platformer(screen, 7, char)
if score_now == -1: pygame.quit()
else: score+=score_now

if cutscene(screen, 10, screen.copy(), vars=char) == -1: pygame.quit()

while True:
    out = boss(screen, char, ["Hermes", 100, 10, [5, 7, 8, 7, 4, 4]]) 
    if out == -1: pygame.quit()
    elif out == 1: cutscene(screen, "10_win", screen.copy(), vars=char)
    else: break

while True:
    secret = cutscene(screen, 11, screen.copy(), vars=char) 
    if secret == -1: pygame.quit()
    elif "show" in secret and "prepared" in secret: break
    else: 
        char.append(secret)
        cutscene(screen, "11_lose", screen.copy(), vars=char)

if cutscene(screen, 12, screen.copy(), vars=char) == -1: pygame.quit()

score_now = platformer(screen, 8, char)
if score_now == -1: pygame.quit()
else: score+=score_now

if cutscene(screen, 13, screen.copy(), vars=char) == -1: pygame.quit()

end_credits(screen, score)

pygame.quit()
