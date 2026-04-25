"""
For testing please open terminal with ctrl+' and write in py -m unittest Testing.py. BE SURE TO BE IN THE CORRECT DIRECTORY!!!
"""

import threading
import time
import random
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from skyfield.api import wgs84
from matplotlib.widgets import TextBox, Button
from datetime import datetime
from skyfield.api import load, EarthSatellite
from Core.Factory import SpaceObjectFactory
from Core.Space_Objects import Satellite, GroundStation
from Data.Manager import Satellite_Manager
from Map.Map import TwoD_Map

now = datetime.utcnow()  #Palydovai naudoja UTC laika, padaryti i class veliau, kad palydovo clase paveldetu
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
"""print(formatted)"""

ts=load.timescale()

class SatelliteApp:
    def __init__(self):
        self.manager = None
        self.satellites = None
        self.map = None

    def setup_system(self):
        url = "https://celestrak.org/NORAD/elements/stations.txt"
        self.satellites = load.tle_file(url)

        self.manager = Satellite_Manager(self.satellites, ts)
        self.manager.load_favorites()
        self.manager.add_satellite("ISS")

        vilnius = SpaceObjectFactory.create_object(
            "ground", "Vilnius", 54.7, 25.3)
        self.manager.active.append(vilnius)
        show_help()

    def setup_ui(self):
        axbox = plt.axes([0.1, 0.02, 0.3, 0.05])
        self.text_box = TextBox(axbox, 'Add Sat:')

        axbutton = plt.axes([0.45, 0.02, 0.1, 0.05])
        button = Button(axbutton, 'Add')

        axremove = plt.axes([0.6, 0.02, 0.1, 0.05])
        remove_button = Button(axremove, 'Remove')

        button.on_clicked(self.add_satellite)
        remove_button.on_clicked(self.remove_satellite)

    def add_satellite(self, event):
        name = self.text_box.text
        self.manager.add_satellite(name)
        self.text_box.set_val("")

    def remove_satellite(self, event):
        name = self.text_box.text
        self.manager.remove_satellite(name)
        self.text_box.set_val("")

def show_help():
    print("\n=== Satellite Tracking System ===")
    print("Made by Laurynas Davidavicius EIRf-25\n")

    print("Commands:")
    print(" list           - shows all satellites")
    print(" list N         - show first N satellites")
    print(" search NAME    - search satellites")
    print(" add NAME       - add satellite to map")
    print(" remove NAME    - remove satellite from map")
    print(" active         - show active satellites\n")

    print("Favorites:")
    print(" fav NAME       - add to favorites")
    print(" unfav NAME     - remove from favorites")
    print(" favorites      - show favorite list")
    print(" savefav        - save favorites to file")
    print(" loadfav        - load favorites from file")
    print(" addfav         - add all favorites to map")
    print(" resetfav       - reset map to favorites only\n")

    print(" help           - show this menu again")
    print("=================================\n")

def input_loop(manager, satellites):
    while True:
        cmd = input("Command: ")
        if cmd == "list":
            for s in satellites:
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
        elif cmd.startswith("fav "):
            manager.add_favorite(cmd[4:])
        elif cmd.startswith("unfav "):
            manager.remove_favorite(cmd[6:])
        elif cmd == "favorites":
            for f in manager.favorites:
                print(f)
        elif cmd == "savefav":
            manager.save_favorites()
        elif cmd == "loadfav":
            manager.load_favorites()
        elif cmd == "addfav":
            manager.add_all_favorites()
        elif cmd == "resetfav":
            manager.reset_to_favorites()
        elif cmd == "help":
            show_help()
        else:
            print("Commands: list, list N, search NAME, add NAME, remove NAME, active, fav NAME, unfav NAME, favorites, savefav, loadfav, addfav, resetfav")

app = SatelliteApp()
app.setup_system()

threading.Thread(
    target=input_loop,
    args=(app.manager, app.satellites),
    daemon=True
).start()

app.map = TwoD_Map(ts)
app.map.setup()

app.setup_ui()

while True:
    app.map.update(app.manager)
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
