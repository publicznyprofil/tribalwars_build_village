import unittest

from game_config import GameConfig


class TestGameConfig(unittest.TestCase):
    def setUp(self):
        self.game_config = GameConfig(world='pl100')

    def test_get_buildings_config(self):
        keys = [
            'smith', 'storage', 'market', 'main',
            'wood', 'wall', 'statue', 'stable',
            'place', 'stone', 'iron', 'garage',
            'hide', 'barracks', 'farm', 'snob'
        ]
        buildings_config = self.game_config.get_buildings_config()

        for key in keys:
            self.assertIn(key, buildings_config)


if __name__ == '__main__':
    unittest.main()
