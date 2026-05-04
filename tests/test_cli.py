"""Tests for CLI mode (non-interactive)."""

import os
import subprocess
import sys
import tempfile

import pytest

MAIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")


def run_cli(*args):
    result = subprocess.run(
        [sys.executable, MAIN, *args],
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result


def run_cli_pipe(input_text, *args):
    result = subprocess.run(
        [sys.executable, MAIN, *args],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=15,
    )
    return result


class TestCliBasicOps:

    def test_lowercase_by_display_name(self):
        r = run_cli("lowercase", "-t", "Hello World")
        assert r.returncode == 0
        assert r.stdout.strip() == "hello world"

    def test_uppercase_by_func_name(self):
        r = run_cli("to_uppercase", "-t", "Hello World")
        assert r.returncode == 0
        assert r.stdout.strip() == "HELLO WORLD"

    def test_sha256_display_name(self):
        r = run_cli("SHA-256 Hash", "-t", "hello")
        assert r.returncode == 0
        assert len(r.stdout.strip()) == 64

    def test_base64_encode_func_name(self):
        r = run_cli("base64_encode", "-t", "hello")
        assert r.returncode == 0
        assert "aGVsbG8=" in r.stdout


class TestCliExtraParams:

    def test_caesar_cipher_with_shift(self):
        r = run_cli("caesar_cipher_encode", "-t", "hello", "-p", "shift=7")
        assert r.returncode == 0
        assert r.stdout.strip() == "olssv"

    def test_truncate_with_width(self):
        r = run_cli("truncate", "-t", "hello world", "-p", "width=5")
        assert r.returncode == 0
        assert "he..." in r.stdout

    def test_center_align_with_width(self):
        r = run_cli("center_align", "-t", "hello", "-p", "width=11")
        assert r.returncode == 0
        result = r.stdout.strip("\n")
        assert len(result) == 11
        assert result == "   hello   "

    def test_pad_left_width_char(self):
        r = run_cli("pad_left", "-t", "42", "-p", "width=5", "-p", "char=0")
        assert r.returncode == 0
        assert r.stdout.strip() == "00042"

    def test_missing_required_param(self):
        r = run_cli("wrap_text", "-t", "some text to wrap")
        assert r.returncode != 0
        assert "TypeError" in r.stderr or "missing" in r.stderr


class TestCliGenerators:

    def test_generate_uuid(self):
        r = run_cli("generate_uuid")
        assert r.returncode == 0
        uuid_str = r.stdout.strip()
        assert len(uuid_str) == 36
        assert uuid_str.count("-") == 4

    def test_generate_password(self):
        r = run_cli("generate_password", "-p", "length=24")
        assert r.returncode == 0
        assert len(r.stdout.strip()) == 24

    def test_generate_lorem_ipsum(self):
        r = run_cli("generate_lorem_ipsum")
        assert r.returncode == 0
        assert len(r.stdout.strip()) > 20


class TestCliPipeInput:

    def test_pipe_stdin(self):
        r = run_cli_pipe("Hello World", "lowercase")
        assert r.returncode == 0
        assert r.stdout.strip() == "hello world"

    def test_pipe_with_sha256(self):
        r = run_cli_pipe("test", "sha256")
        assert r.returncode == 0
        assert len(r.stdout.strip()) == 64

    def test_pipe_reverse_words(self):
        r = run_cli_pipe("one two three", "reverse_words")
        assert r.returncode == 0
        assert r.stdout.strip() == "three two one"


class TestCliFileInput:

    def test_file_input(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("Hello File World")
            f.flush()
            filepath = f.name
        try:
            r = run_cli("lowercase", "-i", filepath)
            assert r.returncode == 0
            assert r.stdout.strip() == "hello file world"
        finally:
            os.unlink(filepath)


class TestCliErrors:

    def test_unknown_operation(self):
        r = run_cli("nonexistent_op", "-t", "test")
        assert r.returncode != 0
        assert "Unknown operation" in r.stderr

    def test_no_input_for_required_op(self):
        r = run_cli("reverse_string")
        assert r.returncode != 0
        assert "No input provided" in r.stderr

    def test_bad_kv_param(self):
        r = run_cli("truncate", "-t", "test", "-p", "badparam")
        assert r.returncode != 0
        assert "KEY=VALUE format" in r.stderr


class TestCliList:

    def test_list_shows_operations(self):
        r = run_cli("--list")
        assert r.returncode == 0
        assert "Case/Text Transform:" in r.stdout
        assert "to_lowercase" in r.stdout
        assert "Hash/Digest:" in r.stdout


class TestCliWithSpaces:

    def test_operation_name_with_spaces(self):
        r = run_cli("Caesar Cipher Encode", "-t", "abc", "-p", "shift=3")
        assert r.returncode == 0
        assert r.stdout.strip().lower() == "def"

    def test_display_name_full_match(self):
        r = run_cli("Sort Lines by Length", "-t", "aaa\nb\ncc")
        assert r.returncode == 0
        lines = r.stdout.strip().split("\n")
        assert lines[0] == "b"
        assert lines[1] == "cc"
        assert lines[2] == "aaa"
