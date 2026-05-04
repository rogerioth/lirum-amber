import unittest
import hashlib
from string_ops.hash_ops import (
    hash_md5,
    hash_sha1,
    hash_sha256,
    hash_sha512,
    hash_crc32,
    hash_hmac,
    hash_md2,
    hash_md4,
    hash_sha224,
    hash_sha384,
    hash_sha512_224,
    hash_sha512_256,
    hash_sha3_224,
    hash_sha3_256,
    hash_sha3_384,
    hash_sha3_512,
    hash_keccak_224,
    hash_keccak_256,
    hash_keccak_384,
    hash_keccak_512,
    hash_shake128,
    hash_shake256,
    hash_blake2b,
    hash_blake2s,
    hash_blake3,
    hash_ripemd160,
    hash_whirlpool,
    hash_tiger,
    hash_crc16,
    hash_fnv1a,
    hash_murmurhash,
    hash_xxhash,
    hash_hmac_md5,
    hash_hmac_sha1,
    hash_hmac_sha256,
    hash_hmac_sha512,
    hash_bcrypt,
    hash_scrypt,
    hash_argon2,
    hash_pbkdf2,
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

    # New hash function tests
    def test_hash_md2(self):
        result = hash_md2("hello")
        self.assertIsInstance(result, str)
        if "requires" not in result:
            self.assertEqual(len(result), 32)  # MD2 hex digest is 32 chars

    def test_hash_md4(self):
        result = hash_md4("hello")
        self.assertIsInstance(result, str)
        if "requires" not in result:
            self.assertEqual(len(result), 32)  # MD4 hex digest is 32 chars

    def test_hash_sha224(self):
        self.assertEqual(hash_sha224(""), hashlib.sha224(b"").hexdigest())
        self.assertEqual(hash_sha224("hello"), hashlib.sha224(b"hello").hexdigest())

    def test_hash_sha384(self):
        self.assertEqual(hash_sha384(""), hashlib.sha384(b"").hexdigest())
        self.assertEqual(hash_sha384("hello"), hashlib.sha384(b"hello").hexdigest())

    def test_hash_sha512_224(self):
        # SHA-512/224 is SHA-512 truncated to 28 bytes
        expected = hashlib.sha512(b"").digest()[:28].hex()
        self.assertEqual(hash_sha512_224(""), expected)
        expected_hello = hashlib.sha512(b"hello").digest()[:28].hex()
        self.assertEqual(hash_sha512_224("hello"), expected_hello)

    def test_hash_sha512_256(self):
        # SHA-512/256 is SHA-512 truncated to 32 bytes
        expected = hashlib.sha512(b"").digest()[:32].hex()
        self.assertEqual(hash_sha512_256(""), expected)
        expected_hello = hashlib.sha512(b"hello").digest()[:32].hex()
        self.assertEqual(hash_sha512_256("hello"), expected_hello)

    def test_hash_sha3_224(self):
        self.assertEqual(hash_sha3_224(""), hashlib.sha3_224(b"").hexdigest())
        self.assertEqual(hash_sha3_224("hello"), hashlib.sha3_224(b"hello").hexdigest())

    def test_hash_sha3_256(self):
        self.assertEqual(hash_sha3_256(""), hashlib.sha3_256(b"").hexdigest())
        self.assertEqual(hash_sha3_256("hello"), hashlib.sha3_256(b"hello").hexdigest())

    def test_hash_sha3_384(self):
        self.assertEqual(hash_sha3_384(""), hashlib.sha3_384(b"").hexdigest())
        self.assertEqual(hash_sha3_384("hello"), hashlib.sha3_384(b"hello").hexdigest())

    def test_hash_sha3_512(self):
        self.assertEqual(hash_sha3_512(""), hashlib.sha3_512(b"").hexdigest())
        self.assertEqual(hash_sha3_512("hello"), hashlib.sha3_512(b"hello").hexdigest())

    def test_hash_keccak_224(self):
        result = hash_keccak_224("hello")
        self.assertIsInstance(result, str)
        if "requires" not in result:
            self.assertEqual(len(result), 56)  # 224 bits = 28 bytes = 56 hex chars

    def test_hash_keccak_256(self):
        result = hash_keccak_256("hello")
        self.assertIsInstance(result, str)
        if "requires" not in result:
            self.assertEqual(len(result), 64)  # 256 bits = 32 bytes = 64 hex chars

    def test_hash_keccak_384(self):
        result = hash_keccak_384("hello")
        self.assertIsInstance(result, str)
        if "requires" not in result:
            self.assertEqual(len(result), 96)  # 384 bits = 48 bytes = 96 hex chars

    def test_hash_keccak_512(self):
        result = hash_keccak_512("hello")
        self.assertIsInstance(result, str)
        if "requires" not in result:
            self.assertEqual(len(result), 128)  # 512 bits = 64 bytes = 128 hex chars

    def test_hash_shake128(self):
        result = hash_shake128("hello")
        self.assertEqual(len(result), 64)  # 32 bytes * 2
        self.assertEqual(result, hashlib.shake_128(b"hello").hexdigest(32))
        # Test custom length
        result_16 = hash_shake128("hello", 16)
        self.assertEqual(len(result_16), 32)  # 16 bytes * 2

    def test_hash_shake256(self):
        result = hash_shake256("hello")
        self.assertEqual(len(result), 64)  # 32 bytes * 2
        self.assertEqual(result, hashlib.shake_256(b"hello").hexdigest(32))
        # Test custom length
        result_16 = hash_shake256("hello", 16)
        self.assertEqual(len(result_16), 32)  # 16 bytes * 2

    def test_hash_blake2b(self):
        self.assertEqual(hash_blake2b(""), hashlib.blake2b(b"").hexdigest())
        self.assertEqual(hash_blake2b("hello"), hashlib.blake2b(b"hello").hexdigest())

    def test_hash_blake2s(self):
        self.assertEqual(hash_blake2s(""), hashlib.blake2s(b"").hexdigest())
        self.assertEqual(hash_blake2s("hello"), hashlib.blake2s(b"hello").hexdigest())

    def test_hash_blake3(self):
        result = hash_blake3("hello")
        self.assertIsInstance(result, str)
        if "required" not in result:
            self.assertEqual(len(result), 64)  # BLAKE3 default 32 bytes = 64 hex chars

    def test_hash_ripemd160(self):
        result = hash_ripemd160("hello")
        self.assertIsInstance(result, str)
        if "requires" not in result:
            self.assertEqual(len(result), 40)  # 160 bits = 20 bytes = 40 hex chars

    def test_hash_whirlpool(self):
        result = hash_whirlpool("hello")
        self.assertIsInstance(result, str)
        if "requires" not in result:
            self.assertEqual(len(result), 128)  # Whirlpool is 512 bits = 128 hex chars

    def test_hash_tiger(self):
        # Tiger hash test (if library available)
        result = hash_tiger("hello")
        self.assertIsInstance(result, str)

    def test_hash_crc16(self):
        result = hash_crc16("hello")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 4)  # CRC16 is 2 bytes = 4 hex chars

    def test_hash_fnv1a(self):
        result = hash_fnv1a("hello")
        self.assertIsInstance(result, str)

    def test_hash_murmurhash(self):
        result = hash_murmurhash("hello")
        self.assertIsInstance(result, str)

    def test_hash_xxhash(self):
        result = hash_xxhash("hello")
        self.assertIsInstance(result, str)
        if "required" not in result:
            self.assertEqual(len(result), 16)  # xxHash64 default is 8 bytes = 16 hex chars

    def test_hash_hmac_md5(self):
        result = hash_hmac_md5("hello")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 32)  # MD5 HMAC is 16 bytes = 32 hex chars
        # Test custom key
        result_key = hash_hmac_md5("hello", "custom_key")
        self.assertNotEqual(result, result_key)

    def test_hash_hmac_sha1(self):
        result = hash_hmac_sha1("hello")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 40)  # SHA1 HMAC is 20 bytes = 40 hex chars

    def test_hash_hmac_sha256(self):
        result = hash_hmac_sha256("hello")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 64)  # SHA256 HMAC is 32 bytes = 64 hex chars

    def test_hash_hmac_sha512(self):
        result = hash_hmac_sha512("hello")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 128)  # SHA512 HMAC is 64 bytes = 128 hex chars

    def test_hash_bcrypt(self):
        self.assertEqual(hash_bcrypt("test"), "Bcrypt requires password parameter")

    def test_hash_scrypt(self):
        self.assertEqual(hash_scrypt("test"), "Scrypt requires password parameter")

    def test_hash_argon2(self):
        self.assertEqual(hash_argon2("test"), "Argon2 requires password parameter")

    def test_hash_pbkdf2(self):
        self.assertEqual(hash_pbkdf2("test"), "PBKDF2 requires password parameter")


if __name__ == '__main__':
    unittest.main()
