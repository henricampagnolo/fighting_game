import pygame.locals
#from Classes.Spritemap import Spritemap
import pygame
import sys

#class IdleJavi (Spritemap):

#    pass

pygame.init()

fps = 5
fpsClock = pygame.time.Clock()
 
coords = [i*144 for i in range(10)]
start = 0

width, height = 144*6, 144*6
screen = pygame.display.set_mode((width, height))

sprite_sheet = pygame.image.load("characters\character1\javi_sprites.png").convert_alpha()
 
# Game loop.
while True:
    screen.fill((255, 255, 255))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Update.
    frame = pygame.transform.flip(pygame.transform.scale_by(sprite_sheet.subsurface((coords[start], 288, width/6, height/6)), 6), 1, 0)

    # Draw.
    screen.blit(frame, (0, 0))
    print(start)
    
    start += 1

    start = start % 10

    pygame.display.flip()
    fpsClock.tick(fps)