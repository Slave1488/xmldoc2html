import layout


class Map:
    def __init__(self):
        self._attr_names = set()
        self._tag_names = {}

    def __getitem__(self, key):
        return self._tag_names[key]

    def __setitem__(self, key, value):
        self._tag_names[key] = value

    def add_attr_points(self, *attr_names):
        self._attr_names |= set(attr_names)

    def add_tag_points(self, *tag_names):
        for name in tag_names:
            if name not in self._tag_names:
                self._tag_names[name] = Map()

    def get_content(self, *tags):
        yield ('\n'.join(tag.get_content()) for tag in tags)
        for aname in self._attr_names:
            yield (attr._value for tag in tags for attr in tag.get_attrs())
        for tname in self._tag_names:
            conts = self._tag_names[tname].get_content(
                *(child_tag for tag in tags
                  for child_tag in tag.get_tags(tname)))
            for cont in conts:
                yield cont
