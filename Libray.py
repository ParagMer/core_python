import json

class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        """Load books from the JSON file."""
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_books(self):
        """Save the books dictionary to the JSON file."""
        with open(self.filename, 'w') as file:
            json.dump(self.books, file, indent=4)

    def add_book(self, book_id, title, author, quantity):
        """Add a new book or update existing book's quantity."""
        if book_id in self.books:
            self.books[book_id]['quantity'] += quantity
        else:
            self.books[book_id] = {'title': title, 'author': author, 'quantity': quantity}
        self.save_books()
        print(f"Book '{title}' added successfully!")

    def delete_book(self, book_id):
        """Delete a book."""
        if book_id in self.books:
            del self.books[book_id]
            self.save_books()
            print(f"Book with ID {book_id} deleted successfully!")
        else:
            print("Book not found!")

    def search_book(self, title=None, author=None):
        """Search for a book by title or author."""
        found_books = [book for book_id, book in self.books.items()
                       if (title and title.lower() in book['title'].lower()) or
                          (author and author.lower() in book['author'].lower())]
        if found_books:
            for book in found_books:
                print(f"ID: {book['book_id']} | Title: {book['title']} | Author: {book['author']} | Quantity: {book['quantity']}")
        else:
            print("No books found matching your search!")

    def borrow_book(self, book_id):
        """Borrow a book."""
        if book_id in self.books and self.books[book_id]['quantity'] > 0:
            self.books[book_id]['quantity'] -= 1
            self.save_books()
            print(f"Successfully borrowed the book '{self.books[book_id]['title']}'!")
        else:
            print("Sorry, the book is not available for borrowing.")

    def return_book(self, book_id):
        """Return a borrowed book."""
        if book_id in self.books:
            self.books[book_id]['quantity'] += 1
            self.save_books()
            print(f"Successfully returned the book '{self.books[book_id]['title']}'!")
        else:
            print("Invalid book ID!")


# Main Program
def main():
    library = Library()

    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. Delete Book")
        print("3. Search Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                book_id = input("Enter book ID: ")
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                quantity = int(input("Enter quantity: "))
                library.add_book(book_id, title, author, quantity)

            elif choice == 2:
                book_id = input("Enter book ID to delete: ")
                library.delete_book(book_id)

            elif choice == 3:
                title = input("Enter title to search (or press Enter to skip): ")
                author = input("Enter author to search (or press Enter to skip): ")
                library.search_book(title if title else None, author if author else None)

            elif choice == 4:
                book_id = input("Enter book ID to borrow: ")
                library.borrow_book(book_id)

            elif choice == 5:
                book_id = input("Enter book ID to return: ")
                library.return_book(book_id)

            elif choice == 6:
                print("Exiting the system...")
                break
            else:
                print("Invalid choice, please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
