import sys

import pygame

class Spritemap:

    def __init__(self, surf, img, fwidth, fheight):
        self.img = img
        self.surface = surf
        self.frame_width = fwidth
        self.frame_height = fheight
        self.frames_w = int(img.get_width()/fwidth)
        self.frames_h = int(img.get_height()/fheight)

    def get_frame(self, x, y):
        x = x % self.frames_w
        y = y % self.frames_h
        frame = self.img.subsurface((x*self.frame_width, y*self.frame_height, self.frame_width, self.frame_height))
        return frame

from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()

#frame_amount = [2, 8, 10]

#Colors
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (255, 255, 255)
SELECTOR_COLORs = [(255, 0, 0), (0, 0, 255)]
POINT_SELECT_COLOR = (0, 255, 0)

POINT_SELECT_RADIUS = 4
SELECTOR_WIDTH = 3

#IMG = pygame.image.load("characters/character1/img.png")
IMG = pygame.image.load("characters\character1\javi_attack_sprites.png")

w, h = 7, 2

grid = [[[[], []] for j in range(w)] for i in range(h)]

PIXEL_SIZE = 6
SCALE_UP = 4

pix_s = PIXEL_SIZE * SCALE_UP
pix_width = 48
pix_height = 48

screen = pygame.display.set_mode((pix_width*pix_s, pix_height*pix_s))

width = screen.get_width()
height = screen.get_height()

imgs = Spritemap(screen, IMG, pix_width*PIXEL_SIZE, pix_height*PIXEL_SIZE)

def draw_grid(screen):
    for i in range(pix_width):
        pygame.draw.line(screen, GRID_COLOR, (i * pix_s, 0), (i * pix_s, height))
    for i in range(pix_height):
        pygame.draw.line(screen, GRID_COLOR, (0, i * pix_s), (width, i * pix_s))

font = pygame.font.SysFont("Arial" , 30 , bold = True)

m3_waspressed= False
mouse_pressed = False
rects = []

index_x = 0
index_y = 0
frames = 0
mode = 0

def scale_down(n):
    return int(n/SCALE_UP)

def grid_txt(grid):
    string = "["
    for line in grid:
        string = string + "["
        for frame in line:
            string = string + "[["
            for rect in frame[0]:
                string = string + f"pygame.Rect({scale_down(rect.left)}, {scale_down(rect.top)}, {scale_down(rect.width)}, {scale_down(rect.height)}),"
            if string[-1] == ",": string = string[0:-1]
            string = string + "], ["
            for rect in frame[1]:
                string = string + f"pygame.Rect({scale_down(rect.left)}, {scale_down(rect.top)}, {scale_down(rect.width)}, {scale_down(rect.height)}),"
            if string[-1] == ",": string = string[0:-1]
            string = string + "]]\n,"
        if string[-1] == ",": string = string[0:-1]
        string = string + "]\n\n\n,"
    if string[-1] == ",": string = string[0:-1]
    string = string + "]"
    return string

# Game loop.
while True:

    screen.fill(BACKGROUND_COLOR)
    frames += 1
    frames = frames % 10

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    keys = pygame.key.get_pressed()
    if keys[K_RETURN]:
        with open("dev_software/hitboxes.txt", "w") as file:
            file.write(grid_txt(grid))
            #for rect in r  ects:
            #    file.write("\n" + str(int(rect.x/SCALE_UP)) + " " + str(int(rect.y/SCALE_UP)) + " " + str(int(rect.width/SCALE_UP)) + " " + str(int(rect.height/SCALE_UP)))
                #print(str(rect.x/SCALE_UP) + " " + str(rect.y/SCALE_UP) + " " + str(rect.width/SCALE_UP) + " " + str(rect.height/SCALE_UP))
        sys.exit()
    if frames == 0:    
        if keys[K_LEFT]:
            index_x -=1
        if keys[K_RIGHT]:
            index_x +=1
        if keys[K_UP]:
            index_y -=1
        if keys[K_DOWN]:
            index_y +=1
        if keys[K_SPACE]:
            mode = -mode + 1

    index_x = index_x % w
    index_y = index_y % h

    m1, m2, m3 = pygame.mouse.get_pressed(num_buttons=3)

    # Update.
    mpos = pygame.mouse.get_pos()
    pix_mpos = (round(mpos[0]/pix_s) * pix_s, round(mpos[1]/pix_s) * pix_s)

    if m1 and not mouse_pressed:
        x1, y1, x2, y2 = pix_mpos[0], pix_mpos[1], pix_mpos[0], pix_mpos[1]
        mouse_pressed = True
        print("click")
    elif m1 and mouse_pressed:
        #print("pressed")
        x2, y2 = pix_mpos[0], pix_mpos[1]
    elif not m1 and mouse_pressed:
        print("end")
        mouse_pressed = False
        if x2 - x1 != 0 and y2 - y1 != 0:
            grid[index_y][index_x][mode].append(pygame.Rect(min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1)))
        print(grid)


    if m3 and not m3_waspressed:
        if len(grid[index_y][index_x]) > 0:
            print("pop")
            grid[index_y][index_x][mode].pop()
        m3_waspressed = True
    elif not m3 and m3_waspressed:
        m3_waspressed = False

    # Draw.
    screen.blit(pygame.transform.scale_by(imgs.get_frame(index_x, index_y), SCALE_UP), (0, 0))


    pygame.draw.circle(screen, POINT_SELECT_COLOR, pix_mpos, POINT_SELECT_RADIUS)
    draw_grid(screen)
    for rect in grid[index_y][index_x][mode]:
        pygame.draw.rect(screen, SELECTOR_COLORs[mode], rect, width=SELECTOR_WIDTH)
    if mouse_pressed:
        width_text = font.render("Width: "+str(int(abs(x2-x1)/SCALE_UP)), 1 , SELECTOR_COLORs[mode])
        screen.blit(width_text,(0,0))

        height_text = font.render("Height: "+str(int(abs(y2-y1)/SCALE_UP)), 1 , SELECTOR_COLORs[mode])
        screen.blit(height_text,(200,0))

        if x2 - x1 != 0 and y2 - y1 != 0:
            pygame.draw.rect(screen, SELECTOR_COLORs[mode], (min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1)), width=SELECTOR_WIDTH)

    
    
    pygame.display.flip()
    fpsClock.tick(fps)