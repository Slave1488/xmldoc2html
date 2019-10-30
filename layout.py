from functools import reduce
from operator import add
import re


def view(content):
    if hasattr(content, 'view'):
        return content.view()
    return content


not_empty_line = re.compile(r'(.+)')


def move_text(text):
    return not_empty_line.sub(r'\t\1', text)


class Attribute:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def view(self):
        return f'{self._name}="{self._value}"'


class Tag:
    def __init__(self, name):
        self._name = name
        self._attrs = []
        self._content = []

    def add_attr(self, attr):
        self._attrs.append(attr)

    def get_attrs(self, name=None):
        if name:
            return filter(lambda attr: attr._name == name, self._attrs)
        return self._attrs

    def add_content(self, *content):
        self._content.extend(content)

    def get_content(self):
        return filter(lambda cont: not isinstance(cont, Tag), self._content)

    def get_tags(self, name=None):
        if name:
            return filter(lambda tag: tag._name == name, self.get_tags())
        return filter(lambda cont: isinstance(cont, Tag), self._content)

    def get_tag(self, name):
        tags = list(self.get_tags(name))
        return tags[0] if tags else None

    def view(self):
        attrs_view = reduce(
            add, map(lambda attr: f' {view(attr)}', self._attrs), '')
        content_view = reduce(
            add, map(lambda cont: f'{view(cont)}\n', self._content), '') or \
            '\n'
        return '<{name}{attr}>\n{cont}</{name}>'.format(
            name=self._name,
            attr=attrs_view,
            cont=move_text(content_view)
        )
