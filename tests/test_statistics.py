import unittest
from string_ops.statistics import (
    count_characters,
    count_characters_no_space,
    count_words,
    count_lines,
    count_bytes,
    character_frequency,
    word_frequency,
    shannon_entropy,
    is_palindrome,
    levenshtein_distance,
    longest_word,
    shortest_word,
    count_unique_words,
    readability_score,
    count_vowels,
    count_consonants,
    jaro_winkler_distance,
    hamming_distance,
    soundex,
    metaphone,
    double_metaphone,
    is_anagram,
    find_most_frequent_word,
    find_most_frequent_char,
)


class TestCounters(unittest.TestCase):
    def test_count_characters(self):
        self.assertEqual(count_characters("hello"), 5)
        self.assertEqual(count_characters(""), 0)
        self.assertEqual(count_characters("hello world"), 11)
        self.assertEqual(count_characters("🔥🎉"), 2)

    def test_count_characters_no_space(self):
        self.assertEqual(count_characters_no_space("hello world"), 10)
        self.assertEqual(count_characters_no_space("a b c"), 3)
        self.assertEqual(count_characters_no_space(""), 0)

    def test_count_words(self):
        self.assertEqual(count_words("hello world"), 2)
        self.assertEqual(count_words(""), 0)
        self.assertEqual(count_words("  hello   world  "), 2)
        self.assertEqual(count_words("one"), 1)

    def test_count_lines(self):
        self.assertEqual(count_lines("a\nb\nc"), 3)
        self.assertEqual(count_lines(""), 0)
        self.assertEqual(count_lines("a"), 1)

    def test_count_bytes(self):
        self.assertEqual(count_bytes("hello"), 5)
        self.assertEqual(count_bytes("café"), 5)
        self.assertEqual(count_bytes("🔥"), 4)

    def test_character_frequency(self):
        freq = character_frequency("aabbc")
        self.assertEqual(freq, {"a": 2, "b": 2, "c": 1})
        self.assertEqual(character_frequency(""), {})

    def test_word_frequency(self):
        freq = word_frequency("hello Hello world hello")
        self.assertEqual(freq["hello"], 2)
        self.assertEqual(freq["Hello"], 1)
        self.assertEqual(freq["world"], 1)

    def test_word_frequency_case_insensitive(self):
        freq = word_frequency("Hello hello HELLO", case_insensitive=True)
        self.assertEqual(freq["hello"], 3)


