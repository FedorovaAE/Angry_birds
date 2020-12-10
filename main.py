import sys
from pygame import *
import pymunk.pygame_util
from settings import *
from level import *
from game_objects import *
import time

# Pygame
pygame.init()
pygame.display.set_caption("Slingshot")
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
# физика
space = pymunk.Space()
space.gravity = (0.0, -700.0)
draw_options = pymunk.pygame_util.DrawOptions(screen)
# обновнление физики каждую секунду
dt = 1.0 / FPS / 2.
upd = dt

balls = []
bricks = []
score = 0
x_mouse = 0
y_mouse = 0
game_state = 4
mouse_distance = 0
angle = 0
counter = 0
effect_volume1 = 0.5
effect_volume2 = 0.2
music_volume = 0.5
rope_length = 90
sling_x, sling_y = 150, 490
sling2_x, sling2_y = 170, 490
restart_counter = False
bonus_score = True
audio = True
music = True
mouse_pressed = False
# шрифты
normal_font = pygame.font.SysFont("arial", 14, bold=True)
font2 = pygame.font.Font("704.ttf", 42)
# создаем пол и стену как статические объекты
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
    # возвращаем вектор из точек p0 = (xo, yo), p1 = (x1, y1)
    ax = p1[0]-p0[0]
    by = p1[1]-p0[1]
    return ax, by


def unit_vector(my_vector):
    # возвращает единичный вектор точек
    h = ((my_vector[0] ** 2) + (my_vector[1] ** 2)) ** 0.5
    if h == 0:
        h = 0.000000000000001
    ua = my_vector[0] / h
    ub = my_vector[1] / h
    return ua, ub


def distance(x_0, y_0, x1, y1):
    # расстояние между точками
    dx = x1 - x_0
    dy = y1 - y_0
    d = ((dx ** 2) + (dy ** 2)) ** 0.5
    return d


def sling_action():
    # Настройка поведения рогатки
    global mouse_distance
    global angle
    global rope_length
    global x_mouse
    global y_mouse
    # Фиксируем шарик к веревке рогатки
    vec = vector((sling_x, sling_y), (x_mouse, y_mouse))
    unit_vec = unit_vector(vec)
    unit_vec_x = unit_vec[0]
    unit_vec_y = unit_vec[1]
    mouse_distance = distance(sling_x, sling_y, x_mouse, y_mouse)
    pos_unit = (unit_vec_x * rope_length + sling_x, unit_vec_y * rope_length + sling_y)
    bigger_rope = 100
    x_ball = x_mouse - 15
    y_ball = y_mouse - 15
    if mouse_distance > rope_length:
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


def draw_level_failed():
    # уровень провален
    global game_state
    failed_caption = font2.render("ВЫ ПРОИГРАЛИ", True, WHITE)
    if level.number_of_balls <= 0 < len(bricks) and \
            time.time() - t1 > 5 and game_state != 1:
        game_state = 2
        screen.blit(failed_caption, (425, 200))
        screen.blit(repeat, (575, 300))


def draw_level_complete():
    # уровень успешно завершен
    global game_state
    global score
    global bonus_score
    level_complete_caption = font2.render("УРОВЕНЬ ЗАВЕРШЕН", True, WHITE)
    if level.number_of_balls >= 0 and len(bricks) == 0 and game_state != 1:
        if bonus_score:
            score += level.number_of_balls * 5000
        bonus_score = False
        game_state = 3
        if score > 30000:
            screen.blit(star, (320, 100))
        if score > 50000:
            screen.blit(star, (520, 100))
        if score > 70000:
            screen.blit(star, (720, 100))
        screen.blit(level_complete_caption, (375, 350))
        screen.blit(repeat, (525, 300))
        screen.blit(resume, (625, 300))


def restart():
    # удаление всех объектов уровня
    global bonus_score
    balls_to_remove = []
    bricks_to_remove = []
    for ball in balls:
        balls_to_remove.append(ball)
    for ball in balls_to_remove:
        space.remove(ball.shape, ball.shape.body)
        balls.remove(ball)
    for brick in bricks:
        bricks_to_remove.append(brick)
    for brick in bricks_to_remove:
        space.remove(brick.shape, brick.shape.body)
        bricks.remove(brick)
    bonus_score = True


