import os
import sys
import pygame
from get_spn_function import get_spn
import requests

toponym_to_find = " ".join(sys.argv[1:])

if get_spn(toponym_to_find):
    ll, spn = get_spn(toponym_to_find)

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": "map",
        "pt": f"{ll},pm2dol"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"

    response = requests.get(map_api_server, params=map_params)

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
