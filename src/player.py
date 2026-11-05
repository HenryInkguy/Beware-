import pygame

from src import config

class Player:
    """The main character, controlled by the player."""
    
    def __init__(self,x,y):
        self.pos = pygame.Vector2(x,y)
        self.speed = config.PLAYER_SPEED
        self.radius = config.PLAYER_RADIUS
        self.color = config.PLAYER_COLOR
        
    def update(self, dt):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0,0)
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1
        
        # Diagonal Movement
        if direction.length() > 0:
            direction = direction.normalize()
        
        self.pos += direction * self.speed * dt
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        