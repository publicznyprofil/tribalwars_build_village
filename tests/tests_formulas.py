import unittest

from formulas import Formulas


class TestFormulas(unittest.TestCase):
    def setUp(self):
        self.formulas = Formulas('pl100')

    def test_build_time(self):
        self.assertEqual(94.53203760417561, self.formulas.build_time('main', 1, 1))
        self.assertEqual(90.03051200397678, self.formulas.build_time('main', 2, 1))
        self.assertEqual(85.74334476569217, self.formulas.build_time('main', 3, 1))
        self.assertEqual(29.31135135468762, self.formulas.build_time('main', 25, 1))
        self.assertEqual(56809.732752740194, self.formulas.build_time('main', 25, 30))

    def test_wood_cost(self):
        self.assertEqual(90, self.formulas.wood_cost('main', 1))
        self.assertEqual(73280, self.formulas.wood_cost('main', 30))

    def test_stone_cost(self):
        self.assertEqual(80, self.formulas.stone_cost('main', 1))
        self.assertEqual(91809, self.formulas.stone_cost('main', 30))

    def test_iron_cost(self):
        self.assertEqual(70, self.formulas.iron_cost('main', 1))
        self.assertEqual(56996, self.formulas.iron_cost('main', 30))

    def test_population_for_upgrade(self):
        self.assertEqual(1, self.formulas.population_for_upgrade('main', 1))
        self.assertEqual(69, self.formulas.population_for_upgrade('main', 30))

    def test_total_population(self):
        self.assertEqual(5, self.formulas.total_population('main', 1))
        self.assertEqual(475, self.formulas.total_population('main', 30))

    def test_production_info(self):
        self.assertEqual(
            (0.008333333333333333, 0.008333333333333333, 0.008333333333333333),
            self.formulas.production_info(1, 1, 1)
        )
        self.assertEqual(
            (0.4236111111111111, 0.49277777777777776, 0.6666666666666666),
            self.formulas.production_info(27, 28, 30)
        )

    def test_farm_population(self):
        self.assertEqual(240, self.formulas.farm_population(1))
        self.assertEqual(24000, self.formulas.farm_population(30))

    def test_storage_capacity(self):
        self.assertEqual(1000, self.formulas.storage_capacity(1))
        self.assertEqual(400000, self.formulas.storage_capacity(30))

    def test_production_per_hour(self):
        self.assertEqual(30, self.formulas.production_per_hour(1))
        self.assertEqual(2400, self.formulas.production_per_hour(30))

    def test_production_per_minut(self):
        self.assertEqual(0.5, self.formulas.production_per_minut(1))
        self.assertEqual(40, self.formulas.production_per_minut(30))

    def test_production_per_second(self):
        self.assertEqual(0.008333333333333333, self.formulas.production_per_second(1))
        self.assertEqual(0.6666666666666666, self.formulas.production_per_second(30))

    def test_points_for_upgrade(self):
        self.assertEqual(10, self.formulas.points_for_upgrade('main', 1))
        self.assertEqual(2, self.formulas.points_for_upgrade('main', 2))
        self.assertEqual(9, self.formulas.points_for_upgrade('main', 10))
        self.assertEqual(49, self.formulas.points_for_upgrade('smith', 16))
