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
    xml_pretty_print,
    xml_minify,
    sql_pretty_print,
    sql_minify,
    css_pretty_print,
    css_minify,
    parse_query_string,
    stringify_query_string,
    jwt_decode,
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


class TestXmlOps(unittest.TestCase):
    def test_xml_pretty_print(self):
        xml = "<root><child>text</child></root>"
        result = xml_pretty_print(xml)
        self.assertIn("\n", result)
        self.assertIn("  ", result)

    def test_xml_pretty_print_invalid(self):
        with self.assertRaises(Exception):
            xml_pretty_print("<invalid>")

    def test_xml_minify(self):
        xml = "<root>\n  <child>text</child>\n</root>"
        result = xml_minify(xml)
        self.assertNotIn("\n", result)
        self.assertNotIn("  ", result)
        self.assertEqual(result, "<root><child>text</child></root>")

    def test_xml_minify_already_minified(self):
        xml = "<root><child/></root>"
        self.assertEqual(xml_minify(xml), xml)


class TestSqlOps(unittest.TestCase):
    def test_sql_pretty_print(self):
        sql = "SELECT * FROM users WHERE id = 1"
        result = sql_pretty_print(sql)
        self.assertIn("\n", result)

    def test_sql_minify(self):
        sql = "SELECT *\nFROM users\nWHERE id = 1"
        result = sql_minify(sql)
        self.assertNotIn("\n", result)

    def test_sql_minify_already_minified(self):
        sql = "SELECT * FROM users"
        self.assertEqual(sql_minify(sql), sql)


class TestCssOps(unittest.TestCase):
    def test_css_pretty_print(self):
        css = "body{color:red;font-size:16px;}"
        result = css_pretty_print(css)
        self.assertIn("\n", result)

    def test_css_minify(self):
        css = "body {\n  color: red;\n  font-size: 16px;\n}"
        result = css_minify(css)
        self.assertNotIn("\n", result)
        self.assertNotIn(" ", result)

    def test_css_minify_already_minified(self):
        css = "body{color:red;}"
        self.assertEqual(css_minify(css), css)


class TestQueryString(unittest.TestCase):
    def test_parse_query_string(self):
        qs = "name=Alice&age=30&hobbies=reading&hobbies=coding"
        result = parse_query_string(qs)
        obj = json.loads(result)
        self.assertEqual(obj["name"], "Alice")
        self.assertEqual(obj["age"], "30")
        self.assertEqual(obj["hobbies"], ["reading", "coding"])

    def test_parse_query_string_empty(self):
        self.assertEqual(parse_query_string(""), "{}")

    def test_stringify_query_string(self):
        json_str = '{"name": "Alice", "age": "30"}'
        result = stringify_query_string(json_str)
        self.assertIn("name=Alice", result)
        self.assertIn("age=30", result)

    def test_stringify_query_string_array(self):
        json_str = '{"hobbies": ["reading", "coding"]}'
        result = stringify_query_string(json_str)
        self.assertIn("hobbies=reading", result)
        self.assertIn("hobbies=coding", result)


class TestJwtDecode(unittest.TestCase):
    def test_jwt_decode(self):
        # JWT: header {"alg":"HS256","typ":"JWT"}, payload {"sub":"1234567890","name":"John Doe"}
        # Base64url encoded header: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
        # Base64url encoded payload: eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0
        # Signature: dummy
        jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIn0.dummy"
        result = jwt_decode(jwt)
        obj = json.loads(result)
        self.assertEqual(obj["header"]["alg"], "HS256")
        self.assertEqual(obj["payload"]["name"], "John Doe")

    def test_jwt_decode_invalid(self):
        with self.assertRaises(Exception):
            jwt_decode("invalid.jwt")


if __name__ == '__main__':
    unittest.main()
