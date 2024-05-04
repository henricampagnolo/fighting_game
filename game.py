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

        self.bg_image, self.platforms = level_select(1)

        self.font = pygame.font.SysFont("Arial" , 20 , bold = True)

        self.player1 = Javi(self.render_surf, x = 300, y = 200, controls=1)
        self.player2 = Javi(self.render_surf, x = 1500, y = 200, controls=2)
        
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
            player.update(self.platforms, self.players)


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

        self.render_surf.blit(self.bg_image, (0, 0))

        for player in self.players:
            player.draw()

        zoomed_rect = self.find_zoom_rect()

        zoomed_area = self.render_surf.subsurface(zoomed_rect)

        for player in self.players:
            player.draw_health(zoomed_area)

        sw = self.screen.get_width()
        sh = self.screen.get_height()

        pygame.transform.scale(zoomed_area, (sw, sh), dest_surface=self.screen)

        pygame.display.flip()
