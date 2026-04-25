import random
from skyfield.api import wgs84

class SpaceObject:
    def __init__(self, name, color=None):
        self._name = name
        self._trail = []
        self._max_trail = 10000

        self._color = color if color else (
            random.random(), random.random(), random.random()
        )
    @property
    def name(self):
        return self._name
    @property
    def trail(self):
        return self._trail
    @property
    def color(self):
        return self._color
    def update_trail(self, lat, lon):
        self._trail.append((lat, lon))
        if len(self._trail) > self._max_trail:
            self._trail.pop(0)
    def get_position(self):
        raise NotImplementedError

class GroundStation(SpaceObject):
    def __init__(self, name, lat, lon):
        super().__init__(name, color=(1, 0, 0))
        self.lat = lat
        self.lon = lon
        self.location = wgs84.latlon(lat, lon)

    def get_position(self):
        return self.location

class Satellite(SpaceObject):
    def __init__(self, skyfield_sat, ts):
        super().__init__(skyfield_sat.name)
        self.sat = skyfield_sat
        self.ts = ts

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