class PhysicsObjects(pygame.sprite.Sprite):
    def __init__(self, img, x, y, speed):
        super().__init__()


class Player(pygame.sprite.Sprite):
    def __init__(self, type_img, x, y, scale, speed, health):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.type_img = type_img
        self.speed = speed
        self.frame_index = 0
        self.action = 0

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


    def update():
        self.update_animation()
        self.chec_alive()

    def move():
        pass

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
