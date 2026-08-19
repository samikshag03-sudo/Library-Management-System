"""
Builds the Project Report PDF for the Library Management System.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Preformatted, ListFlowable, ListItem, HRFlowable
)
from reportlab.pdfbase.pdfmetrics import stringWidth

PROJECT_DIR = "/home/claude/library-management-system"
OUT_PATH = "/mnt/user-data/outputs/Library_Management_System_Project_Report.pdf"

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(name="TitleBig", fontName="Helvetica-Bold", fontSize=26,
                           leading=32, alignment=TA_CENTER, spaceAfter=10,
                           textColor=colors.HexColor("#1a3c6e")))
styles.add(ParagraphStyle(name="SubTitle", fontName="Helvetica", fontSize=14,
                           leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#444444"),
                           spaceAfter=6))
styles.add(ParagraphStyle(name="H1", fontName="Helvetica-Bold", fontSize=17,
                           leading=21, spaceBefore=18, spaceAfter=8,
                           textColor=colors.HexColor("#1a3c6e")))
styles.add(ParagraphStyle(name="H2", fontName="Helvetica-Bold", fontSize=13,
                           leading=17, spaceBefore=12, spaceAfter=6,
                           textColor=colors.HexColor("#2a5599")))
styles.add(ParagraphStyle(name="BodyJust", fontName="Helvetica", fontSize=10.3,
                           leading=15, alignment=TA_JUSTIFY, spaceAfter=8))
styles.add(ParagraphStyle(name="BulletText", fontName="Helvetica", fontSize=10.3,
                           leading=14.5, alignment=TA_LEFT))
styles.add(ParagraphStyle(name="Code", fontName="Courier", fontSize=7.6,
                           leading=9.6, backColor=colors.HexColor("#f4f6f8"),
                           borderPadding=6, spaceAfter=10))
styles.add(ParagraphStyle(name="Caption", fontName="Helvetica-Oblique", fontSize=9,
                           alignment=TA_CENTER, textColor=colors.HexColor("#666666"),
                           spaceAfter=10))

story = []

# ------------------------------------------------------------- COVER PAGE
story.append(Spacer(1, 4*cm))
story.append(Paragraph("Library Management System", styles["TitleBig"]))
story.append(Paragraph("A Python Console Application for Managing Books, Members,<br/>"
                        "and Book Issue &amp; Return Records", styles["SubTitle"]))
story.append(Spacer(1, 1*cm))
story.append(HRFlowable(width="60%", thickness=1, color=colors.HexColor("#1a3c6e"),
                         hAlign="CENTER"))
story.append(Spacer(1, 1*cm))
story.append(Paragraph("Project Report", styles["SubTitle"]))
story.append(Spacer(1, 4*cm))

meta_data = [
    ["Project Title", "Library Management System"],
    ["Language / Platform", "Python 3.8+ (Standard Library only)"],
    ["Project Type", "Console-based (CLI) application"],
    ["Data Storage", "JSON files (books.json, members.json, issues.json)"],
    ["Repository", "Public GitHub Repository"],
    ["Report Date", "August 19, 2026"],
]
t = Table(meta_data, colWidths=[5.5*cm, 9.5*cm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
    ("FONTSIZE", (0, 0), (-1, -1), 10),
    ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#1a3c6e")),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ("TOPPADDING", (0, 0), (-1, -1), 7),
    ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
]))
story.append(t)
story.append(PageBreak())

# ------------------------------------------------------------- TOC (manual)
story.append(Paragraph("Table of Contents", styles["H1"]))
toc_items = [
    "1. Abstract",
    "2. Introduction",
    "3. Objectives",
    "4. System Requirements",
    "5. System Design & Architecture",
    "6. Modules Description",
    "7. Data Model",
    "8. Key Features & Functionality",
    "9. Exception Handling Strategy",
    "10. Data Storage Design",
    "11. Testing",
    "12. Sample Run / Output",
    "13. Source Code (Key Modules)",
    "14. Limitations & Future Scope",
    "15. Conclusion",
    "16. References",
]
story.append(ListFlowable(
    [ListItem(Paragraph(item, styles["BulletText"]), spaceAfter=4) for item in toc_items],
    bulletType="bullet", start="circle", leftIndent=14
))
story.append(PageBreak())

# ------------------------------------------------------------- 1. ABSTRACT
story.append(Paragraph("1. Abstract", styles["H1"]))
story.append(Paragraph(
    "Libraries, whether in schools, colleges, or community centres, need a reliable way to "
    "track their book collection, their members, and who currently holds which book. This "
    "project, the <b>Library Management System</b>, is a Python console application that "
    "digitizes these day-to-day operations. It allows a librarian to add, update, delete, "
    "and search books and members; issue and return books with automatic due-date and "
    "fine calculation; and view real-time statistics about the library's collection. "
    "The system stores all data persistently in JSON files, so records survive between "
    "program runs without requiring a database server. A dedicated exception-handling "
    "layer ensures the application degrades gracefully on invalid input or unexpected "
    "conditions instead of crashing, making it suitable for non-technical end users.",
    styles["BodyJust"]))

# ------------------------------------------------------------- 2. INTRO
story.append(Paragraph("2. Introduction", styles["H1"]))
story.append(Paragraph(
    "Manual, paper-based library record keeping is slow and error-prone: it is hard to "
    "know at a glance which books are available, which members have overdue books, or "
    "how many copies of a title remain. This project addresses that problem by providing "
    "a structured, menu-driven application that centralises book records, member records, "
    "and lending history in one place. The system is built with a clear separation between "
    "its user interface (a text menu), its business logic (validation and lending rules), "
    "and its storage layer (JSON files), which mirrors the layered architecture used in "
    "professional software and makes the codebase easy to extend &mdash; for example, "
    "swapping the console menu for a web interface, or the JSON files for a proper "
    "database, without rewriting the core logic.",
    styles["BodyJust"]))

# ------------------------------------------------------------- 3. OBJECTIVES
story.append(Paragraph("3. Objectives", styles["H1"]))
objectives = [
    "Provide full CRUD (Create, Read, Update, Delete) operations for books and members.",
    "Allow books to be issued to and returned by members, enforcing sensible lending rules.",
    "Automatically calculate late-return fines based on a configurable loan period.",
    "Provide keyword and category-based search/filter for books, and keyword search for members.",
    "Persist all data between program runs using a lightweight, human-readable storage format.",
    "Handle invalid input and error conditions gracefully via a custom exception hierarchy, "
    "so the application never crashes on bad user input.",
    "Keep the codebase modular and well-tested so it can be extended (GUI, web API, database "
    "backend) without reworking core logic.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(o, styles["BulletText"]), spaceAfter=5) for o in objectives],
    bulletType="bullet", leftIndent=14
))

# ------------------------------------------------------------- 4. REQUIREMENTS
story.append(Paragraph("4. System Requirements", styles["H1"]))
story.append(Paragraph("Software Requirements", styles["H2"]))
req_table = [
    ["Component", "Requirement"],
    ["Programming Language", "Python 3.8 or later"],
    ["Libraries Used", "json, dataclasses, uuid, datetime, os, shutil, tempfile, unittest (all standard library)"],
    ["Operating System", "Windows, macOS, or Linux (cross-platform)"],
    ["IDE / Editor", "Any (VS Code, PyCharm, or a plain terminal)"],
    ["Version Control", "Git, hosted on GitHub"],
]
rt = Table(req_table, colWidths=[5*cm, 10*cm])
rt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3c6e")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (0, 1), (0, -1), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.5),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f6f8")]),
]))
story.append(rt)
story.append(Paragraph("Hardware Requirements", styles["H2"]))
story.append(Paragraph(
    "No special hardware is required. The application runs comfortably on any machine "
    "capable of running Python 3 (minimal CPU/RAM/disk footprint, no GPU or network "
    "connection needed for core functionality).", styles["BodyJust"]))

story.append(PageBreak())

# ------------------------------------------------------------- 5. ARCHITECTURE
story.append(Paragraph("5. System Design &amp; Architecture", styles["H1"]))
story.append(Paragraph(
    "The application follows a three-layer architecture, which keeps concerns cleanly "
    "separated and makes the system easier to test, maintain, and extend:", styles["BodyJust"]))

arch_rows = [
    ["Layer", "Module(s)", "Responsibility"],
    ["Presentation", "src/cli.py", "Displays the menu, reads user input, calls the Library "
     "layer, and prints results/errors. Contains no business rules."],
    ["Business Logic", "src/library.py, src/models.py", "Validates input, enforces lending "
     "rules (availability, duplicate loans, member limits), computes fines, and coordinates "
     "the data models with storage."],
    ["Persistence", "src/storage.py", "Reads/writes JSON files atomically (via a temp file "
     "+ rename) so data is never left in a corrupted state."],
]
at = Table(arch_rows, colWidths=[3.1*cm, 4.6*cm, 7.3*cm])
at.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3c6e")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cccccc")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f6f8")]),
]))
story.append(at)
story.append(Spacer(1, 10))

story.append(Paragraph("Data Flow", styles["H2"]))
story.append(Paragraph(
    "User Input (CLI) &rarr; Library (validation &amp; business rules) &rarr; Models "
    "(Book / Member / IssueRecord) &rarr; JSONStorage (load/save) &rarr; JSON files on disk. "
    "Every write goes back through the same path in reverse to confirm the change and "
    "reflect it back to the user.", styles["BodyJust"]))

story.append(Paragraph("Project Directory Structure", styles["H2"]))
tree = """library-management-system/
├── main.py                 # Entry point
├── src/
│   ├── models.py            # Book, Member, IssueRecord data classes
│   ├── exceptions.py        # Custom exception hierarchy
│   ├── storage.py           # JSON persistence layer (atomic writes)
│   ├── library.py           # Core business logic
│   └── cli.py                # Menu-driven command-line interface
├── data/                    # books.json, members.json, issues.json
├── tests/
│   └── test_library.py      # 18 unit tests
├── requirements.txt
├── README.md
└── LICENSE"""
story.append(Preformatted(tree, styles["Code"]))

story.append(PageBreak())

# ------------------------------------------------------------- 6. MODULES
story.append(Paragraph("6. Modules Description", styles["H1"]))

modules = [
    ("models.py", "Defines three dataclasses: <b>Book</b> (isbn, title, author, category, "
     "total_copies, available_copies, added_on), <b>Member</b> (member_id, name, email, "
     "phone, joined_on, max_books), and <b>IssueRecord</b> (record_id, isbn, member_id, "
     "issue_date, due_date, return_date, fine). Each has to_dict()/from_dict() helpers for "
     "JSON serialization and a compute_fine() method on IssueRecord that calculates late "
     "fees based on a 14-day loan period and a per-day fine rate."),
    ("exceptions.py", "Defines a hierarchy rooted at LibraryError, with subtrees for book "
     "errors (BookNotFoundError, DuplicateISBNError, BookNotAvailableError, "
     "InvalidBookDataError), member errors (MemberNotFoundError, DuplicateMemberError, "
     "MembershipLimitExceededError, InvalidMemberDataError), issuing errors "
     "(BookAlreadyIssuedToMemberError, NoActiveIssueRecordError), and StorageError for "
     "file I/O problems."),
    ("storage.py", "A generic JSONStorage class that loads and saves a list of records to a "
     "JSON file. Writes are atomic: data is first written to a temporary file in the same "
     "directory and then moved into place, so an interrupted write (e.g. power loss) can "
     "never leave a half-written, corrupted data file."),
    ("library.py", "The core of the application. The Library class exposes methods such as "
     "add_book, update_book, delete_book, search_books, add_member, update_member, "
     "delete_member, search_members, issue_book, return_book, list_active_issues, "
     "list_overdue, and stats. It validates all input, enforces every business rule, and is "
     "the only layer that talks to both the models and the storage layer."),
    ("cli.py", "Implements the interactive text menu. Each menu option maps to a small "
     "function (e.g. menu_add_book) that prompts for the needed fields, calls the matching "
     "Library method, and prints a friendly confirmation or error. The main run() loop wraps "
     "every action in try/except so no single bad input can crash the whole session."),
    ("main.py", "The application's entry point &mdash; simply configures the data directory "
     "and calls cli.run()."),
]
for name, desc in modules:
    story.append(Paragraph(f"<b>{name}</b>", styles["H2"]))
    story.append(Paragraph(desc, styles["BodyJust"]))

story.append(PageBreak())

# ------------------------------------------------------------- 7. DATA MODEL
story.append(Paragraph("7. Data Model", styles["H1"]))

def field_table(title, rows):
    story.append(Paragraph(title, styles["H2"]))
    tt = Table([["Field", "Type", "Description"]] + rows, colWidths=[3.3*cm, 2.3*cm, 9.4*cm])
    tt.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2a5599")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f6f8")]),
    ]))
    story.append(tt)
    story.append(Spacer(1, 10))

field_table("Book", [
    ["isbn", "str", "Unique identifier for the title (primary key)."],
    ["title", "str", "Book title."],
    ["author", "str", "Author name."],
    ["category", "str", "Genre / subject category (default: 'General')."],
    ["total_copies", "int", "Total copies the library owns."],
    ["available_copies", "int", "Copies currently on the shelf (not issued)."],
    ["added_on", "str (ISO date)", "Date the title was added to the catalogue."],
])
field_table("Member", [
    ["member_id", "str", "Unique identifier for the member (primary key)."],
    ["name", "str", "Full name."],
    ["email", "str", "Contact e-mail (validated for a basic '@' + domain format)."],
    ["phone", "str", "Optional contact number."],
    ["joined_on", "str (ISO date)", "Date the member registered."],
    ["max_books", "int", "Maximum books this member may hold at once (default 3)."],
])
field_table("IssueRecord", [
    ["record_id", "str", "Unique identifier for this loan transaction."],
    ["isbn", "str", "The book issued."],
    ["member_id", "str", "The member who borrowed it."],
    ["issue_date", "str (ISO date)", "Date issued."],
    ["due_date", "str (ISO date)", "issue_date + 14 days."],
    ["return_date", "str (ISO date) / null", "Set when the book is returned; null while outstanding."],
    ["fine", "float", "Late fee, computed at return time (₹5/day overdue)."],
])

story.append(PageBreak())

# ------------------------------------------------------------- 8. FEATURES
story.append(Paragraph("8. Key Features &amp; Functionality", styles["H1"]))

feature_sections = [
    ("Book Management", [
        "Add a book with ISBN, title, author, category, and number of copies.",
        "Update a book's title, author, category, or total copy count.",
        "Delete a book (blocked automatically while a copy is on loan).",
        "List every book currently in the catalogue.",
    ]),
    ("Member Management", [
        "Register a member with a unique ID, name, e-mail (validated), phone, and a "
        "configurable borrowing limit.",
        "Update a member's contact details.",
        "Delete a member (blocked automatically while they hold an unreturned book).",
        "List every registered member.",
    ]),
    ("Issue &amp; Return Books", [
        "Issue a book to a member, provided a copy is available, the member does not already "
        "hold that title, and the member has not reached their borrowing limit.",
        "A 14-day due date is calculated automatically at issue time.",
        "Return a book, which restores the available copy count and computes any late fine "
        "(₹5 per day overdue) automatically.",
        "View all currently issued (outstanding) books, optionally filtered by member.",
        "View overdue books with their running fine, before they are returned.",
    ]),
    ("Search &amp; Filter", [
        "Search books by keyword across title, author, and ISBN, optionally combined with a "
        "category filter and an 'available only' filter.",
        "Search members by keyword across name, e-mail, and member ID.",
    ]),
    ("Data Storage", [
        "All data is stored as JSON under data/books.json, data/members.json, and "
        "data/issues.json.",
        "Writes are atomic (temp file + rename) so the data files cannot be left corrupted "
        "by an interrupted write.",
        "JSON was chosen over a database for this project because it keeps the system "
        "dependency-free, human-readable, and easy to inspect or back up, while the storage "
        "layer is abstracted so it could be swapped for SQLite/PostgreSQL later without "
        "touching business logic.",
    ]),
    ("Exception Handling", [
        "A dedicated exception hierarchy makes every failure mode explicit and catchable "
        "(e.g. DuplicateISBNError, BookNotAvailableError, MembershipLimitExceededError).",
        "The CLI's main loop wraps every menu action in try/except so invalid input, business "
        "rule violations, or unexpected errors are shown as a friendly message rather than a "
        "raw Python traceback &mdash; the application never crashes mid-session.",
        "Input validation (empty fields, non-numeric copy counts, malformed e-mails) is "
        "handled before any data is written.",
    ]),
    ("Reports", [
        "A statistics screen reports total titles, total and available copies, total "
        "members, currently issued books, and overdue books, computed live from the stored "
        "data.",
    ]),
]
for heading, items in feature_sections:
    story.append(Paragraph(heading, styles["H2"]))
    story.append(ListFlowable(
        [ListItem(Paragraph(i, styles["BulletText"]), spaceAfter=4) for i in items],
        bulletType="bullet", leftIndent=14
    ))

story.append(PageBreak())

# ------------------------------------------------------------- 9. EXCEPTION HANDLING
story.append(Paragraph("9. Exception Handling Strategy", styles["H1"]))
story.append(Paragraph(
    "Rather than relying on generic exceptions, the project defines a purpose-built "
    "hierarchy in <font face='Courier'>exceptions.py</font>, rooted at "
    "<font face='Courier'>LibraryError</font>. This lets the CLI layer catch <i>all</i> "
    "expected business-rule failures with a single except clause while still preserving a "
    "precise, descriptive message for the user:", styles["BodyJust"]))

exc_tree = """LibraryError
├── BookError
│   ├── BookNotFoundError
│   ├── DuplicateISBNError
│   ├── BookNotAvailableError
│   └── InvalidBookDataError
├── MemberError
│   ├── MemberNotFoundError
│   ├── DuplicateMemberError
│   ├── MembershipLimitExceededError
│   └── InvalidMemberDataError
├── IssueError
│   ├── BookAlreadyIssuedToMemberError
│   └── NoActiveIssueRecordError
└── StorageError"""
story.append(Preformatted(exc_tree, styles["Code"]))

story.append(Paragraph(
    "In <font face='Courier'>cli.py</font>, the main loop applies a three-tier catch: "
    "<font face='Courier'>LibraryError</font> for expected business failures, "
    "<font face='Courier'>ValueError</font> for basic input-parsing issues (e.g. a "
    "non-numeric copy count), and a final broad <font face='Courier'>Exception</font> "
    "handler as a last-resort safety net so that no unforeseen error can ever terminate the "
    "program. In every case the user sees a clear message and the menu simply loops back, "
    "with all previously saved data left untouched.", styles["BodyJust"]))

# ------------------------------------------------------------- 10. STORAGE DESIGN
story.append(Paragraph("10. Data Storage Design", styles["H1"]))
story.append(Paragraph(
    "Each entity type is stored in its own JSON file as a list of objects. "
    "The JSONStorage class centralises all file I/O and guarantees atomic writes: data is "
    "first serialized to a temporary file in the same directory, and only once that write "
    "succeeds is the temporary file renamed over the real data file "
    "(os.replace-equivalent via shutil.move). This means that even if the process is "
    "killed mid-save, the original data file is left completely intact.", styles["BodyJust"]))
story.append(Paragraph("Example: data/books.json", styles["H2"]))
sample_json = """[
  {
    "isbn": "978-0132350884",
    "title": "Clean Code",
    "author": "Robert C. Martin",
    "category": "Programming",
    "total_copies": 2,
    "available_copies": 1,
    "added_on": "2026-08-19"
  }
]"""
story.append(Preformatted(sample_json, styles["Code"]))

story.append(PageBreak())

# ------------------------------------------------------------- 11. TESTING
story.append(Paragraph("11. Testing", styles["H1"]))
story.append(Paragraph(
    "The project includes an automated unit test suite in "
    "<font face='Courier'>tests/test_library.py</font>, built on Python's built-in "
    "<font face='Courier'>unittest</font> framework (also runnable with pytest). Each test "
    "runs against a fresh, isolated temporary data directory, so tests never interfere with "
    "each other or with real library data. All 18 tests pass.", styles["BodyJust"]))

test_rows = [
    ["#", "Test", "Verifies"],
    ["1", "test_add_and_get_book", "A book can be added and retrieved by ISBN."],
    ["2", "test_duplicate_isbn_rejected", "Adding a duplicate ISBN raises DuplicateISBNError."],
    ["3", "test_invalid_book_data_rejected", "Empty fields / zero copies raise InvalidBookDataError."],
    ["4", "test_get_missing_book_raises", "Looking up a non-existent ISBN raises BookNotFoundError."],
    ["5", "test_delete_book", "A book can be deleted and is then no longer retrievable."],
    ["6", "test_search_books_by_keyword_and_category", "Keyword and category filters return correct subsets."],
    ["7", "test_add_member", "A member can be registered."],
    ["8", "test_duplicate_member_rejected", "Duplicate member IDs raise DuplicateMemberError."],
    ["9", "test_invalid_email_rejected", "A malformed e-mail raises InvalidMemberDataError."],
    ["10", "test_get_missing_member_raises", "Unknown member ID raises MemberNotFoundError."],
    ["11", "test_issue_and_return_book", "Full issue -> return cycle updates available copies correctly."],
    ["12", "test_cannot_issue_unavailable_book", "Issuing with zero copies left raises BookNotAvailableError."],
    ["13", "test_cannot_issue_same_book_twice_to_same_member", "Duplicate active loan raises BookAlreadyIssuedToMemberError."],
    ["14", "test_membership_limit_enforced", "Exceeding max_books raises MembershipLimitExceededError."],
    ["15", "test_return_without_active_issue_raises", "Returning a book never issued raises NoActiveIssueRecordError."],
    ["16", "test_overdue_fine_calculation", "Fine = days late x rate, computed correctly."],
    ["17", "test_cannot_delete_book_with_outstanding_loan", "Deleting a book on loan is blocked."],
    ["18", "test_stats", "Aggregate statistics reflect current data accurately."],
]
tt = Table(test_rows, colWidths=[0.9*cm, 6.3*cm, 7.8*cm])
tt.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a3c6e")),
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    ("FONTNAME", (1, 1), (1, -1), "Courier"),
    ("FONTSIZE", (0, 0), (-1, -1), 8),
    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("TOPPADDING", (0, 0), (-1, -1), 4.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4.5),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f6f8")]),
]))
story.append(tt)
story.append(Spacer(1, 10))
story.append(Paragraph("Run with: <font face='Courier'>python -m unittest discover tests -v</font> "
                        "&nbsp;or&nbsp; <font face='Courier'>python -m pytest tests/ -v</font>. "
                        "Result: <b>Ran 18 tests in 0.02s — OK</b>.", styles["BodyJust"]))

story.append(PageBreak())

# ------------------------------------------------------------- 12. SAMPLE RUN
story.append(Paragraph("12. Sample Run / Output", styles["H1"]))
story.append(Paragraph("Adding a book:", styles["H2"]))
story.append(Preformatted(
"""Choose an option: 1
Add a New Book
ISBN: 978-0132350884
Title: Clean Code
Author: Robert C. Martin
Category [General]: Programming
Number of copies [1]: 2

