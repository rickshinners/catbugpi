__author__ = 'rshinners'

from bibliopixel.led import *

import web
import json

reverse_strip_order = False
led_count = 32
use_visualizer = True

if use_visualizer:
    from bibliopixel.drivers.visualizer import DriverVisualizer
    driver = DriverVisualizer(num=led_count)
else:
    from bibliopixel.drivers.LPD8806 import DriverLPD8806, ChannelOrder
    driver = DriverLPD8806(32, c_order=ChannelOrder.GRB)

led = LEDStrip(driver)

class index:
    def GET(self):
        raise web.seeother('/pixel/0')


class pixel:
    def GET(self, index):
        return json.dumps(led.get(index))
    def PUT(self, index):
        index = get_pixel_index(index)
        try:
            j = json.loads(web.data())
            if 'color' in j:
                led.setRGB(index, j['color']['r'], j['color']['g'], j['color']['b'])
            led.update()
        except Exception as e:
            print e.message
            return web.notacceptable()
        return self.GET(index)


class MyApplication(web.application):
    def run(self, port=80, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('localhost', port))


def get_pixel_index(idx):
    idx = int(idx)
    if idx > led_count or idx < 0:
        raise "LED index out of range. only values 0 through {0} are valid" % (led_count)
    if reverse_strip_order:
        idx = led_count - idx - 1
    return idx

urls = (
    '/', 'index',
    '/pixel/([\d]+)', 'pixel'
)

if __name__ == '__main__':
    led.all_off()
    led.update()
    app = MyApplication(urls, globals())
    app.run(port=9090)