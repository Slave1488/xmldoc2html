import re
from xmlToken import XmlToken, re_xml_token, XmlSummary


def get_token(simple_token):
    if simple_token[0]:
        return XmlToken(XmlSummary.CLOSE_TAG, simple_token[0])
    elif simple_token[1]:
        return XmlToken(XmlSummary.OPEN_TAG, simple_token[1])
    elif simple_token[2]:
        return XmlToken(XmlSummary.CONTENT, simple_token[2])
    else:
        raise ValueError()


def parse(line):
    return (get_token(stoken) for stoken in re_xml_token.findall(line))
