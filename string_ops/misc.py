import re
import random
import string
import uuid


def diff_texts(text1: str, text2: str) -> dict:
    lines1 = text1.split('\n') if text1 else []
    lines2 = text2.split('\n') if text2 else []
    added = [l for l in lines2 if l not in lines1]
    removed = [l for l in lines1 if l not in lines2]
    return {'added': added, 'removed': removed}


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_password(length: int = 16, use_upper: bool = True,
                      use_lower: bool = True, use_digits: bool = True,
                      use_special: bool = True) -> str:
    chars = ''
    if use_upper:
        chars += string.ascii_uppercase
    if use_lower:
        chars += string.ascii_lowercase
    if use_digits:
        chars += string.digits
    if use_special:
        chars += '!@#$%^&*'

    if not chars:
        chars = string.ascii_letters + string.digits

    pw = [random.choice(chars) for _ in range(length)]

    i = 0
    if use_upper:
        pw[i] = random.choice(string.ascii_uppercase)
        i += 1
    if use_lower:
        pw[i] = random.choice(string.ascii_lowercase)
        i += 1
    if use_digits:
        pw[i] = random.choice(string.digits)
        i += 1
    if use_special:
        pw[i] = random.choice('!@#$%^&*')
        i += 1

    random.shuffle(pw)
    return ''.join(pw)


def generate_lorem_ipsum(sentences: int = 3) -> str:
    words = [
        "lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing",
        "elit", "sed", "do", "eiusmod", "tempor", "incididunt", "ut", "labore",
        "et", "dolore", "magna", "aliqua", "enim", "ad", "minim", "veniam",
        "quis", "nostrud", "exercitation", "ullamco", "laboris", "nisi",
        "aliquip", "ex", "ea", "commodo", "consequat", "duis", "aute", "irure",
        "dolor", "in", "reprehenderit", "voluptate", "velit", "esse", "cillum",
        "fugiat", "nulla", "pariatur", "excepteur", "sint", "occaecat",
        "cupidatat", "non", "proident", "sunt", "culpa", "qui", "officia",
        "deserunt", "mollit", "anim", "id", "est", "laborum",
    ]
    result_sentences = []
    for _ in range(sentences):
        sentence_len = random.randint(8, 15)
        sentence_words = [random.choice(words) for _ in range(sentence_len)]
        sentence_words[0] = sentence_words[0].capitalize()
        result_sentences.append(' '.join(sentence_words) + '.')
    return ' '.join(result_sentences)


def generate_sequence(start, end, step=1) -> list:
    if isinstance(start, int) and isinstance(end, int):
        return [str(i) for i in range(start, end + 1, step)]
    elif isinstance(start, str) and isinstance(end, str) and len(start) == 1 and len(end) == 1:
        preserve_case = start.islower()
        start_ord = ord(start.lower())
        end_ord = ord(end.lower())
        result = [chr(i) for i in range(start_ord, end_ord + 1, step)]
        if preserve_case:
            return result
        return [c.upper() for c in result]
    return []


def text_to_morse(s: str) -> str:
    morse_map = {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/',
    }
    return ' '.join(morse_map.get(c.upper(), '') for c in s)


def morse_to_text(s: str) -> str:
    morse_map = {v: k for k, v in {
        'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
        'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
        'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
        'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
        '8': '---..', '9': '----.', ' ': '/',
    }.items()}
    return ''.join(morse_map.get(code, '') for code in s.split())


def pig_latin(s: str) -> str:
    words = s.split()
    result = []
    for word in words:
        if not word:
            result.append('')
            continue
        vowels = 'aeiouAEIOU'
        if word[0] in vowels:
            result.append(word + 'ay')
        else:
            # Find first vowel
            i = 0
            while i < len(word) and word[i] not in vowels:
                i += 1
            if i < len(word):
                result.append(word[i:] + word[:i] + 'ay')
            else:
                result.append(word + 'ay')
    return ' '.join(result)


def atbash(s: str) -> str:
    result = []
    for c in s:
        if 'a' <= c <= 'z':
            result.append(chr(ord('z') - (ord(c) - ord('a'))))
        elif 'A' <= c <= 'Z':
            result.append(chr(ord('Z') - (ord(c) - ord('A'))))
        else:
            result.append(c)
    return ''.join(result)


