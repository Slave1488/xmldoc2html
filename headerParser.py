import re
from enum import Enum
from collections import namedtuple


class MemberCharacter(Enum):
    NAMESPACE = 'N'
    TYPE = 'T'
    METHOD = 'M'
    FIELD = 'F'


MemberID = namedtuple('memberID', [
    'character',
    'description'
])

caption_trash = re.compile(r'\s*[:=;{].*', re.DOTALL)
method_signature = re.compile(r'\(.*\)$')
empty_signature = re.compile(r'\(\s*\)')


def parse(header):
    header = caption_trash.sub('', header)
    signature = method_signature.search(header)
    header_tokens = method_signature.sub('', header).split()
    if len(header_tokens) < 2:
        return
    description = header_tokens[-1]
    if header_tokens[-2] == 'namespace':
        character = MemberCharacter.NAMESPACE
    elif header_tokens[-2] == 'class':
        character = MemberCharacter.TYPE
    elif signature:
        signature = signature.group()
        character = MemberCharacter.METHOD
        if not empty_signature.fullmatch(signature):
            description += signature
    else:
        character = MemberCharacter.FIELD
    return MemberID(character, description)
