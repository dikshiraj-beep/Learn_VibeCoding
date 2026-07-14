#Create a library management system that allows users to add, remove, and search for books in a library. The system should also allow users to check out and return books.
#Books will be stored in a list of dictionaries, where each dictionary represents a book with its title, author, year published, and availability status.
#customers will be stored in a list of dictionaries, where each dictionary represents a customer with their full name, number of books checked-out, book titles, check-out date, and return date.

from logging import exception #added to handle exceptions


def add_book(library, title, author, year=2020):
    book = {"title": title,
        "author": author,
        "year": year,
        "available": True
    }
    library.append(book)
    print(f"book: {title} by {author}, published in {year} successfully added.")

def remove_book(library, title):
    print(f"Removing book: {title}.")
    for book in library:
        if book['title'] == title:
            library.remove(book)
            print(f"book: {title} successfully removed from the library.")
            return
    print(f"book: {title} not found in the library.")

def search_book(library, title):
    for book in library:
        if book['title'] == title:
            print(f"Book found: {title} by {book['author']} ({book['year']}).")
            return
    print(f"Book not found : {title}.")
def check_out_book(library, customers, title, customer_name):
    print(f"{customer_name} is checking out the book: {title}.")
def return_book(library, customers, title, customer_name):
    print(f"{customer_name} is returning the book: {title}.")

def add_customer(customers, full_name):
    print(f"Adding customer: {full_name}.")

def remove_customer(customers, full_name):
    print(f"Removing customer: {full_name}.")

def search_customer(customers, full_name):
    print(f"Searching for customer: {full_name}.")

customers = []
library_books = []

print("Welcome to the Library Management System!")

while True:
    operations = input("Please choose an option: add_book, list_books, remove_book, search_book, check_out_book, return_book, add_customer, remove_customer, search_customer\nEnter your choice: ")

    if operations == 'add_book':
        title = input("Enter the book title: ")
        author = input("Enter the author: ")
        try:
            year = int(input("Enter the year published: "))
        except ValueError:
            print("Invalid input. Please enter a valid year.")
            continue
        except exception as e:
            print(f"An error occurred: {e}")
            continue
        if year > 2000:
            print(f"Adding book: {title} by {author}, published in {year}.")
            add_book(library_books, title, author, year)
        else:
            print("Invalid year. Please enter a year after 2000.")

    elif operations == 'list_books':
        print("List of all books in the library:")
        for book in library_books:
            print(f"- {book['title']} by {book['author']} ({book['year']})")

    elif operations == 'remove_book':
        title = input("Enter the book title to remove: ")
        remove_book(library_books, title)

    elif operations == 'search_book':
        title = input("Enter the book title to search for: ")
        search_book(library_books, title)

    elif operations == 'check_out_book':
        title = input("Enter the book title to check out: ")
        customer_name = input("Enter the customer's full name: ")
        check_out_book(library_books, customers, title, customer_name)

    elif operations == 'return_book':
        title = input("Enter the book title to return: ")
        customer_name = input("Enter the customer's full name: ")
        return_book(library_books, customers, title, customer_name)

    elif operations == 'add_customer':
        full_name = input("Enter the customer's full name: ")
        add_customer(customers, full_name)

    elif operations == 'remove_customer':
        full_name = input("Enter the customer's full name to remove: ")
        remove_customer(customers, full_name)

    elif operations == 'search_customer':
        full_name = input("Enter the customer's full name to search for: ")
        search_customer(customers, full_name)

    elif operations == 'exit':
        print("Exiting the Library Management System. Goodbye!")
        break
    else:
        print("Invalid choice. Please try again.")