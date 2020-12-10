import pygame

# размер окна
SCREEN_SIZE = (WIDTH, HEIGHT) = (1200, 650)
# цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROPE_BACK_COLOR = (68, 36, 103)
ROPE_FRONT_COLOR = (97, 63, 121)
# такт
FPS = 50
# импорт изображений
background = pygame.image.load('images/bg1.jpg')
sling_shot_back = pygame.image.load('images/sling-shot-back2.png')
sling_shot_front = pygame.image.load('images/sling-shot-front2.png')
ball_img = pygame.image.load('images/ball_new.png')
repeat = pygame.image.load('images/return.png')
resume = pygame.image.load('images/resume.png')
pause = pygame.image.load('images/pause.png')
audio_on = pygame.image.load('images/audioOn.png')
audio_off = pygame.image.load('images/audioOff.png')
music_on = pygame.image.load('images/musicOn.png')
music_off = pygame.image.load('images/musicOff.png')
cursor = pygame.image.load('images/cursor.png')
cursor_pressed = pygame.image.load('images/cursor_pressed.png')
star = pygame.image.load('images/01-19.png')

# музыка
brick_crashed = 'music/glass-smash.mp3'
throw = 'music/stuff-up.wav'
jump = 'music/jump.ogg'
bg_song = 'music/bg_music.mp3'
