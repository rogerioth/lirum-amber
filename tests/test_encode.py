import unittest
import base64
from string_ops.encode import (
    base64_encode,
    base64_decode,
    url_encode,
    url_decode,
    html_encode,
    html_decode,
    hex_encode,
    hex_decode,
    rot13,
    unicode_escape,
    unicode_unescape,
    binary_encode,
    binary_decode,
    octal_encode,
    octal_decode,
)


class TestBase64(unittest.TestCase):
    def test_base64_encode(self):
        self.assertEqual(base64_encode("hello"), base64.b64encode(b"hello").decode())
        self.assertEqual(base64_encode(""), "")
        self.assertEqual(base64_encode("Man"), "TWFu")
        self.assertEqual(base64_encode("Man "), "TWFuIA==")
        self.assertEqual(base64_encode("Ma"), "TWE=")
        self.assertEqual(base64_encode("hello world!"), base64.b64encode(b"hello world!").decode())
        self.assertEqual(base64_encode("🔥"), base64.b64encode("🔥".encode("utf-8")).decode())

    def test_base64_decode(self):
        self.assertEqual(base64_decode("SGVsbG8="), "Hello")
        self.assertEqual(base64_decode(""), "")
        self.assertEqual(base64_decode("TWFu"), "Man")
        self.assertEqual(base64_decode("TWFuIA=="), "Man ")
        self.assertEqual(base64_decode("TWE="), "Ma")

    def test_base64_roundtrip(self):
        test_strings = [
            "hello",
            "Hello, World!",
            "The quick brown fox jumps over the lazy dog",
            "",
            "a" * 100,
            "café résumé naïve",
            "你好世界",
            "🔥🎉🚀💻",
            "\x00\x01\x02\xff\xfe\xfd",
            "line1\nline2\r\nline3\ttab",
        ]
        for s in test_strings:
            self.assertEqual(base64_decode(base64_encode(s)), s)

    def test_base64_invalid_decode(self):
        with self.assertRaises(Exception):
            base64_decode("!!!invalid!!!")


class TestUrlEncode(unittest.TestCase):
    def test_url_encode(self):
        self.assertEqual(url_encode("hello world"), "hello%20world")
        self.assertEqual(url_encode("a+b=c"), "a%2Bb%3Dc")
        self.assertEqual(url_encode(""), "")
        self.assertEqual(url_encode("hello"), "hello")
        self.assertEqual(url_encode("foo@bar.com"), "foo%40bar.com")
        self.assertEqual(url_encode("https://example.com/path?q=1&r=2"),
                         "https%3A%2F%2Fexample.com%2Fpath%3Fq%3D1%26r%3D2")
        self.assertEqual(url_encode("café"), "caf%C3%A9")
        self.assertEqual(url_encode("你好"), "%E4%BD%A0%E5%A5%BD")

    def test_url_decode(self):
        self.assertEqual(url_decode("hello%20world"), "hello world")
        self.assertEqual(url_decode("a%2Bb%3Dc"), "a+b=c")
        self.assertEqual(url_decode(""), "")
        self.assertEqual(url_decode("hello"), "hello")
        self.assertEqual(url_decode("foo%40bar.com"), "foo@bar.com")
        self.assertEqual(url_decode("caf%C3%A9"), "café")
        self.assertEqual(url_decode("%E4%BD%A0%E5%A5%BD"), "你好")

    def test_url_roundtrip(self):
        test_strings = [
            "hello world",
            "a+b=c&d=e",
            "café résumé",
            "你好世界",
            "🔥🎉",
            "foo@bar.com/path?q=1",
        ]
        for s in test_strings:
            self.assertEqual(url_decode(url_encode(s)), s)


class TestHtmlEncode(unittest.TestCase):
    def test_html_encode(self):
        self.assertEqual(html_encode("<div>hello</div>"), "&lt;div&gt;hello&lt;/div&gt;")
        self.assertEqual(html_encode('"quoted"'), "&quot;quoted&quot;")
        self.assertEqual(html_encode("a & b"), "a &amp; b")
        self.assertEqual(html_encode(""), "")
        self.assertEqual(html_encode("hello"), "hello")
        self.assertEqual(html_encode("foo &amp; bar"), "foo &amp;amp; bar")

    def test_html_decode(self):
        self.assertEqual(html_decode("&lt;div&gt;"), "<div>")
        self.assertEqual(html_decode("&quot;"), "\"")
        self.assertEqual(html_decode("&amp;"), "&")
        self.assertEqual(html_decode("&nbsp;"), "\u00a0")
        self.assertEqual(html_decode(""), "")
        self.assertEqual(html_decode("hello"), "hello")
        self.assertEqual(html_decode("&lt;&amp;&gt;"), "<&>")

    def test_html_roundtrip(self):
        test_strings = [
            "<p>Hello & goodbye</p>",
            '"test"',
            "a<b>c&d\"e",
            "",
        ]
        for s in test_strings:
            self.assertEqual(html_decode(html_encode(s)), s)


