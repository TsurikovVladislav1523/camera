import pygame
import sys
import os
from config import *

level = input()
size = width, height = W_WIDTH, W_HEIGHT
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    try:
        mapFile = open(filename, 'r')
    except IOError as e:
        print('Такого файла нет, переделывай!!!')
    else:
        with mapFile:
            level_map = [line.strip() for line in mapFile]

            # и подсчитываем максимальную длину
            max_width = max(map(len, level_map))

            # дополняем каждую строку пустыми клетками ('.')
            return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def load_image(name, color_key=None):
    fullname = os.path.join(ASSETS_DIR, name)
    image = pygame.image.load(fullname)
    if color_key is not None:
        image = image.convert()
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def update(self):
        camera.apply(self)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, arg):
        if arg == 1:
            camera.dx = V / FPS
        elif arg == 2:
            camera.dx = -V / FPS
        elif arg == 3:
            camera.dy = V / FPS
        elif arg == 4:
            camera.dy = -V / FPS


class Fon(pygame.sprite.Sprite):
    def __init__(self, image):
        self.image = image
        self.rect = self.image.get_rect()


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (W_WIDTH, W_HEIGHT))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == 768 or \
                    event.type == 1025:
                fon_group.empty()
                return None
            fon_group.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50

player = None

# группы спрайтов
player_group = pygame.sprite.Group()
fon_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player, level_x, level_y = generate_level(load_level(level))
camera = Camera()
start_screen()
screen.fill(pygame.Color('black'))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player.update(3)
                tiles_group.update()
                camera.dx = 0
                camera.dy = 0
            elif event.key == pygame.K_s:
                player.update(4)
                tiles_group.update()
                camera.dx = 0
                camera.dy = 0
            elif event.key == pygame.K_a:
                player.update(1)
                tiles_group.update()
                camera.dx = 0
                camera.dy = 0
            elif event.key == pygame.K_d:
                player.update(2)
                tiles_group.update()
                camera.dx = 0
                camera.dy = 0

    screen.fill(pygame.Color('lightblue'))
    # # изменяем ракурс камеры
    # camera.update(player);
    # # обновляем положение всех спрайтов
    # for sprite in all_sprites:
    #     camera.apply(sprite)
    all_sprites.draw(screen)
    tiles_group.draw(screen)
    player_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()
