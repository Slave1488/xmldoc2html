import unittest
import sys
import os
try:
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 os.path.pardir))
    from filesup import reader
except Exception:
    print('Module is missing!')
    exit(1)


class ReaderTest(unittest.TestCase):
    def test(self):
        with open('tests/some_text.txt') as text:
            lines = text.readlines()
        with open('tests/some_text.txt') as text:
            self.assertEqual(list(reader.get_line_reader(text)), lines)


if __name__ == "__main__":
    unittest.main()
