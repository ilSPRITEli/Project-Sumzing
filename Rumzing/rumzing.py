import pygame
from sys import exit
from random import randint, choice
import math

#setting and elements------------------------------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_index = 0
        player_run1 = pygame.image.load('data/img/Player/player_run1.png').convert_alpha()
        player_run2 = pygame.image.load('data/img/Player/player_run2.png').convert_alpha()
        self.player_run = [player_run1, player_run2]
        self.player_jump = pygame.image.load('data/img/Player/player_run1.png').convert_alpha()
        player_slide1 = pygame.image.load('data/img/Player/player_slide1.png').convert_alpha()
        player_slide2 = pygame.image.load('data/img/Player/player_slide2.png').convert_alpha()
        self.player_slide = [player_slide1, player_slide2]

        self.image = self.player_run[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 285))
        self.gravity = 0
        self.slide = False
        self.jump = False

        self.jump_sound = pygame.mixer.Sound('data/audio/jumps.mp3')
        self.jump_sound.set_volume(0.3)
        self.slide_sound = pygame.mixer.Sound('data/audio/slide.mp3')
        self.slide_sound.set_volume(0.5)
    def player_input(self):
        keys = pygame.key.get_pressed()
        clicks = pygame.mouse.get_pressed()
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.rect.bottom >= 285 and self.jump == False:
            self.jump = True
            self.gravity = -19
            self.jump_sound.play()
        if keys[pygame.K_DOWN] or keys[pygame.K_s] and self.rect.bottom <= 285 and self.slide == False:
            self.slide = True
            self.jump = False
            self.gravity += 19
            self.slide_sound.play()
        if clicks[1] and self.rect.bottom >= 285:
            self.gravity = -19
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s and self.rect.bottom == 330:
                self.slide = False
                self.jump = False
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP and self.rect.bottom >= 285 and self.jump == True:
                self.slide = False
                self.jump = False
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 330 and self.slide == True:
            self.rect.bottom = 330
        elif self.rect.bottom >= 285 and self.slide == False:
            self.rect.bottom = 285
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
    def animation_state(self):
        if self.rect.bottom < 285:
        #jump
            self.image = self.player_jump
        elif self.slide:
            self.player_index += 0.1
            if self.player_index >= len(self.player_slide):
                self.player_index = 0
            self.image = self.player_slide[int(self.player_index)]

        else:
            #run
            self.player_index += 0.1
            if self.player_index >= len(self.player_run):
                self.player_index = 0
            self.image = self.player_run[int(self.player_index)]

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, spd):
        super().__init__()

        if type == 'fly':
            fly_frame1 = pygame.image.load('data/img/Fly/Fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('data/img/Fly/Fly2.png').convert_alpha()
            self.frame = [fly_frame1, fly_frame2]
            y_pos = 210
        else:
            noleg_frame1 = pygame.image.load('data/img/Noleg/nol1.png').convert_alpha()
            noleg_frame2 = pygame.image.load('data/img/Noleg/nol2.png').convert_alpha()
            self.frame = [noleg_frame1, noleg_frame2]
            y_pos = 285
        self.animation_index = 0
        self.spd = spd
        self.image = self.frame[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))
    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frame):
            self.animation_index = 0
        self.image = self.frame[int(self.animation_index)]
    def update(self):
        self.animation_state()
        self.rect.x -= self.spd
        self.destroy()
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                 return False, True
    return True, False

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False, True
    else:
        return True, False


#score-------------------------------------------------------==
def display_score():
    score = pygame.time.get_ticks()//100-start_time
    score_surface = score_font.render(f'SCORE: {score}', True, 'black')
    screen.blit(score_surface, (665, 30))
def get_score():
    score = pygame.time.get_ticks()//100-start_time
    return score
#-------------------------------------------------------------
 
pygame.init()
bg_music = pygame.mixer.Sound('data/audio/music.wav')
bg_music.set_volume(0.1)
bg_music.play(loops= -1)
jump = False
slide = False
score = 0
cnt = 0
hi_score = 0
spd = 5
fps = 60
width = 800
height = 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
begin_font = pygame.font.Font('data/font/DiaryOfAn8BitMage-lYDD.ttf', 40)
game_font = pygame.font.Font('data/font/DiaryOfAn8BitMage-lYDD.ttf', 50)
border_font = pygame.font.Font('data/font/DiaryOfAn8BitMage-lYDD.ttf', 53)
score_font = pygame.font.Font('data/font/DiaryOfAn8BitMage-lYDD.ttf', 20)

#Groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()



#bg setting
bg_surface = pygame.image.load('data/img/dark_sky.png').convert_alpha()
bg_width = bg_surface.get_width()
scroll_bg = 0
tiles_bg = math.ceil(width/bg_width)+1


ground_surface = pygame.image.load('data/img/dark_ground.png').convert_alpha()
ground_width = ground_surface.get_width()
scroll_ground = 0
tiles_ground = math.ceil(width/ground_width)+1


game_active = False
game_over = False
start_time = 0

#text-------------------------------------------------------==

dark_txt_start_surface = score_font.render('PRESS ANY BUTTON TO START', True, 'lavender')

bord_surface = border_font.render('RUMZING', True, 'black')
txt_surface = game_font.render('RUMZING', True, ('lavender'))

txt_game_over_surface = game_font.render('GAME OVER', True, (255,187,255))
bord_game_over_surface = border_font.render('GAME OVER', True, 'black')
#-------------------------------------------------------------

obstacle_rect_list = []

#gravity
player_gravity = 0

#intro
player_stand = pygame.image.load('data/img/Player/player_stand.png')
stand_rect = player_stand.get_rect(center = (400, 200))
player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.scale2x(player_stand)
#-------------------------------------------------------------



pygame.display.set_caption('Rumzing')
pygame.display.set_icon(pygame.image.load('data/img/icon.png'))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

noleg_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(noleg_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)



while True:
    #draw element
    #update
    press = pygame.KEYDOWN
    click = pygame.MOUSEBUTTONDOWN
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == press:
                if event.key == pygame.K_ESCAPE:
                    game_active = False
                    game_over = False

        elif game_over:
            spd = 5
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
                (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1, 0, 0)):
                game_active = False
                game_over = False
                start_time = pygame.time.get_ticks()//100
        else:
            if event.type == press or event.type == click:
                game_active = True
                start_time = pygame.time.get_ticks()//100

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'Noleg', 'Noleg', 'Noleg']), spd))

    
    if game_active:
        # scrolling bg

        for i in range(0, tiles_bg):
            screen.blit(bg_surface, (i*bg_width+scroll_bg, 0))
        for i in range(0, tiles_ground):
            screen.blit(ground_surface, (i*ground_width+scroll_ground, 285))

        
        scroll_bg -= 0.1+spd
        scroll_ground -= 5+spd

        if abs(scroll_bg) > bg_width:
            scroll_bg = 0
        if abs(scroll_ground) > ground_width:
            scroll_ground = 0

        score = display_score()
        scr = get_score()
        if scr > hi_score:
            hi_score = scr
 
        spd += 0.002

        #Player
        player.draw(screen)
        player.update()
        
        obstacle_group.draw(screen)
        obstacle_group.update()



        #collision
        game_active, game_over = collision_sprite()

        

    elif game_over:
        player_gravity = 0
        slide = False
        player.slide = False
        player.jump = False
        spd = 5
        screen.blit(bg_surface, (0, 0))
        screen.blit(ground_surface, (0, 285))
        obstacle_rect_list.clear()

        screen.blit(bord_game_over_surface, (242, 155))
        screen.blit(txt_game_over_surface, (250, 150))
        las_score_surface = score_font.render(f'YOUR SCORE: {scr}', True, 'white')
        screen.blit(las_score_surface, (310, 220))
    else:
        cnt += 1
        press_color = 'orange' if cnt%5 == 0 else 'lavender'
        txt_start_surface = score_font.render('PRESS ANY BUTTON TO START', True, press_color)
        hi_score_surface = score_font.render(f'HiGHEST SCORE: {hi_score}', True, 'lavender')
        screen.fill('darkslategrey')
        screen.blit(txt_surface, (480, 100))
        screen.blit(player_stand, (0, 0))
        screen.blit(hi_score_surface, (510, 200))
        screen.blit(txt_start_surface, (455, 230))
        
    pygame.display.update()
    
    clock.tick(fps)
