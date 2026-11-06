import pygame

from src import config
from src.player import Player
from src.tilemap import Tilemap

class Game:
    """The main thing happens here, lop, input, update, draw."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.player = Player(config.WIDTH / 2, config.HEIGHT / 2 )
        
        self.tilemap = Tilemap()
        
        start = self.tilemap.player_start
        
        self.font = pygame.font.SysFont(None, config.FONT_SIZE)
        
        self.fps_timer = 0
        self.fps_image = None
        self.fps_image2 = None
        
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    
    def update(self, dt):
        self.player.update(dt, self.tilemap)
        
        self.fps_timer -= dt
        if self.fps_timer <= 0 or self.fps_image is None:
            self.fps_timer = config.UPDATE_INTERVAL
            text = f"{self.clock.get_fps():.0f}"
            self.fps_image = self.font.render(text, True, config.FPS_COLOR)
            self.fps_image2 = self.font.render(f"FPS: ", True, config.FPS_COLOR)
    
    def draw(self):
        self.screen.fill(config.BACKGROUND_COLOR)
        self.tilemap.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.flip()
        self.draw_fps()
        pygame.display.flip()
        
        




    def draw_fps(self):
        self.screen.blit(self.fps_image, (40,10))
        self.screen.blit(self.fps_image2, (5,10))
        
        
    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000
            dt = min(dt, config.MAX_DT)
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        

        