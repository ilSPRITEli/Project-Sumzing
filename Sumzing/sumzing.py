import pygame
from sys import exit
from random import randint

#setting and elements------------------------------------------------------
pygame.init()
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= spd
            
            if obstacle_rect.bottom == 285: 
                screen.blit(noleg_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False, True
    return True, False

def player_animation(slide):
    global player_surface, player_index
    if player_rect.bottom < 285:
        #jump
        player_surface = player_jump
    elif slide:
        player_index += 0.1
        if player_index >= len(player_slide):
            player_index = 0
        player_surface = player_slide[int(player_index)]

    else:
        #run
        player_index += 0.1
        if player_index >= len(player_run):
            player_index = 0
        player_surface = player_run[int(player_index)]


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


bg_surface = pygame.image.load('data/img/dark_sky.png').convert_alpha()
ground_surface = pygame.image.load('data/img/dark_ground.png').convert_alpha()

game_active = False
game_over = False
start_time = 0

#text-------------------------------------------------------==

dark_txt_start_surface = score_font.render('PRESS ANY BUTTON TO START', True, 'lavender')

bord_surface = border_font.render('SUMZING', True, 'black')
txt_surface = game_font.render('SUMZING', True, ('lavender'))

txt_game_over_surface = game_font.render('GAME OVER', True, (255,187,255))
bord_game_over_surface = border_font.render('GAME OVER', True, 'black')
#-------------------------------------------------------------
#score-------------------------------------------------------==
def display_score():
    score = pygame.time.get_ticks()//100-start_time
    score_surface = score_font.render(f'SCORE: {score}', True, 'black')
    screen.blit(score_surface, (665, 30))
def get_score():
    score = pygame.time.get_ticks()//100-start_time
    return score
#-------------------------------------------------------------
#Obstacle
#char
noleg_frame1 = pygame.image.load('data/img/Noleg/nol1.png').convert_alpha()
noleg_frame2 = pygame.image.load('data/img/Noleg/nol2.png').convert_alpha()
noleg_frame = [noleg_frame1, noleg_frame2]
noleg_index = 0
noleg_surface = noleg_frame[noleg_index]

fly_frame1 = pygame.image.load('data/img/Fly/Fly1.png').convert_alpha()
fly_frame2 = pygame.image.load('data/img/Fly/Fly2.png').convert_alpha()
fly_frame = [fly_frame1, fly_frame2]
fly_index = 0
fly_surface = fly_frame[fly_index]

obstacle_rect_list = []

#animation
player_index = 0
player_run1 = pygame.image.load('data/img/Player/player_run1.png').convert_alpha()
player_run2 = pygame.image.load('data/img/Player/player_run2.png').convert_alpha()
player_run = [player_run1, player_run2]
player_jump = pygame.image.load('data/img/Player/player_run1.png').convert_alpha()
player_slide1 = pygame.image.load('data/img/Player/player_slide1.png').convert_alpha()
player_slide2 = pygame.image.load('data/img/Player/player_slide2.png').convert_alpha()
player_slide = [player_slide1, player_slide2]

player_slide_surface = player_slide[player_index]
player_surface = player_run[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 285))




#gravity
player_gravity = 0

#intro
player_stand = pygame.image.load('data/img/Player/player_stand.png')
stand_rect = player_stand.get_rect(center = (400, 200))
player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.scale2x(player_stand)
player_stand = pygame.transform.scale2x(player_stand)
#-------------------------------------------------------------



pygame.display.set_caption('Sumzing')

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
            #jump
                if (event.key == pygame.K_SPACE or event.key == pygame.K_UP) and player_rect.bottom >= 285 and jump == False:
                    jump = True
                    slide = False
                    player_gravity = -19
                if event.key == pygame.K_DOWN or event.key == pygame.K_s and player_rect.bottom <= 285:
                    slide = True
                    player_gravity += 19
                if event.key == pygame.K_ESCAPE:
                    game_active = False
                    game_over = False
            # if event.type == pygame.KEYUP:
            if event.type == click:
                if pygame.mouse.get_pressed() == (1, 0, 0) and player_rect.bottom >= 285:
                    player_gravity = -19
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN or event.key == pygame.K_s and player_rect.bottom == 330:
                    slide = False
                    jump = False
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP and player_rect.bottom >= 285 and jump == True:
                    jump = False
                    slide = False

            
            
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
                if randint(0, 2):
                    obstacle_rect_list.append(noleg_surface.get_rect(midbottom = (randint(900, 1100), 285)))
                else:
                    obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 210)))

            if event.type == noleg_animation_timer:
                if noleg_index == 0:
                    noleg_index = 1
                else:
                    noleg_index = 0
                noleg_surface = noleg_frame[noleg_index]

            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index = 0
                fly_surface = fly_frame[fly_index]

    
    if game_active:
        screen.blit(bg_surface, (0, 0))
        screen.blit(ground_surface, (0, 285))


        score = display_score()
        scr = get_score()
        if scr > hi_score:
            hi_score = scr
 
        #noleg_rect.left = def_noleg_x if noleg_rect.left < -100 else noleg_rect.left - spd
        #screen.blit(noleg_surface, noleg_rect)
        spd += 0.0025

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 330 and slide == True:
            player_rect.bottom = 330
        elif player_rect.bottom >= 285 and slide == False:
            player_rect.bottom = 285
        


        player_animation(slide)
        screen.blit(player_surface, player_rect)

        #Obsta movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #collision
        game_active, game_over = collisions(player_rect, obstacle_rect_list)
        

    elif game_over:
        player_gravity = 0
        slide = False
        player_rect.bottom = 285
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
    
    # fps += 0.1
    clock.tick(fps)
