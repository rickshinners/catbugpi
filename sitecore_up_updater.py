__author__ = 'rshinners'

import requests
import json

endpoints = [
    {'url': 'http://cms.vpdev.com/product-pages/rackcards', 'led_index': 5},
    {'url': 'http://cms.vptest.com/product-pages/rackcards', 'led_index': 6},
    {'url': 'http://cms.vppreprod.com/product-pages/rackcards', 'led_index': 7},
    # {'url': 'http://cms.vistaprint.com/product-pages/rackcards', 'led_index': 8},
]

ledstrip_base_url = 'http://localhost:9090'


def send_color(index, color):
    r,g,b = color
    request_obj = {'color': {'r': r, 'g': g, 'b': b}}
    requests.put(ledstrip_base_url + "/pixel/" + str(index), data=json.dumps(request_obj))


def set_led_good(index):
    send_color(index, (0,64,0))


def set_led_bad(index):
    send_color(index, (255,0,0))


for endpoint in endpoints:
    try:
        http_status_code = requests.get(endpoint['url']).status_code
        if http_status_code == 200:
            set_led_good(endpoint['led_index'])
        else:
            set_led_bad(endpoint['led_index'])
    except Exception as e:
        print e
        set_led_bad(endpoint['led_index'])