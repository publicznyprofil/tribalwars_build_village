import unittest

from xml_parser import get_dict_from_xml_string


class TestXmlParser(unittest.TestCase):
    def test_get_dict_from_xml_string(self):
        xml_string = '<config><main><factor>1</factor><pop>2</pop></main><wood><pop>2</pop></wood></config>'
        dict_ = get_dict_from_xml_string(xml_string)

        for key in ['main', 'wood']:
            self.assertIn(key, dict_)
