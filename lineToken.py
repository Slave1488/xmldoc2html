from collections import namedtuple
from enum import Enum
import re
import xmlLexer as xlexer
import headerParser as hparser

LineToken = namedtuple('lineToken', [
    'sum',
    'val'
])


class LineSummary(Enum):
    TRASH, HEADER, DOC = range(3)


re_doc_trash = re.compile(r'///(?!/)')
re_doc_line = re.compile(r'\s*///(?:[^/]|$)')


def create_token(line):
    if re_doc_line.match(line):
        sum = LineSummary.DOC
        line = re_doc_trash.sub('', line)
        val = xlexer.get_tokens(line)
    else:
        member_id = hparser.parse(line)
        if member_id is not None:
            sum = LineSummary.HEADER
            val = member_id
        else:
            sum = LineSummary.TRASH
            val = line
    return LineToken(sum, val)
