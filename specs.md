# String Operations TUI - Specification & Unit Tests

## Overview

A TUI (Text User Interface) Python application for performing string operations. Users paste or load text, select an operation from categorized menus, and view the result.

## Architecture

### TUI Layout
```
┌─────────────────────────────────────────────────────────┐
│  [File] [Edit] [Help]    Search: [____________]        │
├─────────────────────────────────────────────────────────┤
│ Categories: > Transform  Encode  JSON  Format  Regex   │
│             Extract  Hash  Misc                          │
├─────────────────────────────────────────────────────────┤
│ Input                          Output                    │
│ ┌──────────────────────────┐ ┌────────────────────────┐ │
│ │                          │ │                        │ │
│ │                          │ │                        │ │
│ │                          │ │                        │ │
│ └──────────────────────────┘ └────────────────────────┘ │
├─────────────────────────────────────────────────────────┤
│ Status: 0 chars | 0 lines | 0 words | Ctrl+O: Open    │
└─────────────────────────────────────────────────────────┘
```

### Navigation
- Categories expand/collapse on selection
- Operations listed under active category
- Double-click or Enter to execute operation
- Modal dialogs for parameters (find/replace, count, etc.)
- Breadcrumb or back button for nested navigation
- Search filters operations across all categories in real-time

### File Operations
- `Ctrl+O` / `File > Open` — open file dialog, load content into input
- `Ctrl+S` / `File > Save Output` — save output to file
- File path displayed in status bar
- Drag-and-drop file support (via terminal emulator)

### Status Bar
- Character count, word count, line count
- Current category / operation hint
- Keyboard shortcut hints

---

## Categories & Operations

### 1. Transform
| # | Operation | Description |
|---|-----------|-------------|
| 1 | To Uppercase | Convert all characters to uppercase |
| 2 | To Lowercase | Convert all characters to lowercase |
| 3 | To Title Case | Capitalize first letter of each word |
| 4 | To Sentence Case | Capitalize first letter of each sentence |
| 5 | Swap Case | Swap uppercase ↔ lowercase |
| 6 | CamelCase | Convert to camelCase |
| 7 | PascalCase | Convert to PascalCase |
| 8 | snake_case | Convert to snake_case |
| 9 | kebab-case | Convert to kebab-case |
| 10 | CONSTANT_CASE | Convert to CONSTANT_CASE |
| 11 | Reverse | Reverse the entire string |
| 12 | Reverse Words | Reverse word order |
| 13 | Reverse Lines | Reverse line order |
| 14 | Rotate N Characters | Caesar-style character rotation |
| 15 | Repeat N Times | Repeat string N times |

### 2. Encode / Decode
| # | Operation | Description |
|---|-----------|-------------|
| 1 | Base64 Encode | Encode to Base64 |
| 2 | Base64 Decode | Decode from Base64 |
| 3 | URL Encode | Percent-encode for URLs |
| 4 | URL Decode | Percent-decode from URLs |
| 5 | HTML Entity Encode | Convert to HTML entities |
| 6 | HTML Entity Decode | Convert from HTML entities |
| 7 | Hex Encode | Convert to hex string |
| 8 | Hex Decode | Convert from hex string |
| 9 | ROT13 | Apply ROT13 cipher |
| 10 | Unicode Escape | Convert to `\uXXXX` sequences |
| 11 | Unicode Unescape | Convert `\uXXXX` to characters |
| 12 | Binary Encode | Convert to binary representation |
| 13 | Binary Decode | Convert from binary representation |
| 14 | Octal Encode | Convert to octal |
| 15 | Octal Decode | Convert from octal |

### 3. JSON
| # | Operation | Description |
|---|-----------|-------------|
| 1 | JSON Escape | Escape for JSON string literal |
| 2 | JSON Unescape | Unescape JSON string literal |
| 3 | JSON Pretty Print | Format JSON with indentation |
| 4 | JSON Minify | Compact JSON (no whitespace) |
| 5 | JSON to String | Parse JSON → string representation |
| 6 | String to JSON | Wrap text as JSON string value |
| 7 | JSON Diff | Compare two JSON inputs |
| 8 | JSON Path Extract | Extract value by JSONPath expression |

