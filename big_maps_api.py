import os
import math
import pygame
import requests

global point_coords1, point_coords2
point_coords1, point_coords2 = None, None
coords1, coords2, scale = map(float, input().split())
card_type = 'map'
def get_picture(coords1, coords2, scale, card_type):
    if point_coords1:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords1},{coords2}&spn={scale},{scale}&l={card_type}&pt={point_coords1},{point_coords2},pm2rdm"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords1},{coords2}&spn={scale},{scale}&l={card_type}"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file

def get_picture_with_pointer(coords1, coords2, scale, card_type):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords1},{coords2}&spn={scale},{scale}&l={card_type}&pt={coords1},{coords2},pm2rdm"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file

def get_picture_from_name(toponym_to_find, scale, card_type):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        # обработка ошибочной ситуации
        pass
    # Преобразуем ответ в json-объект
    json_response = response.json()
    # Получаем первый топоним из ответа геокодера.
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    # Координаты центра топонима:
    toponym_coodrinates = toponym["Point"]["pos"]
    # Долгота и широта:
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    return get_picture_with_pointer(toponym_longitude, toponym_lattitude, scale, card_type), float(toponym_longitude), float(toponym_lattitude)

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
font = pygame.font.Font(None, 32)
input_box = pygame.Rect(10, 10, 140, 32)
cancel_box = pygame.Rect(10, 50, 90, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color2 = pygame.Color('firebrick')
color = color_inactive
active = False
text = ''
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
                if scale > 0:
                    scale /= 2
                    map_file = get_picture(coords1, coords2, scale, card_type)
            if event.key == pygame.K_PAGEUP:
                if scale <= 45:
                    map_file = get_picture(coords1, coords2, scale * 2, card_type)
                    scale *= 2
            if event.key == pygame.K_UP:
                coords2 = min(coords2 + scale, 90 - scale)
                map_file = get_picture(coords1, coords2, scale, card_type)
            if event.key == pygame.K_DOWN:
                coords2 = max(coords2 - scale, -90 + scale)
                map_file = get_picture(coords1, coords2, scale, card_type)
            if event.key == pygame.K_LEFT:
                coords1 -= scale
                if coords1 < -180:
                    coords1 += 360
                map_file = get_picture(coords1, coords2, scale, card_type)
            if event.key == pygame.K_RIGHT:
                coords1 += scale
                if coords1 > 180:
                    coords1 = coords1 - 360
                map_file = get_picture(coords1, coords2, scale, card_type)
            if event.key == pygame.K_TAB:
                if card_type == 'map':
                    card_type = 'sat'
                elif card_type == 'sat':
                    card_type = 'sat,skl'
                else:
                    card_type = 'map'
                map_file = get_picture(coords1, coords2, scale, card_type)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
                color = color_active if active else color_inactive
            elif cancel_box.collidepoint(event.pos):
                point_coords1, point_coords2 = None, None
                text = ''
                map_file = get_picture(coords1, coords2, scale, card_type)
            else:
                active = False
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_KP_ENTER:
                    map_file, coords1, coords2 = get_picture_from_name(text, scale, card_type)
                    point_coords1 = coords1
                    point_coords2 = coords2
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
    # Render the current text.
    txt_surface = font.render(text, True, color)
    cancel_surface = font.render('Сброс', True, color2)
    # Resize the box if the text is too long.
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    # Blit the text.
    screen.blit(pygame.image.load(map_file), (0, 0))
    screen.blit(cancel_surface, (cancel_box.x + 5, cancel_box.y + 5))
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    # Blit the input_box rect.
    pygame.draw.rect(screen, color, input_box, 2)
    pygame.draw.rect(screen, color2, cancel_box, 2)
    pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)