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


if __name__ == '__main__':
    unittest.main()
