import hashlib
import binascii
import hmac as hmac_module
import zlib
from typing import Optional

# Try/except imports for external libraries
PYCRYPTODOME_AVAILABLE = False
MD2 = MD4 = SHA224 = SHA384 = SHA512 = None
SHA3_224 = SHA3_256 = SHA3_384 = SHA3_512 = None
Keccak_224 = Keccak_256 = Keccak_384 = Keccak_512 = None
Whirlpool = None
RIPEMD160 = None

# Try pycryptodomex (Cryptodome) first
try:
    from Cryptodome.Hash import MD2, MD4, SHA224, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512, Keccak_224, Keccak_256, Keccak_384, Keccak_512, Whirlpool, RIPEMD160
    from Cryptodome.Protocol.KDF import bcrypt, scrypt, argon2, PBKDF2
    PYCRYPTODOME_AVAILABLE = True
except ImportError:
    # Fall back to pycryptodome (Crypto)
    try:
        from Crypto.Hash import MD2, MD4, SHA224, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512, Keccak_224, Keccak_256, Keccak_384, Keccak_512, Whirlpool, RIPEMD160
        from Crypto.Protocol.KDF import bcrypt, scrypt, argon2, PBKDF2
        PYCRYPTODOME_AVAILABLE = True
    except ImportError:
        pass

try:
    import sha3 as sha3_module
    SHA3_PACKAGE_AVAILABLE = True
except ImportError:
    SHA3_PACKAGE_AVAILABLE = False

try:
    import blake3
    BLAKE3_AVAILABLE = True
except ImportError:
    BLAKE3_AVAILABLE = False

try:
    import tiger
    TIGER_AVAILABLE = True
except ImportError:
    TIGER_AVAILABLE = False

try:
    import mmh3
    MMH3_AVAILABLE = True
except ImportError:
    MMH3_AVAILABLE = False

try:
    import xxhash
    XXHASH_AVAILABLE = True
except ImportError:
    XXHASH_AVAILABLE = False

try:
    import bcrypt as bcrypt_module
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False


def hash_md5(s: str) -> str:
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def hash_sha1(s: str) -> str:
    return hashlib.sha1(s.encode('utf-8')).hexdigest()


def hash_sha256(s: str) -> str:
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def hash_sha512(s: str) -> str:
    return hashlib.sha512(s.encode('utf-8')).hexdigest()


def hash_crc32(s: str) -> str:
    return format(binascii.crc32(s.encode('utf-8')) & 0xffffffff, '08x')


def hash_adler32(s: str) -> str:
    return format(zlib.adler32(s.encode('utf-8')) & 0xffffffff, '08x')


def hash_hmac(s: str, key: str) -> str:
    return hmac_module.new(key.encode('utf-8'), s.encode('utf-8'), hashlib.sha256).hexdigest()


# New hash functions
def hash_md2(s: str) -> str:
    if not PYCRYPTODOME_AVAILABLE or MD2 is None:
        return "MD2 requires pycryptodome"
    return MD2.new(s.encode('utf-8')).hexdigest()


def hash_md4(s: str) -> str:
    if PYCRYPTODOME_AVAILABLE and MD4 is not None:
        return MD4.new(s.encode('utf-8')).hexdigest()
    try:
        return hashlib.md4(s.encode('utf-8')).hexdigest()
    except AttributeError:
        return "MD4 requires pycryptodome or hashlib.md4"


def hash_sha224(s: str) -> str:
    return hashlib.sha224(s.encode('utf-8')).hexdigest()


def hash_sha384(s: str) -> str:
    return hashlib.sha384(s.encode('utf-8')).hexdigest()


def hash_sha512_224(s: str) -> str:
    # SHA-512/224 is SHA-512 truncated to 224 bits (28 bytes)
    sha512_digest = hashlib.sha512(s.encode('utf-8')).digest()
    return sha512_digest[:28].hex()


def hash_sha512_256(s: str) -> str:
    # SHA-512/256 is SHA-512 truncated to 256 bits (32 bytes)
    sha512_digest = hashlib.sha512(s.encode('utf-8')).digest()
    return sha512_digest[:32].hex()


def hash_sha3_224(s: str) -> str:
    return hashlib.sha3_224(s.encode('utf-8')).hexdigest()


def hash_sha3_256(s: str) -> str:
    return hashlib.sha3_256(s.encode('utf-8')).hexdigest()


def hash_sha3_384(s: str) -> str:
    return hashlib.sha3_384(s.encode('utf-8')).hexdigest()


def hash_sha3_512(s: str) -> str:
    return hashlib.sha3_512(s.encode('utf-8')).hexdigest()


