from Core.Factory import SpaceObjectFactory
from Core.Space_Objects import GroundStation
import json
import os

BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR, "favorites.json")


class Satellite_Manager:
    def __init__(self, satellites, ts):
        self.all_satellites = satellites
        self.ts = ts
        self.active = []
        self.favorites = []

    def add_favorite(self, name):
        if name.upper() not in [fav.upper() for fav in self.favorites]:
            self.favorites.append(name)
            print(f"Favorited: {name}")

    def remove_favorite(self, name):
        self.favorites = [fav for fav in self.favorites if name.upper() not in fav.upper()]
        print(f"Favorite removed: {name}")

    def save_favorites(self):
        data = {"favorites": self.favorites}
        with open(FILE_PATH, "w") as fav:
            json.dump(data, fav, indent=4)
        print("Favorites saved")

    def load_favorites(self):
        try:
            with open(FILE_PATH) as fav:
                data = json.load(fav)
                self.favorites = data.get("favorites", [])
                print("Favorites loaded")
        except FileNotFoundError:
            print("No favorites file found, save something first")
        except:
            print("Error reading favorites file")

    def add_all_favorites(self):
        for name in self.favorites:
            self.add_satellite(name)
        print("All favorites added to map")

    def reset_to_favorites(self):
        self.active = [obj for obj in self.active if isinstance(obj, GroundStation)]
        self.add_all_favorites()
        print("Showing only favorites")

    def find_sat(self, name):
        for sati in self.all_satellites:
            if name.upper() in sati.name.upper():
                return SpaceObjectFactory.create_object("satellite",sati,self.ts)
        return None

    def add_satellite(self, name):
        sat = self.find_sat(name)
        if not sat:
            print(f"{name}: Not found")
            return
        if sat.name in [s.name for s in self.active]:
            print(f"{sat.name}: Already added")
            return
        self.active.append(sat)
        print(f"{sat.name}: Added")

    def remove_satellite(self, name):
        self.active = [s for s in self.active if name.upper() not in s.name]
        print(f"Removed {name}")