"""
Core business logic for the Library Management System.

The `Library` class is the single entry point the CLI (or any other
front end - a GUI, a web API, etc.) talks to. It owns all validation
rules and coordinates the Book / Member / IssueRecord models with the
JSON storage layer.
"""

import uuid
from datetime import date

from .models import Book, Member, IssueRecord
from .storage import JSONStorage
from .exceptions import (
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


class Library:
    def __init__(self, data_dir: str = "data"):
        self.books_store = JSONStorage(f"{data_dir}/books.json")
        self.members_store = JSONStorage(f"{data_dir}/members.json")
        self.issues_store = JSONStorage(f"{data_dir}/issues.json")

    # ============================================================ BOOKS ===
    def add_book(self, isbn, title, author, category="General", copies=1) -> Book:
        isbn = (isbn or "").strip()
        title = (title or "").strip()
        author = (author or "").strip()

        if not isbn or not title or not author:
            raise InvalidBookDataError("ISBN, title, and author are all required.")
        try:
            copies = int(copies)
        except (TypeError, ValueError):
            raise InvalidBookDataError("Number of copies must be a whole number.")
        if copies < 1:
            raise InvalidBookDataError("Number of copies must be at least 1.")

        books = self.books_store.load()
        if any(b["isbn"] == isbn for b in books):
            raise DuplicateISBNError(isbn)

        book = Book(
            isbn=isbn,
            title=title,
            author=author,
            category=category.strip() or "General",
            total_copies=copies,
            available_copies=copies,
        )
        books.append(book.to_dict())
        self.books_store.save(books)
        return book

    def update_book(self, isbn, **fields) -> Book:
        books = self.books_store.load()
        for b in books:
            if b["isbn"] == isbn:
                editable = {"title", "author", "category", "total_copies", "available_copies"}
                for key, value in fields.items():
                    if key in editable and value is not None:
                        b[key] = value
                self.books_store.save(books)
                return Book.from_dict(b)
        raise BookNotFoundError(isbn)

    def delete_book(self, isbn) -> None:
        books = self.books_store.load()
        remaining = [b for b in books if b["isbn"] != isbn]
        if len(remaining) == len(books):
            raise BookNotFoundError(isbn)
        # Prevent deleting a book that still has an outstanding loan.
        issues = self.issues_store.load()
        if any(i["isbn"] == isbn and i["return_date"] is None for i in issues):
            raise InvalidBookDataError(
                f"Cannot delete book '{isbn}': it currently has an unreturned copy issued."
            )
        self.books_store.save(remaining)

    def get_book(self, isbn) -> Book:
        for b in self.books_store.load():
            if b["isbn"] == isbn:
                return Book.from_dict(b)
        raise BookNotFoundError(isbn)

    def list_books(self) -> list:
        return [Book.from_dict(b) for b in self.books_store.load()]

    def search_books(self, keyword="", category=None, available_only=False) -> list:
        keyword = (keyword or "").strip().lower()
        results = []
        for b in self.books_store.load():
            book = Book.from_dict(b)
            if keyword and keyword not in book.title.lower() \
                    and keyword not in book.author.lower() \
                    and keyword not in book.isbn.lower():
                continue
            if category and category.strip().lower() != book.category.lower():
                continue
            if available_only and not book.is_available:
                continue
            results.append(book)
        return results

    # =========================================================== MEMBERS ==
    def add_member(self, member_id, name, email, phone="", max_books=3) -> Member:
        member_id = (member_id or "").strip()
        name = (name or "").strip()
        email = (email or "").strip()

        if not member_id or not name:
            raise InvalidMemberDataError("Member ID and name are required.")
        if "@" not in email or "." not in email.split("@")[-1]:
            raise InvalidMemberDataError(f"'{email}' does not look like a valid email address.")
        try:
            max_books = int(max_books)
        except (TypeError, ValueError):
            raise InvalidMemberDataError("Max books allowed must be a whole number.")
        if max_books < 1:
            raise InvalidMemberDataError("Max books allowed must be at least 1.")

        members = self.members_store.load()
        if any(m["member_id"] == member_id for m in members):
            raise DuplicateMemberError(member_id)

        member = Member(
            member_id=member_id, name=name, email=email, phone=phone, max_books=max_books
        )
        members.append(member.to_dict())
        self.members_store.save(members)
        return member

    def update_member(self, member_id, **fields) -> Member:
        members = self.members_store.load()
        for m in members:
            if m["member_id"] == member_id:
                editable = {"name", "email", "phone", "max_books"}
                for key, value in fields.items():
                    if key in editable and value is not None:
                        m[key] = value
                self.members_store.save(members)
                return Member.from_dict(m)
        raise MemberNotFoundError(member_id)

    def delete_member(self, member_id) -> None:
        members = self.members_store.load()
        remaining = [m for m in members if m["member_id"] != member_id]
        if len(remaining) == len(members):
            raise MemberNotFoundError(member_id)
        issues = self.issues_store.load()
        if any(i["member_id"] == member_id and i["return_date"] is None for i in issues):
            raise InvalidMemberDataError(
                f"Cannot delete member '{member_id}': they still have book(s) issued."
            )
        self.members_store.save(remaining)

    def get_member(self, member_id) -> Member:
        for m in self.members_store.load():
            if m["member_id"] == member_id:
                return Member.from_dict(m)
        raise MemberNotFoundError(member_id)

    def list_members(self) -> list:
        return [Member.from_dict(m) for m in self.members_store.load()]

    def search_members(self, keyword="") -> list:
        keyword = (keyword or "").strip().lower()
        if not keyword:
            return self.list_members()
        results = []
        for m in self.members_store.load():
            member = Member.from_dict(m)
            if keyword in member.name.lower() or keyword in member.email.lower() \
                    or keyword in member.member_id.lower():
                results.append(member)
        return results

    # ==================================================== ISSUE / RETURN ==
    def issue_book(self, isbn, member_id) -> IssueRecord:
        # Validates existence first so errors are specific and actionable.
        book = self.get_book(isbn)
        self.get_member(member_id)  # raises MemberNotFoundError if missing

        if not book.is_available:
            raise BookNotAvailableError(isbn)

        issues = self.issues_store.load()
        active_for_member = [
            i for i in issues if i["member_id"] == member_id and i["return_date"] is None
        ]
        if any(i["isbn"] == isbn for i in active_for_member):
            raise BookAlreadyIssuedToMemberError(isbn, member_id)

        member = self.get_member(member_id)
        if len(active_for_member) >= member.max_books:
            raise MembershipLimitExceededError(member_id, member.max_books)

        today = date.today()
        record = IssueRecord(
            record_id=uuid.uuid4().hex[:8],
            isbn=isbn,
            member_id=member_id,
            issue_date=today.isoformat(),
            due_date=IssueRecord.new_due_date(today).isoformat(),
        )
        issues.append(record.to_dict())
        self.issues_store.save(issues)

        # Decrement available copies.
        self.update_book(isbn, available_copies=book.available_copies - 1)
        return record

    def return_book(self, isbn, member_id) -> IssueRecord:
        issues = self.issues_store.load()
        for i in issues:
            if i["isbn"] == isbn and i["member_id"] == member_id and i["return_date"] is None:
                i["return_date"] = date.today().isoformat()
                record = IssueRecord.from_dict(i)
                i["fine"] = record.compute_fine()
                self.issues_store.save(issues)

                book = self.get_book(isbn)
                self.update_book(isbn, available_copies=book.available_copies + 1)
                return IssueRecord.from_dict(i)

        raise NoActiveIssueRecordError(isbn, member_id)

    def list_active_issues(self, member_id=None) -> list:
        records = [IssueRecord.from_dict(i) for i in self.issues_store.load()
                   if i["return_date"] is None]
        if member_id:
            records = [r for r in records if r.member_id == member_id]
        return records

    def list_all_issues(self) -> list:
        return [IssueRecord.from_dict(i) for i in self.issues_store.load()]

    def list_overdue(self) -> list:
        today = date.today()
        return [
            r for r in self.list_active_issues()
            if date.fromisoformat(r.due_date) < today
        ]

    # =============================================================== MISC ==
    def stats(self) -> dict:
        books = self.list_books()
        members = self.list_members()
        active = self.list_active_issues()
        overdue = self.list_overdue()
        return {
            "total_titles": len(books),
            "total_copies": sum(b.total_copies for b in books),
            "available_copies": sum(b.available_copies for b in books),
            "total_members": len(members),
            "books_currently_issued": len(active),
            "overdue_books": len(overdue),
        }
