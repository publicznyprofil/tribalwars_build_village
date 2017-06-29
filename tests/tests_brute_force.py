import unittest

from mock import mock

from brute_force import BruteForce


class TestBruteForce(unittest.TestCase):
    @mock.patch('brute_force.open', mock.mock_open())
    @mock.patch('brute_force.print', create=True)
    def test_run(self, *args):
        template = ['main', 'main']

        brute_force = BruteForce(template)
        brute_force.run()
        self.assertListEqual(['main', 'main'], brute_force.template)

        template = ['main', 'main', 'wood']

        brute_force = BruteForce(template)
        brute_force.run()
        self.assertListEqual(['wood', 'main', 'main'], brute_force.template)

    @mock.patch('brute_force.BuildSimulator')
    @mock.patch('brute_force.BuildSimulator', 'build_time', lambda: 0)
    def test_put_new_building_in_every_position(self, *args):
        template = ['main', 'main']

        brute_force = BruteForce(template, buildings=('e'))
        self.assertListEqual([['e', 'main', 'main'], ['main', 'e', 'main']], list(brute_force.put_new_building_in_every_position()))

        brute_force = BruteForce(template)
        self.assertEqual(12, len(list(brute_force.put_new_building_in_every_position())))

    @mock.patch('brute_force.BuildSimulator')
    @mock.patch('brute_force.BuildSimulator', 'build_time', lambda: 0)
    def test_change_order(self, *args):
        template = ['main', 'barracks']

        brute_force = BruteForce(template)
        self.assertListEqual(
            [['main', 'barracks'], ['barracks', 'main'], ['barracks', 'main'], ['main', 'barracks']],
            list(brute_force.change_order())
        )

    @mock.patch('brute_force.BuildSimulator')
    @mock.patch('brute_force.BuildSimulator', 'build_time', lambda: 0)
    def test_move_every_building_in_every_position(self, *args):
        template = ['a', 'b', 'c']

        brute_force = BruteForce(template)
        self.assertListEqual(
            [
                ['a', 'b', 'c'],
                ['b', 'a', 'c'],
                ['b', 'c', 'a'],
                ['b', 'a', 'c'],
                ['a', 'b', 'c'],
                ['a', 'c', 'b'],
                ['c', 'a', 'b'],
                ['a', 'c', 'b'],
                ['a', 'b', 'c']
            ],
            list(brute_force.move_every_building_in_every_position())
        )
