# Library Management System

This is a command-line Library Management System written in Python.

## Files

- `library_management_system.py` - the main Python program
- `books.json` - stores book records after the program runs
- `members.json` - stores library member records after the program runs
- `borrow_history.json` - stores borrow and return history after the program runs

The JSON files are created automatically in the same folder as the Python file.

## How to Run

Open a terminal in this folder and run:

```bash
python library_management_system.py
```

If your computer uses `python3`, run:

```bash
python3 library_management_system.py
```

## What the Program Does

The program has three main menu sections:

1. Book Management
2. Member Management
3. Borrow and Return System

Book management lets you add, view, search, update, and delete books.

Member management lets you add, view, search, update, and delete members.

The borrow and return system lets members borrow available books, return borrowed books, view currently borrowed books, and view full borrowing history.

## Important Rules Included

- A book can only be borrowed when available copies are greater than 0.
- Borrowing a book decreases available copies by 1.
- Returning a book increases available copies by 1.
- The system does not allow returning a book that was not borrowed.
- Borrowing history is saved permanently in `borrow_history.json`.
- Books and members are saved permanently in JSON files.
