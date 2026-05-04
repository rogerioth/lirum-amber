import unittest
from string_ops.rearrange import (
    shuffle_characters,
    shuffle_words,
    shuffle_lines,
    sort_characters_asc,
    sort_characters_desc,
    sort_words_asc,
    sort_words_desc,
    sort_lines_asc,
    sort_lines_desc,
    sort_lines_by_length,
)


class TestShuffleOperations(unittest.TestCase):
    """Tests for shuffle operations."""

    def test_shuffle_characters(self):
        self.assertEqual(shuffle_characters("hello"), "leloh")
        self.assertEqual(shuffle_characters("abc"), "bac")
        self.assertEqual(shuffle_characters(""), "")
        self.assertEqual(shuffle_characters("a"), "a")
        self.assertEqual(shuffle_characters("aaaa"), "aaaa")

    def test_shuffle_words(self):
        self.assertEqual(shuffle_words("hello world foo"), "world hello foo")
        self.assertEqual(shuffle_words("a b c"), "b a c")
        self.assertEqual(shuffle_words("single"), "single")
        self.assertEqual(shuffle_words(""), "")
        self.assertEqual(shuffle_words("word1 word2 word3 word4"), shuffle_words("word1 word2 word3 word4"))

    def test_shuffle_lines(self):
        self.assertEqual(shuffle_lines("line1\nline2\nline3"), "line2\nline1\nline3")
        self.assertEqual(shuffle_lines("a\nb\nc"), "b\na\nc")
        self.assertEqual(shuffle_lines("single line"), "single line")
        self.assertEqual(shuffle_lines(""), "")
        self.assertEqual(shuffle_lines("line1\nline2\nline3\n"), "line2\nline1\nline3\n")


class TestSortCharacters(unittest.TestCase):
    """Tests for character sorting operations."""

    def test_sort_characters_asc(self):
        self.assertEqual(sort_characters_asc("cba"), "abc")
        self.assertEqual(sort_characters_asc(""), "")
        self.assertEqual(sort_characters_asc("aabb"), "aabb")
        self.assertEqual(sort_characters_asc("hello"), "ehllo")
        self.assertEqual(sort_characters_asc("321"), "123")
        self.assertEqual(sort_characters_asc("a"), "a")

    def test_sort_characters_desc(self):
        self.assertEqual(sort_characters_desc("abc"), "cba")
        self.assertEqual(sort_characters_desc(""), "")
        self.assertEqual(sort_characters_desc("aabb"), "bbaa")
        self.assertEqual(sort_characters_desc("hello"), "ollhe")
        self.assertEqual(sort_characters_desc("123"), "321")
        self.assertEqual(sort_characters_desc("a"), "a")


class TestSortWords(unittest.TestCase):
    """Tests for word sorting operations."""

    def test_sort_words_asc(self):
        self.assertEqual(sort_words_asc("banana apple cherry"), "apple banana cherry")
        self.assertEqual(sort_words_asc(""), "")
        self.assertEqual(sort_words_asc("single"), "single")
        self.assertEqual(sort_words_asc("z a m b"), "a b m z")
        self.assertEqual(sort_words_asc("hello hello world"), "hello hello world")

    def test_sort_words_desc(self):
        self.assertEqual(sort_words_desc("apple banana cherry"), "cherry banana apple")
        self.assertEqual(sort_words_desc(""), "")
        self.assertEqual(sort_words_desc("single"), "single")
        self.assertEqual(sort_words_desc("a b c"), "c b a")
        self.assertEqual(sort_words_desc("world hello banana"), "world hello banana")


class TestSortLines(unittest.TestCase):
    """Tests for line sorting operations."""

    def test_sort_lines_asc(self):
        self.assertEqual(sort_lines_asc("c\nb\na"), "a\nb\nc")
        self.assertEqual(sort_lines_asc(""), "")
        self.assertEqual(sort_lines_asc("single"), "single")
        self.assertEqual(sort_lines_asc("zebra\napple\nmango"), "apple\nmango\nzebra")
        self.assertEqual(sort_lines_asc("c\nb\na\n"), "a\nb\nc\n")

    def test_sort_lines_desc(self):
        self.assertEqual(sort_lines_desc("a\nb\nc"), "c\nb\na")
        self.assertEqual(sort_lines_desc(""), "")
        self.assertEqual(sort_lines_desc("single"), "single")
        self.assertEqual(sort_lines_desc("apple\nmango\nzebra"), "zebra\nmango\napple")
        self.assertEqual(sort_lines_desc("a\nb\nc\n"), "c\nb\na\n")

    def test_sort_lines_by_length(self):
        self.assertEqual(sort_lines_by_length("aaa\nbb\nc"), "c\nbb\naaa")
        self.assertEqual(sort_lines_by_length(""), "")
        self.assertEqual(sort_lines_by_length("single"), "single")
        self.assertEqual(sort_lines_by_length("long\nmedium\nshort"), "long\nshort\nmedium")
        self.assertEqual(sort_lines_by_length("a\nbb\nc\n"), "a\nc\nbb\n")


if __name__ == '__main__':
    unittest.main()
