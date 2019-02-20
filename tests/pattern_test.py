import argparse
import unittest

import pattern


class TestPatternValidator(unittest.TestCase):

    def test_simple_valid(self):
        testcases = ['abc.de', 'LLL.de', 'L-L.de', 'NNNNNabcd.de', 'AA.de']
        for testcase in testcases:
            self.assertEqual(pattern.validator(testcase), testcase)

    def test_invalid_chars(self):
        testcases = ['ab.c', 'L%LL.de', 'Ä§""$%=($%.de']
        for testcase in testcases:
            with self.assertRaises(argparse.ArgumentTypeError):
                pattern.validator(testcase)

    def test_dash_at_beginning(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('-ajkf.de')

    def test_dash_at_end(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('ajkf-.de')
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('LNajd-')

    def test_tld_adding(self):
        self.assertEqual(pattern.validator('AA'), 'AA.de')
        self.assertEqual(pattern.validator('abc'), 'abc.de')

    def test_to_short(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('')
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('.e')
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('.de')


class TestPatternGenerateCandidates(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(pattern.generate_candiates('a.de'), ['a.de'])
        self.assertEqual(pattern.generate_candiates('A.de'), ['{}.de'.format(c) for c in pattern.LETTERS + pattern.NUMBERS])

    def test_no_dashes_at_start(self):
        self.assertEqual(len(list(filter(lambda elem: elem[0] is '-', pattern.generate_candiates('AAA.de')))), 0)

    def test_no_dashes_at_end(self):
        self.assertEqual(len(list(filter(lambda elem: elem[-3] is '-', pattern.generate_candiates('abA.de')))), 0)

    def test_generate_enough_candidates(self):
        len_numbers = len(pattern.NUMBERS)
        len_letters = len(pattern.LETTERS)
        len_arbitrary = len_letters + len_numbers

        self.assertEqual(len(pattern.generate_candiates('ahakjdgfdsghfgjfgb.de')), 1)
        self.assertEqual(len(pattern.generate_candiates('N.de')), len_numbers)
        self.assertEqual(len(pattern.generate_candiates('L.de')), len_letters)
        self.assertEqual(len(pattern.generate_candiates('A.de')), len_arbitrary)
        self.assertEqual(len(pattern.generate_candiates('AA.de')), len_arbitrary * len_arbitrary)
        self.assertEqual(len(pattern.generate_candiates('AAA.de')), len_arbitrary * (len_arbitrary + 1) * len_arbitrary)  # + 1 for dash
        self.assertEqual(len(pattern.generate_candiates('aAA.de')), (len_arbitrary + 1) * len_arbitrary)  # + 1 for dash


if __name__ == '__main__':
    unittest.main()
