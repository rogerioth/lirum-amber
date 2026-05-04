import re
import unicodedata


def trim(s: str) -> str:
    return s.strip()


def trim_left(s: str) -> str:
    return s.lstrip()


def trim_right(s: str) -> str:
    return s.rstrip()


def trim_newlines(s: str) -> str:
    return s.strip('\n\r')


def collapse_whitespace(s: str, preserve_breaks: bool = False) -> str:
    if preserve_breaks:
        s = re.sub(r'[^\S\n]+', ' ', s)
        return s.strip()
    return re.sub(r'\s+', ' ', s).strip()


def remove_empty_lines(s: str) -> str:
    return '\n'.join(line for line in s.split('\n') if line.strip())


def remove_duplicate_lines(s: str) -> str:
    seen = set()
    result = []
    for line in s.split('\n'):
        if line not in seen:
            seen.add(line)
            result.append(line)
    return '\n'.join(result)


def sort_lines(s: str, case_insensitive: bool = False) -> str:
    lines = s.split('\n')
    lines.sort(key=lambda x: x.lower() if case_insensitive else x)
    return '\n'.join(lines)


def deduplicate_lines(s: str) -> str:
    if not s:
        return ""
    lines = s.split('\n')
    if not lines:
        return ""
    result = [lines[0]]
    for line in lines[1:]:
        if line != result[-1]:
            result.append(line)
    return '\n'.join(result)


def indent_text(s: str, n: int) -> str:
    if not s:
        return ""
    indent = ' ' * n
    return '\n'.join(indent + line for line in s.split('\n'))


def unindent_text(s: str, n: int) -> str:
    lines = s.split('\n')
    result = []
    for line in lines:
        stripped = line[:n] if len(line) >= n else line
        if stripped == ' ' * min(n, len(line)):
            result.append(line[n:])
        else:
            result.append(line)
    return '\n'.join(result)


def wrap_text(s: str, width: int, preserve_breaks: bool = False) -> str:
    if preserve_breaks:
        paragraphs = s.split('\n\n')
        wrapped = []
        for para in paragraphs:
            lines = para.split('\n')
            wrapped_lines = []
            for line in lines:
                while len(line) > width:
                    # Find last space within width
                    split_at = line.rfind(' ', 0, width)
                    if split_at == -1:
                        split_at = width
                    wrapped_lines.append(line[:split_at])
                    line = line[split_at:].lstrip()
                if line:
                    wrapped_lines.append(line)
            wrapped.append('\n'.join(wrapped_lines))
        return '\n\n'.join(wrapped)

    words = s.split()
    if not words:
        return ""
    lines = []
    current_line = []
    for word in words:
        if len(current_line) == 0:
            current_line.append(word)
        elif len(' '.join(current_line) + ' ' + word) > width:
            lines.append(' '.join(current_line))
            current_line = [word]
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))
    return '\n'.join(lines)


def replace_line_endings(s: str, target: str = 'lf') -> str:
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    if target == 'crlf':
        return s.replace('\n', '\r\n')
    elif target == 'cr':
        return s.replace('\n', '\r')
    return s  # lf (default)


def normalize_unicode(s: str, form: str = 'nfc') -> str:
    return unicodedata.normalize(form, s)


def strip_non_ascii(s: str) -> str:
    return s.encode('ascii', 'ignore').decode('ascii')


def remove_diacritics(s: str) -> str:
    nfkd = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in nfkd if not unicodedata.combining(c))


def slugify(s: str) -> str:
    s = remove_diacritics(s.lower())
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-')
    return s


def truncate(s: str, width: int, suffix: str = '...') -> str:
    if len(s) <= width:
        return s
    if not suffix:
        suffix = '...'
    return s[:width - len(suffix)] + suffix


def pad_left(s: str, width: int, char: str = ' ') -> str:
    return s.rjust(width, char)


def pad_right(s: str, width: int, char: str = ' ') -> str:
    return s.ljust(width, char)


def add_line_numbers(s: str, start: int = 1, width: int = 4) -> str:
    lines = s.split('\n')
    fmt = f'{{:>{width}}}: '
    return '\n'.join(fmt.format(i) + line for i, line in enumerate(lines, start))


def remove_line_numbers(s: str, width: int = 4) -> str:
    lines = s.split('\n')
    pattern = re.compile(r'^\s*\d{1,' + str(width) + r'}:\s')
    return '\n'.join(pattern.sub('', line) for line in lines)


def extract_lines(s: str, start: int, end: int) -> str:
    lines = s.split('\n')
    return '\n'.join(lines[start-1:end])


def repeat_lines(s: str, n: int) -> str:
    lines = s.split('\n')
    result = []
    for line in lines:
        result.extend([line] * n)
    return '\n'.join(result)


def center_align(s: str, width: int = 80) -> str:
    return s.center(width)


def left_align(s: str, width: int = 80) -> str:
    return s.ljust(width)


def right_align(s: str, width: int = 80) -> str:
    return s.rjust(width)


def justify(s: str, width: int = 80) -> str:
    words = s.split()
    if len(words) <= 1:
        return s.ljust(width) if len(s) < width else s
    lines = []
    current_line = [words[0]]
    for word in words[1:]:
        # Calculate length of current line + space + new word
        line_len = len(' '.join(current_line)) + 1 + len(word)
        if line_len <= width:
            current_line.append(word)
        else:
            lines.append(current_line)
            current_line = [word]
    if current_line:
        lines.append(current_line)
    justified = []
    for i, line in enumerate(lines):
        if i == len(lines) - 1 or len(line) == 1:
            justified.append(' '.join(line).ljust(width) if len(' '.join(line)) < width else ' '.join(line))
            continue
        total_spaces = width - sum(len(w) for w in line)
        gaps = len(line) - 1
        base_spaces = total_spaces // gaps
        extra = total_spaces % gaps
        result = line[0]
        for j in range(gaps):
            spaces = base_spaces + (1 if j < extra else 0)
            result += ' ' * spaces + line[j + 1]
        justified.append(result)
    return '\n'.join(justified)


def remove_all_whitespace(s: str) -> str:
    return re.sub(r'\s+', '', s)


def remove_duplicate_words(s: str) -> str:
    words = s.split()
    seen = set()
    result = []
    for word in words:
        if word not in seen:
            seen.add(word)
            result.append(word)
    return ' '.join(result)


def spaces_to_tabs(s: str, tab_width: int = 4) -> str:
    lines = s.split('\n')
    result = []
    for line in lines:
        # Replace leading spaces with tabs
        num_spaces = len(line) - len(line.lstrip(' '))
        tabs = num_spaces // tab_width
        remaining = num_spaces % tab_width
        result.append('\t' * tabs + ' ' * remaining + line.lstrip(' '))
    return '\n'.join(result)


def tabs_to_spaces(s: str, tab_width: int = 4) -> str:
    return s.expandtabs(tab_width)


def expand_tabs(s: str, tab_width: int = 4) -> str:
    return tabs_to_spaces(s, tab_width)


def normalize_newlines_crlf_lf(s: str) -> str:
    return s.replace('\r\n', '\n')


def normalize_newlines_lf_crlf(s: str) -> str:
    return s.replace('\n', '\r\n')


def normalize_newlines_cr_lf(s: str) -> str:
    return s.replace('\r', '\n')
