import pygame, random
from button import Button
def boss(screen, char, boss_in, tutorial=False, medusa_tutorial=False):

    #create game window
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 1000

    class Fighter():
        def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound=None, medusa_sound=None):
            self.player = player
            self.size = data[0]
            self.scale = data[1]
            self.offset = data[2]
            self.flip = flip
            self.animation_list = self.load_images(sprite_sheet, animation_steps)
            self.action = 0#0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
            self.frame_index = 0
            self.image = self.animation_list[self.action][self.frame_index]
            self.update_time = pygame.time.get_ticks()
            self.rect = pygame.Rect((x, y, 80, 180))
            self.vel_y = 0
            self.running = False
            self.jump = False
            self.attacking = False
            self.attack_type = 0
            self.attack_cooldown = 0
            self.attack_sound = sound
            self.hit = False
            self.health = data[3]
            self.speed = data[4]
            self.alive = True
            self.medusa_turned = False
            self.medusa_state = "walking"
            self.medusa_timer = pygame.time.get_ticks()
            self.medusa_turn_interval = random.randint(1000, 2000)
            self.medusa_warning_duration = 400     # visual warning time
            self.medusa_turn_duration = 800        # how long she's facing player
            self.medusa_warning_sound = medusa_sound



        def load_images(self, sprite_sheets, animation_steps):
            #extract images from spritesheet
            animation_list = []
            for y, animation in enumerate(animation_steps):
                temp_img_list = []
                for x in range(animation):
                    temp_img = sprite_sheets[y].subsurface(x * self.size, 0, self.size, self.size)
                    temp_img_list.append(pygame.transform.scale(temp_img, (self.scale, self.scale)))
                animation_list.append(temp_img_list)
            return animation_list


        def move(self, screen_width, screen_height, surface, target, round_over):
            GRAVITY = 2
            dx = 0
            dy = 0
            if boss_in[0] == "Medusa" and not self.player: self.running = True
            else: self.running = False
            self.attack_type = 0

            #get keypresses
            key = pygame.key.get_pressed()

            #can only perform other actions if not currently attacking
            if self.attacking == False and self.alive == True and round_over == False:
                #player actions
                if self.player:
                    #movement
                    if key[pygame.K_LEFT]:
                        dx = -self.speed
                        self.running = True
                    if key[pygame.K_RIGHT]:
                        dx = self.speed
                        self.running = True
                    #jump
                    if key[pygame.K_UP] and self.jump == False:
                        self.vel_y = -35
                        self.jump = True
                    #attack
                    if key[pygame.K_SPACE]:
                        self.attack(target)
            
                #medusa actions
                elif boss_in[0] == "Medusa":

                    current_time = pygame.time.get_ticks()

                    # -------- STATE: WALKING --------
                    if self.medusa_state == "walking":
                        self.running = True
                        self.medusa_turned = False
                        self.flip = False  # facing away from player

                        # time to give warning?
                        if current_time - self.medusa_timer > self.medusa_turn_interval - self.medusa_warning_duration:
                            self.medusa_state = "warning"
                            self.medusa_timer = current_time
                            self.running = False   # <-- stop for visual warning
                            self.medusa_warning_sound.play()

                    # -------- STATE: WARNING --------
                    elif self.medusa_state == "warning":
                        self.running = False
                        self.medusa_turned = False
                        self.flip = False       # still facing away

                        if current_time - self.medusa_timer > self.medusa_warning_duration:
                            self.medusa_state = "turned"
                            self.medusa_timer = current_time

                    # -------- STATE: TURNED (danger) --------
                    elif self.medusa_state == "turned":
                        self.running = False
                        self.medusa_turned = True
                        self.flip = True        # now facing player
                        self.update_action(0)   # idle animation

                        # kill player if moving
                        key = pygame.key.get_pressed()
                        if any(key):
                            target.health = 0
                            target.hit = True

                        # return to walking
                        if current_time - self.medusa_timer > self.medusa_turn_duration:
                            self.medusa_state = "walking"
                            self.medusa_timer = current_time

                            # randomize next cycle
                            self.medusa_turn_interval = random.randint(600, 2000)
                #boss actions
                else:
                    attacking_rect = pygame.Rect(self.rect.centerx - (1 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
                    if target.rect in attacking_rect:
                        self.attack(target)
                        self.attack_type = 1
                    elif self.rect.x>target.rect.x:
                        dx = -self.speed
                        self.running = True
                    else:
                        dx = self.speed
                        self.running = True 

            #apply gravity
            self.vel_y += GRAVITY
            dy += self.vel_y

            #ensure player stays on screen
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
            if self.rect.bottom + dy > screen_height - 280:
                self.vel_y = 0
                self.jump = False
                dy = screen_height - 280 - self.rect.bottom

            #Medusa faces away until turned
            if boss_in[0] == "Medusa":
                if self.medusa_turned:
                    self.flip = True
                else:
                    self.flip = False
            #ensure players face each other
            elif target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            #apply attack cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

            #update player position
            self.rect.x += dx
            self.rect.y += dy


        #handle animation updates
        def update(self):
            #check what action the player is performing
            if self.health <= 0:
                self.health = 0
                self.alive = False
                self.update_action(5)#5:death
            elif self.hit == True:
                self.update_action(4)#4:hit
            elif self.attacking == True:
                self.update_action(3)#3:attack
            elif self.jump == True:
                self.update_action(2)#2:jump
            elif self.running == True:
                self.update_action(1)#1:walk
            else:
                self.update_action(0)#0:idle

            animation_cooldown = 50
            #update image
            self.image = self.animation_list[self.action][self.frame_index]
            #check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = pygame.time.get_ticks()
            #check if the animation has finished
            if self.frame_index >= len(self.animation_list[self.action]):
            #if the player is dead then end the animation
                if self.alive == False:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0
                    #check if an attack was executed
                    if self.action == 3:
                        self.attacking = False
                        self.attack_cooldown = 40
                    #check if damage was taken
                    if self.action == 4:
                        self.hit = False
                        #if the player was in the middle of an attack, then the attack is stopped
                        self.attacking = False
                        self.attack_cooldown = 40


        def attack(self, target):
            if self.attack_cooldown == 0:
                #execute attack
                self.attacking = True
                if self.attack_sound:
                    self.attack_sound.play()
                attacking_rect = pygame.Rect(self.rect.centerx - (1.5 * self.rect.width * self.flip), self.rect.y, 1.5 * self.rect.width, self.rect.height)
                if attacking_rect.colliderect(target.rect) and not self.medusa_turned:
                    target.health -= 10
                    target.hit = True


        def update_action(self, new_action):
            #check if the new action is different to the previous one
            if new_action != self.action:
                self.action = new_action
                #update the animation settings
                self.frame_index = 0
                self.update_time = pygame.time.get_ticks()

        def draw(self, surface):
            img = pygame.transform.flip(self.image, self.flip, False)
            surface.blit(img, (self.rect.x - (self.offset[0] * self.scale), self.rect.y - (self.offset[1] * self.scale)))

    #set framerate
    clock = pygame.time.Clock()
    FPS = 60

    #define colours
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)

    #define game variables
    intro_count = 4
    tutorial_over = True
    if tutorial: tutorial_over = False
    medusa_tutorial_over = True
    if medusa_tutorial: medusa_tutorial_over = False
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]#player scores. [P1, P2]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000
    win = False

    #define fighter variables
    PLAYER_SIZE = 128
    PLAYER_SCALE = 128
    PLAYER_OFFSET = [0, 0]
    if boss_in[0] == "Medusa":
        PLAYER_SPEED = 1
    else:
        PLAYER_SPEED = 10
    PLAYER_DATA = [PLAYER_SIZE, PLAYER_SCALE, PLAYER_OFFSET, 100, PLAYER_SPEED]
    BOSS_SIZE = 128
    BOSS_SCALE = 128
    BOSS_OFFSET = [0, 0]
    BOSS_DATA = [BOSS_SIZE, BOSS_SCALE, BOSS_OFFSET, boss_in[1], boss_in[2]]

    sword_fx = pygame.mixer.Sound("img/sword.wav")
    sword_fx.set_volume(0.5)
    jump_fx = pygame.mixer.Sound("img/jump.wav")
    jump_fx.set_volume(0.75)

    #load background image
    bg_image = pygame.image.load("img/colosseum_bg.png").convert_alpha()
    start_img = pygame.image.load("img/start_btn.png").convert_alpha()
    restart_img = pygame.image.load("img/restart_btn.png").convert_alpha()

    #load spritesheets
    player_sheets = []
    boss_sheets = []

    player_sheets.append(pygame.image.load(f"img/{char[0]}/Idle.png").convert_alpha())
    player_sheets.append(pygame.image.load(f"img/{char[0]}/Walk.png").convert_alpha())
    try: player_sheets.append(pygame.image.load(f"img/{char[0]}/Jump.png").convert_alpha())
    except: player_sheets.append(pygame.image.load(f"img/{char[0]}/Idle.png").convert_alpha())
    player_sheets.append(pygame.image.load(f"img/{char[0]}/Attack.png").convert_alpha())
    player_sheets.append(pygame.image.load(f"img/{char[0]}/Hurt.png").convert_alpha())
    player_sheets.append(pygame.image.load(f"img/{char[0]}/Dead.png").convert_alpha())
    
    boss_sheets.append(pygame.image.load(f"img/{boss_in[0]}/Idle.png").convert_alpha())
    boss_sheets.append(pygame.image.load(f"img/{boss_in[0]}/Walk.png").convert_alpha())
    try: boss_sheets.append(pygame.image.load(f"img/{boss_in[0]}/Jump.png").convert_alpha())
    except: boss_sheets.append(pygame.image.load(f"img/{boss_in[0]}/Idle.png").convert_alpha())
    boss_sheets.append(pygame.image.load(f"img/{boss_in[0]}/Attack.png").convert_alpha())
    boss_sheets.append(pygame.image.load(f"img/{boss_in[0]}/Hurt.png").convert_alpha())
    boss_sheets.append(pygame.image.load(f"img/{boss_in[0]}/Dead.png").convert_alpha())

    #load vicory image
    victory_img = pygame.image.load("img/victory.png").convert_alpha()

    #define number of steps in each animation
    PLAYER_ANIMATION_STEPS = char[1]
    BOSS_ANIMATION_STEPS = boss_in[3]

    #define font
    count_font = pygame.font.SysFont("Arial", 80)
    score_font = pygame.font.SysFont("Arial", 30)
    tutorial_font = pygame.font.SysFont("Bahaus 93", 50)
    tutorial_font2 = pygame.font.SysFont("Bahaus 93", 30)

    #function for drawing text
    def draw_text(text, font, text_col, x, y, center=False):
        img = font.render(text, True, text_col)
        if center:
            img_rect = img.get_rect()
            img_rect.center = (x, y)
        else: img_rect = (x, y)
        screen.blit(img, img_rect)

    #function for drawing background
    def draw_bg():
        scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_bg, (0, 0))

    #function for drawing fighter health bars
    def draw_health_bar(health, x, y):
        ratio = health / 100
        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


    #create two instances of fighters
    player = Fighter(True, 200, 310, False, PLAYER_DATA, player_sheets, PLAYER_ANIMATION_STEPS, sound=sword_fx)
    if boss_in[0] == "Medusa": boss = Fighter(False, 700, 310, True, BOSS_DATA, boss_sheets, BOSS_ANIMATION_STEPS, medusa_sound=jump_fx)
    else: boss = Fighter(False, 700, 310, True, BOSS_DATA, boss_sheets, BOSS_ANIMATION_STEPS)

    
    start_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 400, start_img)
    restart_button = Button(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 30, restart_img)

    #game loop
    while True:

        clock.tick(FPS)

        #draw background
        draw_bg()

        #show player stats
        draw_health_bar(player.health, 20, 20)
        draw_health_bar(boss.health, 580, 20)
        draw_text(f"{char[2]}: " + str(player.health), score_font, RED, 20, 60)
        draw_text(f"{boss_in[0]}: " + str(boss.health), score_font, RED, 580, 60)

        #update countdown
        if intro_count == 4 and not tutorial_over:
            draw_text("TUTORIAL: Boss Fight", tutorial_font, RED, SCREEN_WIDTH // 2, 200, center=True)
            draw_text("Use arrows to move / jump", tutorial_font2, RED, SCREEN_WIDTH // 2, 250, center=True)
            draw_text("Use SPACE to attack", tutorial_font2, RED, SCREEN_WIDTH // 2, 300, center=True)
            draw_text("Tip: you can attack from further than bosses can", tutorial_font2, RED, SCREEN_WIDTH // 2, 350, center=True)
            if start_button.draw(screen): tutorial_over = True
        elif intro_count == 4 and not medusa_tutorial_over:
            draw_text("TUTORIAL: Medusa's Footsteps", tutorial_font, RED, SCREEN_WIDTH // 2, 200, center=True)
            draw_text("Use arrows to move", tutorial_font2, RED, SCREEN_WIDTH // 2, 250, center=True)
            draw_text("You must not move whilst Medusa faces you", tutorial_font2, RED, SCREEN_WIDTH // 2, 300, center=True)
            draw_text("Use SPACE to attack", tutorial_font2, RED, SCREEN_WIDTH // 2, 350, center=True)
            if start_button.draw(screen): medusa_tutorial_over = True
        elif intro_count <= 0:
            #move fighters
            player.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, boss, round_over)
            boss.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player, round_over)
        else:
            #display count timer
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            #update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        #update fighters
        player.update()
        boss.update()

        #draw fighters
        player.draw(screen)
        boss.draw(screen)

        #check for player defeat
        if round_over == False:
            if player.alive == False:
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif boss.alive == False:
                win = True
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            if win:
                #display victory image
                screen.blit(victory_img, (360, 150))
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    return 1
            else:
                draw_text("YOU WERE KILLED", tutorial_font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)
                if boss_in[0] == "Hermes":
                    if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                        return 0
                elif restart_button.draw(screen):
                    round_over = False
                    intro_count = 3
                    player = Fighter(True, 200, 310, False, PLAYER_DATA, player_sheets, PLAYER_ANIMATION_STEPS, sound=sword_fx)
                    if boss_in[0] == "Medusa": boss = Fighter(False, 700, 310, True, BOSS_DATA, boss_sheets, BOSS_ANIMATION_STEPS, medusa_sound=jump_fx)
                    else: boss = Fighter(False, 700, 310, True, BOSS_DATA, boss_sheets, BOSS_ANIMATION_STEPS)

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1


        #update display
        pygame.display.update()

    #exit pygame
    pygame.quit()

# pygame.init()
# screen_width = 1000
# screen_height = 1000
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption('BOSS')
# char = ["Player_M", [8, 8, 8, 4, 3, 3], "Sam"]
# boss(screen, ["Player_M", [8, 8, 8, 4, 3, 3], "Sam"], ["Medusa", 10, 0, [7, 13, 1, 10, 3, 3]])
# boss(screen, char, ["Hermes", 100, 10, [5, 7, 8, 7, 4, 4]]) 