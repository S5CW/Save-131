import pygame
from pygame.locals import *
from pygame import mixer
from os import path


def cutscene(screen, scene_num, bg_surface, vars=None):
    black = (0, 0, 0)

    screen_width = 1000
    screen_height = 1000

    def get_script(scene_num):
        script = []
        with open(f"cutscenes/c{str(scene_num)}.txt", "r") as f:
            for line in f:
                while "{" in line:
                    index = line.index("{")
                    line = line[:index]+vars[int(line[index+1])]+line[index+3:]
                line = line.strip().split(":")
                #assert line[0] in chars
                script.append([line[0], line[1]])
        return script

    script = get_script(scene_num)


    class Bubble:
        def __init__(self, screen, bg_surface):
            self.screen = screen
            self.bg_surface = bg_surface  # a snapshot of the game screen before overlay
            self.image = pygame.image.load("img/scroll.png").convert()
            self.image.set_colorkey((255, 255, 255))
            self.image = pygame.transform.scale(self.image, (1000, 300))
            self.rect = self.image.get_rect(center=(500, 800))
            self.font = pygame.font.SysFont('Bauhaus 93', 25)
            self.speaker_font = pygame.font.SysFont('Bauhaus 93', 50)

        def draw(self, text, speaker):
            # Restore the area behind the bubble
            bg_area = self.bg_surface.subsurface(self.rect).copy()
            self.screen.blit(bg_area, self.rect)

            # Draw the updated bubble
            self.screen.blit(self.image, self.rect)

            # Draw text on top
            text_surface = self.font.render(text, True, black)
            text_rect = text_surface.get_rect(center=self.rect.center)
            self.screen.blit(text_surface, text_rect)

            # draw speaker name on top left
            speaker_text_surface = self.speaker_font.render(speaker, True, black)
            speaker_text_rect = speaker_text_surface.get_rect(topleft=(self.rect.x + 100, self.rect.y + 50))
            self.screen.blit(speaker_text_surface, speaker_text_rect)

            # display speaker icon on top right
            speakers_dict = {"Prof. Lye": "img/Prof. Lye", f"{vars[2]}": f"img/{vars[0]}", "Bandit": "img/Bandit", "Sphinx": "img/Sphinx", "Creon": "img/Warrior",
                "Theseus": "img/Warrior", "Minotaur": "img/Minotaur", "Hooded Stranger": "img/Hooded Stranger", "Stranger": "img/Hooded Stranger",
                "Hermes": "img/Hermes", "Medusa": "img/Medusa", "Zeus": "img/Zeus", "Apollo": "img/Apollo"}
            
            if speaker in speakers_dict.keys():
                if speaker == "Theseus" or speaker == "Bandit" and scene_num == 3:
                    speaker_img_temp = pygame.image.load(speakers_dict[speaker]+"/Dead.png").convert_alpha()
                    speaker_img_len = speaker_img_temp.get_width() // speaker_img_temp.get_height()
                    speaker_img_temp2 = speaker_img_temp.subsurface(speaker_img_temp.get_height()*(speaker_img_len-1), 0, speaker_img_temp.get_height(), speaker_img_temp.get_height())
                else:
                    speaker_img_temp = pygame.image.load(speakers_dict[speaker]+"/Idle.png")
                    speaker_img_len = speaker_img_temp.get_width() // speaker_img_temp.get_height()
                    speaker_img_temp2 = speaker_img_temp.subsurface(0, 0, speaker_img_temp.get_height(), speaker_img_temp.get_height())

                speaker_img = pygame.transform.scale(speaker_img_temp2, (128, 128))

                screen.blit(speaker_img, (self.rect.right - speaker_img.get_width() - 100, self.rect.y))

            pygame.display.update(self.rect)  # only refresh this rect

    cs1 = Bubble(screen, bg_surface)


    for speaker, line in script:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        text_now = ""
        cs1.draw("", speaker)
        if line:
            for i in line:
                text_now += i
                cs1.draw(text_now, speaker)
                pygame.time.wait(60)  # typing speed in ms

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return -1   # so that there is no quit delay (because the 1000ms wait) 
        
            # small pause before next line
            pygame.time.wait(1000)
            
        else:
            while True:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return -1
                    
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            return text_now
                        else:
                            if event.key == pygame.K_SPACE:
                                text_now += " "
                            if event.key == pygame.K_BACKSPACE:
                                try: text_now = text_now[:-1]
                                except: pass
                            elif pygame.K_a <= event.key <= pygame.K_z:  
                                    text_now += chr(event.key)

                            cs1.draw(text_now, speaker)
                




