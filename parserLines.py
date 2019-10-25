import sys
from collections import namedtuple
from functools import reduce
from itertools import chain
import re
ERROR_MISSING_MODULE = 1
try:
    from layout import Tag, Attribute
    from simpleGenerator import SimpleGenerator
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


def compile_tag(open_tag):
    name = tag_name.match(open_tag)
    if name:
        name = name.group()
    else:
        raise ValueError()
    tag = Tag(name)
    for attr in attribute.findall(open_tag):
        tag.add_attribute(Attribute(*attr))
    return tag


def get_generator_content(tokens_iter, tag_name=None):
    def generate():
        token = tokens_iter.__next__()
        if token.sym == CONTENT:
            return token.val,
        elif token.sym == OPEN_TAG:
            tag = compile_tag(token.val)
            fill_tag(tag, tokens_iter)
            return tag,
        elif token.sym == CLOSE_TAG:
            return None,
        else:
            raise ValueError()
    return SimpleGenerator(
        generator=generate
    )


def fill_tag(tag, tokens_iter):
    for content in get_generator_content(tokens_iter):
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


def present(tag):
    ptag = Tag(tag._name)
    pattrs = set(map(lambda attr: attr._name, tag.get_attributes()))
    for pattr in pattrs:
        ptag.add_attribute(pattr)
    tag_names = set(map(lambda tag: tag._name, tag.get_tags()))
    for name in tag_names:
        ptag.add_content(
            reduce(merge_present, map(present, tag.get_tags(name))))
    return ptag


def merge_present(ptag_x, ptag_y):
    if not ptag_x or not ptag_y:
        return ptag_x or ptag_y
    if ptag_x._name != ptag_y._name:
        raise ValueError()
    ptag_m = Tag(ptag_x._name)
    for attr in set(ptag_x.get_attributes() + ptag_y.get_attributes()):
        ptag_m.add_attribute(attr)
    ptag_names = set(map(
        lambda ptag: ptag._name,
        list(ptag_x.get_tags()) + list(ptag_y.get_tags())))
    for name in ptag_names:
        ptag_m.add_content(
            merge_present(ptag_x.get_tag(name), ptag_y.get_tag(name)))
    return ptag_m


def hardcore_pareser(xmldoc):
    from layout import view
    print(view(present(xmldoc)))
