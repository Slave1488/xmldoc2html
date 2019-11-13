import unittest
from layout import attributecreator


class TestAttributeCreator(unittest.TestCase):
    def test(self):
        attr = attributecreator.create_class('class_value')
        self.assertEqual((attr._name, attr._value), ('class', 'class_value'))


if __name__ == "__main__":
    unittest.main()
