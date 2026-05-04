import unittest
import hashlib
from string_ops.hash_ops import (
    hash_md5,
    hash_sha1,
    hash_sha256,
    hash_sha512,
    hash_crc32,
    hash_hmac,
)


class TestHash(unittest.TestCase):
    def test_hash_md5(self):
        self.assertEqual(hash_md5(""), "d41d8cd98f00b204e9800998ecf8427e")
        self.assertEqual(hash_md5("hello"), "5d41402abc4b2a76b9719d911017c592")
        self.assertEqual(hash_md5("hello world"), "5eb63bbbe01eeed093cb22bb8f5acdc3")

    def test_hash_sha256(self):
        self.assertEqual(hash_sha256(""), "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
        self.assertEqual(hash_sha256("hello"), "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824")

    def test_hash_sha512(self):
        result = hash_sha512("hello")
        self.assertEqual(len(result), 128)

    def test_hash_crc32(self):
        result = hash_crc32("hello")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 8)

    def test_hash_hmac(self):
        result = hash_hmac("hello", "secret")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, hash_md5("hello"))

    def test_hash_deterministic(self):
        for hash_fn in [hash_md5, hash_sha1, hash_sha256, hash_sha512]:
            self.assertEqual(hash_fn("test"), hash_fn("test"))

    def test_hash_sha1(self):
        result = hash_sha1("hello")
        self.assertEqual(len(result), 40)
        self.assertEqual(result, hashlib.sha1(b"hello").hexdigest())


if __name__ == '__main__':
    unittest.main()
