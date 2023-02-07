import os
import sys
import pygame
from get_spn_function import get_spn
import requests
import math

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
earth_radius = 6400

toponym_to_find = " ".join(sys.argv[1:])  # адрес из параметров командной строки


# Функция для расчета расстояния от адреса до аптеки
def get_spacing(address_ll, org_point):
    # Долготы и широты адреса и ближайшей аптеки
    toponym_longitude, toponym_lattitude = [float(i) for i in address_ll.split(',')]
    pharmacy_longitude, pharmacy_lattitude = [float(i) for i in org_point.split(',')]

    r1 = abs(toponym_longitude - pharmacy_longitude) * 111.3 * math.cos(
        min([toponym_lattitude, pharmacy_lattitude]))  # Расстояние по долготе в км
    r2 = abs(toponym_lattitude - pharmacy_lattitude) * 111.16  # Расстояние по широте в км
    spacing = math.sqrt((r1 / earth_radius) ** 2 + (
            r2 / earth_radius) ** 2) * earth_radius  # Теорема Пифагора для сферической поверхности

    r = f"{round(spacing * 1000)}м" if round(spacing) == 0 else f"{round(spacing)}км"
    return r


def get_snippet():
    address = json_response["features"][0]["properties"]["description"]
    name = json_response["features"][0]["properties"]["name"]
    time = json_response["features"][0]["properties"]["CompanyMetaData"]["Hours"]["text"]
    spacing = get_spacing(address_ll, org_point)
    snippet = {"Адрес": address,
               "Название": name,
               "Время работы": time,
               "Расстояние": spacing
               }
    return snippet


if get_spn(toponym_to_find):
    address_ll = get_spn(toponym_to_find)[0]
    search_params = {
        "apikey": api_key,
        "text": "аптека",
        "lang": "ru_RU",
        "ll": address_ll,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    json_response = response.json()

    organization = json_response["features"][0]
    point = organization["geometry"]["coordinates"]
    org_point = f"{point[0]},{point[1]}"

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "l": "map",
        "pt": f"{org_point},pm2dgl~{address_ll},pm2dgl"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    for key, value in get_snippet().items():  # Печать сниппета
        print(f"{key}: {value}")

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()

    os.remove(map_file)