### 4. Format
| # | Operation | Description |
|---|-----------|-------------|
| 1 | Trim (both) | Strip leading/trailing whitespace |
| 2 | Trim Left | Strip leading whitespace |
| 3 | Trim Right | Strip trailing whitespace |
| 4 | Trim Newlines | Strip leading/trailing newlines |
| 5 | Collapse Whitespace | Replace runs of whitespace with single space |
| 6 | Remove Empty Lines | Remove blank lines |
| 7 | Remove Duplicate Lines | Remove duplicate lines (preserve order) |
| 8 | Sort Lines | Sort lines alphabetically |
| 9 | Reverse Lines | Reverse line order |
| 10 | Deduplicate Lines | Remove consecutive duplicates |
| 11 | Indent / Unindent | Adjust indentation by N spaces or tab |
| 12 | Wrap Text | Wrap to N columns |
| 13 | Justify Text | Justify paragraph to N columns |
| 14 | Replace Line Endings | CRLF ↔ LF ↔ CR |
| 15 | Normalize Unicode | NFC / NFD / NFKC / NFKD |
| 16 | Strip Non-ASCII | Remove non-ASCII characters |
| 17 | Remove Diacritics | Strip accents/diacritical marks |
| 18 | Slugify | Convert to URL-friendly slug |
| 19 | Truncate | Truncate to N characters with suffix |
| 20 | Pad Left | Pad string to N chars on the left |
| 21 | Pad Right | Pad string to N chars on the right |
| 22 | Add Line Numbers | Prefix each line with a number |
| 23 | Remove Line Numbers | Strip leading line numbers |
| 24 | Extract Lines | Extract lines in range (N-M) |
| 25 | Repeat Lines N Times | Repeat each line N times |
| 26 | Interleave | Interleave two text inputs |

### 5. Find & Replace
| # | Operation | Description |
|---|-----------|-------------|
| 1 | Find and Replace | Find/replace with preview |
| 2 | Find and Replace All | Replace all occurrences |
| 3 | Regex Find | Find all regex matches |
| 4 | Regex Replace | Replace regex matches |
| 5 | Count Matches | Count regex matches |
| 6 | Extract Regex Groups | Extract captured groups |

### 6. Extract
| # | Operation | Description |
|---|-----------|-------------|
| 1 | Extract Emails | Find all email addresses |
| 2 | Extract URLs | Find all URLs |
| 3 | Extract Phone Numbers | Find phone numbers |
| 4 | Extract IP Addresses | Find IPv4/IPv6 addresses |
| 5 | Extract Dates | Find date patterns |
| 6 | Extract JSON Objects | Find JSON objects/arrays |
| 7 | Extract Between Markers | Extract text between two markers |
| 8 | Extract by Regex | Extract all regex matches |
| 9 | Extract First N Chars | Get first N characters |
| 10 | Extract Last N Chars | Get last N characters |
| 11 | Extract by Byte Range | Extract bytes N-M |
| 12 | Extract by Line Range | Extract lines N-M |

### 7. Hash / Digest
| # | Operation | Description |
|---|-----------|-------------|
| 1 | MD5 | Compute MD5 hash |
| 2 | SHA-1 | Compute SHA-1 hash |
| 3 | SHA-256 | Compute SHA-256 hash |
| 4 | SHA-512 | Compute SHA-512 hash |
| 5 | CRC32 | Compute CRC32 checksum |
| 6 | HMAC | Compute HMAC (with key parameter) |
| 7 | FNV-1a | Compute FNV-1a hash |
| 8 | MurmurHash3 | Compute MurmurHash3 |

### 8. Statistics
| # | Operation | Description |
|---|-----------|-------------|
| 1 | Count Characters | Total character count |
| 2 | Count Characters (no space) | Exclude whitespace |
| 3 | Count Words | Word count |
| 4 | Count Lines | Line count |
| 5 | Count Bytes | Byte count |
| 6 | Character Frequency | Frequency of each character |
| 7 | Word Frequency | Frequency of each word |
| 8 | Readability Score | Flesch-Kincaid, etc. |
| 9 | Entropy | Shannon entropy |
| 10 | Palindrome Check | Check if palindrome |
| 11 | Anagram Check | Check if anagram of another string |
| 12 | Levenshtein Distance | Edit distance between two strings |
| 13 | Longest Word | Find the longest word |
| 14 | Shortest Word | Find the shortest word |
| 15 | Unique Words | Count unique words |

