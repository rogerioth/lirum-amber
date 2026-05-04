import base64
import html
import urllib.parse
import quopri

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


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


def base64url_encode(s: str) -> str:
    return base64.urlsafe_b64encode(s.encode('utf-8')).decode('ascii')


def base64url_decode(s: str) -> str:
    # Add padding if missing
    s += '=' * (4 - len(s) % 4) if len(s) % 4 else ''
    return base64.urlsafe_b64decode(s).decode('utf-8')


def base32_encode(s: str) -> str:
    return base64.b32encode(s.encode('utf-8')).decode('ascii')


def base32_decode(s: str) -> str:
    return base64.b32decode(s).decode('utf-8')


def base58_encode(s: str) -> str:
    bytes_data = s.encode('utf-8')
    leading_zeros = 0
    for b in bytes_data:
        if b == 0:
            leading_zeros += 1
        else:
            break
    num = int.from_bytes(bytes_data, 'big')
    encoded = []
    while num > 0:
        num, rem = divmod(num, 58)
        encoded.append(BASE58_ALPHABET[rem])
    encoded.extend(['1'] * leading_zeros)
    return ''.join(reversed(encoded))


def base58_decode(s: str) -> str:
    num = 0
    for c in s:
        num = num * 58 + BASE58_ALPHABET.index(c)
    if num == 0:
        bytes_data = b''
    else:
        bytes_data = num.to_bytes((num.bit_length() + 7) // 8, 'big')
    leading_zeros = len(s) - len(s.lstrip('1'))
    bytes_data = b'\x00' * leading_zeros + bytes_data
    return bytes_data.decode('utf-8')


def base85_encode(s: str) -> str:
    return base64.a85encode(s.encode('utf-8')).decode('ascii')


def base85_decode(s: str) -> str:
    return base64.a85decode(s).decode('utf-8')


def punycode_encode(s: str) -> str:
    encoded = s.encode('punycode').decode('ascii')
    if s.isascii():
        return encoded.rstrip('-')
    return encoded


def punycode_decode(s: str) -> str:
    try:
        return s.encode('ascii').decode('punycode')
    except UnicodeDecodeError:
        return s


def quoted_printable_encode(s: str) -> str:
    encoded = quopri.encodestring(s.encode('utf-8'))
    return encoded.decode('ascii').rstrip('\n')


def quoted_printable_decode(s: str) -> str:
    return quopri.decodestring(s.encode('ascii')).decode('utf-8')


def rot47(s: str) -> str:
    result = []
    for c in s:
        ord_c = ord(c)
        if 33 <= ord_c <= 126:
            if c.isdigit():
                result.append(c)
            else:
                new_ord = ord_c + 47
                if new_ord > 126:
                    new_ord -= 94
                result.append(chr(new_ord))
        else:
            result.append(c)
    return ''.join(result)


def caesar_cipher_encode(s: str, shift: int = 3) -> str:
    result = []
    for c in s:
        if 'a' <= c <= 'z':
            result.append(chr((ord(c) - ord('a') + shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            result.append(chr((ord(c) - ord('A') + shift) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)


def caesar_cipher_decode(s: str, shift: int = 3) -> str:
    return caesar_cipher_encode(s, -shift)
