import pygame
from sys import exit

#setting and elements------------------------------------------------------
pygame.init()
fps = 60
width = 800
height = 400
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
game_font = pygame.font.Font('data/font/DiaryOfAn8BitMage-lYDD.ttf', 50)
border_font = pygame.font.Font('data/font/DiaryOfAn8BitMage-lYDD.ttf', 53)
score_font = pygame.font.Font('data/font/DiaryOfAn8BitMage-lYDD.ttf', 20)


bg_surface = pygame.image.load('data/img/dark_sky.png').convert_alpha()
ground_surface = pygame.image.load('data/img/dark_ground.png').convert_alpha()

game_active = True
start_time = 0

#text-------------------------------------------------------==
bord_surface = border_font.render('SUMZING', True, 'black')
txt_surface = game_font.render('SUMZING', True, (255,187,255))

txt_game_over_surface = game_font.render('GAME OVER', True, (255,187,255))
bord_game_over_surface = border_font.render('GAME OVER', True, 'black')
#-------------------------------------------------------------



#score-------------------------------------------------------==
def display_score():
    score = pygame.time.get_ticks()//100-start_time
    score_surface = score_font.render(f'SCORE: {score}', True, 'black')
    screen.blit(score_surface, (665, 30))
#-------------------------------------------------------------


#char
noleg_surface = pygame.image.load('data/img/Noleg/nol1.png').convert_alpha()
def_noleg_x = 805
noleg_rect = noleg_surface.get_rect(midbottom = (def_noleg_x, 285))


player_surface = pygame.image.load('data/img/Player/player_stand.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 285))

#gravity
player_gravity = 0
#-------------------------------------------------------------

#load img func


pygame.display.set_caption('Sumzing')

while True:
    #draw element
    #update
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.KEYDOWN:
            #jump
                if event.key == pygame.K_SPACE and player_rect.bottom >= 285:
                    player_gravity = -19
            # if event.type == pygame.KEYUP:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0) and player_rect.bottom >= 285:
                    player_gravity = -19
        else:
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
                (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed() == (1, 0, 0)):
                game_active = True
                noleg_rect.left = 805
                start_time = pygame.time.get_ticks()//100

        #exit by Esc button
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            exit()


    
    if game_active:
        screen.blit(bg_surface, (0, 0))
        screen.blit(ground_surface, (0, 285))

        screen.blit(bord_surface, (294, 26))
        screen.blit(txt_surface, (300, 20))
        display_score()

        noleg_rect.left = def_noleg_x if noleg_rect.left < -100 else noleg_rect.left - 5
        screen.blit(noleg_surface, noleg_rect)

        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 285:
            player_rect.bottom = 285

        #player_rect.left = -40 if player_rect.left > 810 else player_rect.left + 6
        screen.blit(player_surface, player_rect)

        if noleg_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.blit(bg_surface, (0, 0))
        screen.blit(ground_surface, (0, 285))

        screen.blit(bord_game_over_surface, (242, 155))
        screen.blit(txt_game_over_surface, (250, 150))

        
    pygame.display.update()
    # fps += 0.1
    clock.tick(fps)
