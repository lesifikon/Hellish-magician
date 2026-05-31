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

# найти им место
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

    img_list = []
    for x in range(TILE_TYPES):
        img = pygame.image.load(f'Level Editor 1/tile/{x}.png')
        img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        img_list.append(img)


    player_image = player.convert_alpha()

    player_rect = player_image.get_rect(topleft=(500, 300))

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
        screen.fill((0, 0, 0))

        world.draw()

        text('game', font, (255, 255, 255), screen, 20, 20)

        peoples.move(world,moving_left = False, moving_right = True)
        peoples.update()
        peoples.draw()

        screen.blit(player_image, player_rect)
        world.process_data(world_data, img_list, TILE_SIZE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    

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



if __name__ == "__main__":
    main_menu()
