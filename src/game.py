import pygame
import os
import math
import random
import bisect
from main import *
from assets.images.img import *
GRAVITY = 0.5

class PhysicsObjects(pygame.sprite.Sprite):
    def __init__(self, type_img, x, y, scale, speed, health, obstacle_list):
        # super().__init__()
        self.obstacle_list = obstacle_list
        self.alive = True
        self.type_img = type_img
        self.speed = speed
        self.health = health
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.flip = False
        self.jump = False
        self.in_air = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # self.scroll_x = 0
        # self.scroll_y = 0

        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # сбросите временный список изображений
            temp_list = []
            # количество файлов в папке
            mum_of_frames = len(os.listdir(f'./assets/images/{self.type_img}/{animation}'))
            for i in range(mum_of_frames):
                img = pygame.image.load(f'./assets/images/{self.type_img}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.legs = pygame.Rect(0, 0, 5, 5)


    def update(self):
        self.update_animation()
        self.chec_alive()

    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.direction = 1

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -15
            self.jump = False
            self.in_air = True

        # графитация 
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # не падает ли существо
        self.legs.center = (self.rect.centerx, (self.rect.centery + self.height))
        floor = [tile[1] for tile in self.obstacle_list]
        # pygame.draw.rect(screen, (255, 0, 255), self.legs)
        if self.legs.collidelist(floor) == -1:
            self.jump == False
            self.in_air = True

        # проверить столкновения
        for tile in self.obstacle_list:
            # проверка на столкновение по оси x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy + 2, self.width, self.height):
                # проверить нахожусь ли я ниже земли, тоесть прыгаю
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.rect.top
                # проверить не нахожусь ли я над зеьлёй, тоесть не падаю
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx
        self.rect.y += dy


    def update_animation(self):
        # обновляет анимацию
        base_cooldown = 150

        if abs(self.speed) > 0:
            ANIMATION_COOLDOWN = base_cooldown - (abs(self.speed) * 10)
        else:
            ANIMATION_COOLDOWN = base_cooldown

        # ограничение по максимуму
        if ANIMATION_COOLDOWN < 30:
            ANIMATION_COOLDOWN = 30
        # изображение обновляется в зависимости от текущего кадра
        self.image = self.animation_list[self.action][self.frame_index]
        # прошло ли достаточно времени с момента прошлого обновления
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # если анимация закончилась, то нужно вернуться к началу
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def chec_alive(self):
        if self.health <= 0:
            self.health = 0
            if self.speed > 0:
                self.speed -= 0.1
            self.alive = False
            self.update_action(3)

    def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

class Player(PhysicsObjects):
    def __init__(self, type_img, x, y, scale, speed, health, obstacle_list):
        super().__init__(type_img, x, y, scale, speed, health, obstacle_list)
        self.mouse_x, self.mouse_y = 0, 0
        self.rel_x, self.rel_y = 0, 0
        self.angle_rad = 0
        self.hand_x, self.hand_y = self.rect.x + (self.width / 2), self.rect.y
        self.hand_img = mini_hamd_player_img.convert_alpha()
        self.lightning_img = mini_lightning.convert_alpha()
        self.purple_square = pygame.Surface((8, 8),pygame.SRCALPHA)
        self.purple_square.fill((128, 0, 128))
        self.purple_square_rect = pygame.Rect(0, 0, 8, 8)
        self.mouse_rect = pygame.Rect(0, 0, 8, 8)
        self.hand_rect = False

    def scroll(self):

        scroll_x = 0
        scroll_y = 0

        playerCenter_x = self.rect.x + (self.width / 2)
        playerCenter_y = self.rect.y + (self.height / 2)

        if playerCenter_x > 1220:
            scroll_x -= round((playerCenter_x - 1220) / 15)
        if playerCenter_x < 500:
            scroll_x += round((500 - playerCenter_x) / 15)
        if playerCenter_y > 780:
            scroll_y += round((780 - playerCenter_y) / 10)
        if playerCenter_y < 300:
            scroll_y += round((300 - playerCenter_y) / 10)

        self.rect.x += scroll_x
        self.rect.y += scroll_y

        return scroll_x, scroll_y

    def hand(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.rel_x, self.rel_y = self.mouse_x - self.hand_x, self.mouse_y - self.rect.y
        angle = (180 / math.pi) * -math.atan2(self.rel_y, self.rel_x)
        h_hand = pygame.transform.rotate(self.hand_img, int(angle))
        self.hand_rect = h_hand.get_rect(center=(self.rect.x + (self.width / 2), self.rect.y))

        self.angle_rad = math.atan2(-self.rel_y, self.rel_x)

        end_hand_x = self.hand_rect.centerx + 8 * math.cos(self.angle_rad)
        end_hand_y = self.hand_rect.centery - 8 * math.sin(self.angle_rad)

        # Привязываем центр маленького квадрата к концу руки
        self.purple_square_rect.center = (int(end_hand_x), int(end_hand_y))
        pygame.draw.rect(screen, (128, 0, 128), self.purple_square_rect)
        self.mouse_rect.center = (self.mouse_x, self.mouse_y)
        pygame.draw.rect(screen, (128, 0, 128), self.mouse_rect)

        screen.blit(h_hand, self.hand_rect)

    def ray_light(self):
        pass

    def lightning_strike(self):

        def findDistance(x_0, x_1, y_0, y_1):
            legx = abs(x_0 - x_1)
            legy = abs(y_0 - y_1)

            hypotenuse = round(((legx ** 2) + (legy ** 2)) ** 0.5)+2
            return hypotenuse

        def drawLightning(list, object, rel_x, rel_y):
            angle_radd = math.atan2(-rel_y, rel_x)
            for i in range(list):
                square = pygame.Rect(0, 0, 6, 6)
                square_x = object.centerx + (i * 16) * math.cos(angle_radd)
                square_y = object.centery - (i * 16) * math.sin(angle_radd)
                square.center = (int(square_x), int(square_y))
                angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
                lig = pygame.transform.rotate(self.lightning_img, int(angle))
                lig_rect = lig.get_rect(center=(int(square_x), int(square_y)))

                screen.blit(lig, lig_rect)
                pygame.draw.rect(screen, (0, 0, 255), square)
            return square.center

        self.hand_x, self.hand_y = self.rect.x + (self.width / 2), self.rect.y

        hypotenuse = findDistance(self.mouse_x, self.hand_x, self.mouse_y, self.hand_y)
        n_j_lightning = round(hypotenuse / 16) + 1
        joint = round(n_j_lightning / 10)

        list_joint = []
        for j in range(joint):
            realism = random.randint(1, hypotenuse)
            square = pygame.Rect(0, 0, 8, 8)
            realism_x = random.randint(-50, 50)
            realism_y = random.randint(-50, 50)
            square_x = self.purple_square_rect.centerx + (realism - realism_x) * math.cos(self.angle_rad) + realism_x
            square_y = self.purple_square_rect.centery - (realism + realism_y) * math.sin(self.angle_rad) - realism_y
            square.center = (int(square_x), int(square_y))
            bisect.insort(list_joint, square.center)
            # pygame.draw.rect(screen, (0, 255, 0), square)


        if self.mouse_x < self.hand_x:
            list_joint.reverse()


        if list_joint:
            first_joint = list_joint[0]
            rel_x, rel_y = first_joint[0] - self.purple_square_rect.centerx, first_joint[1] - self.purple_square_rect.centery

            difference = findDistance(first_joint[0], self.purple_square_rect.centerx, first_joint[1], self.purple_square_rect.centery)
            n_lightning = round(difference / 16) + 1
        else:
            rel_x, rel_y = self.mouse_x- self.purple_square_rect.centerx, self.mouse_y - self.purple_square_rect.centery
            difference = findDistance(self.mouse_x, self.purple_square_rect.centerx, self.mouse_y, self.purple_square_rect.centery)
            n_lightning = round(difference / 16) + 1

        squa = pygame.Rect(0, 0, 6, 6)
        squa.center = drawLightning(n_lightning, self.purple_square_rect, rel_x, rel_y)

        if list_joint:
            for l in (list_joint):
                rel_x, rel_y = l[0] - squa.centerx, l[1] - squa.centery
                difference = findDistance(l[0], squa.centerx, l[1], squa.centery)
                n_lightning = round(difference / 16) + 1
                squa.center = drawLightning(n_lightning, squa, rel_x, rel_y)

        rel_x, rel_y = self.mouse_x - squa.centerx, self.mouse_y - squa.centery
        difference = findDistance(self.mouse_x, squa.centerx, self.mouse_y, squa.centery)
        n_lightning = round(difference / 16) + 1

        squa.center = drawLightning(n_lightning, squa, rel_x, rel_y)

 
    def dash(self):
        pass

    def draw(self):
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


class Shadow(PhysicsObjects):
    def __init__(self, type_img, x, y, scale, speed, health, obstacle_list):
        super().__init__(type_img, x, y, scale, speed, health, obstacle_list)

    def intelligence(self, scroll_x):
        n = random.randint(1,50)
        if n <= 5:
            self.move(moving_left = False, moving_right = True)
        else:
            self.move(moving_left = True, moving_right = False)

        self.rect.x += scroll_x


class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


class World():
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, data, img_list, TILE_SIZE):
        self.level_length = len(data[0])
        # пройти по каждому значению по файлу данный уровня
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    if tile == 15:
                        peoples = Player('player', x * TILE_SIZE, y * TILE_SIZE, 3, 5, 100, self.obstacle_list)
                    if tile == 16:
                        shadow = Shadow('shadow', x * TILE_SIZE, y * TILE_SIZE, 3, 2, 1, self.obstacle_list)

        return peoples, shadow

    def draw(self, scroll_x, scroll_y):
        for tile in self.obstacle_list:
            tile[1][0] += scroll_x
            tile[1][1] += scroll_y
            screen.blit(tile[0], tile[1])

