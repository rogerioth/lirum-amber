import re


def extract_emails(s: str) -> str:
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{1,}'
    return '\n'.join(re.findall(pattern, s))


def extract_urls(s: str) -> str:
    pattern = r'https?://[^\s<>"\')\]]+'
    return '\n'.join(re.findall(pattern, s))


def extract_phone_numbers(s: str) -> str:
    patterns = [
        r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4}',
        r'\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b',
    ]
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, s))
    return '\n'.join(dict.fromkeys(results))  # deduplicate preserving order


def extract_ip_addresses(s: str) -> str:
    import ipaddress
    ipv4 = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    # Use ipaddress module to validate IPv6 addresses
    results = re.findall(ipv4, s)
    # Find potential IPv6 addresses and validate them
    ipv6_pattern = r'\b[0-9a-fA-F:]{2,}\b'
    for match in re.finditer(ipv6_pattern, s):
        try:
            addr = ipaddress.IPv6Address(match.group(0))
            results.append(str(addr))
        except:
            pass
    return '\n'.join(dict.fromkeys(results))


def extract_domains(s: str) -> str:
    """Extract domain names from URLs."""
    urls = re.findall(r'https?://[^\s<>"\')\]]+', s)
    domains = []
    for url in urls:
        match = re.search(r'://([^/]+)', url)
        if match:
            domains.append(match.group(1))
        elif re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', url):
            domains.append(url)
    return '\n'.join(dict.fromkeys(domains))


def extract_ipv6(s: str) -> str:
    """Extract IPv6 addresses."""
    import ipaddress
    ipv6_pattern = r'\b[0-9a-fA-F:]{2,}\b'
    results = []
    for match in re.finditer(ipv6_pattern, s):
        try:
            addr = ipaddress.IPv6Address(match.group(0))
            results.append(str(addr))
        except:
            pass
    return '\n'.join(dict.fromkeys(results))


def extract_mac(s: str) -> str:
    """Extract MAC addresses (colon, hyphen, or dot notation)."""
    patterns = [
        r'\b[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}\b',
        r'\b[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}-[0-9A-Fa-f]{2}\b',
        r'\b[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\.[0-9A-Fa-f]{4}\b',
    ]
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, s))
    return '\n'.join(dict.fromkeys(results))


def extract_numbers(s: str) -> str:
    """Extract all numbers (including decimals)."""
    return '\n'.join(re.findall(r'\d+(?:\.\d+)?', s))


def extract_hashtags(s: str) -> str:
    """Extract hashtags."""
    return '\n'.join(re.findall(r'#\w+', s))


def extract_mentions(s: str) -> str:
    """Extract @mentions."""
    return '\n'.join(re.findall(r'@\w+', s))


def strip_html_tags(s: str) -> str:
    """Remove HTML tags."""
    return re.sub(r'<[^>]+>', '', s)


def strip_markdown_tags(s: str) -> str:
    """Remove markdown formatting."""
    s = re.sub(r'\*{1,2}([^\*]+)\*{1,2}', r'\1', s)  # bold, italic
    s = re.sub(r'`{1,3}[^`]+`{1,3}', lambda m: m.group(0).strip('`'), s)  # code
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)  # links
    return s


def strip_punctuation(s: str) -> str:
    """Remove all punctuation."""
    return re.sub(r'[^\w\s]', '', s)


def strip_ansi_codes(s: str) -> str:
    """Remove ANSI escape codes."""
    return re.sub(r'\x1b\[[0-9;]*m', '', s)


def extract_dates(s: str) -> str:
    patterns = [
        r'\b\d{4}[-/]\d{2}[-/]\d{2}\b',
        r'\b\d{2}[-/]\d{2}[-/]\d{4}\b',
    ]
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, s))
    return '\n'.join(dict.fromkeys(results))


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