def post_solve_ball_brick(arbiter, space, _):
    # Столкновение между шаром и кирпичом
    global score
    brick_to_remove = []
    if arbiter.total_impulse.length > 1100:
        a, b = arbiter.shapes
        for brick in bricks:
            if b == brick.shape:
                # звук столкновения
                brick_crashed_song = pygame.mixer.Sound(brick_crashed)
                brick_crashed_song.play()
                brick_crashed_song.set_volume(effect_volume1)
                brick_to_remove.append(brick)
                number_of_the_ball = level.count_of_balls - level.number_of_balls
                if number_of_the_ball > 0:
                    score += round(5000 / number_of_the_ball)

        for brick in brick_to_remove:
            bricks.remove(brick)

        space.remove(b, b.body)


def post_solve_brick_floor(arbiter, space, _):
    # Столкновение между кирпичом и полом
    global score
    brick_to_remove = []
    a, b = arbiter.shapes
    for brick in bricks:
        if a == brick.shape and (not brick.isBase or
                                 (brick.isBase and math.fabs(round(math.degrees(brick.shape.body.angle))) == 90)):
            # звук столкновения
            brick_crashed_song = pygame.mixer.Sound(brick_crashed)
            brick_crashed_song.play()
            brick_crashed_song.set_volume(effect_volume1)

            brick_to_remove.append(brick)
            space.remove(a, a.body)
            number_of_the_ball = level.count_of_balls - level.number_of_balls
            if number_of_the_ball > 0:
                score += round(5000 / number_of_the_ball)
    for brick in brick_to_remove:
        bricks.remove(brick)


def post_solve_ball_floor(arbiter, space, _):
    # Столкновение между шаром и полом/стеной
    if arbiter.total_impulse.length > 2000:
        a, b = arbiter.shapes
        for ball in balls:
            if a == ball.shape:
                # звук столкновения
                jump_song = pygame.mixer.Sound(jump)
                jump_song.play()
                jump_song.set_volume(effect_volume2)


# взаимодействие шариков и кирпичей
space.add_collision_handler(0, 1).post_solve = post_solve_ball_brick
# взаимодействие неподвижных объектов и кирпичей
space.add_collision_handler(1, 2).post_solve = post_solve_brick_floor
# взаимодействие шариков и неподвижных объектов
space.add_collision_handler(0, 2).post_solve = post_solve_ball_floor

# фоновая музыка
pygame.mixer.music.load(bg_song)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(music_volume)

# постановка кирпичей на уровне
level = Level(bricks, space)
level.load_level()

