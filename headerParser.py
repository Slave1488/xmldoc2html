import re
from memberID import MemberID, Character

re_caption_trash = re.compile(r'\s*[:=;{].*', re.DOTALL)
re_method_signature = re.compile(r'\(.*\)$')
re_empty_signature = re.compile(r'\(\s*\)')


def parse(header):
    header = re_caption_trash.sub('', header)
    signature = re_method_signature.search(header)
    header_tokens = re_method_signature.sub('', header).split()
    if len(header_tokens) < 2:
        return
    description = header_tokens[-1]
    if header_tokens[-2] == 'namespace':
        character = Character.NAMESPACE
    elif header_tokens[-2] == 'class':
        character = Character.TYPE
    elif signature:
        signature = signature.group()
        character = Character.METHOD
        if not re_empty_signature.fullmatch(signature):
            description += signature
    else:
        character = Character.FIELD
    return MemberID(character, description)
