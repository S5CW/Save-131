import pygame
import button
def end_credits(screen, score):
    screen_width = 1000
    screen_height = 1000

    black = (0, 0, 0)
    red = (255, 0, 0)
    white = (255, 255, 255)
    
    bg = pygame.image.load("img/start_bg.png")
    screen.blit(bg, (0,0))

    exit_img = pygame.image.load("img/exit_btn.png").convert_alpha()
    exit_button = button.Button(screen_width - 250, 10, exit_img)

    coin_img = pygame.image.load("img/coin.png")
    coin = pygame.transform.scale(coin_img, (25, 25))
    coin_total = 75

    font1 = pygame.font.SysFont("Bauhaus 93", 80)
    font2 = pygame.font.SysFont("Bauhaus 93", 50)
    font_score = pygame.font.SysFont("Bauhaus 93", 30)

    text1 = font1.render("THANK YOU FOR PLAYING!", True, red)
    text1_rect = text1.get_rect(center=(screen_width//2, screen_height//2 - 100))
    screen.blit(text1, text1_rect)

    credits = ["Designed & Built by Sameer Shukla", "Platformer Inspired by CodingWithRuss", "Sprites from CraftPix.net", "Artwork by ChatGPT"]

    for index, i in enumerate(credits):
        text = font2.render(i, True, black)
        text_rect = text.get_rect(center=(screen_width//2, screen_height - 450 + 100*index))
        screen.blit(text, text_rect)

    screen.blit(coin, (25,25))
    score = font_score.render(f"X {score} / {coin_total}", True, white)
    screen.blit(score, (55,21))

    for i in range(30000):
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

            
        if exit_button.draw(screen):
            return -1

        pygame.time.wait(1)