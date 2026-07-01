import pygame
import sys
import csv

from assets.images.img import player
from src.game import *

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED)

pygame.display.set_caption('маг в аду')
pygame.display.set_icon(pygame.image.load('./assets/images/icon.png'))

clock = pygame.time.Clock()
MAX_FPS = 60

font = pygame.font.SysFont(None, 20)

def text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main_menu ():
    click = False
    while True:
        screen.fill((50, 50, 50))
        text('main_menu', font, (255, 255, 255), screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        buttonPlay = pygame.Rect(50, 100, 200, 50)
        buttonOptions = pygame.Rect(50, 200, 200, 50)
        if buttonPlay.collidepoint((mx, my)):
            if click:
                game()
                # test()
        if buttonOptions.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (255, 0, 0), buttonPlay)
        pygame.draw.rect(screen, (255, 0, 0), buttonOptions)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game()

        pygame.display.flip()
        clock.tick(MAX_FPS)


def game():
    ROWS = 50
    MAX_COLS = 150
    TILE_SIZE = HEIGHT // 16
    TILE_TYPES = 24
    MAX_LEVELS = 9
    level = 1
    circle = 1
    moving_left = False
    moving_right = False
    moving_up = False
    moving_down = False
    hand_use = False
    dash = False
    ligthning = False
    ligthning_time = 0
    scroll_x = 0
    scroll_y = 0

    img_list = []
    for x in range(TILE_TYPES):
        img = pygame.image.load(f'Level Editor 1/tile/{x}.png')
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)


    world_data = []
    for row in range(ROWS):
        r = [-1] * MAX_COLS
        world_data.append(r)
    with open(f'assets/map/circle{circle}/level{level}_data.csv', newline='') as csvfile:
        render = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(render):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

    world = World()
    peoples = world.process_data(world_data, img_list, TILE_SIZE)

    while True:

        screen.fill((200, 25, 25))

        world.draw(scroll_x, scroll_y)

        text('game', font, (255, 255, 255), screen, 20, 20)

        if peoples.alive:
            if not peoples.abilities_use:
                dash = False
            if dash:
                peoples.dash(moving_left, moving_right, moving_up, moving_down)
                peoples.update_action(4)
            else:
                peoples.speed = 5
                peoples.is_dash = False
                peoples.mana_use = False
                if ligthning and ligthning_time <= 10:
                    if ligthning_time % 8 ==0:
                        peoples.lightning_strike()
                    ligthning_time += 1
                else:
                    ligthning = False
                    ligthning_time = 0
                if hand_use:
                    peoples.hand()
                peoples.move(moving_left, moving_right)
                if peoples.in_air:
                    peoples.update_action(2)  # 2: Jump
                elif moving_left or moving_right:
                    peoples.update_action(1)  # 1: Run
                else:
                    peoples.update_action(0)

        scroll_x, scroll_y = peoples.scroll()
        peoples.update()
        peoples.draw()
        peoples.mana_bar()

        enemy_group = world.update_group()

        for enemy in enemy_group:
            enemy.intelligence()
        enemy_group.update()
        enemy_group.draw(screen)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moving_left = True
                if event.key == pygame.K_d:
                    moving_right = True
                if event.key == pygame.K_w:
                    moving_up = True
                if event.key == pygame.K_s:
                    moving_down = True
                if event.key == pygame.K_LSHIFT:
                    if dash:
                        dash = True
                    else:
                        if peoples.mana < (peoples.max_mana * 0.2):
                            dash = False
                        else:
                            dash = True
                if event.key == pygame.K_SPACE:
                    peoples.jump = True
                if event.key == pygame.K_1:
                    if hand_use:
                        hand_use = False
                    else:
                        hand_use = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moving_left = False
                if event.key == pygame.K_d:
                    moving_right = False
                if event.key == pygame.K_w:
                    moving_up = False
                if event.key == pygame.K_s:
                    moving_down = False
                if event.key == pygame.K_LSHIFT:
                    dash = False
                    peoples.update_action(0)
                if event.key == pygame.K_SPACE:
                    peoples.jump = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if hand_use and dash == False:
                        if peoples.mana > (peoples.max_mana * 0.76):
                            peoples.mana -= (peoples.max_mana * 0.75)
                            ligthning = True

        pygame.display.flip()
        clock.tick(MAX_FPS)


def options():
    while True:
        screen.fill((0, 0, 0))

        text('options', font, (255, 255, 255), screen, 20, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(MAX_FPS)


def test():
    # Координаты плеча и параметры руки
    shoulder_x, shoulder_y = 400, 300
    arm_length = 150
    arm_width = 20

    # Создаем поверхность руки (вытянутый прямоугольник)
    arm_surf = pygame.Surface((arm_length, arm_width), pygame.SRCALPHA)
    arm_surf.fill((100, 150, 255))  # Синяя рука

    # Создаем маленький квадрат на конце
    hand_rect = pygame.Rect(0, 0, 20, 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))

        # 1. Получаем позицию мыши и расстояние до нее
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - shoulder_x
        dy = mouse_y - shoulder_y

        # 2. Находим угол в радианах (используем atan2, чтобы избежать деления на ноль)
        # math.atan2 принимает (y, x). В компьютерной графике Y идет вниз, поэтому ставим минус
        angle_rad = math.atan2(-dy, dx)
        angle_deg = math.degrees(angle_rad)  # Переводим в градусы для pygame

        # 3. Поворачиваем картинку руки
        rotated_arm = pygame.transform.rotate(arm_surf, angle_deg)
        
        # Смещаем центр повернутой картинки, чтобы точка вращения осталась в плече
        # Используем стандартные тригонометрические формулы смещения
        offset_x = (arm_length / 2) * math.cos(angle_rad)
        offset_y = -(arm_length / 2) * math.sin(angle_rad)
        
        arm_rect = rotated_arm.get_rect(center=(shoulder_x + offset_x, shoulder_y + offset_y))

        # 4. Находим точную позицию конца руки
        # Координата X = плечо_X + длина * cos(угол)
        # Координата Y = плечо_Y - длина * sin(угол) (минус, так как ось Y в pygame направлена вниз)
        hand_x = shoulder_x + arm_length * math.cos(angle_rad)
        hand_y = shoulder_y - arm_length * math.sin(angle_rad)

        # 5. Привязываем центр маленького квадрата к концу руки
        hand_rect.center = (int(hand_x), int(hand_y))

        # Отрисовка
        screen.blit(rotated_arm, arm_rect)  # Рисуем руку
        pygame.draw.rect(screen, (255, 100, 100), hand_rect)  # Красный квадрат на конце
        pygame.draw.circle(screen, (255, 255, 255), (shoulder_x, shoulder_y), 5)  # Точка плеча

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
