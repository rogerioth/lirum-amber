"""Escape and unescape operations for various formats."""
import json
import html
import re
import shlex


def json_escape(s: str) -> str:
    """Escape a string for use in JSON."""
    return json.dumps(s)[1:-1]  # Remove surrounding quotes


def json_unescape(s: str) -> str:
    """Unescape a JSON-escaped string."""
    return json.loads(f'"{s}"')


def xml_escape(s: str) -> str:
    """Escape special XML characters."""
    s = s.replace('&', '&amp;')
    s = s.replace('<', '&lt;')
    s = s.replace('>', '&gt;')
    s = s.replace('"', '&quot;')
    s = s.replace("'", '&apos;')
    return s


def xml_unescape(s: str) -> str:
    """Unescape XML entities."""
    return html.unescape(s)


def csv_escape(s: str) -> str:
    """Escape a string for use in CSV."""
    if '"' in s or ',' in s or '\n' in s or '\r' in s:
        return '"' + s.replace('"', '""') + '"'
    return s


def csv_unescape(s: str) -> str:
    """Unescape a CSV-escaped string."""
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1].replace('""', '"')
    return s


def sql_escape(s: str) -> str:
    """Escape special SQL characters."""
    return s.replace("'", "''").replace('\\', '\\\\').replace('"', '\\"')


def sql_unescape(s: str) -> str:
    """Unescape SQL-escaped string."""
    return s.replace("''", "'").replace('\\\\', '\\').replace('\\"', '"')


def regex_escape(s: str) -> str:
    """Escape special regex characters."""
    return re.escape(s)


def c_string_escape(s: str) -> str:
    """Escape a string for C string literals."""
    return s.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace('"', '\\"')


def c_string_unescape(s: str) -> str:
    """Unescape a C string literal."""
    return s.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r').replace('\\\\', '\\')


def java_string_escape(s: str) -> str:
    """Escape a string for Java string literals."""
    return s.replace('\\', '\\\\').replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r').replace('"', '\\"')


def java_string_unescape(s: str) -> str:
    """Unescape a Java string literal."""
    return s.replace('\\"', '"').replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r').replace('\\\\', '\\')


def python_string_escape(s: str) -> str:
    """Escape a string for Python string literals."""
    return repr(s)


def python_string_unescape(s: str) -> str:
    """Unescape a Python string literal."""
    try:
        return eval(s) if s.startswith(("'", '"')) else s
    except:
        return s


def bash_escape(s: str) -> str:
    """Escape a string for bash/shell."""
    if not s:
        return ''
    return shlex.quote(s)
