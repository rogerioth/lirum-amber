import unittest
from string_ops.extract import (
    extract_emails,
    extract_urls,
    extract_phone_numbers,
    extract_ip_addresses,
    extract_dates,
    extract_between_markers,
    extract_regex,
    extract_first_n,
    extract_last_n,
    extract_by_line_range,
    extract_domains,
    extract_ipv6,
    extract_mac,
    extract_numbers,
    extract_hashtags,
    extract_mentions,
    strip_html_tags,
    strip_markdown_tags,
    strip_punctuation,
    strip_ansi_codes,
)


class TestExtractEmails(unittest.TestCase):
    def test_extract_emails(self):
        text = "Contact us at info@example.com or support@test.org"
        emails = extract_emails(text)
        self.assertIn("info@example.com", emails)
        self.assertIn("support@test.org", emails)

    def test_extract_emails_none(self):
        self.assertEqual(extract_emails("no emails here"), '')
        self.assertEqual(extract_emails(""), '')

    def test_extract_emails_edge_cases(self):
        self.assertIn("user.name+tag@domain.co.uk", extract_emails("user.name+tag@domain.co.uk"))
        self.assertIn("a@b.c", extract_emails("a@b.c"))


class TestExtractUrls(unittest.TestCase):
    def test_extract_urls(self):
        text = "Visit https://example.com or http://test.org/path?q=1"
        urls = extract_urls(text)
        self.assertIn("https://example.com", urls)
        self.assertIn("http://test.org/path?q=1", urls)

    def test_extract_urls_none(self):
        self.assertEqual(extract_urls("no urls here"), '')
        self.assertEqual(extract_urls(""), '')


class TestExtractPhoneNumbers(unittest.TestCase):
    def test_extract_phone_numbers(self):
        text = "Call 555-123-4567 or (555) 987-6543"
        phones = extract_phone_numbers(text)
        self.assertTrue(len(phones) >= 1)

    def test_extract_phone_numbers_none(self):
        self.assertEqual(extract_phone_numbers("no phones"), '')
        self.assertEqual(extract_phone_numbers(""), '')


class TestExtractIpAddresses(unittest.TestCase):
    def test_extract_ipv4(self):
        text = "Server at 192.168.1.1 and 10.0.0.255"
        ips = extract_ip_addresses(text)
        self.assertIn("192.168.1.1", ips)
        self.assertIn("10.0.0.255", ips)

    def test_extract_ipv6(self):
        text = "IPv6: 2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        ips = extract_ip_addresses(text)
        self.assertTrue(len(ips) >= 1)

    def test_extract_ip_none(self):
        self.assertEqual(extract_ip_addresses("no ips"), '')
        self.assertEqual(extract_ip_addresses(""), '')


class TestExtractDates(unittest.TestCase):
    def test_extract_dates(self):
        text = "Date: 2024-01-15 and 01/15/2024"
        dates = extract_dates(text)
        self.assertTrue(len(dates) >= 1)

    def test_extract_dates_none(self):
        self.assertEqual(extract_dates("no dates"), '')
        self.assertEqual(extract_dates(""), '')


class TestExtractBetweenMarkers(unittest.TestCase):
    def test_extract_between_markers(self):
        text = "start hello end start world end"
        result = extract_between_markers(text, "start ", " end")
        self.assertIn("hello", result)
        self.assertIn("world", result)

    def test_extract_between_markers_include(self):
        text = "[hello] [world]"
        result = extract_between_markers(text, "[", "]", include_markers=True)
        self.assertIn("[hello]", result)
        self.assertIn("[world]", result)


class TestExtractByRegex(unittest.TestCase):
    def test_extract_by_regex(self):
        result = extract_regex("abc123 def456", r'[a-z]+')
        self.assertEqual(result, ['abc', 'def'])


class TestExtractFirstLastN(unittest.TestCase):
    def test_extract_first_n(self):
        self.assertEqual(extract_first_n("hello world", 5), "hello")
        self.assertEqual(extract_first_n("hi", 10), "hi")

    def test_extract_last_n(self):
        self.assertEqual(extract_last_n("hello world", 5), "world")
        self.assertEqual(extract_last_n("hi", 10), "hi")


class TestExtractByLineRange(unittest.TestCase):
    def test_extract_by_line_range(self):
        self.assertEqual(extract_by_line_range("a\nb\nc\nd", 2, 3), "b\nc")

    def test_extract_by_line_range_single(self):
        self.assertEqual(extract_by_line_range("a\nb\nc", 1, 1), "a")


