"""
This is a program meant to track satelite movements and properly display them on a map
"""
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


url = "https://celestrak.org/NORAD/elements/stations.txt"
satellites = load.tle_file(url)

# find ISS
iss_data = next(s for s in satellites if "ISS" in s.name)

# create object
iss = Satellite(iss_data)

# test
iss.print_position()