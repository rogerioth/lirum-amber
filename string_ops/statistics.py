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


def count_vowels(s: str) -> str:
    vowels = 'aeiouAEIOU'
    count = sum(1 for c in s if c in vowels)
    return f"Vowels: {count}"


def count_consonants(s: str) -> str:
    vowels = 'aeiouAEIOU'
    count = sum(1 for c in s if c.isalpha() and c not in vowels)
    return f"Consonants: {count}"


def jaro_winkler_distance(s1: str, s2: str) -> str:
    if not s1 and not s2:
        return "1.0"
    if not s1 or not s2:
        return "0.0"
    
    s1_len, s2_len = len(s1), len(s2)
    match_distance = max(s1_len, s2_len) // 2 - 1
    
    s1_matches = [False] * s1_len
    s2_matches = [False] * s2_len
    
    matches = 0
    transpositions = 0
    
    for i in range(s1_len):
        start = max(0, i - match_distance)
        end = min(s2_len, i + match_distance + 1)
        for j in range(start, end):
            if not s2_matches[j] and s1[i] == s2[j]:
                s1_matches[i] = True
                s2_matches[j] = True
                matches += 1
                break
    
    if matches == 0:
        return "0.0"
    
    k = 0
    for i in range(s1_len):
        if s1_matches[i]:
            while not s2_matches[k]:
                k += 1
            if s1[i] != s2[k]:
                transpositions += 1
            k += 1
    
    transpositions //= 2
    
    jaro = ((matches / s1_len) + (matches / s2_len) + ((matches - transpositions) / matches)) / 3.0
    
    prefix_len = 0
    for i in range(min(len(s1), len(s2))):
        if s1[i] == s2[i]:
            prefix_len += 1
        else:
            break
    prefix_len = min(prefix_len, 4)
    
    winkler = jaro + (0.1 * prefix_len * (1 - jaro))
    return f"{winkler:.6f}"


def hamming_distance(s1: str, s2: str) -> str:
    if len(s1) != len(s2):
        return "-1"
    distance = sum(c1 != c2 for c1, c2 in zip(s1, s2))
    return str(distance)


def soundex(s: str) -> str:
    if not s:
        return "0000"
    
    s = s.upper()
    first_letter = s[0]
    
    soundex_map = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    
    result = first_letter
    prev_code = soundex_map.get(first_letter, '')
    
    for char in s[1:]:
        code = soundex_map.get(char, '')
        if code and code != prev_code:
            result += code
        prev_code = code
    
    result = result.ljust(4, '0')[:4]
    return result


def metaphone(s: str) -> str:
    if not s:
        return ""
    
    s = s.upper()
    result = []
    i = 0
    length = len(s)
    
    while i < length:
        c = s[i]
        
        if c in 'AEIOU':
            if i == 0:
                result.append(c)
        
        elif c == 'B':
            if i == length - 1 and s[i-1] == 'M':
                pass
            else:
                result.append('B')
        
        elif c == 'C':
            if i > 0 and s[i-1] == 'S' and i < length - 1 and s[i+1] in 'AEIOU':
                pass
            elif i < length - 1 and s[i+1] == 'H':
                result.append('X')
                i += 1
            elif i < length - 1 and s[i+1] in 'EIY':
                result.append('S')
            else:
                result.append('K')
        
        elif c == 'D':
            if i < length - 1 and s[i+1] == 'G':
                result.append('J')
                i += 1
            else:
                result.append('T')
        
        elif c == 'G':
            if i < length - 1 and s[i+1] == 'H' and (i == length - 2 or s[i+2] not in 'AEIOU'):
                pass
            elif i < length - 1 and s[i+1] in 'EIY':
                result.append('J')
            else:
                result.append('G')
        
        elif c == 'H':
            if i == 0 or (i > 0 and s[i-1] in 'AEIOU') or (i < length - 1 and s[i+1] in 'AEIOU'):
                result.append('H')
        
        elif c == 'K':
            if i == 0 or s[i-1] != 'C':
                result.append('K')
        
        elif c == 'P':
            if i < length - 1 and s[i+1] == 'H':
                result.append('F')
                i += 1
            else:
                result.append('P')
        
        elif c == 'Q':
            result.append('K')
        
        elif c == 'S':
            if i < length - 2 and s[i+1] == 'H' and s[i+2] in 'AEIOU':
                result.append('X')
                i += 2
            else:
                result.append('S')
        
        elif c == 'T':
            if i < length - 2 and s[i+1] == 'H' and s[i+2] in 'AEIOU':
                result.append('0')
                i += 2
            elif i < length - 1 and s[i+1] in 'EIY':
                result.append('S')
            else:
                result.append('T')
        
        elif c == 'V':
            result.append('F')
        
        elif c == 'W':
            if i < length - 1 and s[i+1] in 'AEIOU':
                result.append('W')
        
        elif c == 'X':
            result.append('KS')
        
        elif c == 'Y':
            if i < length - 1 and s[i+1] in 'AEIOU':
                result.append('Y')
        
        elif c in 'LMNR':
            result.append(c)
        
        i += 1
    
    return ''.join(result)


def double_metaphone(s: str) -> str:
    if not s:
        return ""
    
    primary = metaphone(s)
    return primary


def is_anagram(s1: str, s2: str) -> str:
    s1_clean = ''.join(sorted(s1.lower().replace(' ', '')))
    s2_clean = ''.join(sorted(s2.lower().replace(' ', '')))
    return str(s1_clean == s2_clean)


def find_most_frequent_word(s: str) -> str:
    if not s.strip():
        return ""
    
    words = s.lower().split()
    if not words:
        return ""
    
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    
    return max(freq, key=freq.get)


def find_most_frequent_char(s: str) -> str:
    if not s:
        return ""
    
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    
    return max(freq, key=freq.get)
