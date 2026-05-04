import hashlib
import binascii
import hmac as hmac_module


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


def hash_hmac(s: str, key: str) -> str:
    return hmac_module.new(key.encode('utf-8'), s.encode('utf-8'), hashlib.sha256).hexdigest()