class TestStatisticsAdvanced(unittest.TestCase):
    def test_shannon_entropy(self):
        self.assertAlmostEqual(shannon_entropy("aaaa"), 0.0, places=5)
        entropy_abcd = shannon_entropy("abcd")
        entropy_abab = shannon_entropy("abab")
        self.assertGreater(entropy_abcd, entropy_abab)
        self.assertEqual(shannon_entropy(""), 0.0)

    def test_is_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("a"))
        self.assertTrue(is_palindrome(""))
        self.assertFalse(is_palindrome("hello"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama".replace(" ", "").lower()))

    def test_levenshtein_distance(self):
        self.assertEqual(levenshtein_distance("kitten", "sitting"), 3)
        self.assertEqual(levenshtein_distance("", "abc"), 3)
        self.assertEqual(levenshtein_distance("abc", ""), 3)
        self.assertEqual(levenshtein_distance("abc", "abc"), 0)
        self.assertEqual(levenshtein_distance("abc", "abd"), 1)

    def test_longest_word(self):
        self.assertEqual(longest_word("hello world foo"), "hello")
        self.assertEqual(longest_word(""), None)
        self.assertEqual(longest_word("a bb ccc"), "ccc")

    def test_shortest_word(self):
        self.assertEqual(shortest_word("hello world foo"), "foo")
        self.assertEqual(shortest_word(""), None)
        self.assertEqual(shortest_word("a bb ccc"), "a")

    def test_count_unique_words(self):
        self.assertEqual(count_unique_words("hello world hello"), 2)
        self.assertEqual(count_unique_words("a b c a b"), 3)
        self.assertEqual(count_unique_words(""), 0)

    def test_readability_score(self):
        score = readability_score("The cat sat on the mat.")
        self.assertIsInstance(score, float)
        self.assertGreater(score, 0)


class TestCountVowelsAndConsonants(unittest.TestCase):
    def test_count_vowels_basic(self):
        self.assertEqual(count_vowels("hello"), "Vowels: 2")
        self.assertEqual(count_vowels("aeiou"), "Vowels: 5")

    def test_count_vowels_empty(self):
        self.assertEqual(count_vowels(""), "Vowels: 0")

    def test_count_vowels_uppercase(self):
        self.assertEqual(count_vowels("HELLO"), "Vowels: 2")

    def test_count_vowels_no_vowels(self):
        self.assertEqual(count_vowels("xyz"), "Vowels: 0")

    def test_count_consonants_basic(self):
        self.assertEqual(count_consonants("hello"), "Consonants: 3")
        self.assertEqual(count_consonants("bcdfg"), "Consonants: 5")

    def test_count_consonants_empty(self):
        self.assertEqual(count_consonants(""), "Consonants: 0")

    def test_count_consonants_uppercase(self):
        self.assertEqual(count_consonants("HELLO"), "Consonants: 3")

    def test_count_consonants_no_consonants(self):
        self.assertEqual(count_consonants("aeiou"), "Consonants: 0")


class TestJaroWinkler(unittest.TestCase):
    def test_jaro_winkler_basic(self):
        result = jaro_winkler_distance("MARTHA", "MARHTA")
        self.assertIsInstance(result, str)
        self.assertGreater(float(result), 0.9)

    def test_jaro_winkler_identical(self):
        result = jaro_winkler_distance("hello", "hello")
        self.assertEqual(float(result), 1.0)

    def test_jaro_winkler_different(self):
        result = jaro_winkler_distance("hello", "world")
        self.assertIsInstance(result, str)
        self.assertLess(float(result), 1.0)


class TestHammingDistance(unittest.TestCase):
    def test_hamming_distance_basic(self):
        self.assertEqual(hamming_distance("karolin", "kathrin"), "3")

    def test_hamming_distance_identical(self):
        self.assertEqual(hamming_distance("hello", "hello"), "0")

    def test_hamming_distance_all_different(self):
        self.assertEqual(hamming_distance("abc", "xyz"), "3")

    def test_hamming_distance_empty(self):
        self.assertEqual(hamming_distance("", ""), "0")


class TestSoundex(unittest.TestCase):
    def test_soundex_basic(self):
        self.assertEqual(soundex("Robert"), "R163")
        self.assertEqual(soundex("Rupert"), "R163")

    def test_soundex_generation(self):
        result = soundex("hello")
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 4)

    def test_soundex_empty(self):
        self.assertEqual(soundex(""), "0000")


class TestMetaphone(unittest.TestCase):
    def test_metaphone_basic(self):
        result = metaphone("hello")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_metaphone_empty(self):
        self.assertEqual(metaphone(""), "")


class TestDoubleMetaphone(unittest.TestCase):
    def test_double_metaphone_basic(self):
        result = double_metaphone("hello")
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

    def test_double_metaphone_empty(self):
        self.assertEqual(double_metaphone(""), "")


class TestIsAnagram(unittest.TestCase):
    def test_is_anagram_true(self):
        self.assertEqual(is_anagram("listen", "silent"), "True")
        self.assertEqual(is_anagram("rail safety", "fairy tales"), "True")

    def test_is_anagram_false(self):
        self.assertEqual(is_anagram("hello", "world"), "False")
        self.assertEqual(is_anagram("abc", "def"), "False")

    def test_is_anagram_same_word(self):
        self.assertEqual(is_anagram("hello", "hello"), "True")

    def test_is_anagram_empty(self):
        self.assertEqual(is_anagram("", ""), "True")


class TestMostFrequentWord(unittest.TestCase):
    def test_most_frequent_word_basic(self):
        self.assertEqual(find_most_frequent_word("hello world hello"), "hello")

    def test_most_frequent_word_single(self):
        self.assertEqual(find_most_frequent_word("hello"), "hello")

    def test_most_frequent_word_empty(self):
        self.assertEqual(find_most_frequent_word(""), "")


class TestMostFrequentChar(unittest.TestCase):
    def test_most_frequent_char_basic(self):
        self.assertEqual(find_most_frequent_char("hello"), "l")

    def test_most_frequent_char_single(self):
        self.assertEqual(find_most_frequent_char("a"), "a")

    def test_most_frequent_char_empty(self):
        self.assertEqual(find_most_frequent_char(""), "")


if __name__ == '__main__':
    unittest.main()
