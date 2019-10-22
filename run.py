import sys
from functools import reduce
import operator
import re
from parserLines import SimpleParser


def run():
    def parse_line(line):
        name = re.search(
            r'(?:[^\s()]+(?:\(.*?\S.*?\))?$)|(?:[^\s()]+(?=\(\s*\)$))', line)
        name = name.group() if name else '???'
        sym = '?'
        if re.search(r'class', line):
            sym = 'T'
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
            self._value = text

        def to_string(self):
            return self._value

    class Tag:
        def __init__(self, name):
            self._name = name
            self._attributes = []
            self._content = []

        def __getitem__(self, key):
            return list(filter(lambda c: isinstance(c, Tag) and c._name == key,
                               self._content)) + \
                   list(filter(lambda a: a._name == key,
                               self._attributes))

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
                            map(lambda a: ' ' + a.to_string(),
                                self._attributes),
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
                tw = [t]
                for c in d[1]:
                    if re.fullmatch(r'</.*>', c):
                        tw.pop()
                    elif re.fullmatch(r'<.*>', c):
                        dt = re.findall(r'(?:^\S*)|(?:\S*=\".*?\")',
                                        re.search(r'<(.*)>', c).group(1))
                        nt = Tag(dt[0])
                        for a in dt[1:]:
                            da = re.fullmatch(r'(\S*)=\"(.*?)\"', a)
                            n, v = da[1], da[2]
                            nt.add_attribute(Attribute(n, v))
                        tw[-1].add_tag(nt)
                        tw.append(nt)
                    else:
                        tw[-1].add_text(c)
                val = f"{d[0][0]}:"
                if self._namespace:
                    val += self._namespace + '.'
                    if self._class:
                        val += self._class + '.'
                        temp = re.compile(
                            f'^{self._class}(?=[\\s(]|$)')
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
    for m in mg.create_members(need_data):
        members.add_tag(m)

    assembly = Tag("assembly")
    temp = Tag("name")
    temp.add_text("content")
    assembly.add_tag(temp)

    doc = Tag("doc")
    doc.add_tag(assembly)
    doc.add_tag(members)

    class Translater:
        def __init__(self):
            pass

        def translate(self, xmldoc):
            table = Tag("table")
            caption = Tag("caption")
            table.add_tag(caption)
            for c in xmldoc["assembly"][0]["name"][0]._content:
                caption.add_content(c)
            members = xmldoc["members"][0]

            def get_all_inner(tag):
                return [(tag._name,)] + \
                    [(tag._name, attr._name)
                     for attr in tag._attributes] + \
                    [(tag._name,) + inner
                     for inner_tag in filter(lambda c: isinstance(c, Tag),
                                             tag._content)
                     for inner in get_all_inner(inner_tag)]
            cs = list(filter(
                bool, map(
                    lambda n: n[2:],
                    sorted(filter(
                        lambda n: len(n) > 2 and n[0] == "members" and n[1] == "member",
                        set(get_all_inner(members)))))))
            thead = Tag("thead")
            for c in cs:
                td = Tag("td")
                td.add_text('.'.join(c))
                thead.add_tag(td)
            table.add_tag(thead)
            for m in members["member"]:
                tr = Tag("tr")
                for c in cs:
                    td = Tag("td")
                    cont = [m]
                    for kc in c:
                        cont = [nc for t in cont for nc in t[kc]]
                    for nc in cont:
                        if isinstance(nc, Attribute):
                            td.add_text(nc._value)
                        else:
                            for tc in filter(lambda x: isinstance(x, TextContent), nc._content):
                                td.add_content(tc)
                    tr.add_tag(td)
                table.add_tag(tr)
            return table

    xth = Translater()

    html = xth.translate(doc)

    with open("html.html", 'w') as f:
        f.write(html.to_string())
