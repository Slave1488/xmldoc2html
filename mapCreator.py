from functools import reduce
import layout
from tagMap import Map


def create(tag, *tags):
    tags = (tag,) + tags
    rmap = Map()
    attr_names = reduce(
        lambda acc, ntag: acc | {attr._name for attr in ntag.get_attrs()},
        tags, set())
    tag_names = reduce(
        lambda acc, ntag: acc | {tag._name for tag in ntag.get_tags()},
        tags, set())
    rmap.add_attr_points(*attr_names)
    rmap.add_tag_points(*tag_names)
    for tname in tag_names:
        rmap[tname] = create(
            *[child_tag for tag in tags for child_tag in tag.get_tags(tname)])
    return rmap
