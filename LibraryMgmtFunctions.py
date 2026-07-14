#Create a library management system that allows users to add, remove, and search for books in a library. The system should also allow users to check out and return books.
#Books will be stored in a list of dictionaries, where each dictionary represents a book with its title, author, year published, and availability status.
#customers will be stored in a list of dictionaries, where each dictionary represents a customer with their full name, number of books checked-out, book titles, check-out date, and return date.

def add_book(library, title, author, year):
    print(f"Adding book: {title} by {author}, published in {year}.")

def remove_book(library, title):
    print(f"Removing book: {title}.")
def search_book(library, title):
    print(f"Searching for book: {title}.")
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
books = []

def main():
    print("Welcome to the Library Management System!")
    while True:
        print("\nPlease choose an option:")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Check out a book")
        print("5. Return a book")
        print("6. Add a customer")
        print("7. Remove a customer")
        print("8. Search for a customer")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

        if choice == '1':
            title = input("Enter the book title: ")
            author = input("Enter the author: ")
            year = input("Enter the year published: ")
            add_book(books, title, author, year)
        elif choice == '2':
            title = input("Enter the book title to remove: ")
            remove_book(books, title)
        elif choice == '3':
            title = input("Enter the book title to search for: ")
            search_book(books, title)
        elif choice == '4':
            title = input("Enter the book title to check out: ")
            customer_name = input("Enter the customer's full name: ")
            check_out_book(books, customers, title, customer_name)
        elif choice == '5':
            title = input("Enter the book title to return: ")
            customer_name = input("Enter the customer's full name: ")
            return_book(books, customers, title, customer_name)
        elif choice == '6':
            full_name = input("Enter the customer's full name: ")
            add_customer(customers, full_name)
        elif choice == '7':
            full_name = input("Enter the customer's full name to remove: ")
            remove_customer(customers, full_name)
        elif choice == '8':
            full_name = input("Enter the customer's full name to search for: ")
            search_customer(customers, full_name)
        elif choice == '9':
            print("Exiting the Library Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()


