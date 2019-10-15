import sys
from functools import reduce
import operator
import re


def parse_line(line):
    name = re.search(
        r'(?:[^\s()]+(?:\(.*?\S.*?\))?$)|(?:[^\s()]+(?=\(\s*\)$))', line)
    name = name.group() if name else '???'
    sym = '?'
    if re.search(r'(?:class)|(?:delegate)', line):
        sym = 'T'
    elif re.search(r'event', line):
        sym = 'E'
    elif re.search(r'\(.*\)', line):
        sym = 'M'
    else:
        sym = 'F'
    return sym, name


f = open("content.txt", 'r')

content = f.read()

namespace = ('N', re.search(r'namespace ([^{\s]*)', content).group(1)), []

need_data = [namespace] + [
    (parse_line(re.search(r'(?:[^\s{;=][^{;=]*[^\s{;=])|(?:[^\s{;=])',
                          d[1]).group()),
     re.findall(r'(?:<.*?>)|(?:[^<\s/][^<\n/]*[^<\s])|(?:[^<\s/])',
                d[0]))
    for d in re.findall(r'([ \t\r\f\v]*///.*(?:\s*///.*)+)\n(.*)',
                        content)]


class Attribute:
    def __init__(self, name, value):
        self._name = name
        self._value = value

    def to_string(self):
        return "{0}=\"{1}\"".format(self._name, self._value)


class TextContent:
    def __init__(self, text):
        self._text = text

    def to_string(self):
        return self._text


class Tag:
    def __init__(self, name):
        self._name = name
        self._attributes = []
        self._content = []

    def add_content(self, content):
        self._content.append(content)

    def add_tag(self, tag):
        self.add_content(tag)

    def add_text(self, text):
        self.add_content(TextContent(text))

    def add_attribute(self, attribute):
        self._attributes.append(attribute)

    def to_string(self, *, file=sys.stdout):
        return "<{name}{attr}>{cont}\n</{name}>".format(
            name=self._name,
            attr=reduce(operator.add,
                        map(lambda a: ' ' + a.to_string(), self._attributes),
                        ""),
            cont=reduce(operator.add,
                        map(lambda c: '\n' + c.to_string(), self._content),
                        "").replace('\n', '\n\t') or '\n')


class MemberGen:
    def __init__(self):
        self._namespace = None
        self._class = None

    def create_members(self, data):
        res = []
        for d in data:
            t = Tag("member")
            for c in d[1]:
                t.add_text(c)
            val = "{}:".format(d[0][0])
            if self._namespace:
                val += self._namespace + '.'
                if self._class:
                    val += self._class + '.'
                    temp = re.compile('^{}(?=[\s(]|$)'.format(self._class))
                    if re.match(temp, d[0][1]):
                        val += re.sub(temp, '#ctor', d[0][1])
                    else:
                        val += d[0][1]
                elif d[0][0] == 'T':
                    self._class = d[0][1]
                    val += d[0][1]
                else:
                    print('MAGIC_ERROR')
                    sys.exit(1)
            elif d[0][0] == 'N':
                self._namespace = d[0][1]
                continue
            else:
                print('MAGIC_ERROR')
                sys.exit(1)
            t.add_attribute(Attribute('name', val))
            res.append(t)
        return res


mg = MemberGen()

members = Tag("members")
members._content = mg.create_members(need_data)


print(members.to_string())
