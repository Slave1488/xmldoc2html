import unittest
from shutil import copyfile
from __main__ import main


class ComprehensiveTest(unittest.TestCase):
    def setUp(self):
        copyfile('tests/test_content.txt', 'content.txt')

    def test(self):
        main()


if __name__ == '__main__':
    unittest.main()
