import re
from collections import namedtuple
import parseHeader

TRASH, HEADER, DOC = range(3)
doc_line = re.compile(r'\s*///(?:[^/]|$)')
LineToken = namedtuple('lineToken', [
    'sym',
    'val'
])


def create_line_token(line):
    val = line
    if doc_line.match(line):
        sym = DOC
    elif res := parseHeader.parse_header(line):
        print(res)
        sym = HEADER
    else:
        sym = TRASH
    return LineToken(sym, val)


def get_line_tokens(lines):
    for line in lines:
        yield create_line_token(line)
