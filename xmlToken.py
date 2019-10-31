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
