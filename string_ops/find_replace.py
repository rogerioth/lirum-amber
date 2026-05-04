import re


def find_and_replace(s: str, pattern: str, replacement: str,
                     case_insensitive: bool = False, regex: bool = False) -> str:
    if regex:
        flags = re.IGNORECASE if case_insensitive else 0
        return re.sub(pattern, replacement, s, flags=flags)
    if case_insensitive:
        return re.sub(re.escape(pattern), replacement, s, flags=re.IGNORECASE)
    return s.replace(pattern, replacement, 1)


def find_and_replace_all(s: str, pattern: str, replacement: str,
                         case_insensitive: bool = False, regex: bool = False) -> str:
    if regex:
        flags = re.IGNORECASE if case_insensitive else 0
        return re.sub(pattern, replacement, s, flags=flags)
    if case_insensitive:
        return re.sub(re.escape(pattern), replacement, s, flags=re.IGNORECASE)
    return s.replace(pattern, replacement)


def regex_find(s: str, pattern: str) -> list:
    return re.findall(pattern, s)


def regex_replace(s: str, pattern: str, replacement: str) -> str:
    return re.sub(pattern, replacement, s)


def count_matches(s: str, pattern: str) -> int:
    return len(re.findall(pattern, s))


def extract_regex_groups(s: str, pattern: str) -> list:
    matches = re.finditer(pattern, s)
    results = []
    for m in matches:
        groups = m.groups()
        if groups:
            results.append(groups)
        else:
            results.append((m.group(),))
    return results
