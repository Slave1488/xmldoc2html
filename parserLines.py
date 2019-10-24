import sys
from collections import namedtuple
from functools import reduce
from itertools import chain
import re
MISSING_MODULE = 1
try:
    from layout import Tag, Attribute
except Exception as e:
    print(f'We have some problems: {e}', file=sys.stderr)
    exit(MISSING_MODULE)


class SimpleGenerator:
    def __init__(self, *,
                 init_args=None,
                 move=lambda x: (x, x),
                 validator=lambda x: x):
        self._move = move
        self._validate = validator
        self._curent, self._args = self._move(init_args)

    def __iter__(self):
        return self

    def __next__(self):
        if self._validate(self._curent):
            next_val = self._curent
            self._curent, self._args = self._move(self._args)
            return next_val
        raise StopIteration()

    def next(self):
        return self.__next__()


def get_reader(text_input, validator=lambda line: True):
    reader = SimpleGenerator(
        move=lambda args: (text_input.readline(), args),
        validator=lambda line: line and validator(line)
    )

    def change_validator(val):
        nonlocal validator
        validator = val
    reader.change_validator = change_validator
    return reader


def is_documentation_line(line):
    line = line.lstrip()
    return line[:3] == '///' and line[4] != '/'


def is_simple_line(line):
    return not is_documentation_line(line)


DocObject = namedtuple('docObject', [
    'name',
    'type_name'
])
NAMESPACE = 'N'
TYPE = 'T'
METHOD = 'M'
FIELD = 'F'
caption_trash = re.compile(r'\s*[:=;{].*', re.DOTALL)
method_signature = re.compile(r'\(.*\)$')
empty_signature = re.compile(r'\(\s*\)')


def parse_caption(caption):
    caption = caption_trash.sub('', caption)
    signature = method_signature.search(caption)
    caption = method_signature.sub('', caption).split()
    if len(caption) < 2:
        return
    name = caption[-1]
    if caption[-2] == 'namespace':
        type_name = NAMESPACE
    elif caption[-2] == 'class':
        type_name = TYPE
    elif signature:
        type_name = METHOD
        name = name, signature.group()
    else:
        type_name = FIELD
    return DocObject(name, type_name)


def catch_undocumented_object(line):
    parsed = parse_caption(line)
    if parsed and (parsed.type_name == 'N' or parsed.type_name == 'T'):
        return parsed


DocToken = namedtuple('docToken', [
    'sym',
    'val'
])
OPEN_TAG, CLOSE_TAG, CONTENT = range(3)
doc_trash = re.compile(r'///(?!/)')
doc_token = re.compile(r'(</.*?>)|(<.*?>)|([^<\s][^<]*[^<\s]|[^<\s])')


def get_token(simple_token):
    if simple_token[0]:
        return DocToken(CLOSE_TAG, simple_token[0])
    elif simple_token[1]:
        return DocToken(OPEN_TAG, simple_token[1])
    elif simple_token[2]:
        return DocToken(CONTENT, simple_token[2])
    else:
        raise ValueError()


def parse_doc_line(doc_line):
    doc_line = doc_trash.sub('', doc_line)
    return map(get_token, doc_token.findall(doc_line))


DocData = namedtuple('docData', [
    'doc_object',
    'documentation'
])


def compile_name(type_name, *hierarchy):
    name = '.'.join(hierarchy)
    return f'{type_name}:{name}'


def generate_member(doc_data, args):
    member = Tag('member')
    if doc_data.doc_object.type_name == NAMESPACE:
        args = [doc_data.doc_object.name]
    elif doc_data.doc_object.type_name == TYPE:
        args = args[:1] + [doc_data.doc_object.name]
    elif doc_data.doc_object.type_name == METHOD:
        self_name = doc_data.doc_object.name[0] if \
            not doc_data.doc_object.name[0] == args[1] else '#ctor'
        if not empty_signature.fullmatch(doc_data.doc_object.name[1]):
            self_name += doc_data.doc_object.name[1]
        args = args[:2] + [self_name]
    elif doc_data.doc_object.type_name == FIELD:
        args = args[:2] + [doc_data.doc_object.name]
    else:
        raise ValueError()
    member.add_attribute(Attribute(
        'name', compile_name(doc_data.doc_object.type_name, *args)))
    for token in doc_data.documentation:
        member.add_content(token.val)
    return member, args


def get_simple_parser(text_input):
    reader = get_reader(text_input, is_simple_line)

    def get_doc(args):
        for line in reader:
            catch = catch_undocumented_object(line)
            if catch:
                _, args = generate_member(DocData(catch, []), args)
        reader.change_validator(is_documentation_line)
        doc = list(reduce(chain, map(parse_doc_line, reader), []))
        reader.change_validator(is_simple_line)
        doc_object = parse_caption(reader.next())
        return generate_member(DocData(doc_object, doc), args)
    return SimpleGenerator(
        move=get_doc,
        init_args={}
    )
