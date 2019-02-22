import argparse
import unittest

import chunking


class TestPartitionValidator(unittest.TestCase):

    def test_simple_valid(self):
        testcases = [1, 2, 5, 2000]
        for testcase in testcases:
            self.assertEqual(chunking.validator(testcase), testcase)

    def test_conversion(self):
        testcases = [1, 2, 5, 2000]
        for testcase in testcases:
            self.assertEqual(chunking.validator(str(testcase)), testcase)

    def test_simple_invalud(self):
        testcases = [0, -1, -205865]
        for testcase in testcases:
            with self.assertRaises(argparse.ArgumentTypeError):
                chunking.validator(testcase)


class TestPatternGenerateCandidates(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(chunking.get([1, 2, 3], 1, 3), [1])
        self.assertEqual(chunking.get([1, 2, 3], 2, 3), [2])
        self.assertEqual(chunking.get([1, 2, 3], 3, 3), [3])

    def test_advanced(self):
        test_list = list(range(0, 20000))
        chunks = 39
        result_list = []

        for i in range(1, chunks + 1):
            result_list.extend(chunking.get(test_list, i, chunks))

        self.assertEqual(result_list, test_list)


if __name__ == '__main__':
    unittest.main()
