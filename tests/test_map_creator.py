import unittest
import mapCreator
import layout
import tagMap


tested_tag = layout.Tag('tag')
child_tag = layout.Tag('tag')
child_tag.add_content('second_text')
tested_tag.add_content(child_tag, 'first_text')
tested_tag.add_attrs(layout.Attribute('name', 'value'))

expected_content = ['first_text', 'value', 'second_text']


class TestMapCreator(unittest.TestCase):
    def test(self):
        tmap = mapCreator.create(tested_tag)
        temp = list(map(lambda x: list(x)[0], tmap.get_content(tested_tag)))
        self.assertEqual(temp, expected_content)


if __name__ == "__main__":
    unittest.main()
