import os
import sys

import pygame
import requests

coords1, coords2, scale = map(float, input().split())

def get_picture(coords1, coords2, scale):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords1},{coords2}&z={int(scale)}&l=sat"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
map_file = get_picture(coords1, coords2, scale)
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYUP and event.key == pygame.K_PAGEDOWN:
            if scale > 1:
                scale -= 1
                map_file = get_picture(coords1, coords2, scale)
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
        if event.type == pygame.KEYUP and event.key == pygame.K_PAGEUP:
            try:
                map_file = get_picture(coords1, coords2, scale + 1)
                scale += 1
                screen.blit(pygame.image.load(map_file), (0, 0))
                pygame.display.flip()
            except Exception:
                scale -= 1
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)