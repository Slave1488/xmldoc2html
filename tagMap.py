import layout


class Map:
    def __init__(self):
        self._attr_names = set()
        self._tag_maps = {}

    def __getitem__(self, tag_name):
        return self._tag_maps[tag_name]

    def __setitem__(self, tag_name, tag_map):
        self._tag_maps[tag_name] = tag_map

    def add_attr_points(self, *attr_names):
        self._attr_names |= set(attr_names)

    def add_tag_points(self, *tag_names):
        for name in tag_names:
            if name not in self._tag_maps:
                self._tag_maps[name] = Map()

    def get_content(self, *tags):
        yield ('\n'.join(tag.get_content()) for tag in tags)
        for aname in self._attr_names:
            yield (attr._value for tag in tags for attr in tag.get_attrs())
        for tname in self._tag_maps:
            conts = self._tag_maps[tname].get_content(
                *(child_tag for tag in tags
                  for child_tag in tag.get_tags(tname)))
            for cont in conts:
                yield cont

    def get_names(self, main='main'):
        yield main
        for aname in self._attr_names:
            yield f'{main}.{aname}'
        for tname in self._tag_maps:
            for name in self._tag_maps[tname].get_names(main=tname):
                yield f'{main}.{name}'
