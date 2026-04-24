"""
This is a program meant to track satelite movements and properly display them on a map
"""

import threading
import time
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.widgets import TextBox, Button
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
        self.color = (random.random(), random.random(), random.random())

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
        if len(self.trail) > 500:
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

    def draw_point(self, lat, lon, color):
        x, y = self.convert(lat, lon)
        self.map_axes.scatter(x, y, color=color)

    """
    def display(self):
        plt.show();
    """

    def draw_line(self, trail, color):
        xx = []
        yy = []
        for lat, lon in trail:
            x, y = self.convert(lat, lon)
            xx.append(x)
            yy.append(y)
        self.map_axes.plot(xx, yy, color=color, linewidth=1)

    def legend(self, satellites):
        start_y=20

        for i, sat in enumerate(satellites):
            geo = sat.get_position()
            lat = geo.latitude.degrees
            lon = geo.longitude.degrees
            alt = geo.elevation.km
            text = f"{sat.name[:10]} | {lat:.1f}, {lon:.1f} | {alt:.0f} km"

            self.map_axes.text(
                10,
                start_y + i * 15,
                text,
                fontsize=8,
                color=sat.color
            )

class Satellite_Manager:
    def __init__(self, satellites):
        self.all_satellites=satellites
        self.active=[]

    def find_sat(self, name):
        for sati in self.all_satellites:
            if name.upper() in sati.name.upper():
                return Satellite(sati)
        return None

    def add_satellite(self, name):
        sat=self.find_sat(name)
        if sat and sat.name not in [sati.name for sati in self.active]:
            self.active.append(sat)
            print(f"added: {sat.name}")
        else:
            print("Not found / alredy added")

    def remove_satellite(self, name):
        self.active = [s for s in self.active if name.upper() not in s.name]

def input_loop(manager, satellites):
    while True:
        cmd = input("Command: ")
        if cmd == "list":
            for s in satellites[:50]:
                print(s.name)
        elif cmd.startswith("list "):
            try:
                n = int(cmd.split()[1])
                for s in satellites[:n]:
                    print(s.name)
            except:
                print("Invalid number")
        elif cmd.startswith("search "):
            term = cmd[7:].upper()
            count = 0
            for s in satellites:
                if term in s.name.upper():
                    print(s.name)
                    count += 1
                    if count >= 20:
                        break
        elif cmd.startswith("add "):
            manager.add_satellite(cmd[4:])
        elif cmd.startswith("remove "):
            manager.remove_satellite(cmd[7:])
        elif cmd == "active":
            for sat in manager.active:
                print(sat.name)
        else:
            print("Commands: list, list N, search NAME, add NAME, remove NAME, active")

url = "https://celestrak.org/NORAD/elements/stations.txt"
satellites = load.tle_file(url)

for sati in satellites:
    print(sati.name)

manager=Satellite_Manager(satellites)
manager.add_satellite("ISS")

threading.Thread(target=input_loop, args=(manager, satellites), daemon=True).start()

m=TwoD_Map()
m.setup()
axbox = plt.axes([0.1, 0.02, 0.3, 0.05])
text_box = TextBox(axbox, 'Add Sat:')

axbutton = plt.axes([0.45, 0.02, 0.1, 0.05])
button = Button(axbutton, 'Add')

def add_satellite(event):
    name = text_box.text
    manager.add_satellite(name)
    text_box.set_val("")

axremove = plt.axes([0.6, 0.02, 0.1, 0.05])
remove_button = Button(axremove, 'Remove')

def remove_sat(event):
    name = text_box.text
    manager.remove_satellite(name)
    text_box.set_val("")

remove_button.on_clicked(remove_sat)
button.on_clicked(add_satellite)
while True:
    m.map_axes.clear()
    m.setup()

    for sat in manager.active:
        geo = sat.get_position()
        lat = geo.latitude.degrees
        lon = geo.longitude.degrees

        sat.update_trail(lat, lon)

        m.draw_line(sat.trail, sat.color)
        m.draw_point(lat, lon, sat.color)

        x, y = m.convert(lat, lon)
        m.map_axes.text(x, y, sat.name, fontsize=6)

    m.legend(manager.active)
    plt.pause(0.1)
"""
m.setup()
m.draw_point(0, 0)
m.draw_point(51.5, 0)
m.draw_point(54.7, 25.3)
m.draw_point(-33.9, 151)
m.draw_point(lat, lon)
m.display()
"""