### 9. Misc
| # | Operation | Description |
|---|-----------|-------------|
| 1 | Compare Two Texts | Diff two inputs side by side |
| 2 | Merge Two Texts | Merge two text inputs |
| 3 | Difference (A−B) | Lines in A not in B |
| 4 | Intersection (A∩B) | Common lines in A and B |
| 5 | Symmetric Difference | Lines in A or B but not both |
| 6 | Generate UUID | Generate random UUID |
| 7 | Generate Password | Generate random password |
| 8 | Generate Lorem Ipsum | Generate lorem ipsum text |
| 9 | Generate Sequence | Number/alphabet sequence |
| 10 | Text to Morse Code | Convert to Morse |
| 11 | Morse to Text | Convert from Morse |
| 12 | Text to Braille | Convert to Braille |
| 13 | Braille to Text | Convert from Braille |
| 14 | Pig Latin | Convert to Pig Latin |
| 15 | Atbash Cipher | Atbash substitution cipher |
| 16 | Vigenere Cipher | Vigenere cipher with key |
| 17 | Affine Cipher | Affine cipher with a/b keys |
| 18 | Beaufort Cipher | Beaufort cipher with key |
| 19 | Playfair Cipher | Playfair cipher with key |
| 20 | Columnar Transposition | Columnar transposition with key |

---

## Unit Tests

### Test: Transform Operations

```python
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
        self.assertEqual(to_uppercase("ß"), "SS")  # German eszett
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
        self.assertEqual(to_lowercase("İ"), "i")  # Turkish I
        self.assertEqual(to_lowercase("Ω"), "ω")  # Greek omega

    def test_to_title_case(self):
        self.assertEqual(to_title_case("hello world"), "Hello World")
        self.assertEqual(to_title_case("HELLO WORLD"), "Hello World")
        self.assertEqual(to_title_case("hElLo wOrLd"), "Hello World")
        self.assertEqual(to_title_case(""), "")
        self.assertEqual(to_title_case("a"), "A")
        self.assertEqual(to_title_case("it's a test"), "It'S A Test")  # naive: capitalizes after space
        self.assertEqual(to_title_case("foo-bar_baz"), "Foo-Bar_Baz")
        self.assertEqual(to_title_case("   spaced   ", keep_spaces=True), "   Spaced   ")

    def test_to_sentence_case(self):
        self.assertEqual(to_sentence_case("hello world"), "Hello world")
        self.assertEqual(to_sentence_case("HELLO WORLD"), "Hello world")
        self.assertEqual(to_sentence_case("hello. world. foo."), "Hello. World. Foo.")
        self.assertEqual(to_sentence_case(""), "")
        self.assertEqual(to_sentence_case("a"), "A")
        self.assertEqual(to_sentence_case("first second. third fourth."), "First second. Third fourth.")
        self.assertEqual(to_sentence_case("hello... world"), "Hello... world")
        self.assertEqual(to_sentence_case("h2o is water."), "H2o is water.")

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
        self.assertEqual(to_camel_case("   hello   world   "), "helloWorld")
        self.assertEqual(to_camel_case(""), "")
        self.assertEqual(to_camel_case("a"), "a")
        self.assertEqual(to_camel_case("A"), "a")
        self.assertEqual(to_camel_case("hello  world"), "helloWorld")  # multiple spaces

    def test_to_pascal_case(self):
        self.assertEqual(to_pascal_case("hello world"), "HelloWorld")
        self.assertEqual(to_pascal_case("Hello World"), "HelloWorld")
        self.assertEqual(to_pascal_case("hello-world"), "HelloWorld")
        self.assertEqual(to_pascal_case("hello_world"), "HelloWorld")
        self.assertEqual(to_pascal_case(""), "")
        self.assertEqual(to_pascal_case("a"), "A")
        self.assertEqual(to_pascal_case("hello  world"), "HelloWorld")

    def test_to_snake_case(self):
        self.assertEqual(to_snake_case("helloWorld"), "hello_world")
        self.assertEqual(to_snake_case("HelloWorld"), "hello_world")
        self.assertEqual(to_snake_case("hello-world"), "hello_world")
        self.assertEqual(to_snake_case("hello world"), "hello_world")
        self.assertEqual(to_snake_case("hello"), "hello")
        self.assertEqual(to_snake_case(""), "")
        self.assertEqual(to_snake_case("XMLParser"), "xml_parser")
        self.assertEqual(to_snake_case("IOError"), "i_o_error")
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
        self.assertEqual(reverse_words("  hello   world  "), "world   hello")  # preserve internal spacing
        self.assertEqual(reverse_words("a b c d"), "d c b a")
        self.assertEqual(reverse_words("hello world foo"), "foo world hello")

    def test_reverse_lines(self):
        self.assertEqual(reverse_lines("a\nb\nc"), "c\nb\na")
        self.assertEqual(reverse_lines(""), "")
        self.assertEqual(reverse_lines("a"), "a")
        self.assertEqual(reverse_lines("a\nb\nc\n"), "c\nb\na\n")
        self.assertEqual(reverse_lines("\n\n"), "\n\n")
        self.assertEqual(reverse_lines("line1\n\nline3"), "line3\n\nline1")


class TestTransformMisc(unittest.TestCase):
    """Tests for rotate and repeat operations."""

    def test_rotate_chars_forward(self):
        self.assertEqual(rotate_chars("abc", 1), "bca")
        self.assertEqual(rotate_chars("abc", 3), "abc")
        self.assertEqual(rotate_chars("hello world", 13), "uryyb jbeyq")  # same as ROT13 for shift=13
        self.assertEqual(rotate_chars("", 5), "")
        self.assertEqual(rotate_chars("abc", 0), "abc")
        self.assertEqual(rotate_chars("abc", -1), "cab")  # negative = shift left

    def test_rotate_chars_wrap(self):
        self.assertEqual(rotate_chars("abc", 26), "bca")
        self.assertEqual(rotate_chars("abc", 100), "cab")
        self.assertEqual(rotate_chars("a", 1000000), "a")

    def test_repeat_string(self):
        self.assertEqual(repeat_string("abc", 3), "abcabcabc")
        self.assertEqual(repeat_string("abc", 0), "")
        self.assertEqual(repeat_string("abc", 1), "abc")
        self.assertEqual(repeat_string("", 5), "")
        self.assertEqual(repeat_string("a", 4), "aaaa")
        self.assertEqual(repeat_string("ab\n", 2), "ab\nab\n")
```

