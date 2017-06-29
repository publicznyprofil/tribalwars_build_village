import requests

from xml_parser import get_dict_from_xml_string


class GameConfig:
    def __init__(self, world):
        tribalwars_link = '{}.plemiona.pl'.format(world)
        self.file_name = 'files/{}_building_info.txt'.format(tribalwars_link)
        self.file_link = 'http://{}/interface.php?func=get_building_info'.format(tribalwars_link)

    def get_buildings_config(self):
        xml_string = self.get_file().read()
        buildings_config_with_strings = get_dict_from_xml_string(xml_string)
        buildings_config = {}
        for key, value in buildings_config_with_strings.items():
            buildings_config[key] = value
            for key_, value_ in buildings_config_with_strings[key].items():
                buildings_config[key][key_] = float(value_)
        return buildings_config

    def get_file(self):
        try:
            file_ = open(self.file_name, 'r')
        except FileNotFoundError:
            self.download_file()
            file_ = open(self.file_name, 'r')
        return file_

    def download_file(self):
        with open(self.file_name, 'wb') as handle:
            response = requests.get(self.file_link, stream=True)
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
