import pygame
from world import World
from config import *

pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((WORLD_X * TILESIZE * SCALETILE, WORLD_Y * TILESIZE * SCALETILE))
pygame.display.set_caption('WFC')

world = World(WORLD_X, WORLD_Y)

running = True

while running:
    print(running)
    result = world.wave_function_collapse()
    if not result:
        running = False

world.update()

running = True

while running:

    world.render(display)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()