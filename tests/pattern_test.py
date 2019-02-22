import argparse
import unittest

import pattern


class TestPatternValidator(unittest.TestCase):

    def test_simple_valid(self):
        testcases = ['abc.de', 'LLL.de', 'L-L.de', 'DDDDDabcd.de', 'AA.de']
        for testcase in testcases:
            self.assertEqual(testcase, pattern.validator(testcase))

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
            pattern.validator('LDajd-')

    def test_tld_adding(self):
        self.assertEqual('AA.de', pattern.validator('AA'))
        self.assertEqual('abc.de', pattern.validator('abc'))

    def test_to_short(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('')
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('.e')
        with self.assertRaises(argparse.ArgumentTypeError):
            pattern.validator('.de')


class TestPatternGenerateCandidates(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(['a.de'], pattern.generate_candiates('a.de'))
        self.assertEqual(['{}.de'.format(c) for c in pattern.LETTERS + pattern.DIGITS], pattern.generate_candiates('A.de'))

    def test_no_dashes_at_start(self):
        self.assertEqual(0, len(list(filter(lambda elem: elem[0] is '-', pattern.generate_candiates('AAA.de')))))

    def test_no_dashes_at_end(self):
        self.assertEqual(0, len(list(filter(lambda elem: elem[-3] is '-', pattern.generate_candiates('abA.de')))))

    def test_generate_enough_candidates(self):
        len_digits = len(pattern.DIGITS)
        len_letters = len(pattern.LETTERS)
        len_arbitrary = len_letters + len_digits

        self.assertEqual(1, len(pattern.generate_candiates('ahakjdgfdsghfgjfgb.de')))
        self.assertEqual(len_digits, len(pattern.generate_candiates('D.de')))
        self.assertEqual(len_letters, len(pattern.generate_candiates('L.de')))
        self.assertEqual(len_arbitrary, len(pattern.generate_candiates('A.de')))
        self.assertEqual(len_arbitrary * len_arbitrary, len(pattern.generate_candiates('AA.de')))
        self.assertEqual(len_arbitrary * (len_arbitrary + 1) * len_arbitrary, len(pattern.generate_candiates('AAA.de')))  # + 1 for dash
        self.assertEqual((len_arbitrary + 1) * len_arbitrary, len(pattern.generate_candiates('aAA.de')))  # + 1 for dash


if __name__ == '__main__':
    unittest.main()
