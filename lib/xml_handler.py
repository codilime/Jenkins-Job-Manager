import xmltodict
from pprint import pformat


def snake_to_camel(snake_str: str) -> str:
    """
    Convert snake style string to camel case
    @param snake_str: input string
    @return: converted string
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.capitalize() or "_" for x in components[1:])


def keys_to_camel_case(kwargs: dict) -> dict:
    """
    Convert dict keys to camel case for XML compatibility
    @param kwargs: dictionary
    @return: dictionary with converted keys
    """
    normalized = {snake_to_camel(key): kwargs[key] for key in kwargs}
    return normalized


class XmlElement(dict):
    """
    Defines mechanism to access and modify dict keys as an object's attribute
    """

    def __setattr__(self, key: str, value):
        """
        Assign value to dict key by __setattr__
        @param key: key
        @param value: value
        @return:
        """
        if not key.startswith('_'):
            self[key] = value
        else:
            super().__setattr__(key, value)

    def __getattr__(self, item):
        """
        Allow to get dict item with getattr method
        @param item: dict key
        @return: plain data or new XmlElement
        """
        data = super().__getitem__(item)
        if issubclass(type(data), dict):
            xml_element = XmlElement(data)
            super().__setitem__(item, xml_element)  # reassign current element with new instance of XmlElement
        return super().__getitem__(item)

    def __getitem__(self, item):
        """
        Override getitem so it will return new XmlElement if element is type of dict, reuse __getattr__ implementation
        @param item:
        @return:
        """
        return self.__getattr__(item)
        

class XmlHandler:
    """
    Handle XML document like an OOP object
    """
    def __init__(self, xml_data: str):
        self._data = XmlElement(xmltodict.parse(xml_data))
    
    @property
    def data(self) -> XmlElement:
        """

        @return: XmlElement of root
        """
        return self._data

    def unparse(self) -> str:
        """

        @return: xml as string
        """
        return xmltodict.unparse(self._data, pretty=True)
    
    def __repr__(self):
        return pformat(self._data)