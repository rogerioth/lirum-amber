import unittest
from string_ops.format_ops import (
    trim,
    trim_left,
    trim_right,
    trim_newlines,
    collapse_whitespace,
    remove_empty_lines,
    remove_duplicate_lines,
    sort_lines,
    deduplicate_lines,
    indent_text,
    unindent_text,
    wrap_text,
    replace_line_endings,
    slugify,
    truncate,
    pad_left,
    pad_right,
    add_line_numbers,
    remove_line_numbers,
    extract_lines,
    normalize_unicode,
    strip_non_ascii,
    remove_diacritics,
)


class TestTrim(unittest.TestCase):
    def test_trim(self):
        self.assertEqual(trim("  hello  "), "hello")
        self.assertEqual(trim("\thello\t"), "hello")
        self.assertEqual(trim("\nhello\n"), "hello")
        self.assertEqual(trim("hello"), "hello")
        self.assertEqual(trim(""), "")
        self.assertEqual(trim("   "), "")
        self.assertEqual(trim("\t\n\r hello \t\n\r"), "hello")

    def test_trim_left(self):
        self.assertEqual(trim_left("  hello  "), "hello  ")
        self.assertEqual(trim_left("hello"), "hello")
        self.assertEqual(trim_left(""), "")

    def test_trim_right(self):
        self.assertEqual(trim_right("  hello  "), "  hello")
        self.assertEqual(trim_right("hello"), "hello")
        self.assertEqual(trim_right(""), "")

    def test_trim_newlines(self):
        self.assertEqual(trim_newlines("\n\nhello\n\n"), "hello")
        self.assertEqual(trim_newlines("hello"), "hello")
        self.assertEqual(trim_newlines("\n\n"), "")
        self.assertEqual(trim_newlines("  hello  "), "  hello  ")


class TestWhitespace(unittest.TestCase):
    def test_collapse_whitespace(self):
        self.assertEqual(collapse_whitespace("hello   world"), "hello world")
        self.assertEqual(collapse_whitespace("\thello\tworld\t"), "hello world")
        self.assertEqual(collapse_whitespace("  hello  world  "), "hello world")
        self.assertEqual(collapse_whitespace(""), "")
        self.assertEqual(collapse_whitespace("a\t\t\tb"), "a b")
        self.assertEqual(collapse_whitespace("hello\n\nworld"), "hello world")

    def test_collapse_whitespace_preserve_breaks(self):
        result = collapse_whitespace("hello\n\nworld", preserve_breaks=True)
        self.assertEqual(result, "hello\n\nworld")

    def test_remove_empty_lines(self):
        self.assertEqual(remove_empty_lines("a\n\nb\n\nc"), "a\nb\nc")
        self.assertEqual(remove_empty_lines("\n\n\n"), "")
        self.assertEqual(remove_empty_lines("a\nb\nc"), "a\nb\nc")
        self.assertEqual(remove_empty_lines(""), "")
        self.assertEqual(remove_empty_lines("a\n  \nb"), "a\nb")


class TestLineOps(unittest.TestCase):
    def test_remove_duplicate_lines(self):
        self.assertEqual(remove_duplicate_lines("a\nb\na\nc\nb"), "a\nb\nc")
        self.assertEqual(remove_duplicate_lines("a\na\na"), "a")
        self.assertEqual(remove_duplicate_lines(""), "")
        self.assertEqual(remove_duplicate_lines("a"), "a")

    def test_sort_lines(self):
        self.assertEqual(sort_lines("c\na\nb"), "a\nb\nc")
        self.assertEqual(sort_lines("b\na\nc"), "a\nb\nc")
        self.assertEqual(sort_lines(""), "")
        self.assertEqual(sort_lines("a"), "a")
        self.assertEqual(sort_lines("10\n2\n1"), "1\n10\n2")

    def test_sort_lines_case_insensitive(self):
        self.assertEqual(sort_lines("B\na\nC", case_insensitive=True), "a\nB\nC")

    def test_deduplicate_lines(self):
        self.assertEqual(deduplicate_lines("a\na\nb\nb\nc"), "a\nb\nc")
        self.assertEqual(deduplicate_lines("a\nb\nc"), "a\nb\nc")
        self.assertEqual(deduplicate_lines(""), "")

    def test_indent_text(self):
        self.assertEqual(indent_text("hello\nworld", 4), "    hello\n    world")
        self.assertEqual(indent_text("hello", 2), "  hello")
        self.assertEqual(indent_text("", 4), "")
        self.assertEqual(indent_text("a\n\nb", 2), "  a\n  \n  b")

    def test_unindent_text(self):
        self.assertEqual(unindent_text("    hello\n    world", 4), "hello\nworld")
        self.assertEqual(unindent_text("  hello", 2), "hello")
        self.assertEqual(unindent_text("hello", 4), "hello")