### Test: Encode / Decode Operations

```python
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
        self.assertEqual(html_encode("foo &amp; bar"), "foo &amp;amp; bar")  # double encode existing

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
        self.assertEqual(hex_encode("\x00\x01\xff"), "0001ff")
        self.assertEqual(hex_encode("café"), "636166c3a9")

    def test_hex_decode(self):
        self.assertEqual(hex_decode("68656c6c6f"), "hello")
        self.assertEqual(hex_decode(""), "")
        self.assertEqual(hex_decode("61"), "a")
        self.assertEqual(hex_decode("0001ff"), "\x00\x01\xff")
        self.assertEqual(hex_decode("636166c3a9"), "café")

    def test_hex_case_insensitive(self):
        self.assertEqual(hex_decode("68656C6C6F"), "hello")
        self.assertEqual(hex_decode("68656c6c6f"), "hello")
        self.assertEqual(hex_decode("68656C6c6F"), "hello")

    def test_hex_roundtrip(self):
        test_bytes = [
            b"hello",
            b"\x00\x01\xff",
            "café".encode("utf-8"),
            "🔥".encode("utf-8"),
        ]
        for b in test_bytes:
            self.assertEqual(hex_decode(hex_encode(b.decode("utf-8"))).encode("utf-8") if isinstance(b, bytes) else hex_decode(hex_encode(b)), b if isinstance(b, bytes) else b.encode("utf-8"))


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
        """ROT13 is its own inverse: rot13(rot13(s)) == s"""
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
```

### Test: JSON Operations

