import os

BOOKS_FILE = "books.txt"
CUSTOMERS_FILE = "customers.txt"


def get_menu_choice():
    choice = input("Enter your choice (1-10): ").strip()
    print(f"You entered: {choice}")
    return choice


def load_books(filename):
    books = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                title, author, year, available = line.split("|")
                books.append({
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "available": available.lower() == "true",
                })
    return books


def save_books(filename, books):
    with open(filename, "w", encoding="utf-8") as file:
        for book in books:
            file.write(
                f"{book['title']}|{book['author']}|{book['year']}|{str(book['available']).lower()}\n"
            )


def load_customers(filename):
    customers = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                full_name, borrowed_books = line.split("|", 1)
                borrowed_list = borrowed_books.split(",") if borrowed_books else []
                customers.append({
                    "full_name": full_name,
                    "books_checked_out": [item for item in borrowed_list if item],
                })
    return customers


def save_customers(filename, customers):
    with open(filename, "w", encoding="utf-8") as file:
        for customer in customers:
            borrowed_books = ",".join(customer["books_checked_out"])
            file.write(f"{customer['full_name']}|{borrowed_books}\n")


def add_book(books, title, author, year):
    book = {
        "title": title,
        "author": author,
        "year": int(year),
        "available": True,
    }
    books.append(book)
    return book


def remove_book(books, title):
    for index, book in enumerate(books):
        if book["title"].lower() == title.lower():
            return books.pop(index)
    return None


def search_book(books, title):
    for book in books:
        if book["title"].lower() == title.lower():
            return book
    return None


def list_books(books):
    if not books:
        print("No books found.")
        return

    print("\nBooks in the library:")
    for book in books:
        status = "Available" if book["available"] else "Checked out"
        print(f"- {book['title']} by {book['author']} ({book['year']}) [{status}]")


def add_customer(customers, full_name):
    customer = {
        "full_name": full_name,
        "books_checked_out": [],
    }
    customers.append(customer)
    return customer


def remove_customer(customers, full_name):
    for index, customer in enumerate(customers):
        if customer["full_name"].lower() == full_name.lower():
            return customers.pop(index)
    return None


def search_customer(customers, full_name):
    for customer in customers:
        if customer["full_name"].lower() == full_name.lower():
            return customer
    return None


def check_out_book(books, customers, title, customer_name):
    book = search_book(books, title)
    customer = search_customer(customers, customer_name)

    if not book:
        print("Book not found.")
        return False

    if not customer:
        print("Customer not found.")
        return False

    if not book["available"]:
        print("Book is already checked out.")
        return False

    book["available"] = False
    customer["books_checked_out"].append(book["title"])
    print(f"{customer_name} checked out '{title}'.")
    return True


def return_book(books, customers, title, customer_name):
    book = search_book(books, title)
    customer = search_customer(customers, customer_name)

    if not book:
        print("Book not found.")
        return False

    if not customer:
        print("Customer not found.")
        return False

    if book["available"]:
        print("Book is already available.")
        return False

    book["available"] = True
    if book["title"] in customer["books_checked_out"]:
        customer["books_checked_out"].remove(book["title"])
    print(f"{customer_name} returned '{title}'.")
    return True


def main():
    books = load_books(BOOKS_FILE)
    customers = load_customers(CUSTOMERS_FILE)

    print("Welcome to the Library Management System")

    while True:
        print("\nChoose an option:")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Check out a book")
        print("5. Return a book")
        print("6. Add a customer")
        print("7. Remove a customer")
        print("8. Search for a customer")
        print("9. List all books")
        print("10. Exit")

        choice = get_menu_choice()
        print(f"Selected option: {choice}")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter author: ")
            year = input("Enter year published: ")
            add_book(books, title, author, year)
            save_books(BOOKS_FILE, books)
            print("Book added successfully.")

        elif choice == "2":
            title = input("Enter book title to remove: ")
            removed = remove_book(books, title)
            if removed:
                save_books(BOOKS_FILE, books)
                print("Book removed successfully.")
            else:
                print("Book not found.")

        elif choice == "3":
            title = input("Enter book title to search: ")
            book = search_book(books, title)
            if book:
                print(book)
            else:
                print("Book not found.")

        elif choice == "4":
            title = input("Enter book title to check out: ")
            customer_name = input("Enter customer name: ")
            check_out_book(books, customers, title, customer_name)
            save_books(BOOKS_FILE, books)
            save_customers(CUSTOMERS_FILE, customers)

        elif choice == "5":
            title = input("Enter book title to return: ")
            customer_name = input("Enter customer name: ")
            return_book(books, customers, title, customer_name)
            save_books(BOOKS_FILE, books)
            save_customers(CUSTOMERS_FILE, customers)

        elif choice == "6":
            full_name = input("Enter customer full name: ")
            add_customer(customers, full_name)
            save_customers(CUSTOMERS_FILE, customers)
            print("Customer added successfully.")

        elif choice == "7":
            full_name = input("Enter customer full name to remove: ")
            removed = remove_customer(customers, full_name)
            if removed:
                save_customers(CUSTOMERS_FILE, customers)
                print("Customer removed successfully.")
            else:
                print("Customer not found.")

        elif choice == "8":
            full_name = input("Enter customer full name to search: ")
            customer = search_customer(customers, full_name)
            if customer:
                print(customer)
            else:
                print("Customer not found.")

        elif choice == "9":
            list_books(books)

        elif choice == "10":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
