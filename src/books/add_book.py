import json
import os
import time as ti

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "books_data.json")

def add_book(title, author, language, isbn, release_date, subjects):

    os.system("cls")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    books = data["books"]

    print("Checking if the book already exists...")
    ti.sleep(1)

    if any(book["title"] == title or book["isbn"] == isbn for book in books):
        print("Book already exists! It will not be added again.")
        return

  
    print("Book not found. Adding the book now...")
    ti.sleep(1)

    new_book = {
        "title": title,
        "author": author,
        "language": language,
        "isbn": isbn,
        "release_date": release_date,
        "subjects": subjects
    }

    books.append(new_book)

  
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Book '{title}' added successfully!")

