import pygame
from main import *
GRAVITY = 0.5

class PhysicsObjects(pygame.sprite.Sprite):
    def __init__(self, type_img, x, y, scale, speed, health):
        super().__init__()
        self.alive = True
        self.type_img = type_img
        self.speed = speed
        self.health = health
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        animation_types = ['Idle', 'Run', 'Jump', 'Death']
        for animation in animation_types:
            # сбросите временный список изображений
            temp_list = []
            # количество файлов в папке
            mum_of_frames = len(os.listdir(f'images/{self.type_img}/{animation}'))
            for i in range(mum_of_frames):
                img = pygame.image.load(f'images/{self.type_img}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()


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

        # проверить столкновения
        for tile in world.obstacle_list:
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


class Player(pygame.sprite.Sprite):
    def __init__(self, type_img, x, y, scale, speed, health):
        pygame.sprite.Sprite.__init__(self)
        


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

    def draw(self): # вроде здесть нужно чтобы карта не сразу рендералась
        for tile in self.obstacle_list:
            # tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
