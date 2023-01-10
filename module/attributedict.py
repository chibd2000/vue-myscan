"""
 dict.['aaa'] -> dict.aaa
"""


class AttributeDict(dict):
    def __init__(self, temp_dict=None):
        if temp_dict is None:
            temp_dict = {}
        super().__init__(temp_dict)

    def __setattr__(self, key, value):
        super().__setitem__(key, value)

    def __getattr__(self, key):
        return self.__getitem__(key)
