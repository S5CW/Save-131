import pygame
from button import Button
def character(screen):
    FPS = 60
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Bahuas 93", 70)

    m_attack = pygame.image.load("img/Player_M/Attack.png")
    w_attack = pygame.image.load("img/Player_W/Attack.png")

    m_states = []
    for i in range(4):
        temp_img = m_attack.subsurface(i * 128, 0, 128, 128)
        m_states.append(pygame.transform.scale(temp_img, (500, 500)))

    w_states = []
    for i in range(5):
        temp_img = w_attack.subsurface(i * 128, 0, 128, 128)
        w_states.append(pygame.transform.scale(temp_img, (500, 500)))
    
    bg = pygame.image.load("img/sky.png")

    start_img = pygame.image.load('img/start_btn.png').convert_alpha()
    start_m = Button(100, 700, start_img)
    start_w = Button(600, 700, start_img)

    while True:
        
        screen.blit(bg, (0,0))
        clock.tick(FPS)

        img = font.render("CHOOSE YOUR CHARACTER!", True, (255, 0, 0))
        img_rect = img.get_rect()
        img_rect.center = (500,100)
        screen.blit(img, img_rect)

        screen.blit(m_states[i%4], (0, 100))
        screen.blit(w_states[i%5], (500, 100))

        if start_m.draw(screen): 
            screen.blit(bg, (0,0))
            pygame.display.update()
            return ["Player_M", [8, 8, 8, 4, 3, 3]]
        if start_w.draw(screen): 
            screen.blit(bg, (0,0))
            pygame.display.update()
            return ["Player_W", [6, 7, 6, 5, 3, 4]]

        if pygame.time.get_ticks()%30 == 0: i += 1

        pygame.display.update()

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
    

# pygame.init()
# screen = pygame.display.set_mode((1000, 1000))
# character(screen)

