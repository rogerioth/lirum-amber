import json
import re
import xml.dom.minidom
import base64
import urllib.parse


def json_escape(s: str) -> str:
    return json.dumps(s)


def json_unescape(s: str) -> str:
    return json.loads(s)


def json_pretty_print(s: str) -> str:
    obj = json.loads(s)
    return json.dumps(obj, indent=2, ensure_ascii=False)


def json_minify(s: str) -> str:
    obj = json.loads(s)
    return json.dumps(obj, separators=(',', ':'), ensure_ascii=False)


def json_to_string(s: str) -> str:
    obj = json.loads(s)
    return str(obj)


def string_to_json(s: str) -> str:
    return json.dumps(s)


def json_diff(json1: str, json2: str) -> dict:
    obj1 = json.loads(json1)
    obj2 = json.loads(json2)
    return {
        'identical': obj1 == obj2,
        'json1': obj1,
        'json2': obj2,
    }


def json_path_extract(json_str: str, path: str) -> any:
    obj = json.loads(json_str)
    keys = path.strip('.').split('.')
    current = obj
    for key in keys:
        if isinstance(current, dict):
            current = current.get(key)
        elif isinstance(current, list):
            try:
                current = current[int(key)]
            except (ValueError, IndexError):
                return None
        else:
            return None
    return current


def xml_pretty_print(s: str) -> str:
    dom = xml.dom.minidom.parseString(s)
    return dom.toprettyxml(indent='  ')


def xml_minify(s: str) -> str:
    dom = xml.dom.minidom.parseString(s)
    result = dom.documentElement.toxml()
    # Remove whitespace between tags
    result = re.sub(r'>\s+<', '><', result)
    return result


def sql_pretty_print(s: str) -> str:
    keywords = ['SELECT', 'FROM', 'WHERE', 'AND', 'OR', 'JOIN', 'LEFT JOIN',
                'RIGHT JOIN', 'INNER JOIN', 'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT']
    result = s.strip()
    for kw in keywords:
        result = re.sub(f'(?i)\\b{re.escape(kw)}\\b', f'\n{kw.upper()}', result)
    lines = [line.strip() for line in result.split('\n') if line.strip()]
    if not lines:
        return ''
    formatted = [lines[0]]
    for line in lines[1:]:
        formatted.append(f'  {line}')
    return '\n'.join(formatted)


def sql_minify(s: str) -> str:
    return re.sub(r'\s+', ' ', s).strip()


def css_pretty_print(s: str) -> str:
    s = re.sub(r'\s*\{\s*', ' {\n  ', s)
    s = re.sub(r'\s*;\s*', ';\n  ', s)
    s = re.sub(r'\s*\}\s*', '\n}\n', s)
    s = re.sub(r'\n  \n', '\n', s)
    return s.strip()


def css_minify(s: str) -> str:
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.DOTALL)
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s*\{\s*', '{', s)
    s = re.sub(r'\s*\}\s*', '}', s)
    s = re.sub(r'\s*;\s*', ';', s)
    s = re.sub(r'\s*:\s*', ':', s)
    return s.strip()


def parse_query_string(s: str) -> str:
    parsed = urllib.parse.parse_qs(s)
    # Convert single-item lists to single values
    result = {}
    for k, v in parsed.items():
        result[k] = v[0] if len(v) == 1 else v
    return json.dumps(result)


def stringify_query_string(s: str) -> str:
    obj = json.loads(s)
    return urllib.parse.urlencode(obj, doseq=True)


def jwt_decode(s: str) -> str:
    parts = s.split('.')
    if len(parts) < 2:
        raise ValueError('Invalid JWT')
    header = json.loads(base64.urlsafe_b64decode(parts[0] + '=' * (4 - len(parts[0]) % 4)).decode('utf-8'))
    payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=' * (4 - len(parts[1]) % 4)).decode('utf-8'))
    return json.dumps({'header': header, 'payload': payload})
