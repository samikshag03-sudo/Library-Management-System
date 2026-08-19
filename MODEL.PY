"""
Domain models for the Library Management System.

Each model knows how to convert itself to/from a plain dict so that the
storage layer can serialize it to JSON without the models needing to know
anything about the storage format.
"""

from dataclasses import dataclass, field, asdict
from datetime import date, timedelta


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    category: str = "General"
    total_copies: int = 1
    available_copies: int = 1
    added_on: str = field(default_factory=lambda: date.today().isoformat())

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Book":
        return Book(**data)

    @property
    def is_available(self) -> bool:
        return self.available_copies > 0

    def __str__(self):
        return (
            f"[{self.isbn}] {self.title} by {self.author} "
            f"({self.category}) - {self.available_copies}/{self.total_copies} available"
        )


@dataclass
class Member:
    member_id: str
    name: str
    email: str
    phone: str = ""
    joined_on: str = field(default_factory=lambda: date.today().isoformat())
    max_books: int = 3

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Member":
        return Member(**data)

    def __str__(self):
        return f"[{self.member_id}] {self.name} <{self.email}> - joined {self.joined_on}"


@dataclass
class IssueRecord:
    record_id: str
    isbn: str
    member_id: str
    issue_date: str
    due_date: str
    return_date: str = None
    fine: float = 0.0

    LOAN_PERIOD_DAYS = 14
    FINE_PER_DAY = 5.0  # currency units per day overdue

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "IssueRecord":
        return IssueRecord(**data)

    @property
    def is_returned(self) -> bool:
        return self.return_date is not None

    @staticmethod
    def new_due_date(issue_date: date) -> date:
        return issue_date + timedelta(days=IssueRecord.LOAN_PERIOD_DAYS)

    def compute_fine(self, as_of: date = None) -> float:
        """Compute the (potential) fine for this record.

        If the book has already been returned, the fine is fixed based on
        the return date. Otherwise, it is computed based on `as_of`
        (defaults to today) so members can be warned before returning.
        """
        as_of = as_of or date.today()
        due = date.fromisoformat(self.due_date)
        end = date.fromisoformat(self.return_date) if self.return_date else as_of
        overdue_days = (end - due).days
        if overdue_days <= 0:
            return 0.0
        return round(overdue_days * self.FINE_PER_DAY, 2)

    def __str__(self):
        status = f"returned on {self.return_date}" if self.is_returned else "OUTSTANDING"
        return (
            f"[{self.record_id}] ISBN {self.isbn} -> Member {self.member_id} | "
            f"issued {self.issue_date}, due {self.due_date}, {status}"
        )
