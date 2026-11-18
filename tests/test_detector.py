import unittest
from detection.detector import detect_xss
class TestXSSDetector(unittest.TestCase):
    def test_script_element(self):
        value = "<script>alert(1)</script>"
        findings = detect_xss(value)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule_id"], "XSS-001")
    def test_event_handler(self):
        value = '<img src=x onerror=alert(1)>'
        findings = detect_xss(value)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule_id"], "XSS-002")
    def test_javascript_url(self):
        value = '<a href="javascript:alert(1)">Click</a>'
        findings = detect_xss(value)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule_id"], "XSS-003")
    def test_benign_input(self):
        value = "Hello, welcome to XssGuard!"
        findings = detect_xss(value)
        self.assertEqual(findings, [])
    def test_non_string_input(self):
        value = 12345
        findings = detect_xss(value)
        self.assertEqual(findings, [])
    def test_multiple_patterns(self):
        value = '<script>alert(1)</script><img src=x onerror=alert(1)>'
        findings = detect_xss(value)
        self.assertEqual(len(findings), 2)
    def test_uppercase_script(self):
        findings = detect_xss("<SCRIPT>alert(1)</SCRIPT>")
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]["rule_id"], "XSS-001")
    def test_empty_input(self):
        findings = detect_xss("")
        self.assertEqual(findings, [])
    def test_repeated_script_patterns(self):
        payloads = [
        "<script>alert(1)</script>",
        "<script>alert(2)</script>",
        "<SCRIPT>alert(3)</SCRIPT>"
    ]
        value = "".join(payloads)
        findings = detect_xss(value)
        self.assertEqual(len(findings), 3)
        
if __name__ == "__main__":
    unittest.main()
