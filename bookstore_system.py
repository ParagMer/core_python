#pip install pymongo

from pymongo import MongoClient

# === Connect to MongoDB ===
client = MongoClient("mongodb://localhost:27017/")
db = client["bookstore"]
books = db["books"]

# Create index on title and author for faster search
books.create_index([("title", 1), ("author", 1)])

# === Add New Book ===
def add_book(title, author, category, price, stock):
    book = {
        "title": title,
        "author": author,
        "category": category,
        "price": price,
        "stock": stock
    }
    books.insert_one(book)
    print("✅ Book added successfully.")

# === Update Book ===
def update_book(title, updates):
    result = books.update_one({"title": title}, {"$set": updates})
    if result.modified_count:
        print("🔄 Book updated.")
    else:
        print("⚠️ No matching book found.")

# === Delete Book ===
def delete_book(title):
    result = books.delete_one({"title": title})
    if result.deleted_count:
        print("🗑️ Book deleted.")
    else:
        print("⚠️ No matching book found.")

# === Search Books ===
def search_books(keyword):
    results = books.find({
        "$or": [
            {"title": {"$regex": keyword, "$options": "i"}},
            {"author": {"$regex": keyword, "$options": "i"}},
            {"category": {"$regex": keyword, "$options": "i"}}
        ]
    })
    for book in results:
        print(f"📖 {book['title']} by {book['author']} | {book['category']} | ${book['price']} | Stock: {book['stock']}")

# === Low-Stock Alert ===
def low_stock_alert(threshold=5):
    results = books.find({"stock": {"$lt": threshold}})
    print("\n⚠️ Low Stock Alert:")
    for book in results:
        print(f"❗ {book['title']} - Only {book['stock']} left!")

# === Sample Usage ===
if __name__ == "__main__":
    # Add books
    add_book("Atomic Habits", "James Clear", "Self-help", 12.99, 3)
    add_book("Python Crash Course", "Eric Matthes", "Programming", 24.99, 10)

    # Update a book
    update_book("Atomic Habits", {"price": 10.99, "stock": 5})

    # Search books
    print("\n🔍 Search Results:")
    search_books("python")

    # Show low-stock alert
    low_stock_alert(threshold=6)

    # Delete a book
    # delete_book("Atomic Habits")

