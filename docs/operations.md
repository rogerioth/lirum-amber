# Operations & Categories

## Overview

The project provides 200+ string operations organized into 12 categories. Each operation is a pure function that takes a string (and optionally parameters) and returns a transformed string.

## Category Map

```mermaid
graph TD
    Ops["200+ Operations"] --> C1["Case/Text Transform (16 ops)"]
    Ops --> C2["Rearrange (13 ops)"]
    Ops --> C3["Format (21 ops)"]
    Ops --> C4["Encode/Decode (29 ops)"]
    Ops --> C5["Ciphers (4 ops)"]
    Ops --> C6["Hash/Digest (33 ops)"]
    Ops --> C7["Key Derivation (8 ops)"]
    Ops --> C8["Escape/Unescape (15 ops)"]
    Ops --> C9["JSON/Format (11 ops)"]
    Ops --> C10["Statistics (24 ops)"]
    Ops --> C11["Extract (13 ops)"]
    Ops --> C12["Manipulate (11 ops)"]
    Ops --> C13["Generate (12 ops)"]
```

## Operation Registry

Operations are registered in `operations_mapping.py`:

```python
OPERATIONS = {
    "Category Name": [
        ("Display Name", "function_name"),
        ...
    ],
    ...
}
```

The TUI uses two data structures built from this registry:
- `_operations`: `{category: [(display_name, func_name), ...]}` — for populating the operations table
- `_operation_map`: `{display_name: func_name}` — for dispatching operations by name

## Module-to-Operation Mapping

```mermaid
graph LR
    subgraph "transform.py (21 ops)"
        T1[to_uppercase]
        T2[to_lowercase]
        T3[to_title_case]
        T4[to_camel_case]
        T5[to_pascal_case]
        T6[to_snake_case]
        T7[to_kebab_case]
        T8[to_constant_case]
        T9[to_dot_case]
        T10[to_path_case]
        T11[to_sentence_case]
        T12[swap_case]
        T13[to_alternating_case]
        T14[to_sponge_case]
        T15[capitalize_first_letter]
        T16[decapitalize_first_letter]
        T17[reverse_string]
        T18[reverse_words]
        T19[reverse_lines]
        T20[rotate_chars]
        T21[repeat_string]
    end

    subgraph "encode.py (25 ops)"
        E1[base64_encode/decode]
        E2[base64url_encode/decode]
        E3[base32_encode/decode]
        E4[base58_encode/decode]
        E5[base85_encode/decode]
        E6[punycode_encode/decode]
        E7[quoted_printable_encode/decode]
        E8[url_encode/decode]
        E9[html_encode/decode]
        E10[hex_encode/decode]
        E11[binary_encode/decode]
        E12[octal_encode/decode]
        E13[rot13/rot47]
        E14[atbash/caesar_*]
        E15[unicode_escape/unescape]
    end

    subgraph "hash_ops.py (41 ops)"
        H1[hash_md2/md4/md5]
        H2[hash_sha1/sha224/sha256/sha384/sha512]
        H3[hash_sha3_*]
        H4[hash_keccak_*]
        H5[hash_shake128/256]
        H6[hash_blake2b/blake2s/blake3]
        H7[hash_ripemd160/whirlpool/tiger]
        H8[hash_crc16/crc32/adler32]
        H9[hash_fnv1a/murmurhash/xxhash]
        H10[hash_hmac_md5/sha1/sha256/sha512]
        H11[hash_bcrypt/scrypt/argon2/pbkdf2]
    end

    subgraph "statistics.py (24 ops)"
        S1[count_characters/words/lines/bytes]
        S2[count_vowels/consonants]
        S3[char/word_frequency]
        S4[shannon_entropy]
        S5[is_palindrome/is_anagram]
        S6[levenshtein/jaro_winkler/hamming]
        S7[soundex/metaphone/double_metaphone]
        S8[longest/shortest/most_frequent]
        S9[readability_score]
    end

    subgraph "format_ops.py (35 ops)"
        F1[trim/trim_left/trim_right]
        F2[collapse_whitespace/remove_*]
        F3[pad_left/right/center/left/right_align]
        F4[justify/wrap/spaces_to_tabs/expand_tabs]
        F5[normalize_newlines_*]
        F6[slugify/truncate]
        F7[add_line_numbers/remove_line_numbers]
        F8[extract_lines/repeat_lines]
        F9[deduplicate_lines/sort_lines]
        F10[indent/unindent]
    end

    subgraph "misc.py (12 ops)"
        M1[diff_texts]
        M2[generate_uuid/ulid/nanoid/password/lorem_ipsum/sequence]
        M3[generate_zalgo/leetspeak/upside_down/vaporwave/braille]
        M4[pig_latin/affine_cipher/unslugify]
    end

    subgraph "rearrange.py (10 ops)"
        R1[shuffle_characters/words/lines]
        R2[sort_characters/words/lines_asc/desc]
        R3[sort_lines_by_length]
    end

    subgraph "escape.py (15 ops)"
        ES1[json/xml/csv/sql/regex_escape/unescape]
        ES2[c/java/python_string_escape/unescape]
        ES3[bash_escape]
    end

    subgraph "manipulate.py (10 ops)"
        MA1[split_by_comma/space/newline]
        MA2[join_by_comma/space]
        MA3[chunk_text]
        MA4[add_prefix_lines/suffix_lines]
        MA5[string_to_ascii_array/ascii_array_to_string]
    end

    subgraph "extract.py (20 ops)"
        EX1[extract_emails/urls/dates/phone_numbers]
        EX2[extract_ipv4/ipv6/mac/numbers/domains]
        EX3[extract_hashtags/mentions/regex/between_markers]
        EX4[extract_first_n/last_n/by_line_range]
        EX5[strip_html/markdown/punctuation/ansi]
    end

    subgraph "json_ops.py (11 ops)"
        J1[json_pretty_print/minify/escape/unescape]
        J2[json_to_string/string_to_json]
        J3[json_diff/json_path_extract]
        J4[xml/sql/css_pretty_print/minify]
        J5[parse_query_string/stringify_query_string]
        J6[jwt_decode]
    end

    subgraph "find_replace.py (6 ops)"
        FR1[find_and_replace/find_and_replace_all]
        FR2[regex_find/regex_replace]
        FR3[count_matches/extract_regex_groups]
    end

    subgraph "ciphers.py (4 ops)"
        CI1[vigenere_cipher_encode/decode]
        CI2[morse_encode/decode]
    end
```

