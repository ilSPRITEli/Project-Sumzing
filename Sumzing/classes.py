import pygame, math

class Samurai():
    def __init__(self, x, y):
        self.flip = False
        self.rect = pygame.Rect((x, y, 40, 90))
        self.vel_v = 0
        self.jump = False
        self.atk_type = 0
        self.attacking = False
        self.hp = 100
    
    def move(self, screen_width, screen_height, surface, target, mx, my):
        SPD = 10
        GRAV = 1.5
        dx = 0
        dy = 0

        #key pressed
        key = pygame.key.get_pressed()
        click = pygame.mouse.get_pressed()

        if self.attacking == False:
            #move
            if key[pygame.K_a]:
                if key[pygame.K_LSHIFT]:
                    dx = -(SPD/2)
                else:
                    dx = -SPD
            if key[pygame.K_d]:
                if key[pygame.K_LSHIFT]:
                    dx = SPD/2
                else:
                    dx = SPD

            #jump
            if key[pygame.K_SPACE] and self.jump == False:
                self.vel_v = key[pygame.K_LSHIFT] and -20 or -30
                self.jump = True
            
            #attack

            if click == (1, 0, 0) or click == (0, 0, 1):
                if click == (1, 0, 0):
                    self.atk_type = 1 #light
                    self.attack(surface, target)

                if click == (0, 0, 1):
                    self.atk_type = 2 #spin
                    self.attack(surface, target)
        if self.attacking == True:
            if click == (0, 0, 0):
                self.attacking = False


        #apply gravity
        self.vel_v += GRAV
        dy += self.vel_v

        #ensure player on screen
        if self.rect.left + dx < 0:
            dx = 0 - self.rect.left
        if self.rect.bottom + dy > screen_height - 130:
            self.vel_v = 0
            self.jump = False
            dy = screen_height - 130 - self.rect.bottom

        #ensure player facing
        if mx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True


        self.rect.x += dx
        self.rect.y += dy

    def attack(self, surface, target):
        self.attacking = True
        if self.atk_type == 2:
            atk_rect = pygame.Rect(self.rect.centerx - 2*self.rect.width*self.flip, self.rect.y, 2*self.rect.width, self.rect.height)
        if self.atk_type == 1:
            atk_rect = pygame.Rect(self.rect.centerx - 4*self.rect.width*self.flip, self.rect.centery-10, 4*self.rect.width, self.rect.height/4)
        
        if atk_rect.colliderect(target.rect):
            target.hp -= self.atk_type == 1 and 2 or self.atk_type == 2 and 5
        pygame.draw.rect(surface, (200, 200, 200), atk_rect)

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