```python
import unittest
import json
from string_ops.json_ops import (
    json_escape,
    json_unescape,
    json_pretty_print,
    json_minify,
    json_to_string,
    string_to_json,
    json_diff,
    json_path_extract,
)


class TestJsonEscape(unittest.TestCase):
    def test_json_escape(self):
        self.assertEqual(json_escape("hello"), '"hello"')
        self.assertEqual(json_escape("hello\nworld"), '"hello\\nworld"')
        self.assertEqual(json_escape("hello\tworld"), '"hello\\tworld"')
        self.assertEqual(json_escape('hello"world'), '"hello\\"world"')
        self.assertEqual(json_escape("hello\\world"), '"hello\\\\world"')
        self.assertEqual(json_escape(""), '""')
        self.assertEqual(json_escape("\u0000"), '"\\u0000"')
        self.assertEqual(json_escape("\b\f\r"), '"\\b\\f\\r"')

    def test_json_unescape(self):
        self.assertEqual(json_unescape('"hello"'), "hello")
        self.assertEqual(json_unescape('"hello\\nworld"'), "hello\nworld")
        self.assertEqual(json_unescape('"hello\\tworld"'), "hello\tworld")
        self.assertEqual(json_unescape('"hello\\\\world"'), "hello\\world")
        self.assertEqual(json_unescape('""'), "")
        self.assertEqual(json_unescape('"hello\\u0041world"'), "helloAworld")
        self.assertEqual(json_unescape('"hello\\bworld"'), "hello\x08world")


class TestJsonPretty(unittest.TestCase):
    def test_json_pretty_print(self):
        obj = {"name": "Alice", "age": 30, "hobbies": ["reading", "coding"]}
        result = json_pretty_print(json.dumps(obj))
        self.assertIn("\n", result)
        self.assertIn("  ", result)  # indentation
        parsed = json.loads(result)
        self.assertEqual(parsed, obj)

    def test_json_pretty_print_invalid(self):
        with self.assertRaises(json.JSONDecodeError):
            json_pretty_print("{invalid json}")

    def test_json_minify(self):
        obj = {"name": "Alice", "age": 30}
        pretty = json.dumps(obj, indent=2)
        minified = json_minify(pretty)
        self.assertNotIn("\n", minified)
        self.assertEqual(json.loads(minified), obj)

    def test_json_minify_already_minified(self):
        original = '{"name":"Alice"}'
        self.assertEqual(json_minify(original), original)


class TestJsonToFrom(unittest.TestCase):
    def test_json_to_string(self):
        self.assertEqual(json_to_string('{"key": "value"}'), "{'key': 'value'}")

    def test_string_to_json(self):
        result = string_to_json("hello")
        self.assertEqual(json.loads(result), "hello")
        self.assertIsInstance(result, str)
        self.assertTrue(result.startswith('"') and result.endswith('"'))
```

### Test: Format Operations

```python
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
        self.assertEqual(trim_newlines("  hello  "), "  hello  ")  # only newlines


class TestWhitespace(unittest.TestCase):
    def test_collapse_whitespace(self):
        self.assertEqual(collapse_whitespace("hello   world"), "hello world")
        self.assertEqual(collapse_whitespace("\thello\tworld\t"), "hello world")
        self.assertEqual(collapse_whitespace("  hello  world  "), " hello world ")
        self.assertEqual(collapse_whitespace(""), "")
        self.assertEqual(collapse_whitespace("a\t\t\tb"), "a b")
        self.assertEqual(collapse_whitespace("hello\n\nworld"), "hello\nworld")

    def test_remove_empty_lines(self):
        self.assertEqual(remove_empty_lines("a\n\nb\n\nc"), "a\nb\nc")
        self.assertEqual(remove_empty_lines("\n\n\n"), "")
        self.assertEqual(remove_empty_lines("a\nb\nc"), "a\nb\nc")
        self.assertEqual(remove_empty_lines(""), "")
        self.assertEqual(remove_empty_lines("a\n  \nb"), "a\nb")  # whitespace-only lines


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
        self.assertEqual(sort_lines("10\n2\n1"), "1\n10\n2")  # lexicographic

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
        self.assertEqual(indent_text("a\n\nb", 2), "  a\n\n  b")

    def test_unindent_text(self):
        self.assertEqual(unindent_text("    hello\n    world", 4), "hello\nworld")
        self.assertEqual(unindent_text("  hello", 2), "hello")
        self.assertEqual(unindent_text("hello", 4), "hello")  # can't unindent more than exists


class TestWrap(unittest.TestCase):
    def test_wrap_text(self):
        result = wrap_text("hello world foo bar", 10)
        lines = result.split("\n")
        self.assertTrue(all(len(line) <= 10 for line in lines))
        self.assertEqual(result, "hello\nworld foo\nbar")

    def test_wrap_text_short(self):
        self.assertEqual(wrap_text("hello", 10), "hello")
        self.assertEqual(wrap_text("", 10), "")

    def test_wrap_text_preserve_breaks(self):
        result = wrap_text("hello\nworld\nfoo bar baz", 10, preserve_breaks=True)
        self.assertIn("hello\nworld\n", result)
```

