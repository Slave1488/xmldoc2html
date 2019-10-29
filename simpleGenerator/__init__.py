__all__ = [
    'SimpleGenerator',
    'get_generator'
]


class SimpleGenerator:
    def __init__(self, *,
                 generator=lambda: None,
                 validator=lambda x: x is not None):
        self._generate = generator
        self._validate = validator
        self._save = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._save is not None:
            if self._validate(self._save):
                next_val = self._save
                self._save = None
                return next_val
            else:
                raise StopIteration()
        try:
            next_val = self._generate()
        except StopIteration:
            next_val = None
        if self._validate(next_val):
            return next_val
        else:
            self._save = next_val
            raise StopIteration()

    def next(self):
        return self.__next__()


def get_generator(collection):
    collection_iter = iter(collection)
    return SimpleGenerator(
        generator=lambda: next(collection_iter)
    )
