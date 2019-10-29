import re
from collections import namedtuple
from enum import Enum
import headerParser as hparser
import xmlParser as xparser


LineToken = namedtuple('lineToken', [
    'sum',
    'val'
])


class LineSummary(Enum):
    TRASH, HEADER, DOC = range(3)


doc_line = re.compile(r'\s*///(?:[^/]|$)')
doc_trash = re.compile(r'///(?!/)')


def create_token(line):
    if doc_line.match(line):
        sum = LineSummary.DOC
        line = doc_trash.sub('', line)
        val = xparser.parse(line)
    elif (member_id := hparser.parse(line)) is not None:
        sum = LineSummary.HEADER
        val = member_id
    else:
        sum = LineSummary.TRASH
        val = line
    return LineToken(sum, val)


def get_tokens(lines):
    for line in lines:
        yield create_token(line)
