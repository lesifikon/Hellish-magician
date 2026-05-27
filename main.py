import pygame
import sys

from assets.imeges.img import player

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.SCALED)

pygame.display.set_caption('маг в аду')
pygame.display.set_icon(pygame.image.load('./assets/imeges/icon.png'))

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

    player_image = player.convert_alpha()

    player_rect = player_image.get_rect(topleft=(500, 300))

    while True:
        screen.fill((0, 0, 0))

        text('game', font, (255, 255, 255), screen, 20, 20)

        screen.blit(player_image, player_rect)

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
