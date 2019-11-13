import re
from layout.description import Tag, Attribute
from myxml.token import XmlSummary

attribute = re.compile(r'(\S+)="(.*)"')


def compile(name, tokens_gen, *attrs):
    tag = Tag(name)
    for attr in attrs:
        tag.add_attrs(attr)
    for token in tokens_gen:
        if token.sum == XmlSummary.CONTENT:
            tag.add_content(token.val)
        elif token.sum == XmlSummary.OPEN_TAG:
            name = token.val.split()[0]
            attrs = (Attribute(*adata)
                     for adata in attribute.findall(token.val))
            tag.add_content(compile(name, tokens_gen, *attrs))
        elif token.sum == XmlSummary.CLOSE_TAG:
            return tag
    return tag
