import pygame
import math
from settings import *
from extra_functions import rectangle_collision
#from math import *

class Character:

    def __init__(self, width, height, surface, mvmtsprites, attacksprites, mvmtsprites_steps, attackinfo, x = 0, y = 0, controls = 1, mvmt_rect_offset = (36, 12)):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = width
        self.h = height
        self.surface = surface
        self.controls = controls
        self.rect = pygame.Rect(x, y, width, height)
        
        #Sprite_sheets
        self.mvmt_sprites = mvmtsprites
        self.attack_sprites = attacksprites

        self.mvmt_sprites_steps = mvmtsprites_steps 

        self.mvmt_offset = mvmt_rect_offset

        #Attacks info
        self.attackinfo = attackinfo
        self.load_attacks()

        #Current animation
        self.facing_left = True
        self.prev_anim = "none"
        self.anim = "none"

        self.anim_attack = "ground_special"

        self.frame_t = 0
        self.current_frame = 0

        self.att_frame_t = 0
        self.att_current_frame = 0

        #States
        self.landing = False
        self.was_attacking = False
        self.attacking = False
        self.attacked = False
        self.launched = False
        self.falling = True

        #Inputs
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.attack1 = False
        self.attack2 = False


    def load_attacks(self):
        self.attack_rects = self.attackinfo[0]
        self.attack_times = self.attackinfo[1]
        self.attack_damages = self.attackinfo[2]
        self.knockback_effects = self.attackinfo[3]
        
        self.attack_frame_width = self.attack_sprites.frame_width
        self.attack_frame_height = self.attack_sprites.frame_height

        self.attack_sprites_steps = [len(self.attack_rects[i]) for i in range(NUMBER_OF_ATTACKS)]

        self.attack_offsets = []
    
        for line in self.attack_rects:
            self.attack_offsets.append([])
            for frame in line:
                for rect in frame[0]:
                    self.attack_offsets[-1].append(((rect.x, self.attack_frame_width - rect.x - rect.width), rect.y))


    def anim_n_mvmt(self):
        match self.anim:
            
            case "none":
                return 0
            case "idle":
                return 1
            case "running":
                return 2
            case "jumping":
                return 3
            case "falling":
                return 4
            case "landing":
                return 5
        
        return 0


    def anim_n_attack(self):
        match self.anim_attack:
            
            case "ground_special":
                return 0
            case "ground_quick":
                return 1
            case "air_special":
                return 2
            case "air_quick":
                return 3
        
        return 0


    def get_frame_mvmt(self):

        if self.prev_anim != self.anim:
            self.frame_t = 0
            self.current_frame = 0
            self.landing = False or (self.anim_n_mvmt() == 5)
            

        match self.anim_n_mvmt():

            case 0:
                if self.frame_t > FPS:
                    self.frame_t = 0
                    self.current_frame += 1
                    self.current_frame = self.current_frame % self.mvmt_sprites_steps[0]

            case 1:
                pass

            case 2:
                if self.frame_t > (RUNNING_ANIM_SPEED/abs(self.vx)):
                    self.frame_t = 0
                    self.current_frame += 1
                    self.current_frame = self.current_frame % self.mvmt_sprites_steps[2]

            case 3:
                if self.frame_t > JUMPING_ANIM_SPEED:
                    self.frame_t = 0
                    self.current_frame += 1
                    self.current_frame = self.current_frame - 1 * (self.current_frame >= 3)

            case 4:
                self.current_frame = 0
            
            case 5:
                if self.frame_t > LANDING_ANIM_SPEED * (self.current_frame+1)**LANDING_COMPENSATE:
                    self.frame_t = 0
                    self.current_frame += 1
                    if (self.current_frame >= 3):
                        self.landing = False
                        self.animate()


    def get_frame_attack(self):        
        
        print(self.anim_n_attack(), self.att_current_frame)

        if self.att_frame_t > self.attack_times[self.anim_n_attack()][self.att_current_frame]:
            self.att_frame_t = 0
            self.att_current_frame += 1
            if self.att_current_frame >= self.attack_sprites_steps[self.anim_n_attack()]:
                self.attacking = False
                self.att_current_frame = 0
                self.animate()


    def get_state_mvmt(self):

        if self.attacked:
            self.prev_anim = self.anim
            self.anim = "attacked"

        elif self.vy < 0:
            self.prev_anim = self.anim
            self.anim = "jumping"

        elif self.landing:
            self.prev_anim = self.anim
            self.anim = "landing"

        elif self.vy >= 0 and self.falling:
            self.prev_anim = self.anim
            self.anim = "falling"

        elif abs(self.vx) > RUNNING_ANIM_START:
            self.prev_anim = self.anim
            self.anim = "running"

        else:
            self.prev_anim = self.anim
            self.anim = "none"

        if self.left:
            self.facing_left = True
        if self.right:
            self.facing_left = False


    def get_state_attack(self):
        
        on_ground = not self.falling
        
        if self.attack2 and on_ground:
            self.anim_attack = "ground_special"

        elif self.attack1 and on_ground:
            self.anim_attack = "ground_quick"
        
        elif self.attack2 and self.falling:
            self.anim_attack = "air_special"

        else:
            self.anim_attack = "air_quick"

        if self.left:
            self.facing_left = True
        if self.right:
            self.facing_left = False


    def animate(self):
        if self.attacking:
            self.att_frame_t += 1
            if not self.was_attacking:
                self.get_state_attack()
            self.get_frame_attack()
        else:
            self.frame_t += 1
            self.get_state_mvmt()
            self.get_frame_mvmt()


    def read_inputs(self):
        keys=pygame.key.get_pressed()

        if self.controls == 1:
            if keys[pygame.K_LEFT]:
                self.left = True
            else:
                self.left = False

            if keys[pygame.K_RIGHT]:
                self.right = True
            else:
                self.right = False

            if keys[pygame.K_UP]:
                self.up = True
            else:
                self.up = False
            
            if keys[pygame.K_DOWN]:
                self.down = True
            else:
                self.down = False

            if keys[pygame.K_COLON]:
                self.attack1 = True
            else:
                self.attack1 = False

            if keys[pygame.K_COMMA]:
                self.attack2 = True
            else:
                self.attack2 = False

        if self.controls == 2:
            if keys[pygame.K_a]:
                self.left = True
            else:
                self.left = False

            if keys[pygame.K_d]:
                self.right = True
            else:
                self.right = False

            if keys[pygame.K_w]:
                self.up = True
            else:
                self.up = False
            
            if keys[pygame.K_s]:
                self.down = True
            else:
                self.down = False
            
            if keys[pygame.K_c]:
                self.attack1 = True
            else:
                self.attack1 = False

            if keys[pygame.K_v]:
                self.attack2 = True
            else:
                self.attack2 = False


    def change_velocity(self):
        
        self.was_attacking = self.attacking

        if (self.attack1 or self.attack2) and not self.attacking:
            self.attacking = True

        if not self.attacking:
            #HORIZONTAL MOUVEMENT
            if self.left:
                if self.vx > 0: self.vx = -TURNSPEED*self.vx
                self.vx -= ACCELERATION
            else:
                if self.vx < 0:
                    self.vx *= DESACCELERATION

            if self.right:
                if self.vx < 0: self.vx = -TURNSPEED*self.vx
                self.vx += ACCELERATION
            else:
                if self.vx > 0:
                    self.vx *= DESACCELERATION
            
            #JUMPING
            if self.up and not self.falling:
                self.vy -= JUMP_ACCELERATION
                self.falling = True
            if self.vy < 0 and self.up:
                self.vy -= JUMP_CONTROL
        self.vy += GRAVITY

        #LIMITS
        if self.vx > MAXSPEED:
            self.vx = MAXSPEED
        if self.vx < -MAXSPEED:
            self.vx = -MAXSPEED
        if abs(self.vx) < MINSPEED:
            self.vx = 0
        if self.vy > TERMINAL_VELOCITY:
            self.vy = TERMINAL_VELOCITY


    def collision(self, platforms):
        self.falling = True
        for plat in platforms:
            if self.rect.colliderect(plat):
                side = rectangle_collision(self.rect, plat, math.floor(self.vx), math.floor(self.vy), 0, 0)
                if side == 3 and self.vy > VELOCITY_FOR_LANDING:
                    self.landing = True
                    #print("landed")
                if side == 1 or side == 3:
                    self.falling = False
                    self.vy = 0
                else:
                    self.vx = 0


    def move(self, platforms):
        self.change_velocity()
        self.rect.x += math.floor(self.vx)
        self.rect.y += math.floor(self.vy)
        self.collision(platforms)


    def update(self, platforms):
        self.read_inputs()
        self.move(platforms)
        self.animate()


    def draw(self):
        if self.attacking:
            self.surface.blit(self.attack_sprites.get_frame(self.att_current_frame, self.anim_n_attack(), self.facing_left), (self.rect.x - self.attack_offsets[self.anim_n_attack()][self.att_current_frame][0][self.facing_left], self.rect.y - self.attack_offsets[self.anim_n_attack()][self.att_current_frame][1]))
        else:
            self.surface.blit(self.mvmt_sprites.get_frame(self.current_frame, self.anim_n_mvmt(), self.facing_left), (self.rect.x - self.mvmt_offset[0], self.rect.y - self.mvmt_offset[1]))
