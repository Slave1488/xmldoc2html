import unittest
import sys
import os
try:
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 os.path.pardir))
    from layout import attributecreator
except Exception:
    print('Module is missing!')
    exit(1)


class TestAttributeCreator(unittest.TestCase):
    def test(self):
        attr = attributecreator.create_class('class_value')
        self.assertEqual((attr._name, attr._value), ('class', 'class_value'))


if __name__ == "__main__":
    unittest.main()
