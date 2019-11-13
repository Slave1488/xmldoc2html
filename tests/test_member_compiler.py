import unittest
from layout.description import Tag
from myxml import compiler as xcompiler, token
from myxml.member import compiler as mcompiler, id
from cscode import linetoken

tokens = [
    token.XmlToken(token.XmlSummary.CONTENT, 'text'),
    token.XmlToken(token.XmlSummary.OPEN_TAG, 'tag'),
    token.XmlToken(token.XmlSummary.CONTENT, 'text'),
    token.XmlToken(token.XmlSummary.CLOSE_TAG, 'tag'),
    token.XmlToken(token.XmlSummary.CONTENT, 'text'),
]

expected_tag = Tag('tag')
child_tag = Tag('tag')
child_tag.add_content('text')
expected_tag.add_content('text', child_tag, 'text')


class TestXmlCompiler(unittest.TestCase):
    def test(self):
        tokens_gen = (token for token in tokens)
        tag = xcompiler.compile('tag', tokens_gen)
        self.assertEqual(list(tag.get_content()),
                         list(expected_tag.get_content()))


line_tokens = [
    linetoken.LineToken(linetoken.LineSummary.DOC,
                        [token.XmlToken(token.XmlSummary.CONTENT,
                                        'doc_text')]),
    linetoken.LineToken(linetoken.LineSummary.HEADER,
                        id.MemberID(id.Character.NAMESPACE, 'N'))
]


class TestMemberCompiler(unittest.TestCase):
    def test(self):
        member = list(mcompiler.compile(line_tokens))[0]
        self.assertEqual(list(member.get_content())[0], 'doc_text')


if __name__ == "__main__":
    unittest.main()
