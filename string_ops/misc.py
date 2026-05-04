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

    pw = []
    for _ in range(length):
        pw.append(random.choice(chars))
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
