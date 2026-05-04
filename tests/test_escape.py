import unittest
import json
import html
import re
from string_ops.escape import (
    json_escape,
    json_unescape,
    xml_escape,
    xml_unescape,
    csv_escape,
    csv_unescape,
    sql_escape,
    regex_escape,
    c_string_escape,
    c_string_unescape,
    java_string_escape,
    java_string_unescape,
    python_string_escape,
    python_string_unescape,
    bash_escape,
)


class TestJsonEscape(unittest.TestCase):
    def test_json_escape(self):
        self.assertEqual(json_escape('hello\nworld'), 'hello\\nworld')
        self.assertEqual(json_escape('say "hi"'), 'say \\"hi\\"')
        self.assertEqual(json_escape('back\\slash'), 'back\\\\slash')
        self.assertEqual(json_escape(''), '')
        self.assertEqual(json_escape('no escape needed'), 'no escape needed')

    def test_json_unescape(self):
        self.assertEqual(json_unescape('hello\\nworld'), 'hello\nworld')
        self.assertEqual(json_unescape('say \\"hi\\"'), 'say "hi"')
        self.assertEqual(json_unescape(''), '')
        self.assertEqual(json_unescape('no escape needed'), 'no escape needed')


class TestXmlEscape(unittest.TestCase):
    def test_xml_escape(self):
        self.assertEqual(xml_escape('<tag>'), '&lt;tag&gt;')
        self.assertEqual(xml_escape('"quote"'), '&quot;quote&quot;')
        self.assertEqual(xml_escape("'apostrophe'"), '&apos;apostrophe&apos;')
        self.assertEqual(xml_escape('a & b'), 'a &amp; b')
        self.assertEqual(xml_escape(''), '')

    def test_xml_unescape(self):
        self.assertEqual(xml_unescape('&lt;tag&gt;'), '<tag>')
        self.assertEqual(xml_unescape('&quot;quote&quot;'), '"quote"')
        self.assertEqual(xml_unescape('&apos;apostrophe&apos;'), "'apostrophe'")
        self.assertEqual(xml_unescape('a &amp; b'), 'a & b')
        self.assertEqual(xml_unescape(''), '')


class TestCsvEscape(unittest.TestCase):
    def test_csv_escape(self):
        self.assertEqual(csv_escape('simple'), 'simple')
        self.assertEqual(csv_escape('has,comma'), '"has,comma"')
        self.assertEqual(csv_escape('has "quote"'), '"has ""quote"""')
        self.assertEqual(csv_escape('has\nnewline'), '"has\nnewline"')
        self.assertEqual(csv_escape(''), '')

    def test_csv_unescape(self):
        self.assertEqual(csv_unescape('simple'), 'simple')
        self.assertEqual(csv_unescape('"has,comma"'), 'has,comma')
        self.assertEqual(csv_unescape('"has ""quote"""'), 'has "quote"')
        self.assertEqual(csv_unescape(''), '')


class TestSqlEscape(unittest.TestCase):
    def test_sql_escape(self):
        self.assertEqual(sql_escape("it's"), "it''s")
        self.assertEqual(sql_escape('say "hi"'), 'say \\"hi\\"')
        self.assertEqual(sql_escape('back\\slash'), 'back\\\\slash')
        self.assertEqual(sql_escape(''), '')

    def test_sql_unescape(self):
        from string_ops.escape import sql_unescape
        self.assertEqual(sql_unescape("it''s"), "it's")
        self.assertEqual(sql_unescape('say \\"hi\\"'), 'say "hi"')
        self.assertEqual(sql_unescape(''), '')


class TestRegexEscape(unittest.TestCase):
    def test_regex_escape(self):
        self.assertEqual(regex_escape('hello.world'), 'hello\\.world')
        self.assertEqual(regex_escape('a*b+c?'), 'a\\*b\\+c\\?')
        self.assertEqual(regex_escape('[test]'), '\\[test\\]')
        self.assertEqual(regex_escape(''), '')
        # re.escape also escapes spaces
        self.assertEqual(regex_escape('no escape needed'), 'no\\ escape\\ needed')


class TestCStringEscape(unittest.TestCase):
    def test_c_string_escape(self):
        self.assertEqual(c_string_escape('hello\nworld'), 'hello\\nworld')
        self.assertEqual(c_string_escape('tab\there'), 'tab\\there')
        self.assertEqual(c_string_escape('say "hi"'), 'say \\"hi\\"')
        self.assertEqual(c_string_escape('back\\slash'), 'back\\\\slash')
        self.assertEqual(c_string_escape(''), '')

    def test_c_string_unescape(self):
        self.assertEqual(c_string_unescape('hello\\nworld'), 'hello\nworld')
        self.assertEqual(c_string_unescape('tab\\there'), 'tab\there')
        self.assertEqual(c_string_unescape('say \\"hi\\"'), 'say "hi"')
        self.assertEqual(c_string_unescape(''), '')


class TestJavaStringEscape(unittest.TestCase):
    def test_java_string_escape(self):
        self.assertEqual(java_string_escape('hello\nworld'), 'hello\\nworld')
        self.assertEqual(java_string_escape('tab\there'), 'tab\\there')
        self.assertEqual(java_string_escape('say "hi"'), 'say \\"hi\\"')
        self.assertEqual(java_string_escape(''), '')

    def test_java_string_unescape(self):
        self.assertEqual(java_string_unescape('hello\\nworld'), 'hello\nworld')
        self.assertEqual(java_string_unescape(''), '')


class TestPythonStringEscape(unittest.TestCase):
    def test_python_string_escape(self):
        self.assertEqual(python_string_escape('hello\nworld'), repr('hello\nworld'))
        self.assertEqual(python_string_escape(''), repr(''))

    def test_python_string_unescape(self):
        self.assertEqual(python_string_unescape(repr('hello')), 'hello')
        self.assertEqual(python_string_unescape(repr('hello\nworld')), 'hello\nworld')
        self.assertEqual(python_string_unescape(''), '')


class TestBashEscape(unittest.TestCase):
    def test_bash_escape(self):
        self.assertEqual(bash_escape('simple'), 'simple')
        self.assertEqual(bash_escape('has space'), "'has space'")
        self.assertEqual(bash_escape('has$special'), "'has$special'")
        self.assertEqual(bash_escape('has"quote'), "'has\"quote'")
        self.assertEqual(bash_escape(''), '')


if __name__ == '__main__':
    unittest.main()
