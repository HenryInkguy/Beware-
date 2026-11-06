import pygame

from src import config

# "#" = wall, "." = floor, "P" = player start.
# Every row must have the same length (30 columns, 17 rows).
LAYOUT = [
    "##################################################################",
    "#............#...................................................#",
    "#..P.........#...................................................#",
    "#............#...............#...................................#",
    "#............................#...................................#",
    "#.....,......................#...................................#",
    "#............#...............#...................................#",
    "#............#......###......#...................................#",
    "#............#......###......#...................................#",
    "#............#...............#...................................#",
    "#.....,......#...............#...................................#",
    "#............#...............#...................................#",
    "#............................#...................................#",
    "#.....,...............,......#...................................#",
    "#............#...............#...................................#",
    "#............#...............#...................................#",
    "##################################################################",
]

class Tilemap:
    """A grid of tiles built from a text layout."""
    
    def __init__(self,layout=LAYOUT):
        self.rows = len(layout)
        self.cols = len(layout[0])
        self.grid = []
        self.player_start = pygame.Vector2(0,0)
        
        for row_index, row in enumerate(layout):
            grid_row = []
            for col_index, char in enumerate(row):
                if char == "P":
                    self.player_start = pygame.Vector2(
                        (col_index + 0.5) * config.TILE_SIZE,
                        (row_index + 0.5) * config.TILE_SIZE
                    )
                    char = "."
                grid_row.append(char)
            self.grid.append(grid_row)
        self.surface = self._build_surface()
        
    def _build_surface(self):
        """Draws the whole map once."""
        
        size = config.TILE_SIZE
        surface = pygame.Surface((self.cols * size, self.rows * size))
        surface.fill(config.FLOOR_COLOR)
        
        for row_index, grid_row in enumerate(self.grid):
            for col_index, char in enumerate(grid_row):
                if char == "#":
                    wall = pygame.Rect(col_index * size, row_index * size, size, size)
                    pygame.draw.rect(surface, config.WALL_COLOR, wall)
                elif char == ',':
                    cracked_floor = pygame.Rect(col_index * size, row_index * size, size, size)
                    pygame.draw.rect(surface, config.CRACKED_FLOOR_COLOR, cracked_floor)
                    
                
        return surface
    
    def get_walls_near(self, rect):
        """Yields the wall rects that overlap the tiles around rect."""
        
        size = config.TILE_SIZE
        first_col = max(rect.left // size, 0)
        last_col = min(rect.right // size, self.cols - 1)
        first_row = max(rect.top // size, 0)
        last_row = min(rect.bottom // size, self.rows - 1)
        
        for row in range(first_row, last_row + 1):
            for col in range(first_col, last_col + 1):
                if self.grid[row][col] == "#":
                    yield pygame.Rect(col*size, row*size, size, size)
    
    def draw(self, screen):
        screen.blit(self.surface, (0,0))