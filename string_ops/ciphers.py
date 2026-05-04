def vigenere_cipher_encode(s: str, key: str = "KEY") -> str:
    if not s:
        return ""
    
    result = []
    key = key.upper()
    key_index = 0
    
    for char in s.upper():
        if char.isalpha():
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            encoded_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(encoded_char)
            key_index += 1
    
    return ''.join(result)


def vigenere_cipher_decode(s: str, key: str = "KEY") -> str:
    if not s:
        return ""
    
    result = []
    key = key.upper()
    key_index = 0
    
    for char in s.upper():
        if char.isalpha():
            key_char = key[key_index % len(key)]
            shift = ord(key_char) - ord('A')
            decoded_char = chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
            result.append(decoded_char)
            key_index += 1
    
    return ''.join(result)


MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', ' ': '/'
}

MORSE_TO_CHAR = {v: k for k, v in MORSE_CODE.items() if k != ' '}


def morse_encode(s: str) -> str:
    if not s:
        return ""
    
    words = s.upper().split()
    morse_words = []
    
    for word in words:
        morse_chars = []
        for char in word:
            if char in MORSE_CODE:
                morse_chars.append(MORSE_CODE[char])
        morse_words.append(' '.join(morse_chars))
    
    return ' / '.join(morse_words)


def morse_decode(s: str) -> str:
    if not s:
        return ""
    
    words = s.split(' / ')
    decoded_words = []
    
    for word in words:
        chars = word.split()
        decoded_chars = []
        for char in chars:
            if char in MORSE_TO_CHAR:
                decoded_chars.append(MORSE_TO_CHAR[char])
        decoded_words.append(''.join(decoded_chars))
    
    return ' '.join(decoded_words)
