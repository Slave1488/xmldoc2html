import unittest
import layout.description as layout

attrs = [layout.Attribute('attr', 'val1'), layout.Attribute('attr', 'val2')]

text = 'some_text'

empty_tag = layout.Tag('empty')

tag_with_text = layout.Tag('haveText')
tag_with_text._content.append('secret_text')

tag_with_attr = layout.Tag('haveAttr')
tag_with_attr._content.append(layout.Tag('different'))

combo_tag = layout.Tag('combo')
combo_tag._content.extend(
    ['text1', layout.Tag('tag1'), 'text2', layout.Tag('tag2'), 'text3'])
combo_tag._attrs.extend(attrs)

tags = [empty_tag, tag_with_text, tag_with_attr, combo_tag]
content = [text] + tags


class TagTest(unittest.TestCase):
    def test_contain(self):
        tag = layout.Tag('tested_tag')
        tag.add_content(*content)
        self.assertEqual(tag._content, content, 'break contain content')
        tag.add_attrs(*attrs)
        self.assertEqual(tag._attrs, attrs, 'break contain attribute')

    def test_getter(self):
        tag = layout.Tag('tested_tag')
        tag._content.extend(content)
        self.assertEqual(list(tag.get_tags()), tags, 'break getter tags')
        self.assertEqual(list(tag.get_content()), [text], 'break getter texts')
        tag._attrs.extend(attrs)
        self.assertEqual(list(tag.get_attrs()), attrs, 'break getter attrs')


class AttributeTest(unittest.TestCase):
    def test_attr(self):
        attr = layout.Attribute('secret_name', 'secret_value')
        self.assertEqual((attr._name, attr._value),
                         ('secret_name', 'secret_value'), 'break attribute')


class PageTest(unittest.TestCase):
    def test_contain(self):
        page = layout.Page()
        page.add_content(*content)
        self.assertEqual(page._content, content, 'break contain content')

    def test_getter(self):
        page = layout.Page()
        page._content.extend(content)
        self.assertEqual(list(page.get_tags()), tags, 'break getter tags')
        self.assertEqual(list(page.get_content()), [text], 'break getter text')


if __name__ == "__main__":
    unittest.main()
