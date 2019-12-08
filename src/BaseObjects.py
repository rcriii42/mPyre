"""BaseObjects - Define some basic objects

Space - the meta object for all objects that can be on a map
Map - a dictionary holding all the spaces on a map
"""

class Space:
    """Space - meta object"""

    def __init__(self, coords=(0,0), image=None, owner=None):
        self.coords = coords
        self.image = image
        self.owner = owner


class Map:
    """Map - meta object"""

    def __init__(self, name='The Map', dims=(10,10)):
        self.name = name
        self.dims = dims

    def __getitem__(self, item):
        'only accept spaces or lists of spaces'
        if type(item)==list:
            pass


