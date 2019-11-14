import unittest
import sys
import os
try:
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 os.path.pardir))
    from cscode import lineparser, linelexer, linetoken
    from myxml.member import id
    from myxml import lexer as xlexer, token as xtoken
except Exception:
    print('Module is missing!')
    exit(1)


class TestHeaderParser(unittest.TestCase):
    def test(self):
        parsed_namespace = lineparser.parse('namespace N')
        self.assertEqual(parsed_namespace,
                         id.MemberID(id.Character.NAMESPACE, 'N'))
        parsed_class = lineparser.parse('class T')
        self.assertEqual(parsed_class,
                         id.MemberID(id.Character.TYPE, 'T'))
        parsed_func = lineparser.parse('int foo(int x, int y) { bar(); }')
        self.assertEqual(parsed_func,
                         id.MemberID(id.Character.METHOD,
                                     'foo(int x, int y)'))
        parsed_fild = lineparser.parse('int PI = 314;')
        self.assertEqual(parsed_fild,
                         id.MemberID(id.Character.FIELD, 'PI'))


class TestXmlLexer(unittest.TestCase):
    def test(self):
        tokens = list(xlexer.get_tokens('text <tag>text</tag> text'))
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[1].sum, xtoken.XmlSummary.OPEN_TAG)
        self.assertEqual(tokens[3].sum, xtoken.XmlSummary.CLOSE_TAG)


lines = [
    '/// simple doc',
    'why is it header',
    '{ random string'
]


class TestLineLexer(unittest.TestCase):
    def test(self):
        tokens = list(linelexer.get_tokens(lines))
        self.assertEqual(tokens[0].sum, linetoken.LineSummary.DOC)
        self.assertEqual(tokens[1].sum, linetoken.LineSummary.HEADER)
        self.assertEqual(tokens[2].sum, linetoken.LineSummary.TRASH)


if __name__ == '__main__':
    unittest.main()
