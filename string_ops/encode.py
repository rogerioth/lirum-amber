import base64
import html
import urllib.parse


def base64_encode(s: str) -> str:
    return base64.b64encode(s.encode('utf-8')).decode('ascii')


def base64_decode(s: str) -> str:
    return base64.b64decode(s).decode('utf-8')


def url_encode(s: str) -> str:
    return urllib.parse.quote(s, safe='')


def url_decode(s: str) -> str:
    return urllib.parse.unquote(s)


def html_encode(s: str) -> str:
    return html.escape(s, quote=True)


def html_decode(s: str) -> str:
    return html.unescape(s)


def hex_encode(s: str) -> str:
    return s.encode('utf-8').hex()


def hex_decode(s: str) -> str:
    return bytes.fromhex(s).decode('utf-8')


def rot13(s: str) -> str:
    result = []
    for c in s:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)


def unicode_escape(s: str) -> str:
    return ''.join(f'\\u{ord(c):04x}' if ord(c) > 127 else c for c in s)


def unicode_unescape(s: str) -> str:
    def replace_match(m):
        return chr(int(m.group(1), 16))
    import re
    return re.sub(r'\\u([0-9a-fA-F]{4})', replace_match, s)


def binary_encode(s: str) -> str:
    return ''.join(format(ord(c), '08b') for c in s)


def binary_decode(s: str) -> str:
    chars = []
    for i in range(0, len(s), 8):
        byte = s[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)


def octal_encode(s: str) -> str:
    return ''.join(format(ord(c), '03o') for c in s)


def octal_decode(s: str) -> str:
    chars = []
    for i in range(0, len(s), 3):
        byte = s[i:i+3]
        if len(byte) == 3:
            chars.append(chr(int(byte, 8)))
    return ''.join(chars)
