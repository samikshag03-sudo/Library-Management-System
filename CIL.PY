"""
Menu-driven command-line interface for the Library Management System.

This module is intentionally kept separate from `library.py`: the CLI is
just one possible front end. All business rules and validation live in
Library / models, so a GUI or web API could reuse the same core untouched.
"""

from .library import Library
from .exceptions import LibraryError


DIVIDER = "-" * 60


def prompt(text, required=True):
    while True:
        value = input(text).strip()
        if value or not required:
            return value
        print("  This field is required. Please try again.")


def prompt_int(text, default=None):
    raw = input(text).strip()
    if not raw and default is not None:
        return default
    try:
        return int(raw)
    except ValueError:
        raise ValueError(f"'{raw}' is not a valid whole number.")


# --------------------------------------------------------------- BOOKS ----
def menu_add_book(lib: Library):
    print(DIVIDER, "\nAdd a New Book")
    isbn = prompt("ISBN: ")
    title = prompt("Title: ")
    author = prompt("Author: ")
    category = prompt("Category [General]: ", required=False) or "General"
    copies = prompt_int("Number of copies [1]: ", default=1)
    book = lib.add_book(isbn, title, author, category, copies)
    print(f"\nBook added successfully:\n  {book}")


def menu_update_book(lib: Library):
    print(DIVIDER, "\nUpdate a Book")
    isbn = prompt("ISBN of book to update: ")
    print("Leave a field blank to keep its current value.")
    title = prompt("New title: ", required=False)
    author = prompt("New author: ", required=False)
    category = prompt("New category: ", required=False)
    copies_raw = input("New total copies: ").strip()
    fields = {}
    if title:
        fields["title"] = title
    if author:
        fields["author"] = author
    if category:
        fields["category"] = category
    if copies_raw:
        fields["total_copies"] = int(copies_raw)
    book = lib.update_book(isbn, **fields)
    print(f"\nBook updated:\n  {book}")


def menu_delete_book(lib: Library):
    print(DIVIDER, "\nDelete a Book")
    isbn = prompt("ISBN of book to delete: ")
    lib.delete_book(isbn)
    print(f"\nBook '{isbn}' deleted.")


def menu_search_books(lib: Library):
    print(DIVIDER, "\nSearch / Filter Books")
    keyword = prompt("Keyword (title/author/ISBN, blank for all): ", required=False)
    category = prompt("Filter by category (blank for any): ", required=False)
    only_avail = prompt("Show only available copies? (y/N): ", required=False).lower() == "y"
    results = lib.search_books(keyword, category or None, only_avail)
    print_books(results)


def menu_list_books(lib: Library):
    print(DIVIDER, "\nAll Books")
    print_books(lib.list_books())


def print_books(books):
    if not books:
        print("No books found.")
        return
    for b in books:
        print(f"  {b}")


# ------------------------------------------------------------- MEMBERS ----
def menu_add_member(lib: Library):
    print(DIVIDER, "\nAdd a New Member")
    member_id = prompt("Member ID: ")
    name = prompt("Name: ")
    email = prompt("Email: ")
    phone = prompt("Phone (optional): ", required=False)
    max_books = prompt_int("Max books allowed [3]: ", default=3)
    member = lib.add_member(member_id, name, email, phone, max_books)
    print(f"\nMember added successfully:\n  {member}")


def menu_update_member(lib: Library):
    print(DIVIDER, "\nUpdate a Member")
    member_id = prompt("Member ID to update: ")
    print("Leave a field blank to keep its current value.")
    name = prompt("New name: ", required=False)
    email = prompt("New email: ", required=False)
    phone = prompt("New phone: ", required=False)
    fields = {}
    if name:
        fields["name"] = name
    if email:
        fields["email"] = email
    if phone:
        fields["phone"] = phone
    member = lib.update_member(member_id, **fields)
    print(f"\nMember updated:\n  {member}")


def menu_delete_member(lib: Library):
    print(DIVIDER, "\nDelete a Member")
    member_id = prompt("Member ID to delete: ")
    lib.delete_member(member_id)
    print(f"\nMember '{member_id}' deleted.")


def menu_search_members(lib: Library):
    print(DIVIDER, "\nSearch Members")
    keyword = prompt("Keyword (name/email/ID, blank for all): ", required=False)
    results = lib.search_members(keyword)
    print_members(results)


def menu_list_members(lib: Library):
    print(DIVIDER, "\nAll Members")
    print_members(lib.list_members())


def print_members(members):
    if not members:
        print("No members found.")
        return
    for m in members:
        print(f"  {m}")


# --------------------------------------------------------- ISSUE/RETURN ---
def menu_issue_book(lib: Library):
    print(DIVIDER, "\nIssue a Book")
    isbn = prompt("Book ISBN: ")
    member_id = prompt("Member ID: ")
    record = lib.issue_book(isbn, member_id)
    print(f"\nBook issued. Due back by {record.due_date}.\n  {record}")


def menu_return_book(lib: Library):
    print(DIVIDER, "\nReturn a Book")
    isbn = prompt("Book ISBN: ")
    member_id = prompt("Member ID: ")
    record = lib.return_book(isbn, member_id)
    if record.fine > 0:
        print(f"\nBook returned. This return was late: fine = {record.fine:.2f}")
    else:
        print("\nBook returned on time. No fine due.")


def menu_active_issues(lib: Library):
    print(DIVIDER, "\nCurrently Issued Books")
    member_id = prompt("Filter by member ID (blank for all): ", required=False)
    records = lib.list_active_issues(member_id or None)
    if not records:
        print("No books are currently issued.")
    for r in records:
        print(f"  {r}")


def menu_overdue(lib: Library):
    print(DIVIDER, "\nOverdue Books")
    records = lib.list_overdue()
    if not records:
        print("Nothing is overdue. Nice!")
    for r in records:
        fine = r.compute_fine()
        print(f"  {r}  (fine so far: {fine:.2f})")


# -------------------------------------------------------------- REPORTS ---
def menu_stats(lib: Library):
    print(DIVIDER, "\nLibrary Statistics")
    for key, value in lib.stats().items():
        label = key.replace("_", " ").capitalize()
        print(f"  {label}: {value}")


MENU = """
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
"""

ACTIONS = {
    "1": menu_add_book,
    "2": menu_update_book,
    "3": menu_delete_book,
    "4": menu_list_books,
    "5": menu_search_books,
    "6": menu_add_member,
    "7": menu_update_member,
    "8": menu_delete_member,
    "9": menu_list_members,
    "10": menu_search_members,
    "11": menu_issue_book,
    "12": menu_return_book,
    "13": menu_active_issues,
    "14": menu_overdue,
    "15": menu_stats,
}


def run(data_dir: str = "data"):
    lib = Library(data_dir=data_dir)
    print("Welcome! Your data is saved automatically to the 'data/' folder.")

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        action = ACTIONS.get(choice)
        if not action:
            print("Invalid option. Please choose a number from the menu.")
            continue

        try:
            action(lib)
        except LibraryError as exc:
            # All expected, "business rule" failures (book not found,
            # duplicate ISBN, no copies available, etc.) land here with a
            # clear, user-facing message.
            print(f"\n[Error] {exc}")
        except ValueError as exc:
            print(f"\n[Invalid input] {exc}")
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as exc:  # noqa: BLE001 - last-resort safety net
            # Anything unexpected is caught here too, so the whole program
            # never crashes on the user mid-session and data stays intact.
            print(f"\n[Unexpected error] {type(exc).__name__}: {exc}")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    run()
