import pygame, random
from tile import Tile
from stack import Stack
from config import *

class World:
    def __init__(self, width, height):
        self.x = width
        self.y = height

        self.tile_rows = []
        for y in range(self.y):
            tiles = []
            for x in range(self.x):
                tile = Tile()
                tiles.append(tile)
            self.tile_rows.append(tiles)

        for y in range(self.y):
            for x in range(self.x):
                tile = self.tile_rows[y][x]
                if y > 0:
                    tile.add_neighbor(NORTH, self.tile_rows[y - 1][x])
                if x < self.x - 1:
                    tile.add_neighbor(EAST, self.tile_rows[y][x + 1])
                if y < self.y - 1:
                    tile.add_neighbor(SOUTH, self.tile_rows[y + 1][x])
                if x > 0:
                    tile.add_neighbor(WEST, self.tile_rows[y][x - 1])

        self.font0 = pygame.font.Font(pygame.font.get_default_font(), 14)
        self.font1 = pygame.font.Font(pygame.font.get_default_font(), 11)
        self.font2 = pygame.font.Font(pygame.font.get_default_font(), 8)
        self.spritesheet = pygame.image.load(SPRITESHEET_PATH).convert_alpha()
        self.world_surface = pygame.Surface((WORLD_X * TILESIZE * SCALETILE, WORLD_Y * TILESIZE * SCALETILE))

    def get_entropy(self, x, y):
        return self.tile_rows[y][x].entropy
    
    def get_type(self, x, y):
        return self.tile_rows[y][x].possibilities[0]
    
    def get_lowest_entropy(self):
        lowest = len(list(tile_rules.keys()))
        for y in range(self.y):
            for x in range(self.x):
                tile_entropy = self.tile_rows[y][x].entropy
                if tile_entropy > 0:
                    if tile_entropy < lowest:
                        lowest = tile_entropy
        return lowest
    
    def get_tiles_lowest_entropy(self):
        lowest = len(list(tile_rules.keys()))
        tile_list = []

        for y in range(self.y):
            for x in range(self.x):
                tile_entropy = self.tile_rows[y][x].entropy
                if tile_entropy > 0:
                    if tile_entropy < lowest:
                        tile_list.clear()
                        lowest = tile_entropy
                    if tile_entropy == lowest:
                        tile_list.append(self.tile_rows[y][x])
        return tile_list
    
    def wave_function_collapse(self):
        lowest_entropy_tiles = self.get_tiles_lowest_entropy()

        if len(lowest_entropy_tiles) == 0:
            pygame.image.save(self.world_surface, 'world.png')
            return False
        
        collapse_tile = random.choice(lowest_entropy_tiles)
        collapse_tile.collapse()

        stack = Stack()
        stack.push(collapse_tile)

        while not stack.is_empty():
            tile = stack.pop()
            tile_possibilities = tile.get_possibilities()
            directions = tile.get_directions()

            for direction in directions:
                neighbor = tile.get_neighbor(direction)
                if neighbor.entropy != 0:
                    reduced = neighbor.constrain(tile_possibilities, direction)
                    if reduced == True:
                        stack.push(neighbor)

        return True

    def update(self):
        lowest_entropy = self.get_lowest_entropy()
        for y in range(WORLD_Y):
            for x in range(WORLD_X):
                tile_entropy = self.get_entropy(x, y)
                tile_type = self.get_type(x, y)
                if tile_entropy > 0:
                    tile_image = pygame.Surface((TILESIZE, TILESIZE))
                    if tile_entropy == 27:
                        text_surf = self.font2.render(str(tile_entropy), True, 'darkgrey')
                        tile_image.blit(text_surf, (3, 3))
                    elif tile_entropy >= 10:
                        text_surf = self.font1.render(str(tile_entropy), True, 'grey')
                        tile_image.blit(text_surf, (3, 3))
                    elif tile_entropy < 10:
                        if tile_entropy == lowest_entropy:
                            text_surf = self.font0.render(str(tile_entropy), True, 'green')
                        else:
                            text_surf = self.font0.render(str(tile_entropy), True, 'white')
                        tile_image.blit(text_surf, (4, 1))
                elif tile_type < TILE_FORESTN:
                    pos = tile_sprites[tile_type]
                    tile_image = self.spritesheet.subsurface(pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE))
                else:
                    pos = tile_sprites[TILE_GRASS]
                    tile_image = self.spritesheet.subsurface(pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE))
                    tile_image = pygame.transform.scale_by(tile_image, (SCALETILE, SCALETILE))
                    self.world_surface.blit(tile_image, (x * TILESIZE * SCALETILE, y * TILESIZE * SCALETILE))
                    pos = tile_sprites[tile_type]
                    tile_image = self.spritesheet.subsurface(pygame.Rect(pos[0], pos[1], TILESIZE, TILESIZE))

                tile_image = pygame.transform.scale_by(tile_image, (SCALETILE, SCALETILE))
                self.world_surface.blit(tile_image, (x * TILESIZE * SCALETILE, y * TILESIZE * SCALETILE))

    def render(self, surf):
        surf.blit(self.world_surface, (0, 0))