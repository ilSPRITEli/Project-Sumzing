import pygame
import os
pygame.init()

#setup game's window--------------------------------------------
SC_WID = 1000
SC_HIG = int(SC_WID * 0.8)

base_screen_size = [SC_WID - 200, SC_HIG - 200]
display = pygame.Surface((base_screen_size[0]//3, base_screen_size[1]//3))

def load_img(img_id):
    img = pygame.image.load('data/images/' + img_id).convert()
    img.set_colorkey((0, 0, 0))
    return img
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode((SC_WID, SC_HIG))
pygame.display.set_caption('Project Sumzing')
pygame.display.set_icon(load_img('icon.png'))
clock = pygame.time.Clock()

cursor_img = pygame.transform.scale(load_img('cursor.png'), (33, 33))

FPS = 165
BG = (0, 0, 0)
RED = (255, 0, 0)
def draw_bg(BG):
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 260), (SC_WID, 260))
#---------------------------------------------------------------

#spin_animation = [load_img(f'data/images/spin/spin_{i}.png') for i in range(23)]

GRAVITY = 0.5

move_left = False
move_right = False

#Samurai-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Samurai(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, spd):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = spd
        self.char_type = char_type
        self.direction = 1
        self.vel_y = 0
        self.walk = False
        self.jump = False
        self.in_air = False
        self.flip = False
        self.anilist = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        animation_types = ['idle', 'move']
        for animation in animation_types:
            temp_list = []
            frame_num = len(os.listdir(f'data/images/{self.char_type}/{animation}'))
            for i in range(frame_num - 1):
                img = pygame.image.load(f'data/images/{self.char_type}/{animation}/{animation}_{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.anilist.append(temp_list)
        self.img = self.anilist[self.action][self.index]

        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
        
    def move(self, move_left, move_right):
        #reset movement variables
        dx = 0
        dy = 0

        if move_left:
            dx  = self.walk == False and -self.speed or -((self.speed)/2)
            self.flip = True
            self.direction = -1
        if move_right:
            dx  = self.walk == False and self.speed or (self.speed)/2
            self.flip = False
            self.direction = 1
 
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True #if in air cant jump
        #grav
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy > 260:
            dy = 260 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):

        ANIMATION_CD = 200

        self.img = self.anilist[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_CD:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        if self.index >= len(self.anilist[self.action]):
            self.index = 0
    
    def update_action(self, new_act):
        #check if new act is fidd to the previous 1
        if new_act != self.action:
            self.action = new_act
            #update animation
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Weapon-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, spd):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = spd
        self.direction = 1
        self.vel_y = 0
        self.spin = False
        self.walk = False
        self.jump = False
        self.in_air = False
        self.flip = False
        self.rflip = False
        self.anilist = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        animation_types = ['idle', 'move', 'spin']
        for animation in animation_types:
            temp_list = []
            frame_num = len(os.listdir(f'data/images/katana/{animation}'))
            for i in range(frame_num - 1):
                img = pygame.image.load(f'data/images/katana/{animation}/{animation}_{i}.png')
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.anilist.append(temp_list)
        self.img = self.anilist[self.action][self.index]

        self.rect = self.img.get_rect()
        self.rect.center = (x, y)

    def do_spin(self):
        if self.spin == True:
            self.rflip = True
            self.rect.center = player.rect.center
        else:
            self.rflip = False
            self.rect.center = (self.x, self.y)
        
    def move(self, move_left, move_right):
        #reset movement variables
        dx = 0
        dy = 0

        if move_left:
            dx  = self.walk == False and -self.speed or -((self.speed)/2)
            self.flip = True
            self.direction = -1
        if move_right:
            dx  = self.walk == False and self.speed or (self.speed)/2
            self.flip = False
            self.direction = 1
 
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True #if in air cant jump
        #grav
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        #check collision with floor
        if self.rect.bottom + dy > 250:
            dy = 250 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):

        ANIMATION_CD = 10 

        self.img = self.anilist[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_CD:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        if self.index >= len(self.anilist[self.action]):
            self.index = 0
    
    def update_action(self, new_act):
        #check if new act is fidd to the previous 1
        if new_act != self.action:
            self.action = new_act
            #update animation
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip, self.rflip), self.rect)


player = Samurai('player', 200, 200, 3, 4)
enemy = Samurai('enemy', 400, 200, 3, 4)
katana = Weapon(200, 200, 3, 4)

run = True
while run:
    clock.tick(FPS)
    draw_bg(BG)

    mx, my = pygame.mouse.get_pos()
    true_mx = mx
    true_my = my
    mx -= (screen.get_width() - base_screen_size[0]) // 2
    my -= (screen.get_height() - base_screen_size[1]) // 2
    mx /= base_screen_size[0] / display.get_width()
    my /= base_screen_size[1] / display.get_height()

    player.update_animation()
    player.draw()

    katana.update_animation()
    katana.draw()

    enemy.update_animation()
    enemy.draw()

    #update player action 1 = run 0 = idle
    # 3 = spin for katana
    if player.alive:
        if move_left or move_right:
            player.update_action(1)
        else:
            player.update_action(0)
        
        if katana.spin:
            katana.update_action(2)
        else:
            katana.update_action(0)
        
        
        player.move(move_left, move_right)
        katana.move(move_left, move_right)

    
    #quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        #key pressed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left = True
            if event.key == pygame.K_d:
                move_right = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
                katana.jump = True
            if event.key == pygame.K_LSHIFT:
                player.walk = True
                katana.walk = True
            if event.key == pygame.K_j:
                katana.spin = True
        #key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False
            if event.key == pygame.K_SPACE:
                player.jump = False
                katana.jump = False
            if event.key == pygame.K_LSHIFT:
                player.walk = False
                katana.walk = False
            if event.key == pygame.K_j:
                katana.spin = False
    screen.blit(cursor_img, (true_mx // 3 * 3 + 1, true_my // 3 * 3 + 1))
    pygame.display.update()
pygame.quit()            
