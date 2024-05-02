import pygame

class Platform:

    def __init__(self, coll_rect, img, img_coords, surface, platforms):
       
       platforms.append(coll_rect)
       self.coll_rect = coll_rect
       self.img = img
       self.img_coords = img_coords
       self.surf = surface

       self.timer = 200
       self.alpha = 255


    def update(self, platforms):
        if self.timer > 0:
            self.timer -= 1
        if self.timer == 0:
            platforms.remove(self.coll_rect)
            self.timer = -1
        if self.timer <= 100 and self.alpha >= 2.55:
            self.alpha -= 2.55
    

    def draw(self):
        dispimg = self.img.copy()
        dispimg.fill((255, 255, 255, self.alpha), None, pygame.BLEND_RGBA_MULT)
        self.surf.blit(dispimg, (self.img_coords[0], self.img_coords[1]))