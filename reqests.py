from layout import Tag, Attribute


def get_content(store):
    if isinstance(store, Tag):
        return store.get_content()
    elif isinstance(store, Attribute):
        return store._value
    else:
        raise ValueError()


class Reqest:
    def __init__(self, reqest):
        self._reqests = []
        self._reqest = reqest

    def add_reqest(self, stretcher, reqest):
        self._reqests.append((stretcher, reqest))

    def make_reqest(self, init_thing):
        res = []
        reqest_result = self._reqest(init_thing)
        if reqest_result:
            res.append(reqest_result)
        for stretcher, reqest in self._reqests:
            for thing in stretcher(init_thing):
                res.extend(reqest.make_reqest(thing))
        return res


def get_content_reqest():
    return Reqest(get_content)


def get_tag_stretcher(name):
    return lambda tag: tag.get_tags(name)


def get_attribute_stretcher(name):
    return lambda tag: tag.get_attributs(name)
