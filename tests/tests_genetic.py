import unittest

import mock

from genetic import (
    Creature,
    Population,
)


class TestCreature(unittest.TestCase):
    def setUp(self):
        self.buildings_template = {
            'main': 2,
            'barracks': 2,
        }
        self.creature1 = Creature(self.buildings_template, ['main', 'main', 'main', 'main'])
        self.creature2 = Creature(self.buildings_template, ['barracks', 'barracks', 'barracks', 'barracks'])

    def test_random_chromosome(self):
        creature = Creature(self.buildings_template, random_chromosome=True)
        self.assertCountEqual(['main', 'main', 'barracks', 'barracks'], creature.chromosome)

    def test_add_creatures(self):
        child1, child2 = self.creature1 + self.creature2

        self.assertEqual(['main', 'barracks', 'main', 'barracks'], child1.chromosome)
        self.assertEqual(['barracks', 'main', 'barracks', 'main'], child2.chromosome)

    @mock.patch('random.randint', return_value=3)
    def test_mod_creatures(self, *args):
        child1, child2 = self.creature1 % self.creature2

        self.assertEqual(['main', 'main', 'barracks', 'barracks'], child1.chromosome)
        self.assertEqual(['barracks', 'barracks', 'main', 'main'], child2.chromosome)

    def test_len(self):
        self.assertEqual(4, len(self.creature1))

    def test_normalize(self):
        self.creature1.normalize()
        self.assertEqual(['main', 'main', 'barracks', 'barracks'], self.creature1.chromosome)

    def test_skip_redundant_buildings(self):
        chromosome = []
        self.creature1.skip_redundant_buildings(chromosome)
        self.assertEqual(['main', 'main'], chromosome)

    def test_add_missing_buildings(self):
        chromosome = []
        self.creature1.add_missing_buildings(chromosome)
        self.assertEqual(['barracks', 'barracks'], chromosome)

    @mock.patch('random.randint', return_value=2)
    @mock.patch('random.choice', return_value='wood')
    @mock.patch('genetic.Creature.normalize', return_value=None)
    def test_mutates(self, *args):
        self.creature1.mutates()
        self.assertEqual(['main', 'main', 'wood', 'main'], self.creature1.chromosome)

    def test_build_time(self):
        self.assertEqual(72830.76923076922, self.creature1.build_time)


class TestPopulation(unittest.TestCase):
    def setUp(self):
        self.buildings_template = {
            'main': 2,
            'barracks': 2,
        }

    def test_random_population(self):
        population = Population(self.buildings_template)
        self.assertEqual(45, len(population.creatures))

    @mock.patch('genetic.Creature.normalize', return_value=None)
    @mock.patch('genetic.open', mock.mock_open())
    def test_selection(self, *args):
        population = Population(self.buildings_template)
        population.selection()
        self.assertEqual(45, len(population.creatures))
