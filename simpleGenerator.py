class SimpleGenerator:
    def __init__(self, *,
                 init_args=[],
                 generator=lambda x: (x, ),
                 validator=lambda x: x):
        self._generate = generator
        self._validate = validator
        try:
            self._curent, *self._args = self._generate(*init_args)
        except StopIteration:
            self._curent = None

    def __iter__(self):
        return self

    def __next__(self):
        if self._validate(self._curent):
            next_val = self._curent
            try:
                self._curent, *self._args = self._generate(*self._args)
            except StopIteration:
                self._curent = None
            return next_val
        raise StopIteration()

    def next(self):
        return self.__next__()
