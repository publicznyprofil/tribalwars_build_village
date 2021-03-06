import unittest

from mock import mock

from game_config import GameConfig


class TestGameConfig(unittest.TestCase):
    def setUp(self):
        self.game_config = GameConfig(world='pl100')

    def test_get_buildings_config(self):
        keys = [
            'speed',
            'smith', 'storage', 'market', 'main',
            'wood', 'wall', 'statue', 'stable',
            'place', 'stone', 'iron', 'garage',
            'hide', 'barracks', 'farm', 'snob'
        ]
        config = self.game_config.get_config()

        for key in keys:
            self.assertIn(key, config)

    @mock.patch('requests.get', return_value=type('response', (), {'iter_content': lambda x: [b'0123456', b'']}))
    @mock.patch('game_config.open', mock.mock_open())
    def test_download_file(self, *args):
        self.game_config.download_file(self.game_config.buildings_file_name, self.game_config.buildings_file_link)

    def test_get_file_failure(self):
        self.game_config.download_file = lambda x, y: None
        with mock.patch('game_config.open', mock.MagicMock(), create=True) as mocked_open:
            mocked_open.side_effect = FileNotFoundError()
            self.assertRaises(FileNotFoundError, self.game_config.get_file, self.game_config.buildings_file_name, self.game_config.buildings_file_link)
            self.assertTrue(mocked_open.called)
