import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from Core.Space_Objects import Satellite, GroundStation

class TwoD_Map:
    def __init__(self, ts, width=800, height=400):
        self.width = width
        self.height = height
        self.ts = ts
        self.figure, self.map_axes = plt.subplots(figsize=(8, 4))

    def setup(self):
        base_dir = os.path.dirname(__file__)
        img_path = os.path.join(base_dir, "World_Map.jpg")
        img = mpimg.imread(img_path)
        self.map_axes.imshow(img, extent=[0, self.width, self.height, 0])
        self.map_axes.set_xlim(0, self.width)
        self.map_axes.set_ylim(0, self.height)
        self.map_axes.invert_yaxis()

    def convert(self, lat, lon):
        x = (lon + 180) / 360 * self.width
        y = (90 - lat) / 180 * self.height
        return x, y

    def draw_point(self, lat, lon, color):
        x, y = self.convert(lat, lon)
        self.map_axes.scatter(x, y, color=color)

    def draw_line(self, trail, color):
        xx, yy = [], []
        for lat, lon in trail:
            x, y = self.convert(lat, lon)
            xx.append(x)
            yy.append(y)
        self.map_axes.plot(xx, yy, color=color, linewidth=1)

    def is_visible(self, sat, ground):
        t = self.ts.now()
        difference = sat.sat - ground.location
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()
        return alt.degrees > 0

    def update(self, manager):
        self.map_axes.clear()
        self.setup()

        for obj in manager.active:
            if isinstance(obj, GroundStation):
                lat, lon = obj.lat, obj.lon
                self.draw_point(lat, lon, obj.color)
                x, y = self.convert(lat, lon)
                self.map_axes.text(x + 5, y + 5, obj.name, fontsize=8)

            elif isinstance(obj, Satellite):
                geo = obj.get_position()
                lat = geo.latitude.degrees
                lon = geo.longitude.degrees
                obj.update_trail(lat, lon)
                self.draw_line(obj.trail, obj.color)
                self.draw_point(lat, lon, obj.color)
                x, y = self.convert(lat, lon)
                self.map_axes.text(x, y, obj.name, fontsize=6)

        grounds = [o for o in manager.active if isinstance(o, GroundStation)]
        sats = [o for o in manager.active if isinstance(o, Satellite)]

        for ground in grounds:
            gx, gy = self.convert(ground.lat, ground.lon)
            for sat in sats:
                if self.is_visible(sat, ground):
                    geo = sat.get_position()
                    sx, sy = self.convert(geo.latitude.degrees, geo.longitude.degrees)
                    self.map_axes.plot([gx, sx], [gy, sy], color="red")