import unittest
import headerParser
import memberID
import xmlLexer
import xmlToken
import lineLexer
import lineToken


class TestHeaderParser(unittest.TestCase):
    def test(self):
        parsed_namespace = headerParser.parse('namespace N')
        self.assertEqual(parsed_namespace,
                         memberID.MemberID(memberID.Character.NAMESPACE, 'N'))
        parsed_class = headerParser.parse('class T')
        self.assertEqual(parsed_class,
                         memberID.MemberID(memberID.Character.TYPE, 'T'))
        parsed_func = headerParser.parse('int foo(int x, int y) { bar(); }')
        self.assertEqual(parsed_func,
                         memberID.MemberID(memberID.Character.METHOD,
                                           'foo(int x, int y)'))
        parsed_fild = headerParser.parse('int PI = 314;')
        self.assertEqual(parsed_fild,
                         memberID.MemberID(memberID.Character.FIELD, 'PI'))


class TestXmlLexer(unittest.TestCase):
    def test(self):
        tokens = list(xmlLexer.get_tokens('text <tag>text</tag> text'))
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[1].sum, xmlToken.XmlSummary.OPEN_TAG)
        self.assertEqual(tokens[3].sum, xmlToken.XmlSummary.CLOSE_TAG)


lines = [
    '/// simple doc',
    'why is it header',
    '{ random string'
]


class TestLineLexer(unittest.TestCase):
    def test(self):
        tokens = list(lineLexer.get_tokens(lines))
        self.assertEqual(tokens[0].sum, lineToken.LineSummary.DOC)
        self.assertEqual(tokens[1].sum, lineToken.LineSummary.HEADER)
        self.assertEqual(tokens[2].sum, lineToken.LineSummary.TRASH)


if __name__ == '__main__':
    unittest.main()
