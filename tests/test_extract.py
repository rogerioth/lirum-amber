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
)


class TestExtractEmails(unittest.TestCase):
    def test_extract_emails(self):
        text = "Contact us at info@example.com or support@test.org"
        emails = extract_emails(text)
        self.assertIn("info@example.com", emails)
        self.assertIn("support@test.org", emails)

    def test_extract_emails_none(self):
        self.assertEqual(extract_emails("no emails here"), [])

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
        self.assertEqual(extract_urls("no urls here"), [])


class TestExtractPhoneNumbers(unittest.TestCase):
    def test_extract_phone_numbers(self):
        text = "Call 555-123-4567 or (555) 987-6543"
        phones = extract_phone_numbers(text)
        self.assertTrue(len(phones) >= 1)

    def test_extract_phone_numbers_none(self):
        self.assertEqual(extract_phone_numbers("no phones"), [])


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
        self.assertEqual(extract_ip_addresses("no ips"), [])


class TestExtractDates(unittest.TestCase):
    def test_extract_dates(self):
        text = "Date: 2024-01-15 and 01/15/2024"
        dates = extract_dates(text)
        self.assertTrue(len(dates) >= 1)

    def test_extract_dates_none(self):
        self.assertEqual(extract_dates("no dates"), [])


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


if __name__ == '__main__':
    unittest.main()
