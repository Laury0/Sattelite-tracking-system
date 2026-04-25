import unittest
from Core.Factory import SpaceObjectFactory
from Core.Space_Objects import Satellite, GroundStation
from Data.Manager import Satellite_Manager
from skyfield.api import load

ts = load.timescale()

class TestFactory(unittest.TestCase):

    def test_create_satellite(self):
        fake_sat = type("FakeSat", (), {"name": "TEST-SAT"})
        sat = SpaceObjectFactory.create_object("satellite", fake_sat, ts)
        self.assertIsInstance(sat, Satellite)
        self.assertEqual(sat.name, "TEST-SAT")

    def test_create_ground(self):
        ground = SpaceObjectFactory.create_object("ground", "Vilnius", 54.7, 25.3)
        self.assertIsInstance(ground, GroundStation)
        self.assertEqual(ground.name, "Vilnius")


class TestManager(unittest.TestCase):

    def setUp(self):
        fake_sat = type("FakeSat", (), {"name": "TEST-SAT"})
        self.satellites = [fake_sat]
        self.manager = Satellite_Manager(self.satellites, ts)

    def test_add_satellite(self):
        self.manager.add_satellite("TEST")
        self.assertEqual(len(self.manager.active), 1)

    def test_remove_satellite(self):
        self.manager.add_satellite("TEST")
        self.manager.remove_satellite("TEST")
        self.assertEqual(len(self.manager.active), 0)


class TestSpaceObject(unittest.TestCase):

    def test_trail_update(self):
        ground = GroundStation("Test", 0, 0)
        ground.update_trail(10, 20)
        self.assertEqual(len(ground.trail), 1)


if __name__ == "__main__":
    unittest.main()