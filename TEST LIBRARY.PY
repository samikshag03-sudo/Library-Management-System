"""
Unit tests for the Library Management System.

Run with:  python -m pytest tests/ -v
(or:       python -m unittest discover tests)

Each test uses a fresh temporary data directory so tests never interfere
with each other or with real library data.
"""

import shutil
import tempfile
import unittest
from datetime import date, timedelta

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.library import Library
from src.models import IssueRecord
from src.exceptions import (
    BookNotFoundError,
    DuplicateISBNError,
    BookNotAvailableError,
    InvalidBookDataError,
    MemberNotFoundError,
    DuplicateMemberError,
    MembershipLimitExceededError,
    InvalidMemberDataError,
    BookAlreadyIssuedToMemberError,
    NoActiveIssueRecordError,
)


class LibraryTestCase(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.lib = Library(data_dir=self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    # ---- Book management -------------------------------------------------
    def test_add_and_get_book(self):
        book = self.lib.add_book("111", "Clean Code", "Robert Martin", "Programming", 2)
        self.assertEqual(book.available_copies, 2)
        fetched = self.lib.get_book("111")
        self.assertEqual(fetched.title, "Clean Code")

    def test_duplicate_isbn_rejected(self):
        self.lib.add_book("111", "Clean Code", "Robert Martin")
        with self.assertRaises(DuplicateISBNError):
            self.lib.add_book("111", "Another Title", "Someone Else")

    def test_invalid_book_data_rejected(self):
        with self.assertRaises(InvalidBookDataError):
            self.lib.add_book("", "Title", "Author")
        with self.assertRaises(InvalidBookDataError):
            self.lib.add_book("222", "Title", "Author", copies=0)

    def test_get_missing_book_raises(self):
        with self.assertRaises(BookNotFoundError):
            self.lib.get_book("does-not-exist")

    def test_delete_book(self):
        self.lib.add_book("111", "Clean Code", "Robert Martin")
        self.lib.delete_book("111")
        with self.assertRaises(BookNotFoundError):
            self.lib.get_book("111")

    def test_search_books_by_keyword_and_category(self):
        self.lib.add_book("1", "Python Crash Course", "Eric Matthes", "Programming")
        self.lib.add_book("2", "The Hobbit", "J.R.R. Tolkien", "Fiction")
        results = self.lib.search_books(keyword="python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].isbn, "1")

        results = self.lib.search_books(category="Fiction")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].isbn, "2")

    # ---- Member management --------------------------------------------
    def test_add_member(self):
        member = self.lib.add_member("M1", "Asha Rao", "asha@example.com")
        self.assertEqual(member.name, "Asha Rao")

    def test_duplicate_member_rejected(self):
        self.lib.add_member("M1", "Asha Rao", "asha@example.com")
        with self.assertRaises(DuplicateMemberError):
            self.lib.add_member("M1", "Someone Else", "other@example.com")

    def test_invalid_email_rejected(self):
        with self.assertRaises(InvalidMemberDataError):
            self.lib.add_member("M2", "Bad Email", "not-an-email")

    def test_get_missing_member_raises(self):
        with self.assertRaises(MemberNotFoundError):
            self.lib.get_member("nope")

    # ---- Issue / return --------------------------------------------------
    def test_issue_and_return_book(self):
        self.lib.add_book("111", "Clean Code", "Robert Martin", copies=1)
        self.lib.add_member("M1", "Asha Rao", "asha@example.com")

        record = self.lib.issue_book("111", "M1")
        self.assertFalse(record.is_returned)
        self.assertEqual(self.lib.get_book("111").available_copies, 0)

        returned = self.lib.return_book("111", "M1")
        self.assertTrue(returned.is_returned)
        self.assertEqual(self.lib.get_book("111").available_copies, 1)
        self.assertEqual(returned.fine, 0.0)

    def test_cannot_issue_unavailable_book(self):
        self.lib.add_book("111", "Clean Code", "Robert Martin", copies=1)
        self.lib.add_member("M1", "Asha Rao", "asha@example.com")
        self.lib.add_member("M2", "Kiran Shah", "kiran@example.com")

        self.lib.issue_book("111", "M1")
        with self.assertRaises(BookNotAvailableError):
            self.lib.issue_book("111", "M2")

    def test_cannot_issue_same_book_twice_to_same_member(self):
        self.lib.add_book("111", "Clean Code", "Robert Martin", copies=2)
        self.lib.add_member("M1", "Asha Rao", "asha@example.com")
        self.lib.issue_book("111", "M1")
        with self.assertRaises(BookAlreadyIssuedToMemberError):
            self.lib.issue_book("111", "M1")

    def test_membership_limit_enforced(self):
        self.lib.add_member("M1", "Asha Rao", "asha@example.com", max_books=1)
        self.lib.add_book("111", "Book One", "Author A", copies=1)
        self.lib.add_book("222", "Book Two", "Author B", copies=1)

        self.lib.issue_book("111", "M1")
        with self.assertRaises(MembershipLimitExceededError):
            self.lib.issue_book("222", "M1")

    def test_return_without_active_issue_raises(self):
        self.lib.add_book("111", "Clean Code", "Robert Martin")
        self.lib.add_member("M1", "Asha Rao", "asha@example.com")
        with self.assertRaises(NoActiveIssueRecordError):
            self.lib.return_book("111", "M1")

    def test_overdue_fine_calculation(self):
        overdue_date = date.today() - timedelta(days=20)
        due_date = IssueRecord.new_due_date(overdue_date)  # 14-day loan
        record = IssueRecord(
            record_id="x1", isbn="111", member_id="M1",
            issue_date=overdue_date.isoformat(), due_date=due_date.isoformat(),
        )
        fine = record.compute_fine(as_of=date.today())
        expected_days_late = (date.today() - due_date).days
        self.assertEqual(fine, round(expected_days_late * IssueRecord.FINE_PER_DAY, 2))

    def test_cannot_delete_book_with_outstanding_loan(self):
        self.lib.add_book("111", "Clean Code", "Robert Martin", copies=1)
        self.lib.add_member("M1", "Asha Rao", "asha@example.com")
        self.lib.issue_book("111", "M1")
        with self.assertRaises(InvalidBookDataError):
            self.lib.delete_book("111")

    def test_stats(self):
        self.lib.add_book("111", "Clean Code", "Robert Martin", copies=3)
        self.lib.add_member("M1", "Asha Rao", "asha@example.com")
        self.lib.issue_book("111", "M1")
        stats = self.lib.stats()
        self.assertEqual(stats["total_titles"], 1)
        self.assertEqual(stats["total_copies"], 3)
        self.assertEqual(stats["available_copies"], 2)
        self.assertEqual(stats["books_currently_issued"], 1)


if __name__ == "__main__":
    unittest.main()