def vigenere_cipher(s: str, key: str, decrypt: bool = False) -> str:
    key = key.upper()
    result = []
    key_idx = 0
    for c in s:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            shift = ord(key[key_idx % len(key)]) - ord('A')
            if decrypt:
                shift = -shift
            result.append(chr((ord(c) - base + shift) % 26 + base))
            key_idx += 1
        else:
            result.append(c)
    return ''.join(result)


def affine_cipher(s: str, a: int, b: int, decrypt: bool = False) -> str:
    result = []
    for c in s:
        if c.isalpha():
            base = ord('A') if c.isupper() else ord('a')
            x = ord(c) - base
            if decrypt:
                # Find modular inverse of a mod 26
                a_inv = pow(a, -1, 26)
                x = a_inv * (x - b) % 26
            else:
                x = (a * x + b) % 26
            result.append(chr(x + base))
        else:
            result.append(c)
    return ''.join(result)

def generate_zalgo(s: str) -> str:
    """Add Zalgo text effects (diacritics)."""
    import random
    zalgo_chars = [
        '\u0300', '\u0301', '\u0302', '\u0303', '\u0304', '\u0305', '\u0306', '\u0307',
        '\u0308', '\u0309', '\u030a', '\u030b', '\u030c', '\u030d', '\u030e', '\u030f',
    ]
    result = []
    for c in s:
        result.append(c)
        for _ in range(random.randint(1, 5)):
            result.append(random.choice(zalgo_chars))
    return ''.join(result)


def generate_leetspeak(s: str) -> str:
    """Convert to leetspeak."""
    leet_map = {
        'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7',
        'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5', 'T': '7',
    }
    return ''.join(leet_map.get(c, c) for c in s)


def generate_upside_down(s: str) -> str:
    """Convert to upside-down text."""
    flip_map = {
        'a': '\u0250', 'b': 'q', 'c': '\u0254', 'd': 'p', 'e': '\u01dd',
        'f': '\u025f', 'g': '\u0253', 'h': '\u0265', 'i': '\u0131', 'j': '\u027e',
        'k': '\u029e', 'l': 'l', 'm': '\u026f', 'n': 'u', 'o': 'o',
        'p': 'd', 'q': 'b', 'r': '\u0279', 's': 's', 't': '\u0287',
        'u': 'n', 'v': '\u028c', 'w': '\u028d', 'x': 'x', 'y': '\u028e', 'z': 'z',
    }
    return ''.join(flip_map.get(c, c) for c in reversed(s))


def generate_vaporwave(s: str) -> str:
    """Convert to fullwidth/vaporwave text."""
    result = []
    for c in s:
        if ' ' <= c <= '~':
            result.append(chr(ord(c) + 0xfee0))
        else:
            result.append(c)
    return ''.join(result)


def generate_braille(s: str) -> str:
    """Convert to braille unicode (simplified - A-Z only)."""
    braille_map = {
        'a': '\u2801', 'b': '\u2803', 'c': '\u2809', 'd': '\u2819',
        'e': '\u2811', 'f': '\u280b', 'g': '\u281b', 'h': '\u2813',
        'i': '\u280a', 'j': '\u281a', 'k': '\u2805', 'l': '\u2807',
        'm': '\u280d', 'n': '\u281d', 'o': '\u2815', 'p': '\u280f',
        'q': '\u281f', 'r': '\u2817', 's': '\u280e', 't': '\u281e',
        'u': '\u2825', 'v': '\u2827', 'w': '\u283a', 'x': '\u282d',
        'y': '\u283d', 'z': '\u2835',
    }
    return ''.join(braille_map.get(c.lower(), c) for c in s)


def generate_ulid() -> str:
    """Generate ULID."""
    try:
        import ulid
        return str(ulid.ulid())
    except ImportError:
        import base64
        import time
        ts = int(time.time() * 1000)
        return base64.b32encode(ts.to_bytes(6, 'big')).decode().rstrip('=')[:26]


def generate_nanoid() -> str:
    """Generate NanoID."""
    try:
        from nanoid import generate
        return generate()
    except ImportError:
        import random
        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-'
        return ''.join(random.choice(chars) for _ in range(21))


def unslugify(s: str) -> str:
    """Convert slug to readable text."""
    return s.replace('-', ' ').replace('_', ' ').title()
