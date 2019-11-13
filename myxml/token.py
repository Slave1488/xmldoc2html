from collections import namedtuple
from enum import Enum
import re


XmlToken = namedtuple('xmlToken', [
    'sum',
    'val'
])
re_xml_token = re.compile(r'</(.*?)>|<(.*?)>|([^<\s][^<\n]*[^<\s]|[^<\s])')


class XmlSummary(Enum):
    OPEN_TAG, CLOSE_TAG, CONTENT = range(3)


def get_token(simple_token):
    if simple_token[0]:
        return XmlToken(XmlSummary.CLOSE_TAG, simple_token[0])
    elif simple_token[1]:
        return XmlToken(XmlSummary.OPEN_TAG, simple_token[1])
    elif simple_token[2]:
        return XmlToken(XmlSummary.CONTENT, simple_token[2])
    else:
        raise ValueError()
