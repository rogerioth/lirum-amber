import re


def extract_emails(s: str) -> list:
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}'
    return re.findall(pattern, s)


def extract_urls(s: str) -> list:
    pattern = r'https?://[^\s<>\"\')\]]+'
    return re.findall(pattern, s)


def extract_phone_numbers(s: str) -> list:
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}',
        r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b',
    ]
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, s))
    return list(dict.fromkeys(results))  # deduplicate preserving order


def extract_ip_addresses(s: str) -> list:
    ipv4 = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ipv6 = r'(?:::)?(?:[0-9a-fA-F]{1,4}:){1,7}[0-9a-fA-F]{1,4}'
    results = re.findall(ipv4, s)
    results.extend(re.findall(ipv6, s))
    return list(dict.fromkeys(results))


def extract_dates(s: str) -> list:
    patterns = [
        r'\b\d{4}[-/]\d{2}[-/]\d{2}\b',
        r'\b\d{2}[-/]\d{2}[-/]\d{4}\b',
    ]
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, s))
    return list(dict.fromkeys(results))


def extract_between_markers(s: str, start: str, end: str, include_markers: bool = False) -> list:
    if include_markers:
        pattern = re.escape(start) + r'(.*?)' + re.escape(end)
        return [start + m + end for m in re.findall(pattern, s, re.DOTALL)]
    else:
        pattern = re.escape(start) + r'(.*?)' + re.escape(end)
        return re.findall(pattern, s, re.DOTALL)


def extract_regex(s: str, pattern: str) -> list:
    return re.findall(pattern, s)


def extract_first_n(s: str, n: int) -> str:
    return s[:n]


def extract_last_n(s: str, n: int) -> str:
    return s[-n:] if len(s) >= n else s


def extract_by_line_range(s: str, start: int, end: int) -> str:
    lines = s.split('\n')
    return '\n'.join(lines[start-1:end])
