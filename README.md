# Library Management System

A simple Python-based library management project that allows users to manage books and customers through a console menu.

## Features

- Add, remove, and search for books
- Add, remove, and search for customers
- Check out and return books
- Interactive command-line interface

## Project Files

- LibraryMgmtFunctions.py - Main menu-driven library management program
- LibraryMgmtFunctions_original.py - Original version of the project
- LibraryMgmtFunctions_asperAsphero.py - Alternate version of the implementation
- TestFile.py - Test or scratch file
- README.md - Project documentation

## Python Requirements

- Python 3.8 or newer
- No external libraries are required

## How to Run

1. Open the project folder in your terminal.
2. Activate the virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
3. Run the program:
   ```powershell
   python .\LibraryMgmtFunctions.py
   ```

## Available Operations

When the program starts, you can choose from the following options:

1. Add a book
2. Remove a book
3. Search for a book
4. Check out a book
5. Return a book
6. Add a customer
7. Remove a customer
8. Search for a customer
9. Exit

## Example Usage Flow

1. Run the program.
2. Choose option 1 to add a book.
3. Enter the book title, author, and year.
4. Choose option 6 to add a customer.
5. Choose option 4 to check out a book for that customer.
6. Choose option 5 to return the book later.

## Notes About Current Limitations

This is a beginner-friendly console-based project, so it currently has some limitations:

- Data is not saved permanently between runs
- Book and customer records are handled in memory only
- Search is basic and does not include advanced filters
- The system does not yet connect to a database or file storage
