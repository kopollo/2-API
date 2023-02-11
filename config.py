import os

os.environ['GEOSEARCH_API_KEY'] = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'
os.environ['GEOCODER_API_KEY'] = '40d1649f-0493-4b70-98ba-98533de7710b'

GEOSEARCH_API_KEY = os.environ.get('GEOSEARCH_API_KEY', '#trash')
GEOCODER_API_KEY = os.environ.get('GEOCODER_API_KEY', '#trash')