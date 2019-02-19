import argparse
import unittest

import pattern


class TestPatternValidator(unittest.TestCase):

    def test_simple_valid(self):
        testcases = ['abc', 'LLL', 'L-L', 'NNNNNabcd', 'AA']
        for testcase in testcases:
            self.assertEqual(pattern.validator(testcase), testcase)

    def test_invalid_chars(self):
        testcases = ['ab.c', 'L%LL', 'Ä§""$%=($%']
        for testcase in testcases:
            with self.assertRaises(argparse.ArgumentTypeError):
                pattern.validator(testcase)

    def test_dash_at_beginning(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('-ajkf')

    def test_dash_at_end(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('ajkf-')

    def test_tld_stripping(self):
        self.assertEqual(pattern.validator('AA.de'), 'AA')
        self.assertEqual(pattern.validator('abc.de'), 'abc')

    def test_to_short(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('')
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('a')


class TestPatternGenerateCandidates(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(pattern.generate_candiates("A"), ["{}.de".format(c) for c in pattern.LETTERS + pattern.NUMBERS])


if __name__ == '__main__':
    unittest.main()
