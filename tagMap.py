import layout


class Map:
    def __init__(self):
        self._attr_names = set()
        self._tag_names = {}

    def add_attr_points(self, *attr_names):
        self._attr_names |= set(attr_names)

    def add_tag_points(self, *tag_names):
        for name in tag_names:
            if name not in self._tag_names:
                self._tag_names[name] = Map()

    def __getitem__(self, key):
        return self._tag_names[key]

    def __setitem__(self, key, value):
        self._tag_names[key] = value
