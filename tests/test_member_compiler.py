import unittest
from layout import Tag
import xmlCompiler
import xmlToken
import memberCompiler
import lineToken
import memberID

tokens = [
    xmlToken.XmlToken(xmlToken.XmlSummary.CONTENT, 'text'),
    xmlToken.XmlToken(xmlToken.XmlSummary.OPEN_TAG, 'tag'),
    xmlToken.XmlToken(xmlToken.XmlSummary.CONTENT, 'text'),
    xmlToken.XmlToken(xmlToken.XmlSummary.CLOSE_TAG, 'tag'),
    xmlToken.XmlToken(xmlToken.XmlSummary.CONTENT, 'text'),
]

expected_tag = Tag('tag')
child_tag = Tag('tag')
child_tag.add_content('text')
expected_tag.add_content('text', child_tag, 'text')


class TestXmlCompiler(unittest.TestCase):
    def test(self):
        tokens_gen = (token for token in tokens)
        tag = xmlCompiler.compile('tag', tokens_gen)
        self.assertEqual(list(tag.get_content()),
                         list(expected_tag.get_content()))


line_tokens = [
    lineToken.LineToken(lineToken.LineSummary.DOC,
                        [xmlToken.XmlToken(xmlToken.XmlSummary.CONTENT,
                                           'doc_text')]),
    lineToken.LineToken(lineToken.LineSummary.HEADER,
                        memberID.MemberID(memberID.Character.NAMESPACE, 'N'))
]


class TestMemberCompiler(unittest.TestCase):
    def test(self):
        member = list(memberCompiler.compile(line_tokens))[0]
        self.assertEqual(list(member.get_content())[0], 'doc_text')


if __name__ == "__main__":
    unittest.main()
