import unittest
from string_ops.manipulate import (
    split_by_comma,
    split_by_space,
    split_by_newline,
    join_by_comma,
    join_by_space,
    chunk_text,
    add_prefix_lines,
    add_suffix_lines,
    string_to_ascii_array,
    ascii_array_to_string,
)


class TestSplitOperations(unittest.TestCase):
    def test_split_by_comma(self):
        self.assertEqual(split_by_comma('a,b,c'), 'a\nb\nc')
        self.assertEqual(split_by_comma('single'), 'single')
        self.assertEqual(split_by_comma(''), '')
        self.assertEqual(split_by_comma('a, b, c'), 'a\n b\n c')

    def test_split_by_space(self):
        self.assertEqual(split_by_space('a b c'), 'a\nb\nc')
        self.assertEqual(split_by_space('single'), 'single')
        self.assertEqual(split_by_space(''), '')
        self.assertEqual(split_by_space('  a  b  '), 'a\nb')

    def test_split_by_newline(self):
        self.assertEqual(split_by_newline('a\nb\nc'), 'a\nb\nc')
        self.assertEqual(split_by_newline('single'), 'single')
        self.assertEqual(split_by_newline(''), '')


class TestJoinOperations(unittest.TestCase):
    def test_join_by_comma(self):
        self.assertEqual(join_by_comma('a\nb\nc'), 'a,b,c')
        self.assertEqual(join_by_comma('single'), 'single')
        self.assertEqual(join_by_comma(''), '')
        self.assertEqual(join_by_comma('a\nb\nc\n'), 'a,b,c')

    def test_join_by_space(self):
        self.assertEqual(join_by_space('a\nb\nc'), 'a b c')
        self.assertEqual(join_by_space('single'), 'single')
        self.assertEqual(join_by_space(''), '')


class TestChunkText(unittest.TestCase):
    def test_chunk_text(self):
        self.assertEqual(chunk_text('abcdef', 2), 'ab\ncd\nef')
        self.assertEqual(chunk_text('abcdef', 3), 'abc\ndef')
        self.assertEqual(chunk_text('abc', 5), 'abc')
        self.assertEqual(chunk_text('', 3), '')
        self.assertEqual(chunk_text('a', 3), 'a')


class TestAddPrefixSuffix(unittest.TestCase):
    def test_add_prefix_lines(self):
        self.assertEqual(add_prefix_lines('a\nb\nc', '# '), '# a\n# b\n# c')
        self.assertEqual(add_prefix_lines('single', '> '), '> single')
        self.assertEqual(add_prefix_lines('', '> '), '')
        self.assertEqual(add_prefix_lines('a\nb', ''), 'a\nb')

    def test_add_suffix_lines(self):
        self.assertEqual(add_suffix_lines('a\nb\nc', '!'), 'a!\nb!\nc!')
        self.assertEqual(add_suffix_lines('single', '...'), 'single...')
        self.assertEqual(add_suffix_lines('', '!'), '')
        self.assertEqual(add_suffix_lines('a\nb', ''), 'a\nb')


class TestAsciiArray(unittest.TestCase):
    def test_string_to_ascii_array(self):
        self.assertEqual(string_to_ascii_array('abc'), '97,98,99')
        self.assertEqual(string_to_ascii_array(''), '')
        self.assertEqual(string_to_ascii_array('A'), '65')
        self.assertEqual(string_to_ascii_array('hello'), '104,101,108,108,111')

    def test_ascii_array_to_string(self):
        self.assertEqual(ascii_array_to_string('97,98,99'), 'abc')
        self.assertEqual(ascii_array_to_string(''), '')
        self.assertEqual(ascii_array_to_string('65'), 'A')
        self.assertEqual(ascii_array_to_string('104,101,108,108,111'), 'hello')


if __name__ == '__main__':
    unittest.main()
