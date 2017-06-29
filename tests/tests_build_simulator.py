import unittest

from build_simulator import BuildSimulator


class TestBuildSimulator(unittest.TestCase):
    def test_build_time(self):
        build_simulator = BuildSimulator(['main', 'main', 'main', 'main'])
        self.assertEqual(72830.76923076922, build_simulator.build_time)

        build_simulator = BuildSimulator(['storage', 'farm', 'main', 'main'])
        self.assertEqual(42646.153846153844, build_simulator.build_time)

    def test_target_resources(self):
        build_simulator = BuildSimulator(['storage', 'farm', 'main', 'main'], target_resources=(3, 300, 9000))
        self.assertEqual(1277723.0769230768, build_simulator.build_time)
        self.assertEqual(9000, build_simulator.target_iron)
        self.assertEqual(9000, build_simulator.village.iron)

    def test_build_time_with_supply(self):
        build_simulator = BuildSimulator(['storage', 'farm', 'main', 'main'], supply_resources=True)
        self.assertEqual(438.6286544833749, build_simulator.build_time)
        self.assertEqual(304.83212638428677, build_simulator.need_wood)
        self.assertEqual(268.83212638428677, build_simulator.need_stone)
        self.assertEqual(224.83212638428674, build_simulator.need_iron)

    def test_generate_build_time_with_high_building_level(self):
        build_simulator = BuildSimulator(['farm'] * 35)

        self.assertEqual(build_simulator.template.count('farm'), 30)

    def test_generate_build_time_with_too_small_farm_level(self):
        build_simulator = BuildSimulator(['main'] * 30)

        self.assertEqual(build_simulator.template.count('farm'), 6)

    def test_generate_build_time_with_already_builded_buildings(self):
        build_simulator = BuildSimulator(['main', 'main'])

        build_simulator.build_time = 0
        build_simulator.village.buildings['main'].level = 4

        build_simulator.template = []
        build_simulator.build_template = ['main', 'main', 'main', 'main']
        build_simulator.generate_build_time()
        self.assertEqual(build_simulator.build_time, 0)
