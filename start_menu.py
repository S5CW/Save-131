import pygame
import button

def start_menu(screen):
    light_blue = (173, 216, 230)
    
    screen_width = 1000
    screen_height = 1000

    start_img = pygame.image.load('img/start_btn.png').convert_alpha()
    exit_img = pygame.image.load('img/exit_btn.png').convert_alpha()
    start_bg = pygame.image.load('img/start_bg.png')


    start_button = button.Button(50, screen_height - 150, start_img)
    exit_button = button.Button(screen_width - 250, screen_height - 150, exit_img)

    clock = pygame.time.Clock()

    while True:
        # process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        screen.blit(start_bg, screen.get_rect())
        # draw buttons and check for clicks
        if start_button.draw(screen):
            screen.fill(light_blue)
            pygame.display.update()
            return 0
        if exit_button.draw(screen):
            return -1

        pygame.display.update()
        clock.tick(60)  # limit FPS
