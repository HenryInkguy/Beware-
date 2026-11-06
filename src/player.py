import pygame

from src import config

class Player:
    """The main character, controlled by the player."""
    
    def __init__(self,x,y):
        self.pos = pygame.Vector2(x,y)
        self.speed = config.PLAYER_SPEED
        self.radius = config.PLAYER_RADIUS
        self.color = config.PLAYER_COLOR
        
        # Stamina
        
        self.max_stamina = config.PLAYER_STAMINA
        self.stamina = self.max_stamina
        self.exhausted = False
        self.regen_timer = 0.0
        
        self.aim_direction = pygame.Vector2(1,0)    
    
        
    def update(self, dt):
        current_speed = self.speed
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0,0)
        

            
        
        # Movements
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1 
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1 
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1 
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1
        
        # Diagonal Movement
        moving = direction.length() > 0
        if moving:
            direction = direction.normalize()

        # Sprinting
        wants_sprint = keys[pygame.K_LSHIFT] and moving
        sprinting = wants_sprint and self.stamina > 0 and not self.exhausted
        

        
        if sprinting:
            current_speed *= config.SPRINT_MULTIPLIER
            self.stamina -= config.STAMINA_DRAIN_RATE * dt
            self.regen_timer = 0.0
            
            if self.stamina <= 0:
                self.stamina = 0
                self.exhausted = True
            
            
        else:
            
            self.regen_timer += dt
            
            if self.regen_timer >= config.STAMINA_REGEN_DELAY:
                self.stamina += config.STAMINA_REGEN_RATE * dt
                self.stamina = min(self.stamina, self.max_stamina)

            if self.exhausted and self.stamina >= config.STAMINA_RECOVER_MIN:
                self.exhausted = False
        
        
        
        self.pos += direction * current_speed * dt
        
        
    def update_aim(self):
        """Points the aim at the mouse cursor."""
        
        to_mouse = pygame.Vector2(pygame.mouse.get_pos()) - self.pos
        
        if to_mouse.length() > 0:
            self.aim_direction = to_mouse.normalize()
        
    
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)
        self.draw_stamina_bar(screen)
        
        aim_end = self.pos + self.aim_direction * config.AIM_LINE_LENGTH
        pygame.draw.line(screen, self.color, self.pos, aim_end, config.AIM_LINE_WIDTH)
        
                
    def draw_stamina_bar(self, screen):
        """Stamina Bar, duh."""
        
        x, y, w, h = 20, 30, 200, 16
        ratio = self.stamina / self.max_stamina
        
        # Background
        
        pygame.draw.rect(screen,(40,40,40), (x,y,w,h))
        color = (200, 60, 60) if self.exhausted else (80, 200, 120)
        pygame.draw.rect(screen, color, (x,y, w * ratio, h))
        
        pygame.draw.rect(screen, (255, 255, 255), (x, y, w, h), 2)
        