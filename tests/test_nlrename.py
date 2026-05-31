# Natural Language File Renamer - Tests

import os
import tempfile
import pytest
from datetime import datetime
from nlrename import NaturalLanguageRenamer


def test_add_todays_date():
    renamer = NaturalLanguageRenamer("today's date + original name")
    transformed = renamer.transform("test.txt")
    today = datetime.now().strftime("%Y-%m-%d")
    assert today in transformed


def test_sequential_number():
    renamer = NaturalLanguageRenamer("sequential number + original name")
    assert renamer.transform("test.txt", 1) == "1_test.txt"


def test_lowercase():
    renamer = NaturalLanguageRenamer("lowercase")
    assert renamer.transform("TEST.TXT") == "test.TXT"


def test_uppercase():
    renamer = NaturalLanguageRenamer("uppercase")
    assert renamer.transform("test.txt") == "TEST.txt"


def test_regex():
    renamer = NaturalLanguageRenamer("regex(s/foo/bar/)")
    assert renamer.transform("foo.txt") == "bar.txt"


def test_combined():
    renamer = NaturalLanguageRenamer("today's date + sequential number + original name")
    transformed = renamer.transform("test.txt", 1)
    today = datetime.now().strftime("%Y-%m-%d")
    assert transformed == f"1_{today}_test.txt"