class TestWrap(unittest.TestCase):
    def test_wrap_text(self):
        result = wrap_text("hello world foo bar", 10)
        lines = result.split("\n")
        self.assertTrue(all(len(line) <= 10 for line in lines))

    def test_wrap_text_short(self):
        self.assertEqual(wrap_text("hello", 10), "hello")
        self.assertEqual(wrap_text("", 10), "")

    def test_wrap_text_preserve_breaks(self):
        result = wrap_text("hello\nworld\nfoo bar baz", 10, preserve_breaks=True)
        self.assertIn("hello\nworld\n", result)


class TestLineEndings(unittest.TestCase):
    def test_replace_line_endings_crlf(self):
        self.assertEqual(replace_line_endings("a\nb\nc", "crlf"), "a\r\nb\r\nc")

    def test_replace_line_endings_cr(self):
        self.assertEqual(replace_line_endings("a\nb\nc", "cr"), "a\rb\rc")

    def test_replace_line_endings_lf(self):
        self.assertEqual(replace_line_endings("a\r\nb\rc", "lf"), "a\nb\nc")


class TestSlugify(unittest.TestCase):
    def test_slugify_basic(self):
        self.assertEqual(slugify("Hello World"), "hello-world")
        self.assertEqual(slugify("Hello  World!"), "hello-world")
        self.assertEqual(slugify("Hello, World!"), "hello-world")
        self.assertEqual(slugify("  Hello World  "), "hello-world")

    def test_slugify_with_diacritics(self):
        self.assertEqual(slugify("café résumé"), "cafe-resume")

    def test_slugify_empty(self):
        self.assertEqual(slugify(""), "")


class TestTruncate(unittest.TestCase):
    def test_truncate_short(self):
        self.assertEqual(truncate("hello", 10), "hello")

    def test_truncate_long(self):
        self.assertEqual(truncate("hello world", 8), "hello...")

    def test_truncate_custom_suffix(self):
        self.assertEqual(truncate("hello world", 8, suffix=""), "hello...")
        self.assertEqual(truncate("hello world", 8, suffix="---"), "hello---")


class TestPad(unittest.TestCase):
    def test_pad_left(self):
        self.assertEqual(pad_left("hello", 10), "     hello")
        self.assertEqual(pad_left("hello", 10, '0'), "00000hello")
        self.assertEqual(pad_left("hello", 3), "hello")

    def test_pad_right(self):
        self.assertEqual(pad_right("hello", 10), "hello     ")
        self.assertEqual(pad_right("hello", 10, '0'), "hello00000")
        self.assertEqual(pad_right("hello", 3), "hello")


class TestLineNumbers(unittest.TestCase):
    def test_add_line_numbers(self):
        result = add_line_numbers("a\nb\nc", width=3)
        self.assertIn("  1: a", result)
        self.assertIn("  2: b", result)
        self.assertIn("  3: c", result)

    def test_remove_line_numbers(self):
        self.assertEqual(remove_line_numbers("  1: a\n  2: b"), "a\nb")
        self.assertEqual(remove_line_numbers("a\nb"), "a\nb")


class TestExtractLines(unittest.TestCase):
    def test_extract_lines(self):
        self.assertEqual(extract_lines("a\nb\nc\nd", 2, 3), "b\nc")

    def test_extract_lines_single(self):
        self.assertEqual(extract_lines("a\nb\nc", 1, 1), "a")


class TestUnicode(unittest.TestCase):
    def test_normalize_unicode(self):
        # é can be composed (U+00E9) or decomposed (e + ́)
        composed = "café"
        decomposed = "cafe\u0301"
        result = normalize_unicode(decomposed, 'NFC')
        self.assertEqual(result, composed)

    def test_strip_non_ascii(self):
        self.assertEqual(strip_non_ascii("café"), "caf")
        self.assertEqual(strip_non_ascii("hello"), "hello")
        self.assertEqual(strip_non_ascii(""), "")

    def test_remove_diacritics(self):
        self.assertEqual(remove_diacritics("café"), "cafe")
        self.assertEqual(remove_diacritics("naïve"), "naive")
        self.assertEqual(remove_diacritics("hello"), "hello")


if __name__ == '__main__':
    unittest.main()
