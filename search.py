import os
import sys
import pygame
from get_spn_function import get_spn
import requests
import math

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

toponym_to_find = " ".join(sys.argv[1:])  # адрес из параметров командной строки

address_ll = get_spn(toponym_to_find)[0]
search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

if get_spn(toponym_to_find):
    pharmacies = []
    for i in range(10):
        response = requests.get(search_api_server, params=search_params)
        json_response = response.json()

        organization = json_response["features"][i]
        point = organization["geometry"]["coordinates"]
        org_point = f"{point[0]},{point[1]}"
        try:
            worktime = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
            if "круглосуточно" in worktime:
                pharmacies.append(f"{org_point},pm2gnl")
            else:
                pharmacies.append(f"{org_point},pm2bll")
        except KeyError:
            pharmacies.append(f"{org_point},pm2grl")

    # Собираем параметры для запроса к StaticMapsAPI:
    map_params = {
        "l": "map",
        "pt": '~'.join(pharmacies)
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
