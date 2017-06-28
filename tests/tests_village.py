import unittest

from village import (
    Village,
    Building,
)


class TestBuilding(unittest.TestCase):
    def setUp(self):
        self.world = 'pl100'
        self.building = Building(self.world, 'main', 1)

    def test_time(self):
        self.assertEqual(90.03051200397678, self.building.time(2))

    def test_resources(self):
        self.assertEqual((90, 80, 70), self.building.resources)

    def test_points(self):
        self.assertEqual(10, self.building.points)
        self.assertEqual(512, Building(self.world, 'snob', 1).points)
        self.assertEqual(49, Building(self.world, 'smith', 16).points)


class TestVillage(unittest.TestCase):
    def setUp(self):
        self.world = 'pl100'
        self.village = Village(self.world)

    def test_build_normal_building(self):
        next_building = Building(self.world, 'main', 1)
        self.village.build(next_building)
        self.assertEqual(-90, self.village.wood)
        self.assertEqual(-80, self.village.stone)
        self.assertEqual(-70, self.village.iron)
        self.assertEqual(25, self.village.population)
        self.assertEqual(205, self.village.max_population)
        self.assertEqual(813, self.village.capacity)
        self.assertEqual(1, self.village.buildings['main'].level)
        self.assertEqual(10, self.village.points)

    def test_build_farm(self):
        next_building = Building(self.world, 'storage', 1)
        self.village.build(next_building)
        self.assertEqual(205, self.village.max_population)
        self.assertEqual(1000, self.village.capacity)
        self.assertEqual(6, self.village.points)

    def test_build_storage(self):
        next_building = Building(self.world, 'farm', 1)
        self.village.build(next_building)
        self.assertEqual(240, self.village.max_population)
        self.assertEqual(813, self.village.capacity)
        self.assertEqual(5, self.village.points)

    def test_add_resource(self):
        self.village.add_resource(10)
        self.assertEqual(0.07222222222222223, self.village.wood)
        self.assertEqual(0.07222222222222223, self.village.stone)
        self.assertEqual(0.07222222222222223, self.village.iron)

    def test_add_resource_max_capacity(self):
        self.village.add_resource(100000000000000)
        self.assertEqual(self.village.capacity, self.village.wood)
        self.assertEqual(self.village.capacity, self.village.stone)
        self.assertEqual(self.village.capacity, self.village.iron)


if __name__ == '__main__':
    unittest.main()
