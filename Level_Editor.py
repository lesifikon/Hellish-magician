import pygame
import csv
from src.game import Button

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# игровое окно
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('Level Editor')

# задать параметры игры
ROWS = 50
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // 16
TILE_TYPES = 24
level = 0
circle = 0
current_tile = 0
scroll_up = False
scroll_down = False
scroll_left = False
scroll_right = False
scroll_x = 0
scroll_y = 0
scroll_speed = 1

# загрузить изображение
pine1_img = pygame.image.load('Level Editor 1/pine1.png').convert_alpha()
pine2_img = pygame.image.load('Level Editor 1/pine2.png').convert_alpha()
mountain_img = pygame.image.load('Level Editor 1/mountain.png').convert_alpha()
sky_img = pygame.image.load('Level Editor 1/sky.png').convert_alpha()
# плитки хранятся в списке
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f"Level Editor 1/tile/{x}.png").convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('Level Editor 1/save_button.png').convert_alpha()
load_img = pygame.image.load('Level Editor 1/load_button.png').convert_alpha()

# дать определение цветам
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

# шрифт
font = pygame.font.SysFont(None, 20)


# пустой список tile
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

# создадим плитку с землёй
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 0


# функция для вывода текста на экран
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# создать функцию для отрисовки фона
def draw_bw():
    screen.fill(RED)
    width = sky_img.get_width()
    for x in range(5):
        screen.blit(sky_img, ((x * width) - scroll_x * 0.5, 0 - scroll_y))
        screen.blit(mountain_img, ((x * width) - scroll_x * 0.6, (SCREEN_HEIGHT - mountain_img.get_height() - 180) - scroll_y))
        screen.blit(pine1_img, ((x * width) - scroll_x * 0.7, (SCREEN_HEIGHT - pine1_img.get_height() - 90) - scroll_y))
        screen.blit(pine2_img, ((x * width) - scroll_x * 0.8, (SCREEN_HEIGHT - pine2_img.get_height() - 38) - scroll_y))


# нарисовать сетку
def draw_grid():
    # вертикальные линии
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll_x, 0), (c * TILE_SIZE - scroll_x, SCREEN_HEIGHT))
    # горизонтальные линии
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE - scroll_y), (SCREEN_WIDTH, c * TILE_SIZE - scroll_y))


# функция для рисования плиток мира
def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll_x, y * TILE_SIZE - scroll_y))


# создание кнопок
save_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 50, save_img, 1)
load_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 50, load_img, 1)
# создать список кнопок
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

run = True
while run:

    clock.tick(FPS)

    draw_bw()
    draw_grid()
    draw_world()

    draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text(f'circle: {circle}', font, WHITE, 100, SCREEN_HEIGHT + LOWER_MARGIN - 90)
    draw_text('w,a,s,d -- передвигать камирой\nh,l -- круги ада\nj,k -- перемещение по уровню', font, WHITE, 10,
              SCREEN_HEIGHT + LOWER_MARGIN - 60)

    # сохранить и загрузить данные
    if save_button.draw(screen):
        # нужно сохранить данные уроня
        with open(f'assets/map/circle{circle}/level{level}_data.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for row in world_data:
                writer.writerow(row)
    if load_button.draw(screen):
        # загрузить данные уроня
        # вернуть прокрутку к началу уровня
        scroll_x = 0
        scroll_y = 0
        with open(f'assets/map/circle{circle}/level{level}_data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)

    # нарисовать панель с плитками
    pygame.draw.rect(screen, GREEN, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT + 1))

    # выберете плитку
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count

    # чтобы выделить выбранную кнопку
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # нужно прокрутить карту
    if scroll_left == True and scroll_x > 0:
        scroll_x -= 5 * scroll_speed
    if scroll_right == True and scroll_x < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
        scroll_x += 5 * scroll_speed
    if scroll_up == True and scroll_y > 0:
        scroll_y -= 5 * scroll_speed
    if scroll_down == True and scroll_y < 1350:
        scroll_y += 5 * scroll_speed

    # добавить новые плитки на экран
    # получить о положении миши
    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll_x) // TILE_SIZE
    y = (pos[1] + scroll_y) // TILE_SIZE

    # координаты должны находиться в области
    if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
        # обновить значение миши
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # нажатие клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                scroll_up = True
            if event.key == pygame.K_s :
                scroll_down = True
            if event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_d:
                scroll_right = True
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 5

            # перемещение между уровнями
            if event.key == pygame.K_h and circle > 0:
                circle -= 1
                level = 0
            if event.key == pygame.K_l:
                circle += 1
                level = 0
            if event.key == pygame.K_j and level > 0:
                level -= 1
            if event.key == pygame.K_k:
                level += 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                scroll_up = False
            if event.key == pygame.K_s:
                scroll_down = False
            if event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_LSHIFT:
                scroll_speed = 1

    pygame.display.update()

pygame.quit()