while True:
    # фон игры
    screen.fill(WHITE)
    screen.blit(background, (0, -50))

    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            sys.exit(0)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 \
                and (x_mouse < 400 and y_mouse > 100) and game_state == 0:
            mouse_pressed = True

        elif event.type == pygame.MOUSEBUTTONUP and mouse_pressed:
            # выпускаем новый шар
            mouse_pressed = False
            if level.number_of_balls > 0:
                level.number_of_balls -= 1
                x0 = 164
                y0 = 163
                if mouse_distance > rope_length:
                    mouse_distance = rope_length
                # звук вылета
                trow_song = pygame.mixer.Sound(throw)
                trow_song.play()
                trow_song.set_volume(effect_volume2)

                if x_mouse < sling_x:
                    ball = Ball(mouse_distance, angle, x0, y0, space)
                    balls.append(ball)
                else:
                    ball = Ball(-mouse_distance, angle, x0, y0, space)
                    balls.append(ball)
                if level.number_of_balls == 0:
                    t1 = time.time()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if (10 <= x_mouse <= 60) and (10 <= y_mouse <= 60):
                # кнопка паузы
                upd = 0
                game_state = 1
            if game_state == 0:
                # Играть
                upd = dt
            if game_state == 1:
                if (425 <= x_mouse <= 475) and (300 <= y_mouse <= 350):
                    # кнопка продолжить играть
                    upd = dt
                    game_state = 0
                if (525 <= x_mouse <= 575) and (300 <= y_mouse <= 350):
                    # кнопка начать заново
                    restart()
                    level.load_level()
                    game_state = 0
                    score = 0
                if (625 <= x_mouse <= 675) and (300 <= y_mouse <= 350):
                    # кнопка вкл/выкл звуков
                    audio = not audio
                    if audio:
                        effect_volume1 = 0.2
                        effect_volume2 = 0.5
                    else:
                        effect_volume1 = effect_volume2 = 0
                if (725 <= x_mouse <= 775) and (300 <= y_mouse <= 350):
                    # кнопка вкл/выкл музыки
                    music = not music
                    if music:
                        music_volume = 0.5
                    else:
                        music_volume = 0
                    pygame.mixer.music.set_volume(music_volume)
            if game_state == 2:
                # проигрыш
                if (575 <= x_mouse <= 625) and (300 <= y_mouse <= 350):
                    # повторить уровень
                    restart()
                    level.load_level()
                    game_state = 0
                    score = 0
            if game_state == 3:
                # уровень успешно завершен
                if (525 <= x_mouse <= 575) and (300 <= y_mouse <= 350):
                    # кнопка повтора
                    restart()
                    level.load_level()
                    game_state = 0
                    score = 0
                if (625 <= x_mouse <= 675) and (300 <= y_mouse <= 350):
                    # кнопка следующий уровень
                    restart()
                    level.number += 1
                    game_state = 0
                    level.load_level()
                    score = 0
            if game_state == 4:
                if (575 <= x_mouse <= 625) and (300 <= y_mouse <= 350):
                    # начальный запуск игры
                    game_state = 0

    # позиция мышки
    x_mouse, y_mouse = pygame.mouse.get_pos()
    balls_to_remove = []
    # русуем рогатку
    screen.blit(sling_shot_back, (140, 470))
    # след от мяча
    counter += 1
    if restart_counter:
        counter = 0
        restart_counter = False

    # шарики, которые ждут
    if level.number_of_balls > 0:
        for i in range(level.number_of_balls - 1):
            x = 110 - (i * 32.5)
            screen.blit(ball_img, (x, 570))

    # стрельба из рогатки
    if mouse_pressed and level.number_of_balls > 0:
        sling_action()
    else:
        if level.number_of_balls > 0:
            screen.blit(ball_img, (150, 475))
        else:
            pygame.draw.line(screen, ROPE_BACK_COLOR, (sling_x, sling_y + 2), (sling2_x, sling2_y), 5)

    for ball in balls:
        # шарики для удаления
        if ball.body.position.y < 60:
            balls_to_remove.append(ball)
        # положение мяча
        p = ball.body.position
        p = Vec2d(to_pygame(p))
        # след
        for point in ball.ball_path:
            pygame.draw.circle(screen, ball.path_color, point, 3, 0)
        # добавить / удалить след
        if counter >= 3:
            ball.ball_path.append(p + (0, 50))
            restart_counter = True
            if len(ball.ball_path) >= 20:
                ball.ball_path.pop(0)

        # Поворот изображения шара и установка координат
        angle_degrees = math.degrees(ball.body.angle) + 180
        rotated_logo_img = pygame.transform.rotate(ball_img, angle_degrees)
        offset = Vec2d(rotated_logo_img.get_size()) / 2.
        p = p - offset + (0, 50)
        # рисовка крутящегося шарика
        screen.blit(rotated_logo_img, p)
    # рисуем  кирпичи
    for brick in bricks:
        brick.draw_brick(screen)
    # удалить шарики
    for ball in balls_to_remove:
        space.remove(ball.shape, ball.shape.body)
        balls.remove(ball)
    # задняя сторона рогатки
    screen.blit(sling_shot_front, (140, 470))
    # рисование иконок
    screen.blit(pause, (10, 10))
    if game_state == 1:
        pause_caption = font2.render("ПАУЗА", True, WHITE)
        screen.blit(pause_caption, (520, 200))
        screen.blit(resume, (425, 300))
        screen.blit(repeat, (525, 300))
        if audio:
            screen.blit(audio_on, (625, 300))
        else:
            screen.blit(audio_off, (625, 300))
        if music:
            screen.blit(music_on, (725, 300))
        else:
            screen.blit(music_off, (725, 300))
    # первое положение игры - запуск
    if game_state == 4:
        start_caption = font2.render("НАЧАТЬ ИГРУ", True, WHITE)
        screen.blit(start_caption, (435, 200))
        screen.blit(resume, (575, 300))

    # вывод на экран счета
    score_value = normal_font.render(str(score), True, WHITE)
    score_caption = normal_font.render("score: ", True, WHITE)
    if score == 0:
        screen.blit(score_caption, (545, 20))
        screen.blit(score_value, (590, 20))
    else:
        screen.blit(score_caption, (535, 20))
        screen.blit(score_value, (580, 20))

    draw_level_complete()
    draw_level_failed()
    # курсор
    if not mouse_pressed:
        screen.blit(cursor, (x_mouse, y_mouse))
    else:
        screen.blit(cursor_pressed, (x_mouse, y_mouse))
    # обновление физики
    for x in range(2):
        space.step(upd)
    pygame.display.flip()
    clock.tick(FPS)
