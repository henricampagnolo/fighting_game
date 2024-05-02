import pygame
from settings import *
from Classes.Character import Character
from Classes.Spritemap import Spritemap

class Javi(Character):

    def __init__(self, surface, x=0, y=0, controls=1):
        
        width, height = 72, 132

        #mvmt
        raw_img_mvmt = pygame.image.load("characters\character1\javi_sprites.png").convert_alpha()
        mvmtsprites = Spritemap(surface, raw_img_mvmt, 144, 144)
        mvmtsprites_steps = [2, 7, 10, 3, 1, 3]

        #attack (this is temporary)
        raw_img_attack = pygame.image.load("characters\character1\javi_attack_sprites.png").convert_alpha()
        attacksprites = Spritemap(surface, raw_img_attack, 288, 288)
        attack_info = self.set_up_attacks()

        mvmt_rect_offset = (36, 12)
        
        super().__init__(width, height, surface, mvmtsprites, attacksprites, mvmtsprites_steps, attack_info, x, y, controls, mvmt_rect_offset)


    def set_up_attacks(self):
        
        rects_attack = [[[[pygame.Rect(168, 624, 288, 528)], []]
        ,[[pygame.Rect(168, 624, 288, 528)], []]
        ,[[pygame.Rect(192, 624, 288, 528)], [pygame.Rect(504, 816, 120, 144)]]
        ,[[pygame.Rect(192, 624, 288, 528)], [pygame.Rect(624, 768, 120, 264),pygame.Rect(744, 792, 48, 216),pygame.Rect(528, 792, 96, 216)]]
        ,[[pygame.Rect(240, 624, 288, 528)], [pygame.Rect(672, 744, 192, 312),pygame.Rect(864, 768, 48, 264),pygame.Rect(912, 840, 24, 120),pygame.Rect(600, 768, 72, 264)]]
        ,[[pygame.Rect(192, 624, 288, 528)], [pygame.Rect(696, 744, 168, 240)]]
        ,[[pygame.Rect(192, 624, 288, 528)], [pygame.Rect(720, 888, 96, 72)]]
        ],
        
        [],
        
        [],
        
        []]

        attack_time = [[10, 10, 10, 10, 10, 10, 10], [], [], []]

        attack_damage = [30, 0, 0, 0]

        knockback_effect = [(10, 0), (0, 0), (0, 0), (0, 0)]

        return [rects_attack, attack_time, attack_damage, knockback_effect]
'''

    def load_art(self):
        pass

    def update(self):
        self.frame_t += 1
        self.get_state()
        self.get_frame()
        print(self.animation)
    
    def state_n(self, name):
        match name:
            
            case "none":
                return 0
            case "idle":
                return 1
            case "running":
                return 2
            case "falling":
                return 3
        
        return 0
            
    def get_frame(self):
        match self.state_n(self.animation):

            case 0:
                pass
            case 1:
                pass
            case 2:
                if self.frame_t > (RUNNING_ANIM_SPEED/abs(self.vx)):
                    self.frame_t = 0
                    self.current_frame += 1
                    self.current_frame = self.current_frame % ANIMATION_N_FRAMES[2]

    def get_state(self):

        if self.attacked:
            self.prev_animation = self.animation
            self.animation = "attacked"

        elif self.vy < 0:
            self.prev_animation = self.animation
            self.animation = "jumping"
        #add landing later?

        elif self.vy > 0:
            self.prev_animation = self.animation
            self.animation = "falling"

        elif abs(self.vx) > RUNNING_ANIM_START:
            self.prev_animation = self.animation
            self.animation = "running"

        else:
            self.prev_animation = self.animation
            self.animation = "none"


    def draw(self, surface):
        print("funny")
        pygame.draw.rect(surface, (30, 100, 200), self.rect)
        #self.surface.blit(self.mvmt_sprites.get_frame(self.current_frame, self.state_n(self.animation)), (self.rect.left - self.frame_offset[0], self.rect.top - self.frame_offset[1]))
        surface.blit(self.mvmt_sprites.get_frame(0, 0), (self.rect.x - self.frame_offset[0], self.rect.y - self.frame_offset[1]))

'''