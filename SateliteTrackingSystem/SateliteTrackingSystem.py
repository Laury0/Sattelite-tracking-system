"""
This is a program meant to track satelite movements and properly display them on a map
"""
import matplotlib.pyplot as plt
from datetime import datetime
from skyfield.api import load, EarthSatellite

now = datetime.utcnow()  #Palydovai naudoja UTC laika, padaryti i class veliau, kad palydovo clase paveldetu
formatted = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted)

class Satellite:
    def __init__(self, skyfield_sat):
        self.name = skyfield_sat.name
        self.sat = skyfield_sat
        self.ts = load.timescale()

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
        self.map_axes.set_xlim(0, self.width)
        self.map_axes.set_ylim(0, self.height)
        self.map_axes.invert_yaxis()

    def draw_point(self, lat, lon):
        x, y=self.convert(lat, lon)
        self.map_axes.scatter(x, y)

    def display(self):
        plt.show();

url = "https://celestrak.org/NORAD/elements/stations.txt"
satellites = load.tle_file(url)

iss_data = next(s for s in satellites if "ISS" in s.name)
iss = Satellite(iss_data)
iss.print_position()

m=TwoD_Map()
m.setup()
m.draw_point(30, 30)
m.display()

