from settings import *
import pygame
import math

def level_select(n):
    rects = []
    f = open("./stages/level" + str(n) + "/rects.txt", "r")
    #image = pygame.image.load("stages/level" + str(n) + " bg.png")
    image = pygame.image.load('stages/level' + str(n) + "/bg.bmp")
    nr = int(f.readline())
    for i in range(nr):
        res = f.readline().split(" ")
        rects.append(pygame.Rect(int(res[0])*PIXEL_SCALE, int(res[1])*PIXEL_SCALE, int(res[2])*PIXEL_SCALE, int(res[3])*PIXEL_SCALE))
    return image, rects

def rectangle_collision(rect1: pygame.Rect, rect2: pygame.Rect, vx1, vy1, vx2, vy2):
    sides_r1 = [rect1.left, rect1.top, rect1.right, rect1.bottom]
    sides_r2 = [rect2.right, rect2.bottom, rect2.left, rect2.top]
    dvs = [vx2 - vx1, vy2 - vy1]
    v1s = [vx1, vy1]
    ts = []
    
    #print(rect1, rect2)
    #print("vx", vx1)
    #print("vy", vy1)
    #print("vxr", vx2)
    #print("vyr", vy2)

    for i in range(4):
        if dvs[i%2] != 0:
            t = (sides_r1[i]- sides_r2[i] + dvs[i%2])/dvs[i%2]
            #if t >= -1 and t < 0: t = 0
        else:
            t = 1
        #print("T n", i, "is", t)
        if t >= 0 and t < 1: ts.append([t, i])
    
    if len(ts) == 2 and ts[0][0] > ts[1][0]:
        i = ts[0][1]
        side_pos = ts[0][0]*v1s[i%2] + sides_r1[i] - v1s[i%2]
    else:
        i = ts[-1][1]
        side_pos = ts[-1][0]*v1s[i%2] + sides_r1[i] - v1s[i%2]
    
    #print("side pos", side_pos)
    #print(" ")
    match i:
        case 0:
            rect1.left = side_pos
            rect2.right = side_pos
        case 1:
            rect1.top = side_pos
            rect2.bottom = side_pos
        case 2:
            rect1.right = side_pos
            rect2.left = side_pos
        case 3:
            rect1.bottom = side_pos
            rect2.top = side_pos
    return i

def len_vec(x, y):
    return math.sqrt(x**2 + y**2)
#r1, r2 = pygame.Rect(2, 1, 4, 2), pygame.Rect(4, 2, 3, 4)
#r1, r2 = pygame.Rect(6, 0, 4, 4), pygame.Rect(7, 2, 5, 2)

#print(rectangle_collision(r1, r2, 2, 0, -3, 0))

#print(r1, r2)