### Test: Find & Replace Operations

```python
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
        self.assertEqual(find_and_replace("hello world", "xyz", "abc"), "hello world")  # not found
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
```

### Test: Extract Operations

```python
import unittest
from string_ops.extract import (
    extract_emails,
    extract_urls,
    extract_phone_numbers,
    extract_ip_addresses,
    extract_dates,
    extract_between_markers,
    extract_regex,
    extract_first_n,
    extract_last_n,
    extract_by_line_range,
)


class TestExtractEmails(unittest.TestCase):
    def test_extract_emails(self):
        text = "Contact us at info@example.com or support@test.org"
        emails = extract_emails(text)
        self.assertIn("info@example.com", emails)
        self.assertIn("support@test.org", emails)

    def test_extract_emails_none(self):
        self.assertEqual(extract_emails("no emails here"), [])

    def test_extract_emails_edge_cases(self):
        self.assertIn("user.name+tag@domain.co.uk", extract_emails("user.name+tag@domain.co.uk"))
        self.assertIn("a@b.c", extract_emails("a@b.c"))
```

### Test: Hash Operations

```python
import unittest
import hashlib
from string_ops.hash_ops import (
    hash_md5,
    hash_sha1,
    hash_sha256,
    hash_sha512,
    hash_crc32,
    hash_hmac,
)


class TestHash(unittest.TestCase):
    def test_hash_md5(self):
        self.assertEqual(hash_md5(""), "d41d8cd98f00b204e9800998ecf8427e")
        self.assertEqual(hash_md5("hello"), "5d41402abc4b2a76b9719d911017c592")
        self.assertEqual(hash_md5("hello world"), "5eb63bbbe01eeed093cb22bb8f5acdc3")

    def test_hash_sha256(self):
        self.assertEqual(hash_sha256(""), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
        self.assertEqual(hash_sha256("hello"), "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")

    def test_hash_sha512(self):
        result = hash_sha512("hello")
        self.assertEqual(len(result), 128)  # 512 bits = 128 hex chars

    def test_hash_crc32(self):
        result = hash_crc32("hello")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 8)  # 32 bits = 8 hex chars

    def test_hash_hmac(self):
        result = hash_hmac("hello", "secret")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, hash_md5("hello"))  # should differ from plain MD5

    def test_hash_deterministic(self):
        for hash_fn in [hash_md5, hash_sha1, hash_sha256, hash_sha512]:
            self.assertEqual(hash_fn("test"), hash_fn("test"))
```

### Test: Statistics Operations

```python
import unittest
from string_ops.statistics import (
    count_characters,
    count_characters_no_space,
    count_words,
    count_lines,
    count_bytes,
    character_frequency,
    word_frequency,
    shannon_entropy,
    is_palindrome,
    levenshtein_distance,
    longest_word,
    shortest_word,
    count_unique_words,
    readability_score,
)


class TestCounters(unittest.TestCase):
    def test_count_characters(self):
        self.assertEqual(count_characters("hello"), 5)
        self.assertEqual(count_characters(""), 0)
        self.assertEqual(count_characters("hello world"), 11)
        self.assertEqual(count_characters("🔥🎉"), 2)

    def test_count_characters_no_space(self):
        self.assertEqual(count_characters_no_space("hello world"), 10)
        self.assertEqual(count_characters_no_space("a b c"), 3)
        self.assertEqual(count_characters_no_space(""), 0)

    def test_count_words(self):
        self.assertEqual(count_words("hello world"), 2)
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words("  hello   world  "), 2)
        self.assertEqual(count_words("one"), 1)

    def test_count_lines(self):
        self.assertEqual(count_lines("a\nb\nc"), 3)
        self.assertEqual(count_lines(""), 0)
        self.assertEqual(count_lines("a"), 1)
        self.assertEqual(count_lines("a\nb\n"), 3)  # trailing newline counts

    def test_count_bytes(self):
        self.assertEqual(count_bytes("hello"), 5)
        self.assertEqual(count_bytes("café"), 5)  # UTF-8: é = 2 bytes
        self.assertEqual(count_bytes("🔥"), 4)  # UTF-8: emoji = 4 bytes

    def test_character_frequency(self):
        freq = character_frequency("aabbc")
        self.assertEqual(freq, {"a": 2, "b": 2, "c": 1})
        self.assertEqual(character_frequency(""), {})

    def test_word_frequency(self):
        freq = word_frequency("hello Hello world hello")
        # case-sensitive
        self.assertEqual(freq["hello"], 2)
        self.assertEqual(freq["Hello"], 1)
        self.assertEqual(freq["world"], 1)

    def test_word_frequency_case_insensitive(self):
        freq = word_frequency("Hello hello HELLO", case_insensitive=True)
        self.assertEqual(freq["hello"], 3)
```

