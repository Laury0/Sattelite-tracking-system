"""
This is a program meant to track satelite movements and properly display them on a map
"""

import threading
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from datetime import datetime
from skyfield.api import load, EarthSatellite

now = datetime.utcnow()  #Palydovai naudoja UTC laika, padaryti i class veliau, kad palydovo clase paveldetu
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)

ts=load.timescale()

class Satellite:
    def __init__(self, skyfield_sat):
        self.name = skyfield_sat.name
        self.sat = skyfield_sat
        self.ts = load.timescale()
        self.trail=[]

    def get_position(self):
        t = self.ts.now()
        geo = self.sat.at(t).subpoint()
        return geo

    def print_position(self):
        geo = self.get_position()

        lat = geo.latitude.degrees
        lon = geo.longitude.degrees
        alt = geo.elevation.km

        lat_dir = "N" if lat >= 0 else "S"
        lon_dir = "E" if lon >= 0 else "W"

        print("Satellite:", self.name)
        print(f"Latitude: {abs(lat):.2f}° {lat_dir}")
        print(f"Longitude: {abs(lon):.2f}° {lon_dir}")
        print(f"Altitude: {alt:.1f} km")

    def update_trail(self, lat, lon):
        self.trail.append((lat, lon))
        if len(self.trail) > 50:
            self.trail.pop(0)

class TwoD_Map:
    def __init__(self, width=800, height=400):
        self.width=width
        self.height=height
        self.figure, self.map_axes=plt.subplots(figsize=(8, 4))

    def convert(self, lat, lon):
        x=(lon+180)/360*self.width
        y=(90-lat)/180*self.height
        return x, y

    def setup(self):
        img=mpimg.imread("World_Map.jpg")
        self.map_axes.imshow(img, extent=[0, self.width, self.height, 0])
        self.map_axes.set_xlim(0, self.width)
        self.map_axes.set_ylim(0, self.height)
        self.map_axes.invert_yaxis()

    def draw_point(self, lat, lon):
        x, y=self.convert(lat, lon)
        self.map_axes.scatter(x, y)

    """
    def display(self):
        plt.show();
    """

    def draw_line(self, trail):
        xx = []
        yy = []
        for lat, lon in trail:
            x, y = self.convert(lat, lon)
            xx.append(x)
            yy.append(y)
        self.map_axes.plot(xx, yy, color='red', linewidth=1)

class Satellite_Manager:
    def __init__(self, satellites):
        self.all_satellites=satellites
        self.active=[]

    def find_sat(self, name):
        for sati in self.all_satellites:
            if name.upper() in sati.name:
                return Satellite(sati)
        return None

    def add_satellite(self, name):
        sat=self.find_sat(name)
        if sat and sat.name not in [sati.name for sati in self.active]:
            self.active.append(sat)
            print(f"added: {sat.name}")
        else:
            print("Not found / alredy added")

def input_loop(manager):
    while True:
        name=input("Add satllite: ")
        manager.add_satellite(name)

url = "https://celestrak.org/NORAD/elements/stations.txt"
satellites = load.tle_file(url)

for sati in satellites:
    print(sati.name)

manager=Satellite_Manager(satellites)
manager.add_satellite("ISS")

threading.Thread(target=input_loop, args=(manager,), daemon=True).start()

trail=[]
m=TwoD_Map()
while True:
    m.map_axes.clear()
    m.setup()

    for sat in manager.active:
        geo = sat.get_position()
        lat = geo.latitude.degrees
        lon = geo.longitude.degrees
        sat.update_trail(lat, lon)
        m.draw_line(sat.trail)
        m.draw_point(lat, lon)

    plt.pause(1)
    time.sleep(10)
"""
m.setup()
m.draw_point(0, 0)
m.draw_point(51.5, 0)
m.draw_point(54.7, 25.3)
m.draw_point(-33.9, 151)
m.draw_point(lat, lon)
m.display()
"""
