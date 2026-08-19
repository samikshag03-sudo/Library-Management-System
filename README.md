# 📚 Library Management System

A menu-driven Python application for managing books, members, and book
issue/return records in a small or medium-sized library. Built with clean,
modular architecture, persistent JSON storage, and comprehensive exception
handling — no external database or framework required.

## Features

- **Book Management** — add, update, delete, and list books (ISBN, title,
  author, category, total/available copies).
- **Member Management** — add, update, delete, and list members, each with
  a configurable maximum number of books they may borrow at once.
- **Issue & Return Books** — issue a book to a member (with a 14-day loan
  period), return it, and automatically calculate late fines (₹5/day).
- **Search & Filter** — search books by keyword (title/author/ISBN) and
  category, or filter to only currently-available copies. Search members
  by name, email, or ID.
- **Data Storage** — all data is persisted to human-readable JSON files
  under `data/`, using atomic writes so a crash mid-save can never corrupt
  your data.
- **Exception Handling** — a dedicated exception hierarchy
  (`DuplicateISBNError`, `BookNotAvailableError`, `MembershipLimitExceededError`,
  etc.) gives precise, user-friendly error messages instead of raw
  tracebacks, and the CLI never crashes on bad input.
- **Reports** — a statistics screen summarizing titles, copies, members,
  active loans, and overdue books.

## Project Structure

```
library-management-system/
├── main.py                 # Entry point — run this
├── src/
│   ├── models.py           # Book, Member, IssueRecord data classes
│   ├── exceptions.py       # Custom exception hierarchy
│   ├── storage.py          # JSON persistence layer (atomic writes)
│   ├── library.py          # Core business logic (validation + rules)
│   └── cli.py               # Menu-driven command-line interface
├── data/                   # JSON data files (auto-created at runtime)
├── tests/
│   └── test_library.py     # Unit tests (18 tests, unittest/pytest)
├── requirements.txt
├── LICENSE
└── README.md
```

The design separates concerns deliberately:

- **`models.py`** — plain data classes, no business logic.
- **`storage.py`** — knows nothing about books or members, only how to
  persist a list of dicts to a JSON file safely.
- **`library.py`** — the only place business rules live (e.g. "you can't
  issue a book with zero available copies"). This is the layer a GUI or
  a REST API could reuse as-is.
- **`cli.py`** — purely presentation: prompts the user, calls `Library`,
  and prints results.

## Requirements

- Python 3.8 or later
- No third-party packages are required to run the app (only the standard
  library is used). `pytest` is listed in `requirements.txt` as an
  optional, nicer test runner.

## Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/library-management-system.git
cd library-management-system

# 2. (Optional) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. (Optional) install dev/test dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
```

On first run, the app creates a `data/` folder containing `books.json`,
`members.json`, and `issues.json`. All changes you make in the menu are
saved to these files immediately, so your library persists between runs.

## Usage

Running `python main.py` opens a numbered menu:

```
============================================================
               LIBRARY MANAGEMENT SYSTEM
============================================================
 Book Management
   1. Add Book            2. Update Book
   3. Delete Book          4. List All Books
   5. Search / Filter Books

 Member Management
   6. Add Member           7. Update Member
   8. Delete Member        9. List All Members
  10. Search Members

 Issue / Return
  11. Issue Book          12. Return Book
  13. Currently Issued    14. Overdue Books

 Reports
  15. Library Statistics

   0. Exit
============================================================
```

Enter the number of the action you want and follow the prompts. Every
action is wrapped in exception handling, so typos or invalid input (a
duplicate ISBN, a missing member, trying to return a book that was never
issued, etc.) print a clear message instead of crashing the program.

### Example session

```
Choose an option: 1
Add a New Book
ISBN: 978-0132350884
Title: Clean Code
Author: Robert C. Martin
Category [General]: Programming
Number of copies [1]: 2

Book added successfully:
  [978-0132350884] Clean Code by Robert C. Martin (Programming) - 2/2 available
```

```
Choose an option: 11
Issue a Book
Book ISBN: 978-0132350884
Member ID: M1

Book issued. Due back by 2026-09-02.
  [79dd3b67] ISBN 978-0132350884 -> Member M1 | issued 2026-08-19, due 2026-09-02, OUTSTANDING
```

## Business Rules

- A book cannot be issued if it has zero available copies
  (`BookNotAvailableError`).
- A member cannot borrow the same book twice at the same time
  (`BookAlreadyIssuedToMemberError`).
- A member cannot exceed their configured `max_books` limit
  (`MembershipLimitExceededError`).
- Returning a book that was never issued (or already returned) to that
  member raises `NoActiveIssueRecordError`.
- Books/members with an outstanding (unreturned) loan cannot be deleted,
  to keep the data consistent.
- Loans have a 14-day period; returning late accrues a fine of ₹5/day,
  computed automatically on return (and previewable on the "Overdue
  Books" screen before it's returned).

## Running the Tests

```bash
python -m unittest discover tests -v
# or, if you installed pytest:
python -m pytest tests/ -v
```

The test suite covers book/member CRUD, search/filter, the full
issue-and-return lifecycle, overdue fine calculation, and every custom
exception in the error hierarchy (18 tests total).

## Extending the Project

Because `Library` in `src/library.py` has no dependency on the CLI, it can
be reused directly by:

- A GUI (e.g. Tkinter or PyQt) that calls the same `Library` methods.
- A REST API (e.g. Flask/FastAPI) exposing `add_book`, `issue_book`, etc.
  as HTTP endpoints.
- A different storage backend (e.g. swap `JSONStorage` for a SQLite-backed
  class) without touching business logic, since `library.py` only talks
  to the storage layer through `load()`/`save()`.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).
