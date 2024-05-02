import pygame
from settings import *
from characters.character1.Javi import Javi
from Classes.Character import Character
from Classes.Platforms import Platform
from extra_functions import *

class FightingFoo:
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("FightingFoo")

        self.screen = pygame.display.set_mode(INITIAL_SCREENSIZE, pygame.RESIZABLE)

        self.set_game_variables()


    def set_game_variables(self):
        self.running = True
        self.render_surf = pygame.Surface(RENDER_RES)

        self.clock = pygame.time.Clock()

        #self.platforms = [pygame.Rect(100, 700, 1400, 100), pygame.Rect(200, 500, 300, 50), pygame.Rect(700, 300, 300, 50), pygame.Rect(1300, 400, 200, 300)]

        #self.bg_image = pygame.transform.scale(pygame.image.load('image.png'), self.render_surf.get_size())

        self.bg_image, self.platforms = level_select(1)

        print(self.platforms)

        #self.bg_image = pygame.image.load(os.path.join('stages/level1', "bg.bmp")) self.platforms = [pygame.Rect(66*6, 87*6, 64*6, 16*6), pygame.Rect(178*6, 87*6, 64*6, 16*6), pygame.Rect(42*6, 127*6, 224*6, 16*6), pygame.Rect(106*6, 143*6, 96*6, 16*6)]

        self.font = pygame.font.SysFont("Arial" , 20 , bold = True)

        '''
        self.player1 = Character(PLAYER_SIZE[0], PLAYER_SIZE[1],
                                pygame.image.load("characters/character1/img.png").convert_alpha(),
                                self.render_surf,
                                #x = CAM_LEFT_BORDER + 100 , y = (RENDER_RES[1] - PLAYER_SIZE[1])/2,
                                x = 500 , y = 200,
                                controls=1)
        
        
        self.player2 = Character(PLAYER_SIZE[0], PLAYER_SIZE[1],
                                pygame.image.load("characters/character1/img.png").convert_alpha(),
                                self.render_surf,
                                #x = RENDER_RES[0] - CAM_RIGHT_BORDER - 100, y = (RENDER_RES[1] - PLAYER_SIZE[1])/2,
                                x = 1000 , y = 200,
                                controls=2)
        '''
        self.player1 = Javi(self.render_surf, x = 400, y = 200, controls=1)
        self.player2 = Javi(self.render_surf, x = 1000, y = 200, controls=2)
        '''
        self.temp_platforms = [Platform(pygame.Rect
                                       (CAM_LEFT_BORDER, (RENDER_RES[1] + PLAYER_SIZE[1])/2, 96, 16),
                                       pygame.image.load("assets/spawn_platform.png"),
                                       (CAM_LEFT_BORDER-24, (RENDER_RES[1] + PLAYER_SIZE[1])/2),
                                       self.render_surf,
                                       self.platforms)]
        '''
                                       
        self.players = [self.player1, self.player2]


    def main_loop(self):

        while self.running:
            self.handle_input()
            self.game_logic()
            self.draw()
            self.clock.tick(FPS)


    def fps_counter(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1 , pygame.Color("GREEN"))
        self.render_surf.blit(fps_t,(0,0))

        vx_char = self.font.render(str(self.player1.vx) , 1 , pygame.Color("RED"))
        self.render_surf.blit(vx_char,(50,0))

        vy_char = self.font.render(str(self.player1.vy) , 1 , pygame.Color("BLUE"))
        self.render_surf.blit(vy_char,(100,0))


    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    

    def game_logic(self):
        for player in self.players:
            player.update(self.platforms)


    def find_zoom_rect(self):

        p1r = self.player1.rect
        p2r = self.player2.rect

        min_width = MIN_CAM_SIZE[0]
        min_height = MIN_CAM_SIZE[1]

        #center_players = ((p1r.centerx + p2r.centerx)/2,
        #                  (p1r.centery + p2r.centery)/2)

        min_left = min(p1r.left, p2r.left)
        max_right = max(p1r.right, p2r.right)
        min_top = min(p1r.top, p2r.top)
        max_bottom = max(p1r.bottom, p2r.bottom)

        if abs(min_left - max_right) + CAM_LEFT_BORDER + CAM_RIGHT_BORDER > min_width:
            min_width = abs(min_left - max_right) + CAM_LEFT_BORDER + CAM_RIGHT_BORDER
        centerx = (min_left + max_right)/2


        if abs(min_top - max_bottom) + CAM_TOP_BORDER + CAM_BOTTOM_BORDER > min_height:
            min_height = abs(min_top - max_bottom) + CAM_TOP_BORDER + CAM_BOTTOM_BORDER
        centery = (min_top + max_bottom)/2
        
        aspect_ratio = RENDER_RES[1]/RENDER_RES[0]

        if min_width > aspect_ratio*min_height:
            min_height = min_width*aspect_ratio
        else:
            min_width = min_height/aspect_ratio

        if min_width > RENDER_RES[0]:
            min_width, min_height = RENDER_RES[0], RENDER_RES[1]

        rl = centerx - min_width/2
        rr = centery - min_height/2

        result = pygame.Rect(rl, rr, min_width, min_height)

        if result.left < 0: result.left = 0
        if result.right > RENDER_RES[0]: result.right = RENDER_RES[0]
        if result.top < 0: result.top = 0
        if result.bottom > RENDER_RES[1]: result.bottom = RENDER_RES[1]

        return result


    def draw(self):
        #Background
        #self.render_surf.fill((0, 0, 255))
        #self.resized_bg_image = pygame.transform.scale(self.bg_image, self.screen.get_size())
        self.render_surf.blit(self.bg_image, (0, 0))

        #Elements
        #for platform in self.platforms:
        #    pygame.draw.rect(self.render_surf, (100, 0, 200), platform)

        #for plat in self.platforms:
        #    pygame.draw.rect(self.render_surf, (255, 0, 255), plat)

        for player in self.players:
            player.draw()

        #self.fps_counter()
        
        #pygame.transform.scale2x(self.render_surf, self.render_surf)

        #self.render_surf.scroll(dx=-self.player1.rect.left/2, dy=-self.player1.rect.top/2)

        #zoomed_rect = pygame.Rect(only_pos(self.player1.rect.centerx-RENDER_RES[0]/4), only_pos(self.player1.rect.centery-RENDER_RES[1]/4), MIN_CAM_SIZE[0], MIN_CAM_SIZE[1])
        zoomed_rect = self.find_zoom_rect()

        zoomed_area = self.render_surf.subsurface(zoomed_rect)

        sw = self.screen.get_width()
        sh = self.screen.get_height()

        pygame.transform.scale(zoomed_area, (sw, sh), dest_surface=self.screen)
        #self.screen.blit(scale_img, (0, 0))
        #self.screen.blit(scale_img, (-(self.player1.x * propx) - sw, -(self.player1.y*propy) - sh))

        pygame.display.flip()
