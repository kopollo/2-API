import requests
from config import GEOSEARCH_API_KEY


def get_request(server: str, params: dict[str, str] = None):
    try:
        response = requests.get(server, params)
        if not response:
            print('Server is sad with status code', response.status_code)
            print(response.reason)
            return response
        return response
    except requests.RequestException as exc:
        print('Oh ship :(')
        print(exc)


def geocoder_request(apikey: str, geocode: str, format: str = 'json'):
    API_SERVER = 'https://geocode-maps.yandex.ru/1.x/'
    params = {
        'apikey': apikey,
        'geocode': geocode,
        'format': format,
    }

    response = get_request(API_SERVER, params)
    json = response.json()
    return json["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"]


def static_maps_request(*, center_point, org_point, scale, map_type):
    API_SERVER = 'https://static-maps.yandex.ru/1.x/'
    params = {
        'll': center_point,
        'z': scale,
        'l': map_type,
        "pt": "{0},pm2dgl".format(org_point)
    }
    response = get_request(API_SERVER, params)
    return response.content


def generate_image(*, center_point, org_point, scale, map_type):
    img_content = static_maps_request(
        center_point=center_point,
        org_point=org_point,
        map_type=map_type,
        scale=scale
    )
    with open('map.png', 'wb') as file:
        file.write(img_content)


class GeosearchController:
    def __init__(self):
        self.apikey = GEOSEARCH_API_KEY

    def get_ll_by_address(self, *, address):
        geosearch_json = self.geosearch_request(
            apikey=self.apikey,
            text=address,
        )
        organization = geosearch_json["features"][0]
        point = organization["geometry"]["coordinates"]
        point = "{0},{1}".format(point[0], point[1])
        return point.replace(' ', ',')

    def get_full_address(self, *, address):
        geosearch_json = self.geosearch_request(
            apikey=self.apikey,
            text=address,
        )
        organization = geosearch_json["features"][0]
        address = organization["properties"]['description']
        return address

    @staticmethod
    def geosearch_request(*, apikey, text, lang: str = 'ru_RU',
                          type_: str = 'biz'):
        API_SERVER = "https://search-maps.yandex.ru/v1/"
        map_params = {
            'apikey': apikey,
            'text': text,
            'lang': lang,
            'type': type_,
        }
        response = get_request(API_SERVER, params=map_params)
        json = response.json()
        return json


geosearch_controller = GeosearchController()
