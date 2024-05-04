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
        mvmtsprites_steps = [2, 7, 10, 3, 1, 3, 4]

        #attack (this is temporary)
        raw_img_attack = pygame.image.load("characters\character1\javi_attack_sprites.png").convert_alpha()
        attacksprites = Spritemap(surface, raw_img_attack, 288, 288)
        attack_info = self.set_up_attacks()

        mvmt_rect_offset = (36, 12)
        
        super().__init__(width, height, surface, mvmtsprites, attacksprites, mvmtsprites_steps, attack_info, x, y, controls, mvmt_rect_offset)


    def set_up_attacks(self):
        
        rects_attack = [[[[pygame.Rect(48, 156, 72, 132)], []]
        ,[[pygame.Rect(42, 156, 72, 132)], []]
        ,[[pygame.Rect(48, 156, 72, 132)], [pygame.Rect(126, 204, 30, 36)]]
        ,[[pygame.Rect(48, 156, 72, 132)], [pygame.Rect(186, 198, 12, 54),pygame.Rect(156, 192, 30, 66),pygame.Rect(138, 198, 18, 54)]]
        ,[[pygame.Rect(54, 156, 72, 132)], [pygame.Rect(222, 198, 12, 54),pygame.Rect(168, 186, 54, 78),pygame.Rect(144, 192, 24, 66)]]
        ,[[pygame.Rect(48, 156, 72, 132)], [pygame.Rect(174, 192, 42, 48)]]
        ,[[pygame.Rect(48, 156, 72, 132)], [pygame.Rect(180, 216, 24, 24)]]
        ],
        [[[pygame.Rect(48, 156, 72, 132)], []]
        ,[[pygame.Rect(60, 156, 72, 132)], [pygame.Rect(156, 210, 12, 42)]]
        ,[[pygame.Rect(66, 156, 72, 132)], [pygame.Rect(156, 198, 36, 42)]]
        ,[[pygame.Rect(54, 156, 72, 132)], []]],

        [[[pygame.Rect(114, 18, 72, 132)], []]
        ,[[pygame.Rect(120, 12, 72, 132)], []]
        ,[[pygame.Rect(132, 24, 72, 132)], []]
        ,[[pygame.Rect(126, 0, 72, 132)], [pygame.Rect(114, 168, 102, 84)]]
        ,[[pygame.Rect(126, 24, 72, 132)], [pygame.Rect(108, 162, 108, 36),pygame.Rect(90, 198, 150, 60)]]
        ,[[pygame.Rect(114, 24, 72, 132)], [pygame.Rect(102, 186, 108, 42),pygame.Rect(108, 228, 60, 18)]]
        ,[[pygame.Rect(126, 30, 72, 132)], []]
        ,[[pygame.Rect(120, 24, 72, 132)], []]],
        []
        ]

        grab_hitboxes = [
        [],
        [],
        [[]
        ,[]
        ,[]
        ,[pygame.Rect(132, 156, 72, 132)]
        ,[pygame.Rect(132, 156, 72, 132)]
        ,[pygame.Rect(120, 156, 72, 132)]
        ,[pygame.Rect(66, 96, 72, 132)]
        ,[pygame.Rect(30, 30, 72, 132)]
        ],
        []
        ]

        attack_time = [[12, 12, 5, 5, 15, 8, 10], [4, 4, 8, 4], [10, 10, 8, 8, 8, 8, 5, 3], []]

        attack_damage = [50, 15, 40, 0]

        knockback_effect = [(10, 2), (2, -10), (-20, -15), (0, 0)]

        #This is the frame where is you hold the attack it will charge and not finish immidiatly(comme in a pair with the max time you can charge it for)
        holding_frame = [(1, 90), (0, 0), (0, 0), (0, 0)]

        attack_desacellaretation = [0.9, 1, 1, 0]

        knockback_self = [(0, 0), (0, 0), (0, -50), (0, 0)]

        attack_gravity = [1, 1, 0, 1]
        attack_cooldown = 20

        return [rects_attack, attack_time, attack_damage, knockback_effect, holding_frame, attack_desacellaretation, knockback_self, attack_gravity, grab_hitboxes, attack_cooldown]
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