import pygame

# размер окна
SCREEN_SIZE = (WIDTH, HEIGHT) = (1200, 650)
# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROPE_BACK_COLOR = (68, 36, 103)
ROPE_FRONT_COLOR = (97, 63, 121)

FPS = 50
# импорт изображений
background = pygame.image.load('images/bg1.jpg')
sling_shot_back = pygame.image.load('images/sling-shot-back2.png')
sling_shot_front = pygame.image.load('images/sling-shot-front2.png')
ball_img = pygame.image.load('images/ball_new.png')
repeat = pygame.image.load('images/return.png')
resume = pygame.image.load('images/resume.png')

# музыка
brick_crashed = 'music/glassy-tap.wav'
throw = 'music/stuff-up.wav'
jump = 'music/jump.ogg'
bg_song = 'music/bg.mp3'