Book added successfully:
  [978-0132350884] Clean Code by Robert C. Martin (Programming) - 2/2 available""",
    styles["Code"]))

story.append(Paragraph("Issuing a book:", styles["H2"]))
story.append(Preformatted(
"""Choose an option: 11
Issue a Book
Book ISBN: 978-0132350884
Member ID: M1

Book issued. Due back by 2026-09-02.
  [79dd3b67] ISBN 978-0132350884 -> Member M1 | issued 2026-08-19, due 2026-09-02, OUTSTANDING""",
    styles["Code"]))

story.append(Paragraph("Handling an error gracefully (duplicate ISBN):", styles["H2"]))
story.append(Preformatted(
"""Choose an option: 1
Add a New Book
ISBN: 978-0132350884
Title: Clean Code (2nd copy attempt)
Author: Robert C. Martin
Category [General]:
Number of copies [1]:

[Error] A book with ISBN '978-0132350884' already exists.

Press Enter to continue...""",
    styles["Code"]))

story.append(Paragraph("Library statistics report:", styles["H2"]))
story.append(Preformatted(
"""Choose an option: 15
Library Statistics
  Total titles: 1
  Total copies: 2
  Available copies: 1
  Total members: 1
  Books currently issued: 1
  Overdue books: 0""",
    styles["Code"]))

story.append(PageBreak())

# ------------------------------------------------------------- 13. SOURCE CODE
story.append(Paragraph("13. Source Code (Key Modules)", styles["H1"]))
story.append(Paragraph(
    "The complete, runnable source code is included in the accompanying GitHub repository "
    "and project archive. The core modules are reproduced below for reference.",
    styles["BodyJust"]))

code_files = [
    ("src/exceptions.py", "src/exceptions.py"),
    ("src/models.py", "src/models.py"),
    ("src/storage.py", "src/storage.py"),
    ("src/library.py", "src/library.py"),
    ("src/cli.py", "src/cli.py"),
    ("main.py", "main.py"),
]

def make_code_flowables(code_text, max_chars_per_line=98):
    """Wrap long lines so they don't overflow the page width."""
    lines = code_text.split("\n")
    wrapped = []
    for line in lines:
        if len(line) <= max_chars_per_line:
            wrapped.append(line)
        else:
            while len(line) > max_chars_per_line:
                wrapped.append(line[:max_chars_per_line])
                line = "    " + line[max_chars_per_line:]
            wrapped.append(line)
    return "\n".join(wrapped)

