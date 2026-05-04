import unicodedata


def to_uppercase(s: str) -> str:
    return s.upper()


def to_lowercase(s: str) -> str:
    return s.lower()


def to_title_case(s: str, keep_spaces: bool = False) -> str:
    if not keep_spaces:
        return s.title()
    # Title case that preserves leading/trailing spaces
    stripped = s.strip()
    result = stripped.title()
    return s[:len(s) - len(stripped)] + result + s[len(stripped):] if s != stripped else result


def to_sentence_case(s: str) -> str:
    if not s:
        return ""
    # Capitalize first letter of each sentence
    import re
    # First handle ... as a single unit
    s_temp = s.replace('...', '\x00DOTTED\x00')
    # Split on sentence terminators (.!?) followed by whitespace or end
    parts = re.split(r'(?<=[.!?])(?=\s|$)', s_temp)
    result = []
    for part in parts:
        if not part:
            continue
        stripped = part.lstrip()
        leading = part[:len(part) - len(stripped)]
        if stripped:
            new_stripped = list(stripped)
            new_stripped[0] = stripped[0].upper()
            result.append(leading + ''.join(new_stripped))
        else:
            result.append(part)
    output = ''.join(result)
    # Restore ...
    output = output.replace('\x00DOTTED\x00', '...')
    # If no sentence terminators found, lowercase everything then capitalize first letter
    if not any(c in '.!?' for c in s):
        output = output.lower()
        chars = [c for c in output if c != ' ']
        if chars:
            first_idx = output.index(chars[0])
            new_output = list(output)
            new_output[first_idx] = chars[0].upper()
            output = ''.join(new_output)
    return output


def swap_case(s: str) -> str:
    return s.swapcase()


def _split_words(s: str):
    """Split string into words and separators using regex-like logic."""
    import re
    return re.findall(r'[a-zA-Z0-9]+|[^a-zA-Z0-9]+', s)


def to_camel_case(s: str) -> str:
    words = _split_words(s)
    words = [w for w in words if w.isalnum()]
    if not words:
        return ""
    result = words[0].lower()
    for w in words[1:]:
        result += w.capitalize()
    return result


def to_pascal_case(s: str) -> str:
    words = _split_words(s)
    words = [w for w in words if w.isalnum()]
    if not words:
        return ""
    return ''.join(w.capitalize() for w in words)


def to_snake_case(s: str) -> str:
    # Insert underscore before uppercase letters that follow lowercase
    import re
    s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    s1 = re.sub(r'([A-Z])([A-Z])(?=[a-z])', r'\1_\2', s1)
    s1 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s1)
    s1 = re.sub(r'([a-zA-Z])([0-9])', r'\1_\2', s1)
    s1 = re.sub(r'([0-9])([a-zA-Z])', r'\1_\2', s1)
    s1 = re.sub(r'[-\s]+', '_', s1)
    return s1.lower()


def to_kebab_case(s: str) -> str:
    import re
    s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', s)
    s1 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', s1)
    s1 = re.sub(r'[-_\s]+', '-', s1)
    return s1.lower()


def to_constant_case(s: str) -> str:
    import re
    s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    s1 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s1)
    s1 = re.sub(r'[-\s]+', '_', s1)
    return s1.upper()


def reverse_string(s: str) -> str:
    return s[::-1]


def reverse_words(s: str) -> str:
    # Split preserving internal whitespace
    import re
    parts = re.split(r'(\s+)', s)
    words = [p for p in parts if p and not p.isspace()]
    separators = [p for p in parts if p and p.isspace()]
    if not words:
        return s
    reversed_words = words[::-1]
    # Reconstruct: word, sep1, word, sep2, ...
    result = []
    wi = 0
    for p in parts:
        if p and not p.isspace():
            result.append(reversed_words[wi])
            wi += 1
        else:
            result.append(p)
    return ''.join(result)


def reverse_lines(s: str) -> str:
    if not s:
        return ""
    lines = s.split('\n')
    # Preserve trailing newline if present
    trailing = ''
    if s.endswith('\n'):
        trailing = '\n'
        lines = lines[:-1]
    result = '\n'.join(lines[::-1])
    return result + trailing if trailing else result


def rotate_chars(s: str, n: int) -> str:
    if not s:
        return ""
    n = n % len(s)
    if n == 0:
        return s
    return s[n:] + s[:n]


def repeat_string(s: str, n: int) -> str:
    return s * n