### Test: Statistics Advanced

```python
class TestStatisticsAdvanced(unittest.TestCase):
    def test_shannon_entropy(self):
        # "aaaa" has zero entropy (no randomness)
        self.assertAlmostEqual(shannon_entropy("aaaa"), 0.0, places=5)
        # "abcd" has higher entropy
        entropy_abcd = shannon_entropy("abcd")
        entropy_abab = shannon_entropy("abab")
        self.assertGreater(entropy_abcd, entropy_abab)
        self.assertEqual(shannon_entropy(""), 0.0)

    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("a"))
        self.assertTrue(is_palindrome(""))
        self.assertFalse(is_palindrome("hello"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama".replace(" ", "").lower()))

    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("", "abc"), 3)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
        self.assertEqual(levenshtein_distance("abc", "abc"), 0)
        self.assertEqual(levenshtein_distance("abc", "abd"), 1)

    def test_longest_word(self):
        self.assertEqual(longest_word("hello world foo"), "hello")
        self.assertEqual(longest_word(""), None)
        self.assertEqual(longest_word("a bb ccc"), "ccc")

    def test_shortest_word(self):
        self.assertEqual(shortest_word("hello world foo"), "foo")
        self.assertEqual(shortest_word(""), None)
        self.assertEqual(shortest_word("a bb ccc"), "a")

    def test_count_unique_words(self):
        self.assertEqual(count_unique_words("hello world hello"), 2)
        self.assertEqual(count_unique_words("a b c a b"), 3)
        self.assertEqual(count_unique_words(""), 0)

    def test_readability_score(self):
        score = readability_score("The cat sat on the mat.")
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0)
```

### Test: Misc Operations

