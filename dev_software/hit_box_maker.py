import sys
 
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
#Colors
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (255, 255, 255)
SELECTOR_COLOR = (255, 0, 0)
POINT_SELECT_COLOR = (0, 255, 0)

POINT_SELECT_RADIUS = 4
SELECTOR_WIDTH = 3

#IMG = pygame.image.load("characters/character1/img.png")
IMG = pygame.image.load("assets/spawn_platform.png")
PIXEL_SIZE = 6
SCALE_UP = 8
new_img = pygame.transform.scale_by(IMG, SCALE_UP)

pix_s = PIXEL_SIZE * SCALE_UP
pix_width = int(new_img.get_width()/pix_s)
pix_height = int(new_img.get_height()/pix_s)

width, height = new_img.get_width(), new_img.get_height()
screen = pygame.display.set_mode((width, height))

def draw_grid(screen):
    for i in range(pix_width):
        pygame.draw.line(screen, GRID_COLOR, (i * pix_s, 0), (i * pix_s, height))
    for i in range(pix_height):
        pygame.draw.line(screen, GRID_COLOR, (0, i * pix_s), (width, i * pix_s))

font = pygame.font.SysFont("Arial" , 30 , bold = True)

m3_waspressed= False
mouse_pressed = False
rects = []

# Game loop.
while True:

    screen.fill(BACKGROUND_COLOR)
  
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[K_RETURN]:
        with open("dev_software/hitboxes.txt", "w") as file:
            file.write(str(len(rects)))
            for rect in rects:
                file.write("\n" + str(int(rect.x/SCALE_UP)) + " " + str(int(rect.y/SCALE_UP)) + " " + str(int(rect.width/SCALE_UP)) + " " + str(int(rect.height/SCALE_UP)))
                #print(str(rect.x/SCALE_UP) + " " + str(rect.y/SCALE_UP) + " " + str(rect.width/SCALE_UP) + " " + str(rect.height/SCALE_UP))
        sys.exit()

    m1, m2, m3 = pygame.mouse.get_pressed(num_buttons=3)

    # Update.
    mpos = pygame.mouse.get_pos()
    pix_mpos = (round(mpos[0]/pix_s) * pix_s, round(mpos[1]/pix_s) * pix_s)

    if m1 and not mouse_pressed:
        x1, y1, x2, y2 = pix_mpos[0], pix_mpos[1], pix_mpos[0], pix_mpos[1]
        mouse_pressed = True
        print("click")
    elif m1 and mouse_pressed:
        print("pressed")
        x2, y2 = pix_mpos[0], pix_mpos[1]
    elif not m1 and mouse_pressed:
        print("end")
        mouse_pressed = False
        if x2 - x1 != 0 and y2 - y1 != 0:
            rects.append(pygame.Rect(min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1)))


    if m3 and not m3_waspressed:
        if len(rects) > 0:
            print("pop")
            rects.pop()
        m3_waspressed = True
    elif not m3 and m3_waspressed:
        m3_waspressed = False

    # Draw.
    screen.blit(new_img, (0, 0))
    pygame.draw.circle(screen, POINT_SELECT_COLOR, pix_mpos, POINT_SELECT_RADIUS)
    draw_grid(screen)
    for rect in rects:
        pygame.draw.rect(screen, SELECTOR_COLOR, rect, width=SELECTOR_WIDTH)
    if mouse_pressed:
        width_text = font.render("Width: "+str(int(abs(x2-x1)/SCALE_UP)), 1 , SELECTOR_COLOR)
        screen.blit(width_text,(0,0))

        height_text = font.render("Height: "+str(int(abs(y2-y1)/SCALE_UP)), 1 , SELECTOR_COLOR)
        screen.blit(height_text,(200,0))

        if x2 - x1 != 0 and y2 - y1 != 0:
            pygame.draw.rect(screen, SELECTOR_COLOR, (min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1)), width=SELECTOR_WIDTH)

    
    
    pygame.display.flip()
    fpsClock.tick(fps)