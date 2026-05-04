import unittest
from string_ops.find_replace import (
    find_and_replace,
    find_and_replace_all,
    regex_find,
    regex_replace,
    count_matches,
    extract_regex_groups,
)


class TestFindReplace(unittest.TestCase):
    def test_find_and_replace(self):
        self.assertEqual(find_and_replace("hello world", "world", "earth"), "hello earth")
        self.assertEqual(find_and_replace("hello world", "xyz", "abc"), "hello world")
        self.assertEqual(find_and_replace("", "a", "b"), "")
        self.assertEqual(find_and_replace("hello", "hello", ""), "")

    def test_find_and_replace_case_insensitive(self):
        self.assertEqual(find_and_replace("Hello World", "hello", "hi", case_insensitive=True), "hi World")

    def test_find_and_replace_all(self):
        self.assertEqual(find_and_replace_all("aaa bbb aaa", "aaa", "ccc"), "ccc bbb ccc")
        self.assertEqual(find_and_replace_all("aaaa", "aa", "bb"), "bbbb")
        self.assertEqual(find_and_replace_all("hello", "x", "y"), "hello")

    def test_find_and_replace_regex(self):
        self.assertEqual(
            find_and_replace("hello  world   foo", r"\s+", " ", regex=True),
            "hello world foo"
        )

    def test_regex_find(self):
        result = regex_find("hello 123 world 456", r'\d+')
        self.assertEqual(result, ['123', '456'])

    def test_regex_find_none(self):
        result = regex_find("hello world", r'\d+')
        self.assertEqual(result, [])

    def test_regex_replace(self):
        self.assertEqual(regex_replace("hello 123 world 456", r'\d+', 'X'), "hello X world X")

    def test_count_matches(self):
        self.assertEqual(count_matches("hello 123 world 456", r'\d+'), 2)
        self.assertEqual(count_matches("hello world", r'\d+'), 0)

    def test_extract_regex_groups(self):
        result = extract_regex_groups("abc123 def456", r'([a-z]+)(\d+)')
        self.assertEqual(result, [('abc', '123'), ('def', '456')])

    def test_extract_regex_groups_no_groups(self):
        result = extract_regex_groups("hello world", r'\w+')
        self.assertEqual(result, [('hello',), ('world',)])


if __name__ == '__main__':
    unittest.main()
