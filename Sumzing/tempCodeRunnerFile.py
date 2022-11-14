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
BG = (10, 10, 10)
RED = (255, 0, 0)
def draw_bg(BG):
    screen.fill(BG)
    pygame.draw.line(screen, RED, (0, 260), (SC_WID, 260))