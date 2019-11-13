import unittest
from filesup import reader


class ReaderTest(unittest.TestCase):
    def test(self):
        with open('tests/some_text.txt') as text:
            lines = text.readlines()
        with open('tests/some_text.txt') as text:
            self.assertEqual(list(reader.get_line_reader(text)), lines)


if __name__ == "__main__":
    unittest.main()
