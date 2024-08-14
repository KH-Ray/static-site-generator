import unittest

from page_generation import extract_title


class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        extracted_title = extract_title("# Hello")
        result = "Hello"

        self.assertEqual(result, extracted_title)
