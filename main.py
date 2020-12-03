import pymunk
import time
import sys
from pymunk import Vec2d
from pygame import *
import random
import math
import pymunk.pygame_util
from settings import *

# Pygame
pygame.init()
pygame.display.set_caption("Моя курсовая")
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
# Physics
space = pymunk.Space()
space.gravity = (0.0, -700.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)
# Update physics per second
dt = 1.0 / FPS / 2.
upd = dt

x_mouse = 0
y_mouse = 0
score = 0
game_state = 0
# Fonts
normal_font = pygame.font.SysFont("arial", 14, bold=False)
# Static floor
static_body = pymunk.Body(body_type=pymunk.Body.STATIC)
static_lines = [pymunk.Segment(static_body, (0.0, 60.0), (1200.0, 60.0), 0.0),
                pymunk.Segment(static_body, (1200.0, 60.0), (1200.0, 800.0), 0.0)]
for line in static_lines:
    line.elasticity = 0.95
    line.friction = 1
    line.collision_type = 2

space.add(static_lines)


# приведение координат pymunk к координатам pygame
def to_pygame(p):
    return int(p.x), int(-p.y + 600)


while True:
    screen.fill(WHITE)
    screen.blit(background, (0, -50))
    keys = pygame.key.get_pressed()
    for i in pygame.event.get():
        if i.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            sys.exit(0)
    for x in range(2):
        space.step(upd)
    pygame.display.flip()
    clock.tick(FPS)
