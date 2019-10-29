from collections import namedtuple
from lineLexer import LineToken, LineSummary
import xmlCompiler as xcomiler
from layout import Attribute


Member = namedtuple('member', [
    'memberID',
    'documentation'
])


def compile(line_tokens):
    doc_tokens = []
    for token in line_tokens:
        if token.sum == LineSummary.DOC:
            doc_tokens.extend(token.val)
        elif token.sum == LineSummary.HEADER:
            yield xcomiler.compile(
                'member', (token for token in doc_tokens),
                Attribute('name', '{}:{}'.format(
                    token.val.character.value,
                    token.val.description
                )))
            doc_tokens = []
        elif token.sum == LineSummary.TRASH:
            pass
        else:
            raise ValueError()
