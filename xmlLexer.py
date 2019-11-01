import re
from xmlToken import re_xml_token, get_token


def get_tokens(line):
    return (get_token(stoken) for stoken in re_xml_token.findall(line))
