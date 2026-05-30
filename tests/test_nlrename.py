#!/usr/bin/env python3
"""
Test suite for nlrename.
"""

import os
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from nlrename import parse_expression


class TestNLRename(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = Path(self.test_dir.name) / "test.txt"
        self.test_file.write_text("test content")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_todays_date(self):
        today = datetime.now().strftime("%Y-%m-%d")
        result = parse_expression("today's date", "test.txt")
        self.assertEqual(result, f"{today}_test.txt")

    def test_lowercase(self):
        result = parse_expression("lowercase", "TEST.TXT")
        self.assertEqual(result, "test.txt")

    def test_uppercase(self):
        result = parse_expression("uppercase", "test.txt")
        self.assertEqual(result, "TEST.TXT")

    def test_replace(self):
        result = parse_expression('replace "test" with "demo"', "test.txt")
        self.assertEqual(result, "demo.txt")


if __name__ == "__main__":
    unittest.main()