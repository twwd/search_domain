import argparse
import unittest

import chunking


class TestPartitionValidator(unittest.TestCase):

    def test_simple_valid(self):
        testcases = [1, 2, 5, 2000]
        for testcase in testcases:
            self.assertEqual(testcase, chunking.validator(testcase))

    def test_conversion(self):
        testcases = [1, 2, 5, 2000]
        for testcase in testcases:
            self.assertEqual(testcase, chunking.validator(str(testcase)))

    def test_simple_invalud(self):
        testcases = [0, -1, -205865]
        for testcase in testcases:
            with self.assertRaises(argparse.ArgumentTypeError):
                chunking.validator(testcase)


class TestPatternGenerateCandidates(unittest.TestCase):

    def test_simple(self):
        self.assertEqual([1], chunking.get([1, 2, 3], 1, 3))
        self.assertEqual([2], chunking.get([1, 2, 3], 2, 3))
        self.assertEqual([3], chunking.get([1, 2, 3], 3, 3))

    def test_medium(self):
        test_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual([0, 1], chunking.get(test_list, 1, 5))
        self.assertEqual([2, 3], chunking.get(test_list, 2, 5))
        self.assertEqual([4, 5], chunking.get(test_list, 3, 5))
        self.assertEqual([6, 7], chunking.get(test_list, 4, 5))
        self.assertEqual([8, 9], chunking.get(test_list, 5, 5))

    def test_surplus(self):
        test_list = [1, 2, 3, 4, 5]
        self.assertEqual([1, 2], chunking.get(test_list, 1, 2))
        self.assertEqual([3, 4, 5], chunking.get(test_list, 2, 2))

    def test_advanced(self):
        test_list = list(range(0, 20000))
        chunks = 39
        result_list = []

        for i in range(1, chunks + 1):
            result_list.extend(chunking.get(test_list, i, chunks))

        self.assertEqual(test_list, result_list)


if __name__ == '__main__':
    unittest.main()
