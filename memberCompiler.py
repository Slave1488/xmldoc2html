from lineToken import LineSummary
import xmlCompiler as xcomiler
from layout import Attribute


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
                    token.val.description)))
            doc_tokens.clear()
        elif token.sum == LineSummary.TRASH:
            if doc_tokens:
                doc_tokens.clear()
        else:
            raise ValueError()