def hash_keccak_224(s: str) -> str:
    if PYCRYPTODOME_AVAILABLE and Keccak_224 is not None:
        return Keccak_224.new(s.encode('utf-8')).hexdigest()
    return "Keccak requires pycryptodome"


def hash_keccak_256(s: str) -> str:
    if PYCRYPTODOME_AVAILABLE and Keccak_256 is not None:
        return Keccak_256.new(s.encode('utf-8')).hexdigest()
    return "Keccak requires pycryptodome"


def hash_keccak_384(s: str) -> str:
    if PYCRYPTODOME_AVAILABLE and Keccak_384 is not None:
        return Keccak_384.new(s.encode('utf-8')).hexdigest()
    return "Keccak requires pycryptodome"


def hash_keccak_512(s: str) -> str:
    if PYCRYPTODOME_AVAILABLE and Keccak_512 is not None:
        return Keccak_512.new(s.encode('utf-8')).hexdigest()
    return "Keccak requires pycryptodome"


def hash_shake128(s: str, length: int = 32) -> str:
    return hashlib.shake_128(s.encode('utf-8')).hexdigest(length)


def hash_shake256(s: str, length: int = 32) -> str:
    return hashlib.shake_256(s.encode('utf-8')).hexdigest(length)


def hash_blake2b(s: str) -> str:
    return hashlib.blake2b(s.encode('utf-8')).hexdigest()


def hash_blake2s(s: str) -> str:
    return hashlib.blake2s(s.encode('utf-8')).hexdigest()


def hash_blake3(s: str) -> str:
    if not BLAKE3_AVAILABLE:
        return "blake3 required for BLAKE3"
    return blake3.blake3(s.encode('utf-8')).hexdigest()


def hash_ripemd160(s: str) -> str:
    if PYCRYPTODOME_AVAILABLE and RIPEMD160 is not None:
        return RIPEMD160.new(s.encode('utf-8')).hexdigest()
    return "RIPEMD-160 requires pycryptodome"


def hash_whirlpool(s: str) -> str:
    if PYCRYPTODOME_AVAILABLE and Whirlpool is not None:
        return Whirlpool.new(s.encode('utf-8')).hexdigest()
    return "Whirlpool requires pycryptodome"


def hash_tiger(s: str) -> str:
    if not TIGER_AVAILABLE:
        return "Tiger hash requires tiger package"
    return tiger.hash(s.encode('utf-8')).hex()


def hash_crc16(s: str) -> str:
    data = s.encode('utf-8')
    crc = 0xFFFF
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ 0x1021
            else:
                crc <<= 1
            crc &= 0xFFFF
    return format(crc, '04x')


def hash_fnv1a(s: str) -> str:
    data = s.encode('utf-8')
    fnv_offset_basis = 0xCBF29CE484222325
    fnv_prime = 0x100000001B3
    hash_val = fnv_offset_basis
    for byte in data:
        hash_val ^= byte
        hash_val = (hash_val * fnv_prime) & 0xFFFFFFFFFFFFFFFF
    return format(hash_val, '016x')


def hash_murmurhash(s: str) -> str:
    if not MMH3_AVAILABLE:
        return "mmh3 required for MurmurHash"
    return format(mmh3.hash(s, seed=0), '08x')


def hash_xxhash(s: str) -> str:
    if not XXHASH_AVAILABLE:
        return "xxhash required for xxHash"
    return xxhash.xxh64(s.encode('utf-8')).hexdigest()


def hash_hmac_md5(s: str, key: str = "secret") -> str:
    return hmac_module.new(key.encode('utf-8'), s.encode('utf-8'), hashlib.md5).hexdigest()


def hash_hmac_sha1(s: str, key: str = "secret") -> str:
    return hmac_module.new(key.encode('utf-8'), s.encode('utf-8'), hashlib.sha1).hexdigest()


def hash_hmac_sha256(s: str, key: str = "secret") -> str:
    return hmac_module.new(key.encode('utf-8'), s.encode('utf-8'), hashlib.sha256).hexdigest()


def hash_hmac_sha512(s: str, key: str = "secret") -> str:
    return hmac_module.new(key.encode('utf-8'), s.encode('utf-8'), hashlib.sha512).hexdigest()


def hash_bcrypt(s: str) -> str:
    return "Bcrypt requires password parameter"


def hash_scrypt(s: str) -> str:
    return "Scrypt requires password parameter"


def hash_argon2(s: str) -> str:
    return "Argon2 requires password parameter"


def hash_pbkdf2(s: str) -> str:
    return "PBKDF2 requires password parameter"