for label, relpath in code_files:
    story.append(Paragraph(label, styles["H2"]))
    full_path = os.path.join(PROJECT_DIR, relpath)
    with open(full_path, "r", encoding="utf-8") as f:
        code = f.read()
    code = make_code_flowables(code)
    story.append(Preformatted(code, styles["Code"]))
    story.append(PageBreak())

# ------------------------------------------------------------- 14. LIMITATIONS
story.append(Paragraph("14. Limitations &amp; Future Scope", styles["H1"]))
story.append(Paragraph("Current Limitations", styles["H2"]))
limits = [
    "Single-user, local console application &mdash; no concurrent multi-user access or "
    "network access.",
    "JSON file storage is well-suited to small/medium libraries but is not optimized for "
    "very large catalogues (tens of thousands of records) the way a relational database "
    "would be.",
    "No authentication/authorization layer (any user running the program has full access).",
    "Fine amount and loan period are constants in the code rather than configurable at "
    "runtime.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(i, styles["BulletText"]), spaceAfter=4) for i in limits],
    bulletType="bullet", leftIndent=14
))
story.append(Paragraph("Future Scope", styles["H2"]))
future = [
    "Add a graphical user interface (Tkinter, PyQt) or a web front end, reusing the same "
    "Library business-logic class unchanged.",
    "Migrate the storage layer to SQLite or PostgreSQL for larger datasets, again without "
    "touching business logic, since it only depends on the load()/save() interface.",
    "Add user authentication and role-based access (librarian vs. member self-service).",
    "Add e-mail/SMS notifications for due-soon and overdue books.",
    "Make the loan period and fine rate configurable via a settings file.",
    "Add CSV/PDF export of reports and a book cover-image lookup via an external API.",
]
story.append(ListFlowable(
    [ListItem(Paragraph(i, styles["BulletText"]), spaceAfter=4) for i in future],
    bulletType="bullet", leftIndent=14
))

