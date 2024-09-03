# test_inc_dec.py

import unittest  # Or use 'import pytest' if you prefer pytest
import inc_dec 

class TestIncDec(unittest.TestCase):

    def test_increment(self):
        self.assertEqual(inc_dec.increment(5), 6)
        self.assertEqual(inc_dec.increment(-3), -2)
        self.assertEqual(inc_dec.increment(0), 1)

    def test_decrement(self):
        self.assertEqual(inc_dec.decrement(7), 6)
        self.assertEqual(inc_dec.decrement(-2), -3)
        self.assertEqual(inc_dec.decrement(0), -1)

if __name__ == '__main__':
    unittest.main()