```python
import unittest
from string_ops.misc import (
    diff_texts,
    generate_uuid,
    generate_password,
    generate_lorem_ipsum,
    text_to_morse,
    morse_to_text,
    pig_latin,
    atbash,
    vigenere_cipher,
    affine_cipher,
    generate_sequence,
)


class TestDiff(unittest.TestCase):
    def test_diff_same(self):
        self.assertEqual(diff_texts("hello", "hello"), {"added": [], "removed": []})

    def test_diff_different(self):
        result = diff_texts("hello\nworld", "hello\nearth")
        self.assertIn("world", result["removed"])
        self.assertIn("earth", result["added"])

    def test_diff_empty(self):
        self.assertEqual(diff_texts("", ""), {"added": [], "removed": []})
        self.assertEqual(diff_texts("hello", ""), {"added": [], "removed": ["hello"]})
        self.assertEqual(diff_texts("", "hello"), {"added": ["hello"], "removed": []})


class TestGenerate(unittest.TestCase):
    def test_generate_uuid(self):
        uuid = generate_uuid()
        # UUID format: 8-4-4-4-12 hex
        parts = uuid.split("-")
        self.assertEqual(len(parts), 5)
        for part in parts:
            int(part, 16)  # should be valid hex
        # Uniqueness
        uuid2 = generate_uuid()
        self.assertNotEqual(uuid, uuid2)

    def test_generate_password(self):
        pw = generate_password(length=16)
        self.assertEqual(len(pw), 16)
        self.assertTrue(any(c.isupper() for c in pw))
        self.assertTrue(any(c.islower() for c in pw))
        self.assertTrue(any(c.isdigit() for c in pw))
        self.assertTrue(any(c in "!@#$%^&*" for c in pw))

        pw_short = generate_password(length=4)
        self.assertEqual(len(pw_short), 4)

    def test_generate_lorem_ipsum(self):
        lorem = generate_lorem_ipsum(sentences=3)
        self.assertTrue(len(lorem) > 0)
        # Should contain common lorem ipsum words
        words = lorem.lower().split()
        self.assertIn("lorem", words)
        self.assertIn("ipsum", words)

    def test_generate_sequence(self):
        self.assertEqual(generate_sequence(1, 5), ["1", "2", "3", "4", "5"])
        self.assertEqual(generate_sequence("a", "c"), ["a", "b", "c"])
        self.assertEqual(generate_sequence(1, 3, step=2), ["1", "3"])
        self.assertEqual(generate_sequence("A", "D"), ["A", "B", "C", "D"])


class TestMorse(unittest.TestCase):
    def test_text_to_morse(self):
        morse = text_to_morse("SOS")
        self.assertIn("...", morse)
        self.assertIn("---", morse)

    def test_morse_to_text(self):
        text = morse_to_text("... --- ...")
        self.assertEqual(text, "SOS")

    def test_morse_roundtrip(self):
        original = "HELP"
        self.assertEqual(morse_to_text(text_to_morse(original)), original)


class TestPigLatin(unittest.TestCase):
    def test_pig_latin(self):
        self.assertEqual(pig_latin("hello"), "ellohay")
        self.assertEqual(pig_latin("apple"), "appleay")
        self.assertEqual(pig_latin("hello world"), "ellohay orldway")
        self.assertEqual(pig_latin(""), "")


class TestAtbash(unittest.TestCase):
    def test_atbash(self):
        self.assertEqual(atbash("hello"), "svool")
        self.assertEqual(atbash("Hello"), "Svool")
        self.assertEqual(atbash("xyz"), "cba")
        self.assertEqual(atbash("Hello World"), "Svool Dliow")
        self.assertEqual(atbash(""), "")

    def test_atbash_involution(self):
        for s in ["hello", "Hello World", "abc", "xyz"]:
            self.assertEqual(atbash(atbash(s)), s)


class TestVigenere(unittest.TestCase):
    def test_vigenere_encrypt(self):
        result = vigenere_cipher("HELLO", "KEY")
        self.assertNotEqual(result, "HELLO")

    def test_vigenere_roundtrip(self):
        original = "HELLO WORLD"
        key = "KEY"
        encrypted = vigenere_cipher(original, key)
        decrypted = vigenere_cipher(encrypted, key, decrypt=True)
        self.assertEqual(decrypted, original)


class TestAffine(unittest.TestCase):
    def test_affine_roundtrip(self):
        original = "HELLO"
        a, b = 5, 8
        encrypted = affine_cipher(original, a, b)
        decrypted = affine_cipher(encrypted, a, b, decrypt=True)
        self.assertEqual(decrypted, original)
```

---

## File Structure

```
string_ops_tui/
├── pyproject.toml
├── README.md
├── string_ops/
│   ├── __init__.py
│   ├── transform.py
│   ├── encode.py
│   ├── json_ops.py
│   ├── format_ops.py
│   ├── find_replace.py
│   ├── extract.py
│   ├── hash_ops.py
│   ├── statistics.py
│   ├── misc.py
│   └── utils.py
├── tui/
│   ├── __init__.py
│   ├── app.py
│   ├── categories.py
│   ├── search.py
│   ├── file_dialog.py
│   └── widgets.py
├── tests/
│   ├── __init__.py
│   ├── test_transform.py
│   ├── test_encode.py
│   ├── test_json.py
│   ├── test_format.py
│   ├── test_find_replace.py
│   ├── test_extract.py
│   ├── test_hash.py
│   ├── test_statistics.py
│   ├── test_statistics_advanced.py
│   └── test_misc.py
└── main.py
```

## Dependencies

- `textual` — modern Python TUI framework
- `rich` — optional, for rich text rendering in textual

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save output |
| `Ctrl+/` | Toggle search |
| `Esc` | Close modal / go back |
| `↑/↓` | Navigate categories / operations |
| `Enter` | Execute operation |
| `q` | Quit |

## Error Handling

- Invalid input for decode operations shows error in output view
- File open errors shown in status bar
- JSON parse errors highlighted with line/column info
- Regex errors shown with message
- Graceful degradation for unsupported operations
