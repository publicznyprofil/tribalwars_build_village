import requests

from xml_parser import get_dict_from_xml_string


class GameConfig:
    def __init__(self, world):
        tribalwars_link = '{}.plemiona.pl'.format(world)
        self.buildings_file_name = 'files/{}_building_info.txt'.format(tribalwars_link)
        self.buildings_file_link = 'http://{}/interface.php?func=get_building_info'.format(tribalwars_link)

        self.config_file_name = 'files/{}_config.txt'.format(tribalwars_link)
        self.config_file_link = 'http://{}/interface.php?func=get_config'.format(tribalwars_link)

    def get_config(self):
        xml_string_buildings = self.get_file(self.buildings_file_name, self.buildings_file_link).read()
        xml_string_config = self.get_file(self.config_file_name, self.config_file_link).read()
        buildings_with_strings = get_dict_from_xml_string(xml_string_buildings)
        config_with_strings = get_dict_from_xml_string(xml_string_config)

        config = {
            'speed': float(config_with_strings['speed'])
        }
        for key, value in buildings_with_strings.items():
            config[key] = value
            for key_, value_ in value.items():
                config[key][key_] = float(value_)
        return config

    def get_file(self, file_name, file_link):
        try:
            file_ = open(file_name, 'r')
        except FileNotFoundError:
            self.download_file(file_name, file_link)
            file_ = open(file_name, 'r')
        return file_

    def download_file(self, file_name, file_link):
        with open(file_name, 'wb') as handle:
            response = requests.get(file_link, stream=True)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
