"""
Custom exception hierarchy for the Library Management System.

Keeping exceptions specific (instead of raising generic Exception/ValueError
everywhere) makes it possible for the CLI layer to catch precise error
conditions and show the user a helpful, actionable message.
"""


class LibraryError(Exception):
    """Base class for all library-related errors."""
    pass


# ---------------------------------------------------------------- Books ----
class BookError(LibraryError):
    """Base class for book-related errors."""
    pass


class BookNotFoundError(BookError):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"No book found with ISBN '{isbn}'.")


class DuplicateISBNError(BookError):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"A book with ISBN '{isbn}' already exists.")


class BookNotAvailableError(BookError):
    def __init__(self, isbn):
        self.isbn = isbn
        super().__init__(f"Book with ISBN '{isbn}' has no available copies right now.")


class InvalidBookDataError(BookError):
    pass


# -------------------------------------------------------------- Members ----
class MemberError(LibraryError):
    """Base class for member-related errors."""
    pass


class MemberNotFoundError(MemberError):
    def __init__(self, member_id):
        self.member_id = member_id
        super().__init__(f"No member found with ID '{member_id}'.")


class DuplicateMemberError(MemberError):
    def __init__(self, member_id):
        self.member_id = member_id
        super().__init__(f"A member with ID '{member_id}' already exists.")


class MembershipLimitExceededError(MemberError):
    def __init__(self, member_id, limit):
        self.member_id = member_id
        self.limit = limit
        super().__init__(
            f"Member '{member_id}' already has the maximum of {limit} books issued."
        )


class InvalidMemberDataError(MemberError):
    pass


# ------------------------------------------------------------- Issuing -----
class IssueError(LibraryError):
    """Base class for issue/return related errors."""
    pass


class BookAlreadyIssuedToMemberError(IssueError):
    def __init__(self, isbn, member_id):
        super().__init__(
            f"Book '{isbn}' is already issued to member '{member_id}'."
        )


class NoActiveIssueRecordError(IssueError):
    def __init__(self, isbn, member_id):
        super().__init__(
            f"No active (unreturned) issue record found for book '{isbn}' "
            f"and member '{member_id}'."
        )


# ------------------------------------------------------------- Storage -----
class StorageError(LibraryError):
    """Raised when reading/writing the JSON data files fails."""
    pass