class TestHexEncode(unittest.TestCase):
    def test_hex_encode(self):
        self.assertEqual(hex_encode("hello"), "68656c6c6f")
        self.assertEqual(hex_encode(""), "")
        self.assertEqual(hex_encode("a"), "61")
        self.assertEqual(hex_encode("café"), "636166c3a9")
        self.assertEqual(hex_encode("café"), "636166c3a9")

    def test_hex_decode(self):
        self.assertEqual(hex_decode("68656c6c6f"), "hello")
        self.assertEqual(hex_decode(""), "")
        self.assertEqual(hex_decode("61"), "a")
        self.assertEqual(hex_decode("c3a9"), "é")
        self.assertEqual(hex_decode("636166c3a9"), "café")

    def test_hex_case_insensitive(self):
        self.assertEqual(hex_decode("68656C6C6F"), "hello")
        self.assertEqual(hex_decode("68656c6c6f"), "hello")

    def test_hex_roundtrip(self):
        test_strings = [
            "hello",
            "café",
            "🔥",
            "test string",
        ]
        for s in test_strings:
            self.assertEqual(hex_decode(hex_encode(s)), s)


class TestRot13(unittest.TestCase):
    def test_rot13(self):
        self.assertEqual(rot13("hello"), "uryyb")
        self.assertEqual(rot13("uryyb"), "hello")
        self.assertEqual(rot13(""), "")
        self.assertEqual(rot13("a"), "n")
        self.assertEqual(rot13("n"), "a")
        self.assertEqual(rot13("The quick brown fox jumps over the lazy dog"),
                         "Gur dhvpx oebja sbk whzcf bire gur ynml qbt")
        self.assertEqual(rot13("ABCxyz"), "NOPklm")
        self.assertEqual(rot13("123"), "123")

    def test_rot13_involution(self):
        test_strings = ["hello", "HELLO", "The quick brown fox", "123!@#"]
        for s in test_strings:
            self.assertEqual(rot13(rot13(s)), s)


class TestUnicodeEscape(unittest.TestCase):
    def test_unicode_escape(self):
        self.assertIn("Hello", unicode_escape("Hello"))
        self.assertIn("\\u", unicode_escape("café"))
        self.assertEqual(unicode_escape(""), "")

    def test_unicode_unescape(self):
        self.assertEqual(unicode_unescape("\\u0048\\u0065\\u006c\\u006c\\u006f"), "Hello")
        self.assertEqual(unicode_unescape(""), "")
        self.assertEqual(unicode_unescape("no escape here"), "no escape here")


class TestBinary(unittest.TestCase):
    def test_binary_encode(self):
        self.assertEqual(binary_encode("hello"), "0110100001100101011011000110110001101111")
        self.assertEqual(binary_encode(""), "")
        self.assertEqual(binary_encode("a"), "01100001")

    def test_binary_decode(self):
        self.assertEqual(binary_decode("0110100001100101011011000110110001101111"), "hello")
        self.assertEqual(binary_decode(""), "")
        self.assertEqual(binary_decode("01100001"), "a")

    def test_binary_roundtrip(self):
        for s in ["hello", "a", "test"]:
            self.assertEqual(binary_decode(binary_encode(s)), s)


class TestOctal(unittest.TestCase):
    def test_octal_encode(self):
        self.assertEqual(octal_encode("hello"), "150145154154157")
        self.assertEqual(octal_encode(""), "")

    def test_octal_decode(self):
        self.assertEqual(octal_decode("150145154154157"), "hello")
        self.assertEqual(octal_decode(""), "")

    def test_octal_roundtrip(self):
        for s in ["hello", "a", "test"]:
            self.assertEqual(octal_decode(octal_encode(s)), s)


if __name__ == '__main__':
    unittest.main()
