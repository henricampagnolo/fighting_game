import pygame
import math
from settings import *
from extra_functions import rectangle_collision, len_vec
from Classes.Spritemap import Spritemap
#from math import *

class Character:

    def __init__(self, width, height, surface, mvmtsprites, attacksprites, mvmtsprites_steps, attackinfo, x = 0, y = 0, controls = 1, mvmt_rect_offset = (36, 12)):
        self.spawn_x = x
        self.spawn_y = y
        self.vx = 0
        self.vy = 0
        self.w = width
        self.h = height
        self.surface = surface
        self.controls = controls
        self.rect = pygame.Rect(x, y, width, height)
        self.jumps_left = N_JUMPS
        self.jump_cooldown = 0
        self.lives = N_LIVES
        
        #damage meter
        self.damage = 0
        self.health_bars = Spritemap(surface, pygame.image.load("assets\health_bars.png").convert_alpha(), 192, 96)
        
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
        
        self.invicible_frames = 0

        #States
        self.dead = False
        self.grabbed = False
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
        self.attack_hold = self.attackinfo[4]
        self.attack_desacellaretations = self.attackinfo[5]
        self.knockback_self = self.attackinfo[6]
        self.attack_gravity = self.attackinfo[7]
        self.attack_grabs = self.attackinfo[8]

        self.is_grab = [len(i)> 0 for i in self.attack_grabs]
        
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
            case "victory_dance":
                return 1
            case "running":
                return 2
            case "jumping":
                return 3
            case "falling":
                return 4
            case "landing":
                return 5
            case "launched":
                return 6
        
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
                if self.frame_t > 8:
                    self.frame_t = 0
                    self.current_frame += 1
                    self.current_frame = self.current_frame % self.mvmt_sprites_steps[1]

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
            
            case 6:
                if self.frame_t > LAUNCHED_ANIM_SPEED:
                    self.frame_t = 0
                    self.current_frame += 1
                    self.current_frame = self.current_frame % self.mvmt_sprites_steps[6]


    def get_frame_attack(self):        
        
        #print(self.anim_n_attack(), self.att_current_frame)

        if self.att_frame_t > self.attack_times[self.anim_n_attack()][self.att_current_frame] + (self.attack_hold[self.anim_n_attack()][0] == self.att_current_frame and self.chosen_attack == self.anim_attack)*self.attack_hold[self.anim_n_attack()][1]:
            self.att_frame_t = 0
            self.att_current_frame += 1
            if self.att_current_frame >= self.attack_sprites_steps[self.anim_n_attack()]:
                for player in self.players:
                    if player != self and player.grabbed:
                        player.grabbed = False
                self.attacking = False
                self.att_current_frame = 0
                self.animate()


    def get_state_mvmt(self):

        if self.launched:
            self.prev_anim = self.anim
            self.anim = "launched"

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
            self.chosen_attack = "ground_special"

        elif self.attack1 and on_ground:
            self.chosen_attack = "ground_quick"
        
        elif self.attack2 and self.falling:
            self.chosen_attack = "air_special"

        else:
            self.chosen_attack = "ground_quick"

        """
        else:
            self.chosen_attack = "air_quick"
        """
        

        if not self.was_attacking:
            if self.left:
                self.facing_left = True
            if self.right:
                self.facing_left = False
            self.anim_attack = self.chosen_attack


    def animate(self):
        if self.attacking:
            self.att_frame_t += 1
            self.get_state_attack()
            self.get_frame_attack()
            if self.attacking:
                self.attack_coll()
        else:
            self.frame_t += 1
            self.get_state_mvmt()
            self.get_frame_mvmt()


    def read_inputs(self):
        keys=pygame.key.get_pressed()

        if self.controls == 1:
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

        if self.controls == 2:
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

            if keys[pygame.K_PERIOD]:
                self.attack1 = True
            else:
                self.attack1 = False

            if keys[pygame.K_COMMA]:
                self.attack2 = True
            else:
                self.attack2 = False


    def change_velocity(self):
        
        self.was_attacking = self.attacking
        
        if self.launched and not self.falling:
            self.vx *= LAUNCHED_SPEED_LOSS_GROUND
            self.vy *= LAUNCHED_SPEED_LOSS_GROUND
        elif self.launched:
            self.vx *= LAUNCHED_SPEED_LOSS_AIR
            self.vy *= LAUNCHED_SPEED_LOSS_AIR

        if self.jump_cooldown:
            self.jump_cooldown -= 1

        if self.attacked and self.invicible_frames < INVICIBILITY_FRAMES:
            self.invicible_frames += 1
        else:
            self.invicible_frames = 0
            self.attacked = False

        if ((self.attack1 or self.attack2) and not self.attacking) and not self.launched:
            self.attacking = True

        if not self.attacking and not self.launched:
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
        if self.up and self.jumps_left > 0 and self.jump_cooldown == 0 and len_vec(self.vx, self.vy) < LAUNCHED and not self.attacking:
            self.launched = False
            self.vy =- JUMP_ACCELERATION
            self.falling = True
            self.jumps_left -= 1
            self.jump_cooldown = JUMP_COOLDOWN
        if self.vy < 0 and self.up and len_vec(self.vx, self.vy) < LAUNCHED:
            self.vy -= JUMP_CONTROL
    
        elif self.attacking and not self.launched:
            self.vx *= self.attack_desacellaretations[self.anim_n_attack()]

        if not self.grabbed:
            if self.attacking:
                if self.attack_gravity[self.anim_n_attack()]:
                    self.vy += GRAVITY
                elif self.was_attacking:
                    self.vy = 0
                else:
                    self.vy += GRAVITY
            else:
                self.vy += GRAVITY

        #LIMITS
        if not self.launched:
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
            if self.rect.colliderect(plat) and not self.grabbed:
                side = rectangle_collision(self.rect, plat, math.floor(self.vx), math.floor(self.vy), 0, 0)
                if self.launched:
                    if side == 1 or side == 3:
                        self.falling = False
                        self.jumps_left = N_JUMPS
                        self.vy *= -LAUNCHED_BOUNCINESS
                    else:
                        self.vx *= -LAUNCHED_BOUNCINESS
                else:
                    if side == 3 and self.vy > VELOCITY_FOR_LANDING:
                        self.landing = True
                        #print("landed")
                    if side == 1 or side == 3:
                        self.falling = False
                        self.jumps_left = N_JUMPS
                        self.vy = 0
                    else:
                        self.vx = 0


    def attack_coll(self):
        n_att = self.anim_n_attack()
        n_frame = self.att_current_frame

        att_offset = (self.rect.x - self.attack_offsets[n_att][n_frame][0][self.facing_left], self.rect.y - self.attack_offsets[n_att][n_frame][1])

        for player in self.players:
            if player != self:
                #print("new_attack")
                for rect in self.attack_rects[n_att][n_frame][1]:
                    rect = rect.move(att_offset[0] + (self.attack_frame_width - 2*rect.x)*(self.facing_left), att_offset[1])
                    #print(rect, player.rect)
                    if rect.colliderect(player.rect) and not player.attacked:

                        if self.is_grab[n_att]:
                            player.grabbed = True

                        self.vx, self.vy = self.vx + self.knockback_self[n_att][0]*((not self.facing_left)*2 - 1), self.vy + self.knockback_self[self.anim_n_attack()][1]
                        player.is_attacked(self.attack_damages[n_att], self.knockback_effects[n_att], self.facing_left)

                if player.grabbed:
                    rect = self.attack_grabs[n_att][n_frame][0]
                    player.rect.x , player.rect.y = rect.x + att_offset[0] + (self.attack_frame_width - 2*rect.x)*(self.facing_left), rect.y + att_offset[1]


    def is_attacked(self, dam, knockback, direc):
        self.damage += dam
        self.attacked = True
        self.attacking = False
        self.vx += int(knockback[0]*(self.damage/KNOCK_BACK_SCALE))*((not direc)*2 - 1)
        self.vy += int(knockback[1]*(self.damage/KNOCK_BACK_SCALE))
        if len_vec(self.vx, self.vy) > LAUNCHED:
            self.launched = True


    def check_dead(self):
        #left / right / bottom
        if self.rect.x + self.rect.width <= 0 or self.rect.x > RENDER_RES[0] or self.rect.y > RENDER_RES[1]:
            self.lives -= 1
            if self.lives > 0:
                self.reset()
            else:
                self.rect.x = 10000
                self.rect.y = 10000
                self.dead = True


    def reset(self):
        self.vx = 0
        self.vy = 0
        self.rect = pygame.Rect(self.spawn_x, self.spawn_y, self.w, self.h)
        self.jumps_left = N_JUMPS
        self.jump_cooldown = 0
        
        #damage meter
        self.damage = 0

        #Current animation
        self.facing_left = True
        self.prev_anim = "none"
        self.anim = "none"

        self.anim_attack = "ground_special"

        self.frame_t = 0
        self.current_frame = 0

        self.att_frame_t = 0
        self.att_current_frame = 0
        
        self.invicible_frames = 0

        #States
        self.grabbed = False
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


    def move(self, platforms):
        self.change_velocity()
        self.rect.x += math.floor(self.vx)
        self.rect.y += math.floor(self.vy)
        self.collision(platforms)


    def check_win(self):
        other_alive = False
        for player in self.players:
            if not player.dead and player != self:
                other_alive = True
        return  not other_alive


    def update(self, platforms, players):
        self.players = players
        if self.check_win():
            self.frame_t += 1
            self.prev_anim = "victory_dance"
            self.anim = "victory_dance"
            self.get_frame_mvmt()
        else:
            if not self.dead:
                self.read_inputs()
                self.move(platforms)
                self.animate()
                self.check_dead()


    def draw(self):
        if self.attacking:
            #self.surface.blit(self.attack_sprites.get_frame(0, 0, self.facing_left), (1000, 1000))
            self.surface.blit(self.attack_sprites.get_frame(self.att_current_frame, self.anim_n_attack(), self.facing_left), (self.rect.x - self.attack_offsets[self.anim_n_attack()][self.att_current_frame][0][self.facing_left], self.rect.y - self.attack_offsets[self.anim_n_attack()][self.att_current_frame][1]))
        else:
            self.surface.blit(self.mvmt_sprites.get_frame(self.current_frame, self.anim_n_mvmt(), self.facing_left), (self.rect.x - self.mvmt_offset[0], self.rect.y - self.mvmt_offset[1]))
    

    def draw_health(self, resized_screen):
        prop = resized_screen.get_width()/self.surface.get_width()
        frame = pygame.transform.scale_by(self.health_bars.get_frame(0, min(DC_BARS, math.floor(self.damage/DC_BAR_VAL)), False), prop)
        fw = frame.get_width()
        fh = frame.get_width()
        sw = resized_screen.get_width()
        sh = resized_screen.get_height()
        border = DC_BORDER * prop
        if self.controls == 1:
            resized_screen.blit(frame, (border, border))
        if self.controls == 2:
            resized_screen.blit(frame, (sw - fw - border, border))
        if self.controls == 3:
            resized_screen.blit(frame, (border, sh - fh - border))
        if self.controls == 4:
            resized_screen.blit(frame, (sw - fw -  border, sh - fh - border))
