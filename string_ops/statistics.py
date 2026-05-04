import math


def count_characters(s: str) -> int:
    return len(s)


def count_characters_no_space(s: str) -> int:
    return len(s.replace(' ', '').replace('\t', '').replace('\n', '').replace('\r', ''))


def count_words(s: str) -> int:
    return len(s.split()) if s.strip() else 0


def count_lines(s: str) -> int:
    if not s:
        return 0
    lines = s.split('\n')
    # If string ends with newline, the last empty element is not a real line
    if s.endswith('\n'):
        return len(lines) - 1
    return len(lines)


def count_bytes(s: str) -> int:
    return len(s.encode('utf-8'))


def character_frequency(s: str) -> dict:
    freq = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    return freq


def word_frequency(s: str, case_insensitive: bool = False) -> dict:
    words = s.split()
    if case_insensitive:
        words = [w.lower() for w in words]
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    return freq


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    freq = character_frequency(s)
    length = len(s)
    entropy = 0.0
    for count in freq.values():
        p = count / length
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy


def is_palindrome(s: str) -> bool:
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


def levenshtein_distance(s1: str, s2: str) -> int:
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if not s2:
        return len(s1)

    prev_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = prev_row[j + 1] + 1
            deletions = curr_row[j] + 1
            substitutions = prev_row[j] + (c1 != c2)
            curr_row.append(min(insertions, deletions, substitutions))
        prev_row = curr_row
    return prev_row[-1]


def longest_word(s: str) -> str | None:
    words = s.split()
    if not words:
        return None
    return max(words, key=len)


def shortest_word(s: str) -> str | None:
    words = s.split()
    if not words:
        return None
    return min(words, key=len)


def count_unique_words(s: str) -> int:
    return len(set(s.split())) if s.strip() else 0


def readability_score(s: str) -> float:
    sentences = [s.strip() for s in s.replace('!', '.').replace('?', '.').split('.') if s.strip()]
    num_sentences = max(len(sentences), 1)
    num_words = count_words(s)
    num_syllables = 0
    for word in s.split():
        word = word.lower().strip('.,!?;:')
        if not word:
            continue
        vowels = 'aeiou'
        count = 0
        prev_vowel = False
        for c in word:
            is_vowel = c in vowels
            if is_vowel and not prev_vowel:
                count += 1
            prev_vowel = is_vowel
        if word.endswith('e'):
            count -= 1
        num_syllables += max(count, 1)

    if num_words == 0:
        return 0.0

    score = 206.835 - 1.015 * (num_words / num_sentences) - 84.6 * (num_syllables / num_words)
    return round(score, 2)
