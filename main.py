import pygame
from world import World
from config import *

SEED = True
INTERACTIVE = True
INTERACTIVE_KEYPRESS = False

pygame.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((WORLD_X * TILESIZE * SCALETILE, WORLD_Y * TILESIZE * SCALETILE))
pygame.display.set_caption('WFC')

world = World(WORLD_X, WORLD_Y)

running = True
done = False

if not INTERACTIVE:
    while running:
        result = world.wave_function_collapse()
        if not result:
            running = False
else:
    mouse_pos = pygame.mouse.get_pos()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    if INTERACTIVE == True and INTERACTIVE_KEYPRESS == True:
                        world.wave_function_collapse()
                        world.update()

        if INTERACTIVE == True and INTERACTIVE_KEYPRESS == False:
            if not done:
                result = world.wave_function_collapse()
                if result == 0:
                    pygame.image.save(display, 'world.png')
                    done = True
            world.update()

        world.render(display)
        pygame.display.flip()
        clock.tick(30)

pygame.quit()