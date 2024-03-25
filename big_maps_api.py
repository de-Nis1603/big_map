import os
import sys
import math
import pygame
import requests

ze_dict = [3000, 3000, 3000, 1000, 700, 300, 200, 90, 40, 20, 9, 5, 2, 1, 0.6, 0.3, 0.1, 0.07, 0.04, 0.02, 0.009, 0.005]

coords1, coords2, scale = map(float, input().split())
card_type = 'map'
def get_picture(coords1, coords2, scale, card_type):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords1},{coords2}&z={int(scale)}&l={card_type}"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file

def lonlat_distance(a, b):

    degree_to_meters_factor = 111 * 1000 # 111 километров в метрах
    a_lon, a_lat = a
    b_lon, b_lat = b

    # Берем среднюю по широте точку и считаем коэффициент для нее.
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)

    # Вычисляем смещения в метрах по вертикали и горизонтали.
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor

    # Вычисляем расстояние между точками.
    distance = math.sqrt(dx * dx + dy * dy)

    return distance

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
map_file = get_picture(coords1, coords2, scale, card_type)
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEDOWN:
                if scale > 1:
                    scale -= 1
                    map_file = get_picture(coords1, coords2, scale, card_type)
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
            if event.key == pygame.K_PAGEUP:
                try:
                    map_file = get_picture(coords1, coords2, scale + 1, card_type)
                    scale += 1
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
                except Exception:
                    scale -= 1
            """
            if event.key == pygame.K_UP:
                print('up')
                print(coords2)
                coords2 = min(coords2 + 8 * ze_dict[int(scale)] / 111, 90)
                print(coords2)
                map_file = get_picture(coords1, coords2, scale)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            if event.key == pygame.K_DOWN:
                print('down')
                print(coords2)
                coords2 = max(coords2 - 8 * ze_dict[int(scale)] / 111, -90)
                print(coords2)
                map_file = get_picture(coords1, coords2, scale)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            """
            if event.key == pygame.K_BACKSPACE:
                if card_type == 'map':
                    card_type = 'sat'
                elif card_type == 'sat':
                    card_type = 'sat,skl'
                else:
                    card_type = 'map'
                map_file = get_picture(coords1, coords2, scale, card_type)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)