# ------------------------------------------------------------- 15. CONCLUSION
story.append(Paragraph("15. Conclusion", styles["H1"]))
story.append(Paragraph(
    "The Library Management System successfully meets all the stated objectives: it "
    "provides complete book and member management, a rules-based issue/return workflow "
    "with automatic fine calculation, flexible search and filtering, durable JSON-based "
    "storage, and robust exception handling throughout. Its layered architecture keeps "
    "business rules isolated from both the user interface and the storage mechanism, which "
    "was validated by an 18-test automated suite covering every major code path and error "
    "condition. The result is a small but production-quality piece of software that is easy "
    "to run, easy to understand, and straightforward to extend with a GUI, a web API, or a "
    "full database backend in the future.",
    styles["BodyJust"]))

# ------------------------------------------------------------- 16. REFERENCES
story.append(Paragraph("16. References", styles["H1"]))
refs = [
    "Python Software Foundation. <i>Python 3 Documentation</i>. https://docs.python.org/3/",
    "Python Software Foundation. <i>dataclasses &mdash; Data Classes</i>. "
    "https://docs.python.org/3/library/dataclasses.html",
    "Python Software Foundation. <i>json &mdash; JSON encoder and decoder</i>. "
    "https://docs.python.org/3/library/json.html",
    "Python Software Foundation. <i>unittest &mdash; Unit testing framework</i>. "
    "https://docs.python.org/3/library/unittest.html",
    "Martin, Robert C. <i>Clean Code: A Handbook of Agile Software Craftsmanship</i>. "
    "Prentice Hall, 2008 (used as the sample data in this report).",
]
story.append(ListFlowable(
    [ListItem(Paragraph(r, styles["BulletText"]), spaceAfter=5) for r in refs],
    bulletType="bullet", leftIndent=14
))

# ---------------------------------------------------------------- BUILD
def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#888888"))
    canvas.drawCentredString(A4[0] / 2, 1.2 * cm, f"Page {doc.page}")
    canvas.drawString(2 * cm, 1.2 * cm, "Library Management System — Project Report")
    canvas.restoreState()


os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    topMargin=2*cm, bottomMargin=2*cm, leftMargin=2*cm, rightMargin=2*cm,
    title="Library Management System - Project Report",
    author="Library Management System Project",
)
doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
print("PDF written to", OUT_PATH)
