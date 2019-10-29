import sys
from collections import namedtuple
from functools import reduce
from itertools import chain
import re
ERROR_MISSING_MODULE = 1
try:
    from layout import Tag, Attribute
    from simpleGenerator import SimpleGenerator, get_generator
except Exception as e:
    print(f'We have some problems: {e}', file=sys.stderr)
    exit(ERROR_MISSING_MODULE)


def get_reader(text_input, validator=lambda line: True):
    reader = SimpleGenerator(
        generator=lambda: (text_input.readline(),),
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
    'name_type'
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
        name_type = NAMESPACE
    elif caption[-2] == 'class':
        name_type = TYPE
    elif signature:
        name_type = METHOD
        name = name, signature.group()
    else:
        name_type = FIELD
    return DocObject(name, name_type)


def catch_undocumented_object(line):
    parsed = parse_caption(line)
    if parsed and (parsed.name_type == 'N' or parsed.name_type == 'T'):
        return parsed


DocToken = namedtuple('docToken', [
    'sym',
    'val'
])
OPEN_TAG, CLOSE_TAG, CONTENT = range(3)
doc_trash = re.compile(r'///(?!/)')
doc_token = re.compile(r'</(.*?)>|<(.*?)>|([^<\s][^<]*[^<\s]|[^<\s])')


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


def shove_doc_object(name_hierarchy, doc_object):
    name = doc_object.name
    name_type = doc_object.name_type
    if name_type == NAMESPACE:
        name_hierarchy = [name]
    elif name_type == TYPE:
        name_hierarchy = name_hierarchy[:1] + [name]
    elif name_type in [METHOD, FIELD]:
        name_hierarchy = name_hierarchy[:2] + [name]
    else:
        raise ValueError()
    return name_hierarchy


def compile_name(name_type, name_hierarchy):
    if name_type == METHOD:
        name_hierarchy[-1], signature = name_hierarchy[-1]
        if name_hierarchy[-1] == name_hierarchy[1]:
            name_hierarchy[-1] = '#ctor'
        if not empty_signature.fullmatch(signature):
            name_hierarchy[-1] += signature
    hierarchy_name = '.'.join(name_hierarchy)
    return f'{name_type}:{hierarchy_name}'


tag_name = re.compile(r'\S+')
attribute = re.compile(r'(\S+)="(.*)"')


def compile_tag(open_tag, content):
    name = tag_name.match(open_tag)
    if name:
        name = name.group()
    else:
        raise ValueError()
    tag = Tag(name)
    for attr in attribute.findall(open_tag):
        tag.add_attribute(Attribute(*attr))
    fill_tag(tag, content)
    return tag


def get_generator_tag(tokens, tag_name=None):
    def generate():
        token = tokens.__next__()
        if token.sym == CONTENT:
            return token.val,
        elif token.sym == OPEN_TAG:
            tag = compile_tag(token.val, tokens)
            return tag,
        elif token.sym == CLOSE_TAG:
            return None,
        else:
            raise ValueError()
    return SimpleGenerator(
        generator=generate
    )


def fill_tag(tag, tokens):
    for content in get_generator_tag(tokens):
        tag.add_content(content)


def compile_member(doc_data, name_hierarchy):
    member = Tag('member')
    member.add_attribute(Attribute(
        'name', compile_name(doc_data.doc_object.name_type, name_hierarchy)))
    fill_tag(member, iter(doc_data.documentation))
    return member


def get_generator_member(generator_doc):
    def generate(name_hierarchy):
        doc_data = generator_doc.__next__()
        name_hierarchy = shove_doc_object(name_hierarchy, doc_data.doc_object)
        member = compile_member(doc_data, name_hierarchy)
        return member, name_hierarchy
    return SimpleGenerator(
        generator=generate,
        init_args=([],)
    )


def get_generator_doc(reader):
    def generate():
        reader.change_validator(is_simple_line)
        for line in reader:
            catch = catch_undocumented_object(line)
            if catch:
                return DocData(catch, []),
        reader.change_validator(is_documentation_line)
        doc = list(reduce(chain, map(parse_doc_line, reader), []))
        reader.change_validator(is_simple_line)
        doc_object = parse_caption(reader.next())
        return DocData(doc_object, doc),
    return SimpleGenerator(
        generator=generate
    )


def compile_members(members):
    tag_members = Tag('members')
    for member in members:
        tag_members.add_content(member)
    return tag_members


file_extension = re.compile(r'\..*?$')


def compile_xmldoc(file_name, members):
    doc = Tag('doc')
    assembly = Tag('assembly')
    doc.add_content(assembly)
    assembly_name = Tag('name')
    assembly.add_content(assembly_name)
    name = file_extension.sub('', file_name)
    assembly_name.add_content(name)
    members = compile_members(members)
    doc.add_content(members)
    return doc


def simple_parse(text_input):
    reader = get_reader(text_input, is_simple_line)
    generator_doc = get_generator_doc(reader)
    generator_member = get_generator_member(
        filter(lambda doc: doc.documentation, generator_doc))
    return compile_xmldoc(text_input.name, generator_member)


def make_map(tag, name_key=None):
    if name_key:
        return reduce(
            merge_map, map(make_map, tag.get_tags(name_key)), Tag(name_key))
    mtag = Tag(tag._name)
    attrs = set(map(lambda attr: attr._name, tag.get_attributes()))
    for attr in attrs:
        mtag.add_attribute(attr)
    tag_names = set(map(lambda tag: tag._name, tag.get_tags()))
    for name in tag_names:
        mtag.add_content(make_map(tag, name))
    return mtag


def merge_map(mtag_x, mtag_y):
    if not mtag_x or not mtag_y:
        return mtag_x or mtag_y
    if mtag_x._name != mtag_y._name:
        raise ValueError()
    mtag_m = Tag(mtag_x._name)
    for attr in set(mtag_x.get_attributes() + mtag_y.get_attributes()):
        mtag_m.add_attribute(attr)
    mtag_names = set(map(
        lambda ptag: ptag._name,
        list(mtag_x.get_tags()) + list(mtag_y.get_tags())))
    for name in mtag_names:
        mtag_m.add_content(
            merge_map(mtag_x.get_tag(name), mtag_y.get_tag(name)))
    return mtag_m


class Cell:
    def __init__(self, *things):
        self._contents = things

    def add(self, *things):
        self._contents.extend(things)

    def merge(self, cell):
        self.add(*cell.get_content())

    def get_content(self):
        return self._contents


def hardcore_pareser(xmldoc):
    member_map = make_map(xmldoc.get_tag('members'), 'member')
