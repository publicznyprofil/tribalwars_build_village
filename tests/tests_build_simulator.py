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


if __name__ == '__main__':
    unittest.main()
