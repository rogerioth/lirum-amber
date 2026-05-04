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
        self.assertIn("  ", result)
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


class TestJsonDiff(unittest.TestCase):
    def test_json_diff_identical(self):
        data = '{"name": "Alice", "age": 30}'
        result = json_diff(data, data)
        self.assertTrue(result['identical'])

    def test_json_diff_different(self):
        result = json_diff('{"a": 1}', '{"a": 2}')
        self.assertFalse(result['identical'])
        self.assertEqual(result['json1'], {"a": 1})
        self.assertEqual(result['json2'], {"a": 2})


class TestJsonPathExtract(unittest.TestCase):
    def test_json_path_extract_nested(self):
        data = '{"users": [{"name": "Alice"}, {"name": "Bob"}]}'
        result = json_path_extract(data, 'users.0.name')
        self.assertEqual(result, "Alice")

    def test_json_path_extract_simple(self):
        data = '{"name": "Alice"}'
        result = json_path_extract(data, 'name')
        self.assertEqual(result, "Alice")

    def test_json_path_extract_missing(self):
        data = '{"name": "Alice"}'
        result = json_path_extract(data, 'age')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
