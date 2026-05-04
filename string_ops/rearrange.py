"""String rearrange operations - shuffle and sort functions."""

import random


def shuffle_characters(s: str) -> str:
    random.seed(42)
    chars = list(s)
    random.shuffle(chars)
    return ''.join(chars)


def shuffle_words(s: str) -> str:
    random.seed(42)
    words = s.split()
    random.shuffle(words)
    return ' '.join(words)


def shuffle_lines(s: str) -> str:
    random.seed(42)
    ends_with_newline = s.endswith('\n')
    if ends_with_newline:
        s = s[:-1]
    lines = s.split('\n')
    random.shuffle(lines)
    result = '\n'.join(lines)
    if ends_with_newline:
        result += '\n'
    return result


def sort_characters_asc(s: str) -> str:
    return ''.join(sorted(s))


def sort_characters_desc(s: str) -> str:
    return ''.join(sorted(s, reverse=True))


def sort_words_asc(s: str) -> str:
    words = s.split()
    return ' '.join(sorted(words))


def sort_words_desc(s: str) -> str:
    words = s.split()
    return ' '.join(sorted(words, reverse=True))


def sort_lines_asc(s: str) -> str:
    ends_with_newline = s.endswith('\n')
    if ends_with_newline:
        s = s[:-1]
    lines = s.split('\n')
    result = '\n'.join(sorted(lines))
    if ends_with_newline:
        result += '\n'
    return result


def sort_lines_desc(s: str) -> str:
    ends_with_newline = s.endswith('\n')
    if ends_with_newline:
        s = s[:-1]
    lines = s.split('\n')
    result = '\n'.join(sorted(lines, reverse=True))
    if ends_with_newline:
        result += '\n'
    return result


def sort_lines_by_length(s: str) -> str:
    ends_with_newline = s.endswith('\n')
    if ends_with_newline:
        s = s[:-1]
    lines = s.split('\n')
    result = '\n'.join(sorted(lines, key=len))
    if ends_with_newline:
        result += '\n'
    return result
