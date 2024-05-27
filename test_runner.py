import io
import sys
import unittest


def run_tests():
    original_stdout = sys.stdout
    sys.stdout = io.StringIO()
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    unittest.TextTestRunner().run(test_suite)
    sys.stdout = original_stdout


if __name__ == '__main__':
    run_tests()
