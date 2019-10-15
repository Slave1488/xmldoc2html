import unittest
from shutil import copyfile
from run import run


class ComprehensiveTest(unittest.TestCase):
    def setUp(self):
        copyfile('tests/test_content.txt', 'content.txt')

    def test(self):
        try:
            run()
        except Exception as e:
            self.fail()


if __name__ == '__main__':
    unittest.main()
