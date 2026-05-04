"""String manipulation operations."""

def split_by_comma(s: str) -> str:
    """Split string by comma, one item per line."""
    if not s:
        return ''
    return '\n'.join(s.split(','))


def split_by_space(s: str) -> str:
    """Split string by whitespace, one item per line."""
    if not s:
        return ''
    return '\n'.join(s.split())


def split_by_newline(s: str) -> str:
    """Ensure string is split by newline."""
    return s


def join_by_comma(s: str) -> str:
    """Join lines by comma."""
    if not s:
        return ''
    lines = [line for line in s.split('\n') if line]
    return ','.join(lines)


def join_by_space(s: str) -> str:
    """Join lines by space."""
    if not s:
        return ''
    lines = [line for line in s.split('\n') if line]
    return ' '.join(lines)


def chunk_text(s: str, size: int = 100) -> str:
    """Split text into chunks of specified size."""
    if not s:
        return ''
    chunks = []
    for i in range(0, len(s), size):
        chunks.append(s[i:i+size])
    return '\n'.join(chunks)


def add_prefix_lines(s: str, prefix: str = "# ") -> str:
    """Add prefix to each line."""
    if not s:
        return ''
    lines = s.split('\n')
    return '\n'.join(prefix + line for line in lines)


def add_suffix_lines(s: str, suffix: str = "...") -> str:
    """Add suffix to each line."""
    if not s:
        return ''
    lines = s.split('\n')
    return '\n'.join(line + suffix for line in lines)


def string_to_ascii_array(s: str) -> str:
    """Convert string to comma-separated ASCII codes."""
    if not s:
        return ''
    return ','.join(str(ord(c)) for c in s)


def ascii_array_to_string(s: str) -> str:
    """Convert comma-separated ASCII codes to string."""
    if not s:
        return ''
    try:
        codes = [int(c.strip()) for c in s.split(',') if c.strip()]
        return ''.join(chr(c) for c in codes)
    except:
        return ''
