import pymunk
import pygame
from pymunk import Vec2d
import random
import math


class Ball:
    def __init__(self, angle, x, y, space):
        mass = 5
        radius = 15
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.position = x, y
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.95
        shape.friction = 1
        shape.collision_type = 0
        shape.add(body, shape)
        self.body = body
        self.shape = shape


class Brick:
    def __init__(self, space, size=(30, 30)):
        mass = 5
        moment = 1000
        body = pymunk.Body(mass, moment)
        body.position = Vec2d()
        shape = pymunk.Poly.create_box(body, size)
        shape.friction = 0.5
        shape.collision_type = 1
        shape.add(body, shape)
        self.body = body
        self.shape = shape
        self.image = pygame.image.load("")

    def to_pygame(self, p):
        return int(p.x), int(-p.y + 600)
