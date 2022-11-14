import pygame, math
from classes import Samurai

pygame.init()

SCRN_W = 1000
SCRN_H = 600

#load image
def load_img(img_id):
    img = pygame.image.load(f'data/images/{img_id}.png').convert()
    img.set_colorkey((0, 0, 0))
    return img

screen = pygame.display.set_mode((SCRN_W, SCRN_H))
pygame.display.set_caption('Project Sumzing')
pygame.display.set_icon(load_img('icon'))

#set FPS
clock = pygame.time.Clock()
FPS = 100

#bg
bg_img = load_img('bg')
bg_img = pygame.transform.scale(bg_img, (1000, 600)) #resized bg
def draw_bg():
    screen.blit(bg_img, (0, 0))



#hp bar
def draw_hp(health, x, y):
    ratio = health / 100

    #hp color
    if health <= 70 and health > 30:
        hp_color = (255,153,18)
    elif health <= 30:
        hp_color = (220,20,60)
    else:
        hp_color = (127,255,0)

    pygame.draw.rect(screen, (100, 100, 100), (x - 5, y - 5, 410, 40))
    pygame.draw.rect(screen, (10, 10, 10), (x, y, 400, 30))
    pygame.draw.rect(screen, hp_color, (x, y, 400 * ratio, 30))

#char
player = Samurai(200, 360)
enemy = Samurai(700, 380)







#game running
run = True
while run:

    clock.tick(FPS)
    
    #mouse pos
    mx, my = pygame.mouse.get_pos()

    #draw bg
    draw_bg()

    #show hp
    draw_hp(player.hp, 20, 20)
    draw_hp(enemy.hp, 520, 20)

    #move update
    player.move(SCRN_W, SCRN_H, screen, enemy, mx, my)

    #draw char
    player.draw(screen)
    enemy.draw(screen)

    #event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
