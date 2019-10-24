from functools import reduce
from operator import add
import re


def view(content):
    if hasattr(content, 'view'):
        return content.view()
    return f'{content}\n'


not_empty_line = re.compile(r'([^\n]+\n)')


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
        self._attributs = []
        self._content = []

    def add_attribute(self, attribute):
        self._attributs.append(attribute)

    def add_content(self, content):
        self._content.append(content)

    def view(self):
        attrs_view = reduce(
            add, map(lambda attr: f' {view(attr)}', self._attributs), '')
        content_view = reduce(
            add, map(lambda cont: f'{view(cont)}', self._content), '') or \
            '\n'
        return '<{name}{attr}>\n{cont}</{name}>\n'.format(
            name=self._name,
            attr=attrs_view,
            cont=move_text(content_view)
        )
