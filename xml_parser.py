import xml.etree.ElementTree as ElementTree


class XmlListConfig(list):
    def __init__(self, list_):
        for element in list_:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    dict_ = XmlDictConfig(element)
                else:
                    dict_ = {element[0].tag: XmlListConfig(element)}
                if element.items():
                    dict_.update(dict(element.items()))
                self.update({element.tag: dict_})
            elif element.items():
                self.update({element.tag: dict(element.items())})
            else:
                self.update({element.tag: element.text})


def get_dict_from_xml_string(xml_string):
    root = ElementTree.XML(xml_string)
    return XmlDictConfig(root)