class TestExtractDomains(unittest.TestCase):
    def test_extract_domains(self):
        text = "Visit https://example.com/path and http://sub.test.org?q=1"
        result = extract_domains(text)
        self.assertIn("example.com", result)
        self.assertIn("sub.test.org", result)
        self.assertEqual(len(result.split('\n')), 2)

    def test_extract_domains_no_urls(self):
        self.assertEqual(extract_domains("no urls here"), "")

    def test_extract_domains_no_domains(self):
        self.assertEqual(extract_domains("https://"), "")


class TestExtractIPv6(unittest.TestCase):
    def test_extract_ipv6(self):
        text = "IPv6: 2001:0db8:85a3::8a2e:0370:7334"
        result = extract_ipv6(text)
        # ipaddress module normalizes (removes leading zeros)
        self.assertIn("2001:db8:85a3::8a2e:370:7334", result)
        self.assertEqual(len(result.split('\n')), 1)

    def test_extract_ipv6_no_ipv6(self):
        self.assertEqual(extract_ipv6("IPv4: 192.168.1.1"), "")


class TestExtractMac(unittest.TestCase):
    def test_extract_mac(self):
        text = "MAC: 00:1A:2B:3C:4D:5E and 00-1A-2B-3C-4D-5E and 001A.2B3C.4D5E"
        result = extract_mac(text)
        self.assertIn("00:1A:2B:3C:4D:5E", result)
        self.assertIn("00-1A-2B-3C-4D-5E", result)
        self.assertIn("001A.2B3C.4D5E", result)
        self.assertEqual(len(result.split('\n')), 3)

    def test_extract_mac_none(self):
        self.assertEqual(extract_mac("no mac here"), "")


class TestExtractNumbers(unittest.TestCase):
    def test_extract_numbers(self):
        text = "abc 123 def 45.6 789"
        result = extract_numbers(text)
        self.assertIn("123", result)
        self.assertIn("45.6", result)
        self.assertIn("789", result)
        self.assertEqual(len(result.split('\n')), 3)

    def test_extract_numbers_none(self):
        self.assertEqual(extract_numbers("no numbers"), "")


class TestExtractHashtags(unittest.TestCase):
    def test_extract_hashtags(self):
        text = "Love #coding #python3! #123"
        result = extract_hashtags(text)
        self.assertIn("#coding", result)
        self.assertIn("#python3", result)
        self.assertIn("#123", result)
        self.assertEqual(len(result.split('\n')), 3)

    def test_extract_hashtags_none(self):
        self.assertEqual(extract_hashtags("no hashtags"), "")


class TestExtractMentions(unittest.TestCase):
    def test_extract_mentions(self):
        text = "Hello @user1 @user2! @123"
        result = extract_mentions(text)
        self.assertIn("@user1", result)
        self.assertIn("@user2", result)
        self.assertIn("@123", result)
        self.assertEqual(len(result.split('\n')), 3)

    def test_extract_mentions_none(self):
        self.assertEqual(extract_mentions("no mentions"), "")


class TestStripHtmlTags(unittest.TestCase):
    def test_strip_html_tags(self):
        html = "<p>Hello</p> <br/>World <div class='test'>Python</div>"
        result = strip_html_tags(html)
        self.assertEqual(result.strip(), "Hello World Python")

    def test_strip_html_tags_no_tags(self):
        self.assertEqual(strip_html_tags("no tags here"), "no tags here")


class TestStripMarkdownTags(unittest.TestCase):
    def test_strip_markdown_tags(self):
        md = "**bold** *italic* `code` [link](url)"
        result = strip_markdown_tags(md)
        self.assertEqual(result.strip(), "bold italic code link")

    def test_strip_markdown_tags_no_tags(self):
        self.assertEqual(strip_markdown_tags("no markdown"), "no markdown")


class TestStripPunctuation(unittest.TestCase):
    def test_strip_punctuation(self):
        text = "Hello, world! How are you?"
        result = strip_punctuation(text)
        self.assertEqual(result, "Hello world How are you")

    def test_strip_punctuation_no_punct(self):
        self.assertEqual(strip_punctuation("no punct"), "no punct")


class TestStripAnsiCodes(unittest.TestCase):
    def test_strip_ansi_codes(self):
        text = "\x1b[31mRed\x1b[0m \x1b[1mBold\x1b[0m"
        result = strip_ansi_codes(text)
        self.assertEqual(result, "Red Bold")

    def test_strip_ansi_codes_no_codes(self):
        self.assertEqual(strip_ansi_codes("no ansi"), "no ansi")


if __name__ == '__main__':
    unittest.main()
