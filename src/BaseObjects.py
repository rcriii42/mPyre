"""BaseObjects - Define some basic objects

Space - the meta object for all objects that can be on a map
Map - a dictionary holding all the spaces on a map
"""

class Unit(object):
    """Space - meta object"""

    def __init__(self, coords=(0,0)):
        self.coords = coords


class Map(object):
    """Map - meta object"""

    def __init__(self, name='The Map', dims=(10,10)):
        self.name = name
        self.dims = dims

    def __getitem__(self, item):
        'only accept spaces or lists of spaces'
        if type(item)==list:
            pass


