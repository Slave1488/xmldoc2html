from collections import namedtuple


class SimpleGenerator:
    def __init__(self, *,
                 init_args=None,
                 move=None,
                 verify=None):
        self._move = move or (lambda x: (x, x))
        self._verify = verify or (lambda x: x)
        self._curent, self._args = self._move(init_args)

    def __iter__(self):
        return self

    def __next__(self):
        if self._verify(self._curent):
            next_val = self._curent
            self._curent, self._args = self._move(self._args)
            return next_val
        raise StopIteration()

    def next(self):
        return self.__next__()


def empty(generator):
    for temp in generator:
        pass


def get_reader(text_input, extra_verify=lambda line: True):
    def read(args):
        line = text_input.readline()
        return line, args

    def verify(line):
        return line and extra_verify(line)
    return SimpleGenerator(
        move=read,
        verify=verify
    )


def is_documentation_line(line):
    line = line.lstrip()
    return line[:3] == '///' and line[4] != '/'


def is_simple_line(line):
    return not is_documentation_line(line)


DocData = namedtuple('docData', [
    'caption',
    'documentation'
])


def get_simple_parser(text_input):
    VERIFY = is_simple_line

    def verify(line):
        return VERIFY(line)
    reader = get_reader(text_input, verify)

    def get_doc(args):
        nonlocal VERIFY
        empty(reader)
        VERIFY = is_documentation_line
        doc = list(map(lambda line: line.lstrip()[3:].strip(), reader))
        VERIFY = is_simple_line
        try:
            caption = reader.next().strip()
        except Exception:
            caption = None
        return DocData(caption, doc), args
    return SimpleGenerator(
        move=get_doc,
        verify=lambda doc_data: doc_data.caption
    )
