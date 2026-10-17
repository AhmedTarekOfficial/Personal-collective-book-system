import json
import os
import time as ti

COLLECTION_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "person_collectingbooks.json")

def delete_book(user_id, book_title):

    os.system("cls")
    print("Loading your book collection...")
    ti.sleep(1)

    with open(COLLECTION_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        collection = json.loads(content) if content else {}

    if user_id not in collection or len(collection[user_id]) == 0:
        os.system("cls")
        print(f"You don't have any books in your collection yet.")
        return

    user_books = collection[user_id]

    os.system("cls")
    print("Searching for books with that title...")
    ti.sleep(1)

    matching_books = []
    for i, book in enumerate(user_books):
        if book["title"].lower() == book_title.lower():
            matching_books.append((i, book))

    if len(matching_books) == 0:
        os.system("cls")
        print(f"No book with the title '{book_title}' was found in your collection.")
        return

    if len(matching_books) == 1:
        index_to_delete = matching_books[0][0]
        deleted_book = user_books.pop(index_to_delete)

        os.system("cls")
        print("Deleting the book...")
        ti.sleep(1)

        with open(COLLECTION_FILE, "w", encoding="utf-8") as f:
            json.dump(collection, f, ensure_ascii=False, indent=2)

        os.system("cls")
        print(f"Book '{deleted_book['title']}' has been deleted from your collection successfully!")
        return

    os.system("cls")
    print(f"Found {len(matching_books)} copies of '{book_title}' in your collection:\n")

    for number, (index, book) in enumerate(matching_books, start=1):
        print(f"  [{number}] Title   : {book['title']}")
        print(f"       Author  : {book.get('author', 'N/A')}")
        print(f"       ISBN    : {book.get('isbn', 'N/A')}")
        print(f"       Language: {book.get('language', 'N/A')}")
        print(f"       Released: {book.get('release_date', 'N/A')}")
        print()

    while True:
        choice = input(f"Which book do you want to delete? Enter a number (1 to {len(matching_books)}): ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(matching_books):
            chosen_number = int(choice)
            break
        else:
            print(f"Invalid choice. Please enter a number between 1 and {len(matching_books)}.")

    index_to_delete = matching_books[chosen_number - 1][0]
    deleted_book = user_books.pop(index_to_delete)

    os.system("cls")
    print("Deleting the book...")
    ti.sleep(1)

    with open(COLLECTION_FILE, "w", encoding="utf-8") as f:
        json.dump(collection, f, ensure_ascii=False, indent=2)

    os.system("cls")
    print(f"Book '{deleted_book['title']}' (ISBN: {deleted_book.get('isbn', 'N/A')}) has been deleted from your collection successfully!")
