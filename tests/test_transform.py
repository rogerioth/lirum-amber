import unittest
from string_ops.transform import (
    to_uppercase,
    to_lowercase,
    to_title_case,
    to_sentence_case,
    swap_case,
    to_camel_case,
    to_pascal_case,
    to_snake_case,
    to_kebab_case,
    to_constant_case,
    reverse_string,
    reverse_words,
    reverse_lines,
    rotate_chars,
    repeat_string,
    to_dot_case,
    to_path_case,
    to_alternating_case,
    to_sponge_case,
    capitalize_first_letter,
    decapitalize_first_letter,
)


class TestTransformCase(unittest.TestCase):
    """Tests for case transformation operations."""

    def test_to_uppercase(self):
        self.assertEqual(to_uppercase("hello"), "HELLO")
        self.assertEqual(to_uppercase("Hello World"), "HELLO WORLD")
        self.assertEqual(to_uppercase("HELLO"), "HELLO")
        self.assertEqual(to_uppercase(""), "")
        self.assertEqual(to_uppercase("123"), "123")
        self.assertEqual(to_uppercase("hElLo wOrLd"), "HELLO WORLD")
        self.assertEqual(to_uppercase("café"), "CAFÉ")
        self.assertEqual(to_uppercase("你好"), "你好")
        self.assertEqual(to_uppercase("ß"), "SS")
        self.assertEqual(to_uppercase("Straße"), "STRASSE")

    def test_to_lowercase(self):
        self.assertEqual(to_lowercase("HELLO"), "hello")
        self.assertEqual(to_lowercase("Hello World"), "hello world")
        self.assertEqual(to_lowercase("hello"), "hello")
        self.assertEqual(to_lowercase(""), "")
        self.assertEqual(to_lowercase("123"), "123")
        self.assertEqual(to_lowercase("HELLO WORLD"), "hello world")
        self.assertEqual(to_lowercase("CAFÉ"), "café")
        self.assertEqual(to_lowercase("你好"), "你好")
        self.assertEqual(to_lowercase("Ω"), "ω")

    def test_to_title_case(self):
        self.assertEqual(to_title_case("hello world"), "Hello World")
        self.assertEqual(to_title_case("HELLO WORLD"), "Hello World")
        self.assertEqual(to_title_case("hElLo wOrLd"), "Hello World")
        self.assertEqual(to_title_case(""), "")
        self.assertEqual(to_title_case("a"), "A")
        self.assertEqual(to_title_case("foo-bar_baz"), "Foo-Bar_Baz")

    def test_to_sentence_case(self):
        self.assertEqual(to_sentence_case("hello world"), "Hello world")
        self.assertEqual(to_sentence_case("HELLO WORLD"), "Hello world")
        self.assertEqual(to_sentence_case("hello. world. foo."), "Hello. World. Foo.")
        self.assertEqual(to_sentence_case(""), "")
        self.assertEqual(to_sentence_case("a"), "A")
        self.assertEqual(to_sentence_case("first second. third fourth."), "First second. Third fourth.")
        self.assertEqual(to_sentence_case("hello... world"), "Hello... world")

    def test_swap_case(self):
        self.assertEqual(swap_case("Hello"), "hELLO")
        self.assertEqual(swap_case("HELLO"), "hello")
        self.assertEqual(swap_case("hello"), "HELLO")
        self.assertEqual(swap_case(""), "")
        self.assertEqual(swap_case("123"), "123")
        self.assertEqual(swap_case("Hello World 123"), "hELLO wORLD 123")
        self.assertEqual(swap_case("café"), "CAFÉ")

    def test_to_camel_case(self):
        self.assertEqual(to_camel_case("hello world"), "helloWorld")
        self.assertEqual(to_camel_case("Hello World"), "helloWorld")
        self.assertEqual(to_camel_case("hello-world"), "helloWorld")
        self.assertEqual(to_camel_case("hello_world"), "helloWorld")
        self.assertEqual(to_camel_case("hello.world"), "helloWorld")
        self.assertEqual(to_camel_case(""), "")
        self.assertEqual(to_camel_case("a"), "a")
        self.assertEqual(to_camel_case("A"), "a")

    def test_to_pascal_case(self):
        self.assertEqual(to_pascal_case("hello world"), "HelloWorld")
        self.assertEqual(to_pascal_case("Hello World"), "HelloWorld")
        self.assertEqual(to_pascal_case("hello-world"), "HelloWorld")
        self.assertEqual(to_pascal_case("hello_world"), "HelloWorld")
        self.assertEqual(to_pascal_case(""), "")
        self.assertEqual(to_pascal_case("a"), "A")

    def test_to_snake_case(self):
        self.assertEqual(to_snake_case("helloWorld"), "hello_world")
        self.assertEqual(to_snake_case("HelloWorld"), "hello_world")
        self.assertEqual(to_snake_case("hello-world"), "hello_world")
        self.assertEqual(to_snake_case("hello world"), "hello_world")
        self.assertEqual(to_snake_case("hello"), "hello")
        self.assertEqual(to_snake_case(""), "")
        self.assertEqual(to_snake_case("XMLParser"), "xml_parser")
        self.assertEqual(to_snake_case("IOError"), "io_error")
        self.assertEqual(to_snake_case("getHTTPResponse"), "get_http_response")
        self.assertEqual(to_snake_case("already_snake"), "already_snake")
        self.assertEqual(to_snake_case("__init__"), "__init__")

    def test_to_kebab_case(self):
        self.assertEqual(to_kebab_case("helloWorld"), "hello-world")
        self.assertEqual(to_kebab_case("HelloWorld"), "hello-world")
        self.assertEqual(to_kebab_case("hello_world"), "hello-world")
        self.assertEqual(to_kebab_case("hello world"), "hello-world")
        self.assertEqual(to_kebab_case("hello"), "hello")
        self.assertEqual(to_kebab_case(""), "")
        self.assertEqual(to_kebab_case("already-kebab"), "already-kebab")
        self.assertEqual(to_kebab_case("XMLParser"), "xml-parser")

    def test_to_constant_case(self):
        self.assertEqual(to_constant_case("helloWorld"), "HELLO_WORLD")
        self.assertEqual(to_constant_case("HelloWorld"), "HELLO_WORLD")
        self.assertEqual(to_constant_case("hello_world"), "HELLO_WORLD")
        self.assertEqual(to_constant_case("hello world"), "HELLO_WORLD")
        self.assertEqual(to_constant_case("hello"), "HELLO")
        self.assertEqual(to_constant_case(""), "")
        self.assertEqual(to_constant_case("XMLParser"), "XML_PARSER")

    def test_to_dot_case(self):
        self.assertEqual(to_dot_case("hello world"), "hello.world")
        self.assertEqual(to_dot_case("HelloWorld"), "hello.world")
        self.assertEqual(to_dot_case(""), "")
        self.assertEqual(to_dot_case("hello   world"), "hello.world")
        self.assertEqual(to_dot_case("hello-world"), "hello.world")

    def test_to_path_case(self):
        self.assertEqual(to_path_case("hello world"), "hello/world")
        self.assertEqual(to_path_case("HelloWorld"), "hello/world")
        self.assertEqual(to_path_case(""), "")
        self.assertEqual(to_path_case("hello   world"), "hello/world")
        self.assertEqual(to_path_case("hello-world"), "hello/world")

    def test_to_alternating_case(self):
        self.assertEqual(to_alternating_case("hello"), "hElLo")
        self.assertEqual(to_alternating_case("Hello"), "hElLo")
        self.assertEqual(to_alternating_case(""), "")
        self.assertEqual(to_alternating_case("test"), "tEsT")
        self.assertEqual(to_alternating_case("HELLO"), "hElLo")

    def test_to_sponge_case(self):
        import random
        random.seed(42)
        self.assertEqual(to_sponge_case("hello"), "HellO")
        self.assertEqual(to_sponge_case(""), "")
        random.seed(123)
        self.assertEqual(to_sponge_case("test"), "test")

    def test_capitalize_first_letter(self):
        self.assertEqual(capitalize_first_letter("hello world"), "Hello world")
        self.assertEqual(capitalize_first_letter("Hello world"), "Hello world")
        self.assertEqual(capitalize_first_letter(""), "")
        self.assertEqual(capitalize_first_letter("hELLO"), "HELLO")
        self.assertEqual(capitalize_first_letter("a"), "A")

    def test_decapitalize_first_letter(self):
        self.assertEqual(decapitalize_first_letter("Hello world"), "hello world")
        self.assertEqual(decapitalize_first_letter("hello world"), "hello world")
        self.assertEqual(decapitalize_first_letter(""), "")
        self.assertEqual(decapitalize_first_letter("HELLO"), "hELLO")
        self.assertEqual(decapitalize_first_letter("A"), "a")


