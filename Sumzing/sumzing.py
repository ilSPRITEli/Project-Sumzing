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


bg_surface = pygame.image.load('data/img/dark_sky.png').convert_alpha()
ground_surface = pygame.image.load('data/img/dark_ground.png').convert_alpha()


#text-------------------------------------------------------==
bord_surface = border_font.render('SUMZING', True, 'black')
txt_surface = game_font.render('SUMZING', True, (255,187,255))
#-------------------------------------------------------------


#char
noleg_surface = pygame.image.load('data/img/snail/snail1.png').convert_alpha()
def_noleg_x = 805
noleg_rect = noleg_surface.get_rect(midbottom = (def_noleg_x, 285))


player_surface = pygame.image.load('data/img/Player/player_stand.png').convert_alpha()
player_rect = player_surface.get_rect(midbottom = (80, 285))
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
    
    screen.blit(bg_surface, (0, 0))
    screen.blit(ground_surface, (0, 285))

    screen.blit(bord_surface, (294, 26))
    screen.blit(txt_surface, (300, 20))

    noleg_rect.left = def_noleg_x if noleg_rect.left < -100 else noleg_rect.left - 4
    screen.blit(noleg_surface, noleg_rect)

    #player_rect.left = -40 if player_rect.left > 810 else player_rect.left + 6
    screen.blit(player_surface, player_rect)

    pygame.display.update()
    fps += 0.1
    clock.tick(fps)
