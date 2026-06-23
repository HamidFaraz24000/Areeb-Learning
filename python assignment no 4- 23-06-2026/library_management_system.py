import json
from datetime import datetime
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent
BOOKS_FILE = DATA_DIR / "books.json"
MEMBERS_FILE = DATA_DIR / "members.json"
BORROW_HISTORY_FILE = DATA_DIR / "borrow_history.json"


def load_json(file_path):
    """Load a JSON file. If it does not exist yet, start with an empty list."""
    if not file_path.exists():
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []


def save_json(file_path, data):
    """Save Python data into a JSON file."""
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def get_input(prompt, required=True):
    """Ask the user for input and optionally require a non-empty answer."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field cannot be empty.")


def get_positive_int(prompt):
    """Ask the user for a positive whole number."""
    while True:
        value = input(prompt).strip()
        try:
            number = int(value)
            if number >= 0:
                return number
            print("Please enter a number that is 0 or greater.")
        except ValueError:
            print("Please enter a valid whole number.")


def pause():
    input("\nPress Enter to continue...")


class LibrarySystem:
    def __init__(self):
        self.books = load_json(BOOKS_FILE)
        self.members = load_json(MEMBERS_FILE)
        self.borrow_history = load_json(BORROW_HISTORY_FILE)

    def save_all_data(self):
        save_json(BOOKS_FILE, self.books)
        save_json(MEMBERS_FILE, self.members)
        save_json(BORROW_HISTORY_FILE, self.borrow_history)

    def generate_id(self, records, prefix, id_key):
        highest_number = 0

        for record in records:
            record_id = str(record.get(id_key, ""))
            if record_id.startswith(prefix):
                number_part = record_id.replace(prefix, "", 1)
                if number_part.isdigit():
                    highest_number = max(highest_number, int(number_part))

        return f"{prefix}{highest_number + 1:03d}"

    def find_book_by_id(self, book_id):
        for book in self.books:
            if book["book_id"].lower() == book_id.lower():
                return book
        return None

    def find_member_by_id(self, member_id):
        for member in self.members:
            if member["member_id"].lower() == member_id.lower():
                return member
        return None

    def display_books(self, books=None):
        books = self.books if books is None else books

        if not books:
            print("No books found.")
            return

        print("\nBooks")
        print("-" * 95)
        print(f"{'ID':<8}{'Title':<25}{'Author':<20}{'Category':<15}{'Total':<8}{'Available':<10}")
        print("-" * 95)
        for book in books:
            print(
                f"{book['book_id']:<8}"
                f"{book['title']:<25}"
                f"{book['author']:<20}"
                f"{book['category']:<15}"
                f"{book['total_copies']:<8}"
                f"{book['available_copies']:<10}"
            )

    def display_members(self, members=None):
        members = self.members if members is None else members

        if not members:
            print("No members found.")
            return

        print("\nMembers")
        print("-" * 80)
        print(f"{'ID':<10}{'Name':<25}{'Phone':<18}{'Email':<25}")
        print("-" * 80)
        for member in members:
            print(
                f"{member['member_id']:<10}"
                f"{member['name']:<25}"
                f"{member['phone']:<18}"
                f"{member['email']:<25}"
            )

    def add_book(self):
        print("\nAdd New Book")
        title = get_input("Title: ")
        author = get_input("Author: ")
        category = get_input("Category: ")
        total_copies = get_positive_int("Total copies: ")

        book = {
            "book_id": self.generate_id(self.books, "B", "book_id"),
            "title": title,
            "author": author,
            "category": category,
            "total_copies": total_copies,
            "available_copies": total_copies,
        }

        self.books.append(book)
        self.save_all_data()
        print(f"Book added successfully. Book ID: {book['book_id']}")

    def search_books_by_title(self):
        title = get_input("Enter title to search: ")
        matches = [book for book in self.books if title.lower() in book["title"].lower()]
        self.display_books(matches)

    def search_books_by_author(self):
        author = get_input("Enter author to search: ")
        matches = [book for book in self.books if author.lower() in book["author"].lower()]
        self.display_books(matches)

    def update_book(self):
        book_id = get_input("Enter Book ID to update: ")
        book = self.find_book_by_id(book_id)

        if book is None:
            print("Book not found.")
            return

        borrowed_copies = book["total_copies"] - book["available_copies"]

        print("Leave a field blank to keep the current value.")
        title = get_input(f"Title [{book['title']}]: ", required=False)
        author = get_input(f"Author [{book['author']}]: ", required=False)
        category = get_input(f"Category [{book['category']}]: ", required=False)

        while True:
            total_text = get_input(f"Total copies [{book['total_copies']}]: ", required=False)
            if not total_text:
                new_total = book["total_copies"]
                break
            try:
                new_total = int(total_text)
                if new_total >= borrowed_copies:
                    break
                print(f"Total copies cannot be less than borrowed copies ({borrowed_copies}).")
            except ValueError:
                print("Please enter a valid whole number.")

        book["title"] = title or book["title"]
        book["author"] = author or book["author"]
        book["category"] = category or book["category"]
        book["total_copies"] = new_total
        book["available_copies"] = new_total - borrowed_copies

        self.save_all_data()
        print("Book updated successfully.")

    def delete_book(self):
        book_id = get_input("Enter Book ID to delete: ")
        book = self.find_book_by_id(book_id)

        if book is None:
            print("Book not found.")
            return

        if book["available_copies"] != book["total_copies"]:
            print("Cannot delete this book because some copies are currently borrowed.")
            return

        self.books.remove(book)
        self.save_all_data()
        print("Book deleted successfully.")

    def add_member(self):
        print("\nAdd New Member")
        name = get_input("Name: ")
        phone = get_input("Phone number: ")
        email = get_input("Email: ")

        member = {
            "member_id": self.generate_id(self.members, "M", "member_id"),
            "name": name,
            "phone": phone,
            "email": email,
        }

        self.members.append(member)
        self.save_all_data()
        print(f"Member added successfully. Member ID: {member['member_id']}")

    def search_members_by_name(self):
        name = get_input("Enter member name to search: ")
        matches = [member for member in self.members if name.lower() in member["name"].lower()]
        self.display_members(matches)

    def update_member(self):
        member_id = get_input("Enter Member ID to update: ")
        member = self.find_member_by_id(member_id)

        if member is None:
            print("Member not found.")
            return

        print("Leave a field blank to keep the current value.")
        name = get_input(f"Name [{member['name']}]: ", required=False)
        phone = get_input(f"Phone [{member['phone']}]: ", required=False)
        email = get_input(f"Email [{member['email']}]: ", required=False)

        member["name"] = name or member["name"]
        member["phone"] = phone or member["phone"]
        member["email"] = email or member["email"]

        self.save_all_data()
        print("Member updated successfully.")

    def delete_member(self):
        member_id = get_input("Enter Member ID to delete: ")
        member = self.find_member_by_id(member_id)

        if member is None:
            print("Member not found.")
            return

        active_borrow = self.find_active_borrow(member_id=member_id)
        if active_borrow is not None:
            print("Cannot delete this member because they still have a borrowed book.")
            return

        self.members.remove(member)
        self.save_all_data()
        print("Member deleted successfully.")

    def find_active_borrow(self, member_id=None, book_id=None):
        for record in self.borrow_history:
            if record["status"] != "Borrowed":
                continue

            member_matches = member_id is None or record["member_id"].lower() == member_id.lower()
            book_matches = book_id is None or record["book_id"].lower() == book_id.lower()

            if member_matches and book_matches:
                return record

        return None

    def borrow_book(self):
        member_id = get_input("Enter Member ID: ")
        member = self.find_member_by_id(member_id)

        if member is None:
            print("Member not found.")
            return

        book_id = get_input("Enter Book ID: ")
        book = self.find_book_by_id(book_id)

        if book is None:
            print("Book not found.")
            return

        if book["available_copies"] <= 0:
            print("This book is not available right now.")
            return

        record = {
            "borrow_id": self.generate_id(self.borrow_history, "BR", "borrow_id"),
            "book_id": book["book_id"],
            "book_title": book["title"],
            "member_id": member["member_id"],
            "member_name": member["name"],
            "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "return_date": "",
            "status": "Borrowed",
        }

        book["available_copies"] -= 1
        self.borrow_history.append(record)
        self.save_all_data()
        print("Book borrowed successfully.")

    def return_book(self):
        member_id = get_input("Enter Member ID: ")
        book_id = get_input("Enter Book ID: ")
        active_borrow = self.find_active_borrow(member_id=member_id, book_id=book_id)

        if active_borrow is None:
            print("This member has not borrowed this book, or it was already returned.")
            return

        book = self.find_book_by_id(book_id)
        if book is not None:
            book["available_copies"] += 1

        active_borrow["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        active_borrow["status"] = "Returned"
        self.save_all_data()
        print("Book returned successfully.")

    def view_borrowed_books(self):
        borrowed_books = [record for record in self.borrow_history if record["status"] == "Borrowed"]

        if not borrowed_books:
            print("No books are currently borrowed.")
            return

        print("\nCurrently Borrowed Books")
        print("-" * 100)
        print(f"{'Borrow ID':<12}{'Book ID':<10}{'Title':<25}{'Member ID':<12}{'Member':<20}{'Borrow Date':<20}")
        print("-" * 100)
        for record in borrowed_books:
            print(
                f"{record['borrow_id']:<12}"
                f"{record['book_id']:<10}"
                f"{record['book_title']:<25}"
                f"{record['member_id']:<12}"
                f"{record['member_name']:<20}"
                f"{record['borrow_date']:<20}"
            )

    def view_borrowing_history(self):
        if not self.borrow_history:
            print("No borrowing history found.")
            return

        print("\nBorrowing History")
        print("-" * 125)
        print(
            f"{'Borrow ID':<12}{'Book ID':<10}{'Title':<25}{'Member ID':<12}"
            f"{'Member':<20}{'Borrow Date':<20}{'Return Date':<20}{'Status':<10}"
        )
        print("-" * 125)
        for record in self.borrow_history:
            print(
                f"{record['borrow_id']:<12}"
                f"{record['book_id']:<10}"
                f"{record['book_title']:<25}"
                f"{record['member_id']:<12}"
                f"{record['member_name']:<20}"
                f"{record['borrow_date']:<20}"
                f"{record['return_date']:<20}"
                f"{record['status']:<10}"
            )

    def book_menu(self):
        while True:
            print("\nBook Management")
            print("1. Add a new book")
            print("2. View all books")
            print("3. Search book by title")
            print("4. Search book by author")
            print("5. Update book details")
            print("6. Delete a book")
            print("7. Back to main menu")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_book()
            elif choice == "2":
                self.display_books()
            elif choice == "3":
                self.search_books_by_title()
            elif choice == "4":
                self.search_books_by_author()
            elif choice == "5":
                self.update_book()
            elif choice == "6":
                self.delete_book()
            elif choice == "7":
                break
            else:
                print("Invalid choice. Please try again.")

            pause()

    def member_menu(self):
        while True:
            print("\nMember Management")
            print("1. Add a new member")
            print("2. View all members")
            print("3. Search member by name")
            print("4. Update member details")
            print("5. Delete a member")
            print("6. Back to main menu")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.add_member()
            elif choice == "2":
                self.display_members()
            elif choice == "3":
                self.search_members_by_name()
            elif choice == "4":
                self.update_member()
            elif choice == "5":
                self.delete_member()
            elif choice == "6":
                break
            else:
                print("Invalid choice. Please try again.")

            pause()

    def borrow_return_menu(self):
        while True:
            print("\nBorrow and Return System")
            print("1. Borrow a book")
            print("2. Return a book")
            print("3. View borrowed books")
            print("4. View borrowing history")
            print("5. Back to main menu")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.borrow_book()
            elif choice == "2":
                self.return_book()
            elif choice == "3":
                self.view_borrowed_books()
            elif choice == "4":
                self.view_borrowing_history()
            elif choice == "5":
                break
            else:
                print("Invalid choice. Please try again.")

            pause()

    def main_menu(self):
        while True:
            print("\nLibrary Management System")
            print("1. Book Management")
            print("2. Member Management")
            print("3. Borrow and Return System")
            print("4. Exit")

            choice = input("Choose an option: ").strip()

            if choice == "1":
                self.book_menu()
            elif choice == "2":
                self.member_menu()
            elif choice == "3":
                self.borrow_return_menu()
            elif choice == "4":
                self.save_all_data()
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    library = LibrarySystem()
    library.main_menu()