class TestTransformReverse(unittest.TestCase):
    """Tests for reverse operations."""

    def test_reverse_string(self):
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string(""), "")
        self.assertEqual(reverse_string("a"), "a")
        self.assertEqual(reverse_string("ab"), "ba")
        self.assertEqual(reverse_string("hello world"), "dlrow olleh")
        self.assertEqual(reverse_string("12321"), "12321")
        self.assertEqual(reverse_string("a b c"), "c b a")
        self.assertEqual(reverse_string("café"), "éfac")
        self.assertEqual(reverse_string("你好世界"), "界世好你")
        self.assertEqual(reverse_string("🔥🎉"), "🎉🔥")

    def test_reverse_words(self):
        self.assertEqual(reverse_words("hello world"), "world hello")
        self.assertEqual(reverse_words(""), "")
        self.assertEqual(reverse_words("a"), "a")
        self.assertEqual(reverse_words("hello"), "hello")
        self.assertEqual(reverse_words("hello world foo"), "foo world hello")

    def test_reverse_lines(self):
        self.assertEqual(reverse_lines("a\nb\nc"), "c\nb\na")
        self.assertEqual(reverse_lines(""), "")
        self.assertEqual(reverse_lines("a"), "a")
        self.assertEqual(reverse_lines("a\nb\nc\n"), "c\nb\na\n")
        self.assertEqual(reverse_lines("line1\n\nline3"), "line3\n\nline1")


class TestTransformMisc(unittest.TestCase):
    """Tests for rotate and repeat operations."""

    def test_rotate_chars_forward(self):
        self.assertEqual(rotate_chars("abc", 1), "bca")
        self.assertEqual(rotate_chars("abc", 3), "abc")
        self.assertEqual(rotate_chars("", 5), "")
        self.assertEqual(rotate_chars("abc", 0), "abc")
        self.assertEqual(rotate_chars("abc", -1), "cab")

    def test_rotate_chars_wrap(self):
        self.assertEqual(rotate_chars("abc", 26), "cab")
        self.assertEqual(rotate_chars("abc", 100), "bca")
        self.assertEqual(rotate_chars("a", 1000000), "a")

    def test_repeat_string(self):
        self.assertEqual(repeat_string("abc", 3), "abcabcabc")
        self.assertEqual(repeat_string("abc", 0), "")
        self.assertEqual(repeat_string("abc", 1), "abc")
        self.assertEqual(repeat_string("", 5), "")
        self.assertEqual(repeat_string("a", 4), "aaaa")
        self.assertEqual(repeat_string("ab\n", 2), "ab\nab\n")


if __name__ == '__main__':
    unittest.main()