## Operation Function Signature

All operations follow a common pattern:

```python
def operation_name(input_text: str, **kwargs) -> str:
    """Description of what the operation does."""
    # ... implementation ...
    return result
```

Operations that need additional parameters (like `find_and_replace`, `rotate_chars`, `repeat_string`) show a modal dialog (via `OperationModal`) when selected, since they can't execute with just the input string.

## Error Handling

```mermaid
graph TD
    Run[_run_operation] --> Exists{func exists in module?}
    Exists -->|No| Null[Return None]
    Exists -->|Yes| Call["Call func(input_text)"]
    Call --> TypeError{TypeError?}
    TypeError -->|Yes| ParamErr["Return 'Error: requires additional parameters'"]
    TypeError -->|No| OtherErr{Other Exception?}
    OtherErr -->|Yes| OpErr["Return 'Error executing operation: ...'"]
    OtherErr -->|No| Success[Return result string]
```

## Categories Detail

| # | Category | Module(s) | Count |
|---|----------|-----------|-------|
| 1 | Case/Text Transform | `transform.py` | 16 |
| 2 | Rearrange | `rearrange.py`, `transform.py` | 13 |
| 3 | Format | `format_ops.py` | 21 |
| 4 | Encode/Decode | `encode.py` | 29 |
| 5 | Ciphers | `ciphers.py` | 4 |
| 6 | Hash/Digest | `hash_ops.py` | 33 |
| 7 | Key Derivation | `hash_ops.py` | 8 |
| 8 | Escape/Unescape | `escape.py`, `encode.py` | 15 |
| 9 | JSON/Format | `json_ops.py` | 11 |
| 10 | Statistics | `statistics.py` | 24 |
| 11 | Extract | `extract.py` | 13 |
| 12 | Manipulate | `manipulate.py` | 11 |
| 13 | Generate | `misc.py` | 12 |
