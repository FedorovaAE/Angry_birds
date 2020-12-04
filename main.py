import pymunk
import time
import sys
from pymunk import Vec2d
from pygame import *
import random
import math
import pymunk.pygame_util
from settings import *
from level import *
from game_objects import *

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
mouse_distance = 0
angle = 0
rope_lenght = 90
sling_x, sling_y = 150, 490
sling2_x, sling2_y = 170, 490
balls = []
mouse_pressed = False  # нажата ли мышка
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


def vector(p0, p1):
    a = p1[0]-p0[0]
    b = p1[1]-p0[1]
    return a, b


def unit_vector(my_vector):
    h = ((my_vector[0] ** 2) + (my_vector[1] ** 2)) ** 0.5
    if h == 0:
        h = 0.000000000000001  # на ноль делить нельзя
    ua = my_vector[0] / h
    ub = my_vector[1] / h
    return ua, ub


def distance(x0, y0, x, y):
    dx = x - x0
    dy = y - y0
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


def sling_action():
    global mouse_distance
    global angle
    global rope_lenght
    global x_mouse
    global y_mouse

    vec = vector((sling_x, sling_y), (x_mouse, y_mouse))
    unit_vec = unit_vector(vec)
    unit_vec_x = unit_vec[0]
    unit_vec_y = unit_vec[1]
    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
    pos_unit = (unit_vec_x * rope_lenght + sling_x, unit_vec_y * rope_lenght + sling_y)
    bigger_rope = 100
    x_ball = x_mouse - 15
    y_ball = y_mouse - 15
    if mouse_distance > rope_lenght:
        pos_unit_x, pos_unit_y = pos_unit
        pos_unit_x -= 15
        pos_unit_y -= 15
        pos_unit_ball = pos_unit_x, pos_unit_y
        pos_unit_2 = (unit_vec_x * bigger_rope + sling_x, unit_vec_y * bigger_rope + sling_y)
        pygame.draw.line(screen, ROPE_BACK_COLOR, (sling2_x, sling2_y), pos_unit_2, 5)
        screen.blit(ball_img, pos_unit_ball)
        pygame.draw.line(screen, ROPE_FRONT_COLOR, (sling_x, sling_y), pos_unit_2, 5)
    else:
        mouse_distance += 10
        pos_unit_3 = (unit_vec_x * mouse_distance + sling_x, unit_vec_y * mouse_distance + sling_y)
        pygame.draw.line(screen, ROPE_BACK_COLOR, (sling2_x, sling2_y), pos_unit_3, 5)
        screen.blit(ball_img, (x_ball, y_ball))
        pygame.draw.line(screen, ROPE_FRONT_COLOR, (sling_x, sling_y), pos_unit_3, 5)
        # Угол импульса
        dy = y_mouse - sling_y
        dx = x_mouse - sling_x
        if dx == 0:
            dx = 0.00000000000001
        angle = math.atan((float(dy)) / dx)


level = Level(space)

while True:
    screen.fill(WHITE)
    screen.blit(background, (0, -50))
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            sys.exit(0)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                and (x_mouse < 400 and y_mouse > 100) and game_state == 0:
            mouse_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and mouse_pressed:
            mouse_pressed = False
            if level.number_of_bolls > 0:
                level.number_of_bolls -= 1
                x0 = 164
                y0 = 163
                if mouse_distance > rope_lenght:
                    mouse_distance = rope_lenght

                    if x_mouse < sling_x:
                        ball = Ball(mouse_distance, angle, x0, y0, space)
                        balls.append(ball)
                    else:
                        ball = Ball(-mouse_distance, angle, x0, y0, space)
                        balls.append(ball)
                    if level.number_of_bolls == 0:
                        t1 = time.time()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == 0:
                    # Play game
                    upd = dt

    x_mouse, y_mouse = pygame.mouse.get_pos()

    balls_to_remove = []

    # русуем рогатку
    screen.blit(sling_shot_back, (140, 470))


    if level.number_of_bolls > 0:
        for i in range(level.number_of_bolls - 1):
            x = 110 - (i * 32.5)
            screen.blit(ball_img, (x, 570))

    if mouse_pressed and level.number_of_bolls > 0:
        sling_action()
    else:
        if level.number_of_bolls > 0:
            screen.blit(ball_img, (150, 475))
        else:
            pygame.draw.line(screen, ROPE_BACK_COLOR, (sling_x, sling_y + 2), (sling2_x, sling2_y), 5)

    for ball in balls:
        if ball.body.position.y < 60:
            balls_to_remove.append(ball)

        p = ball.body.position
        p = Vec2d(to_pygame(p))

        # Rotate of the ball image and set coordinates
        angle_degrees = math.degrees(ball.body.angle) + 180
        rotated_logo_img = pygame.transform.rotate(ball_img, angle_degrees)
        offset = Vec2d(rotated_logo_img.get_size()) / 2.
        p = p - offset + (0, 50)
        # Draw sprite ball
        screen.blit(rotated_logo_img, p)

    screen.blit(sling_shot_front, (140, 470))

    for x in range(2):
        space.step(upd)
    pygame.display.flip()
    clock.tick(FPS)
