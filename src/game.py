import pygame

from src import config
from src.player import Player

class Game:
    """The main thing happens here, lop, input, update, draw."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        pygame.display.set_caption(config.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.player = Player(config.WIDTH / 2, config.HEIGHT / 2 )
    
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def update(self, dt):
        self.player.update(dt)
    
    def draw(self):
        self.screen.fill(config.BACKGROUND_COLOR)
        self.player.draw(self.screen)
        pygame.display.flip()
        
    def run(self):
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()
        