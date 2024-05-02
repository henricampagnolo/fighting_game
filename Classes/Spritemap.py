import pygame

class Spritemap:

    def __init__(self, surf, img, fwidth, fheight):
        self.img = img
        self.surface = surf
        self.frame_width = fwidth
        self.frame_height = fheight
        self.frames_w = int(img.get_width()/fwidth)
        self.frames_h = int(img.get_height()/fheight)

    def get_frame(self, x, y, flip):
        x = x % self.frames_w
        y = y % self.frames_h
        frame = self.img.subsurface((x*self.frame_width, y*self.frame_height, self.frame_width, self.frame_height))
        return pygame.transform.flip(frame, flip, 0)

    