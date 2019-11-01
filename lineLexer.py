import re
from lineToken import create_token


def get_tokens(lines):
    for line in lines:
        yield create_token(line)
