import requests

url_geocode = "http://geocode-maps.yandex.ru/1.x/"
apikey = "40d1649f-0493-4b70-98ba-98533de7710b"


def get_spn(toponym):
    response = requests.get(url_geocode, params={
        "geocode": toponym,
        "apikey": apikey,
        "format": "json"
    })
    try:
        res_j = response.json()
        coords = res_j["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split()
        ll = ",".join(coords)
        left, bottom = res_j["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"][
            "lowerCorner"].split()
        right, top = res_j["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["boundedBy"]["Envelope"][
            "upperCorner"].split()
        dx = abs(float(left) - float(right)) / 2
        dy = abs(float(bottom) - float(top)) / 2
        spn = f"{dx},{dy}"
        return ll, spn
    except Exception:
        print("Неверный ввод")
        return False
