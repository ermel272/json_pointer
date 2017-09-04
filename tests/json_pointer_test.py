import unittest

from json_pointer import JsonPointer


class JsonPointerTest(unittest.TestCase):

    def setUp(self):
        self.pointer = JsonPointer('/foo/1')

    def test_move_pointer_forward(self):
        self.pointer.move_pointer_forward('baz')
        self.assertEqual(str(self.pointer), '/foo/1/baz')

        self.pointer.move_pointer_forward(0)
        self.assertEqual(str(self.pointer), '/foo/1/baz/0')

    def test_move_pointer_backward(self):
        attr = self.pointer.move_pointer_backward()
        self.assertEqual(attr, '1')
        self.assertEqual(str(self.pointer), '/foo')

        attr = self.pointer.move_pointer_backward()
        self.assertEqual(attr, 'foo')
        self.assertEqual(str(self.pointer), '')

        attr = self.pointer.move_pointer_backward()
        self.assertEqual(attr, None)
        self.assertEqual(str(self.pointer), '')
