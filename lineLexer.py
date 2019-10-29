import re
from collections import namedtuple


TRASH, DOC = range(2)
doc_line = re.compile(r'\s*///(?:[^/]|$)')
LineToken = namedtuple('lineToken', [
    'sym',
    'val'
])


def create_line_token(line):
    if doc_line.match(line):
        sym = DOC
    else:
        sym = TRASH
    val = line
    return LineToken(sym, val)


def get_line_tokens(lines):
    for line in lines:
        yield create_line_token(line)
