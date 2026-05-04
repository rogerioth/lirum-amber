import unittest
from string_ops.misc import (
    diff_texts,
    generate_uuid,
    generate_password,
    generate_lorem_ipsum,
    generate_sequence,
    text_to_morse,
    morse_to_text,
    pig_latin,
    atbash,
    vigenere_cipher,
    affine_cipher,
)


class TestDiff(unittest.TestCase):
    def test_diff_same(self):
        self.assertEqual(diff_texts("hello", "hello"), {"added": [], "removed": []})

    def test_diff_different(self):
        result = diff_texts("hello\nworld", "hello\nearth")
        self.assertIn("world", result["removed"])
        self.assertIn("earth", result["added"])

    def test_diff_empty(self):
        self.assertEqual(diff_texts("", ""), {"added": [], "removed": []})
        self.assertEqual(diff_texts("hello", ""), {"added": [], "removed": ["hello"]})
        self.assertEqual(diff_texts("", "hello"), {"added": ["hello"], "removed": []})


class TestGenerate(unittest.TestCase):
    def test_generate_uuid(self):
        uuid = generate_uuid()
        parts = uuid.split("-")
        self.assertEqual(len(parts), 5)
        for part in parts:
            int(part, 16)
        uuid2 = generate_uuid()
        self.assertNotEqual(uuid, uuid2)

    def test_generate_password(self):
        pw = generate_password(length=16)
        self.assertEqual(len(pw), 16)
        self.assertTrue(any(c.isupper() for c in pw))
        self.assertTrue(any(c.islower() for c in pw))
        self.assertTrue(any(c.isdigit() for c in pw))

        pw_short = generate_password(length=4)
        self.assertEqual(len(pw_short), 4)

    def test_generate_lorem_ipsum(self):
        # Run multiple times to account for randomness
        found_lorem = False
        found_ipsum = False
        for _ in range(20):
            lorem = generate_lorem_ipsum(sentences=3)
            words = lorem.lower().split()
            if "lorem" in words and "ipsum" in words:
                found_lorem = True
                found_ipsum = True
                break
        self.assertTrue(found_lorem, "lorem not found in generated text")
        self.assertTrue(found_ipsum, "ipsum not found in generated text")

    def test_generate_sequence(self):
        self.assertEqual(generate_sequence(1, 5), ["1", "2", "3", "4", "5"])
        self.assertEqual(generate_sequence("a", "c"), ["a", "b", "c"])
        self.assertEqual(generate_sequence(1, 3, step=2), ["1", "3"])
        self.assertEqual(generate_sequence("A", "D"), ["A", "B", "C", "D"])


class TestMorse(unittest.TestCase):
    def test_text_to_morse(self):
        morse = text_to_morse("SOS")
        self.assertIn("...", morse)
        self.assertIn("---", morse)

    def test_morse_to_text(self):
        text = morse_to_text("... --- ...")
        self.assertEqual(text, "SOS")

    def test_morse_roundtrip(self):
        original = "HELP"
        self.assertEqual(morse_to_text(text_to_morse(original)), original)


class TestPigLatin(unittest.TestCase):
    def test_pig_latin(self):
        self.assertEqual(pig_latin("hello"), "ellohay")
        self.assertEqual(pig_latin("apple"), "appleay")
        self.assertEqual(pig_latin("hello world"), "ellohay orldway")
        self.assertEqual(pig_latin(""), "")


class TestAtbash(unittest.TestCase):
    def test_atbash(self):
        self.assertEqual(atbash("hello"), "svool")
        self.assertEqual(atbash("Hello"), "Svool")
        self.assertEqual(atbash("xyz"), "cba")
        self.assertEqual(atbash("Hello World"), "Svool Dliow")
        self.assertEqual(atbash(""), "")

    def test_atbash_involution(self):
        for s in ["hello", "Hello World", "abc", "xyz"]:
            self.assertEqual(atbash(atbash(s)), s)


class TestVigenere(unittest.TestCase):
    def test_vigenere_encrypt(self):
        result = vigenere_cipher("HELLO", "KEY")
        self.assertNotEqual(result, "HELLO")

    def test_vigenere_roundtrip(self):
        original = "HELLO WORLD"
        key = "KEY"
        encrypted = vigenere_cipher(original, key)
        decrypted = vigenere_cipher(encrypted, key, decrypt=True)
        self.assertEqual(decrypted, original)


class TestAffine(unittest.TestCase):
    def test_affine_roundtrip(self):
        original = "HELLO"
        a, b = 5, 8
        encrypted = affine_cipher(original, a, b)
        decrypted = affine_cipher(encrypted, a, b, decrypt=True)
        self.assertEqual(decrypted, original)


if __name__ == '__main__':
    unittest.main()
