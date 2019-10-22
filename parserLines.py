class SimpleGenerator:
    def __init__(self, *,
                 default_val=None,
                 move=lambda x: (x, x),
                 move_args=None,
                 verify=bool):
        self._curent = default_val
        self._verify = verify
        self._move = move
        self._move_args = move_args | self._curent

    def __iter__(self):
        return self

    def __next__(self):
        self._curent, self._move_args = self._move(self._move_args)
        if self._verify(self._curent):
            return self._curent
        raise StopIteration()


class SimpleParser(SimpleGenerator):
    def __init__(self):
        super().__init__()
