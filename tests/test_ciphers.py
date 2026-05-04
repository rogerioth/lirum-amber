import unittest
from string_ops.ciphers import (
    vigenere_cipher_encode,
    vigenere_cipher_decode,
    morse_encode,
    morse_decode,
)


class TestVigenereCipher(unittest.TestCase):
    def test_vigenere_encode_basic(self):
        self.assertEqual(vigenere_cipher_encode("ATTACK", "KEY"), "KXRKGI")

    def test_vigenere_encode_lowercase(self):
        self.assertEqual(vigenere_cipher_encode("attack", "KEY"), "KXRKGI")

    def test_vigenere_encode_with_spaces(self):
        self.assertEqual(vigenere_cipher_encode("HELLO WORLD", "KEY"), "RIJVSUYVJN")

    def test_vigenere_encode_default_key(self):
        result = vigenere_cipher_encode("HELLO")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 5)

    def test_vigenere_encode_empty_string(self):
        self.assertEqual(vigenere_cipher_encode("", "KEY"), "")

    def test_vigenere_decode_basic(self):
        self.assertEqual(vigenere_cipher_decode("KXRKGI", "KEY"), "ATTACK")

    def test_vigenere_decode_lowercase(self):
        self.assertEqual(vigenere_cipher_decode("kxrkgi", "KEY"), "ATTACK")

    def test_vigenere_decode_with_spaces(self):
        self.assertEqual(vigenere_cipher_decode("RIJVS UYVJN", "KEY"), "HELLOWORLD")

    def test_vigenere_decode_default_key(self):
        encoded = vigenere_cipher_encode("HELLO")
        decoded = vigenere_cipher_decode(encoded)
        self.assertEqual(decoded, "HELLO")

    def test_vigenere_decode_empty_string(self):
        self.assertEqual(vigenere_cipher_decode("", "KEY"), "")

    def test_vigenere_roundtrip(self):
        original = "SECRETMESSAGE"
        key = "PASSWORD"
        encoded = vigenere_cipher_encode(original, key)
        decoded = vigenere_cipher_decode(encoded, key)
        self.assertEqual(decoded, original)


class TestMorseCode(unittest.TestCase):
    def test_morse_encode_basic(self):
        self.assertEqual(morse_encode("A"), ".-")
        self.assertEqual(morse_encode("AB"), ".- -...")

    def test_morse_encode_hello(self):
        self.assertEqual(morse_encode("HELLO"), ".... . .-.. .-.. ---")

    def test_morse_encode_with_spaces(self):
        self.assertEqual(morse_encode("HELLO WORLD"), ".... . .-.. .-.. --- / .-- --- .-. .-.. -..")

    def test_morse_encode_lowercase(self):
        self.assertEqual(morse_encode("hello"), ".... . .-.. .-.. ---")

    def test_morse_encode_empty_string(self):
        self.assertEqual(morse_encode(""), "")

    def test_morse_encode_multiple_words(self):
        self.assertEqual(morse_encode("A B"), ".- / -...")

    def test_morse_decode_basic(self):
        self.assertEqual(morse_decode(".-"), "A")
        self.assertEqual(morse_decode(".- -..."), "AB")

    def test_morse_decode_hello(self):
        self.assertEqual(morse_decode(".... . .-.. .-.. ---"), "HELLO")

    def test_morse_decode_with_slash(self):
        self.assertEqual(morse_decode(".... . .-.. .-.. --- / .-- --- .-. .-.. -.."), "HELLO WORLD")

    def test_morse_decode_lowercase_input(self):
        self.assertEqual(morse_decode(".... . .-.. .-.. ---"), "HELLO")

    def test_morse_decode_empty_string(self):
        self.assertEqual(morse_decode(""), "")

    def test_morse_roundtrip(self):
        original = "HELLO WORLD"
        encoded = morse_encode(original)
        decoded = morse_decode(encoded)
        self.assertEqual(decoded, original)


if __name__ == '__main__':
    unittest.main()
