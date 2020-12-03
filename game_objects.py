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
        self.body = body
        self.shape = shape
