import requests


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


def static_maps_request(address_ll, scale, map_type):
    API_SERVER = 'https://static-maps.yandex.ru/1.x/'
    params = {
        'll': address_ll,
        'z': scale,
        'l': map_type,
        "pt": "{0},pm2dgl".format(address_ll)
    }
    response = get_request(API_SERVER, params)
    # print(response.url)
    return response.content


def geosearch_request(*, apikey, text, lang: str = 'ru_RU', type_: str = 'biz'):
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


def generate_image(*, address_ll, scale, map_type):
    # organization = geosearch_json["features"][0]
    # point = organization["geometry"]["coordinates"]
    # org_point = "{0},{1}".format(point[0], point[1])
    img_content = static_maps_request(
        address_ll=address_ll,
        map_type=map_type,
        scale=scale
    )
    with open('map.png', 'wb') as file:
        file.write(img_content)


def get_ll_by_address(key, address):
    coords = geocoder_request(key, address)['Point']['pos']
    return coords.replace(' ', ',')

